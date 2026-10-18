---
name: scheduled-jobs
description: >-
  Design, implement and operate jobs that run on a schedule or from a job
  queue: cron and crontab syntax, systemd timers, Kubernetes CronJobs, cloud
  schedulers, and background job queues as examples; timezones and daylight
  saving, overlapping runs and locking, retries and idempotency, catch-up and
  missed-run semantics, timeouts, alerting on silent failure (dead man's
  switch), logging and observability. Use when asked to run something every
  N minutes, nightly, or at a set time, write or debug a crontab or timer,
  build a recurring or background job, or investigate a job that did not run,
  ran twice, or runs at the wrong time.
metadata:
  category: automation
  related: scripting-and-shell, workflow-automation, etl-pipelines, observability, concurrency-and-async, kubernetes, incident-response
---

# Scheduled Jobs

Scheduled jobs are the code nobody watches. They run while everyone sleeps, they fail without an error page, and they are discovered broken when someone notices the report did not arrive last Thursday — or the last six Thursdays. The scheduling syntax is the easy part. The hard parts are what happens when a run is slow, missed, doubled, interrupted, or quietly does nothing.

## Scope

Covers: time-triggered work (cron, systemd timers, Kubernetes CronJobs, cloud schedulers such as managed cron services and event-bridge-style rules, CI scheduled pipelines, application-level schedulers) and queue-driven background jobs (worker pools pulling from a queue, delayed and recurring jobs).

Related:
- Writing the script the job runs: `scripting-and-shell`.
- Data pipelines with dependencies, backfills and data checks: `etl-pipelines` (orchestrators include their own schedulers; this skill's principles still apply).
- Multi-step business processes: `workflow-automation`.
- Monitoring and alerting practice in general: `observability`.

## Core principles

1. **Absence is the failure mode.** A job that crashes may at least log an error; a job that never starts (scheduler down, crontab overwritten, timer disabled, host replaced) produces nothing at all. Alert on "expected success did not happen", not only on "an error occurred".

2. **Assume every run can overlap, repeat, or be skipped.** Schedulers fire twice (failovers, clock changes, at-least-once semantics in distributed schedulers), runs take longer than the interval, hosts reboot mid-run. Design the job so these are harmless: idempotent work, locking against overlap, and explicit catch-up behaviour.

3. **Make the job's unit of work explicit.** "Process yesterday's orders" is a window; "process everything new since the last successful run" is a checkpoint. Either is fine, but the job must know which, persist the checkpoint only after success, and accept an explicit window for manual reruns.

4. **Time is harder than it looks.** Timezones, daylight saving transitions, leap days, month ends, and server clocks set to different zones all change when jobs run and what "today" means. Decide the timezone deliberately and write it down.

5. **The schedule belongs in version control.** Hand-edited crontabs on a single server are invisible, unreviewed and lost when the server is rebuilt. Define schedules as code alongside the job.

## Choosing a mechanism

| Mechanism (examples) | Good for | Watch out for |
|---|---|---|
| cron on a single host | Simple host-local maintenance | Single point of failure; minimal environment; no built-in locking, history or alerting; hand edits |
| systemd timers | Host-level jobs on Linux | `Persistent=true` for catch-up; logs in the journal; randomised delays available |
| Kubernetes CronJob | Containerised jobs in a cluster | `concurrencyPolicy`, `startingDeadlineSeconds`, history limits, timezone field support depends on version |
| Cloud scheduler services | Triggering serverless functions, HTTP endpoints, containers | At-least-once delivery; retry configuration; IAM for the target |
| CI scheduled pipelines | Repository chores, nightly builds, dependency checks | Often disabled on inactive repos; queue delays; not for business-critical work |
| Application scheduler / job library (e.g. in-process schedulers, queue-based recurring jobs) | Jobs that need app code and data | Multiple app replicas each running the schedule unless leader election or a shared lock is used |
| Workflow orchestrator | Jobs with dependencies, backfills, data windows | Heavier; see `etl-pipelines` |
| Job queue with workers | Event-triggered background work, fan-out, retries | Visibility timeouts, poison messages, at-least-once delivery |

Prefer the mechanism the environment already uses and monitors. Host cron is fine for host housekeeping; business-critical jobs deserve a scheduler with history, retries and alerting, and should not depend on one machine staying alive.

## Schedule syntax

Classic five-field cron: minute, hour, day of month, month, day of week.

```
# ┌ minute (0-59)
# │ ┌ hour (0-23)
# │ │ ┌ day of month (1-31)
# │ │ │ ┌ month (1-12)
# │ │ │ │ ┌ day of week (0-6, Sunday=0; 7 is also Sunday on many implementations)
# │ │ │ │ │
 15 2 * * *     /opt/app/bin/nightly-report      # 02:15 every day
 */10 * * * *   /opt/app/bin/poll-queue          # every 10 minutes, on :00, :10, ...
 0 9 * * 1-5    /opt/app/bin/standup-digest      # 09:00 Mon-Fri
 0 0 1 * *      /opt/app/bin/monthly-close       # midnight on the 1st
```

Gotchas:
- **Day-of-month AND day-of-week**: when both are restricted (not `*`), most cron implementations run when *either* matches, not both. `0 0 13 * 5` runs on every 13th and every Friday, not only Friday the 13th.
- **`*/N` is aligned to the field's start**, not to when you installed the job. `*/7` in minutes runs at :00, :07 … :56, then :00 again (a 4-minute gap).
- **Syntax varies**: some systems use six or seven fields (seconds, year), Quartz-style `?` and `L`, or non-standard shortcuts (`@daily`, `@reboot`). Check the dialect of your scheduler; do not assume.
- **`%` is special in crontab lines** (newline) and must be escaped as `\%`, a classic source of broken `date +%F` commands.
- **Last day of month** is not expressible in standard cron; schedule daily and check in code, or use a scheduler that supports it.
- Validate expressions with a tool that prints the next several fire times, in the intended timezone, before deploying.

systemd timer equivalent, illustrative:

```ini
# nightly-report.timer
[Timer]
OnCalendar=*-*-* 02:15:00
Persistent=true          # run at boot if a scheduled run was missed while off
RandomizedDelaySec=300   # spread load across a fleet

[Install]
WantedBy=timers.target
```

## Timezones and daylight saving

- **Know the scheduler's timezone.** Host cron uses the system timezone (or `CRON_TZ`/`TZ` where supported); managed schedulers often default to UTC; Kubernetes CronJobs default to the controller's timezone unless a timezone field is set.
- **UTC schedules** never skip or repeat, but drift relative to local business hours twice a year.
- **Local-time schedules** match business expectations ("9 a.m. for the London office") but hit DST edges:
  - Spring forward: times in the skipped hour (e.g. 02:30 local) may not run at all, or run at 03:00, depending on implementation.
  - Fall back: times in the repeated hour may run twice.
- **Rule of thumb**: schedule maintenance and data jobs in UTC; schedule human-facing jobs (digests, reminders) in the audience's local zone, and avoid the 01:00–03:00 local window where DST transitions happen.
- **Inside the job**, compute business dates in an explicit zone. "Yesterday" at 00:30 UTC is still "today" in the Americas.
- Multi-region audiences need per-region schedules or per-recipient send-time logic, not one global cron.

## Overlap and locking

If a run can take longer than the interval, or the scheduler can fire twice, decide the policy:

| Policy | Use when |
|---|---|
| Skip if previous still running | Polling/sync jobs where the next run will catch up |
| Queue / wait | Each run's window must be processed, in order |
| Replace (kill the old run) | Only the latest run matters and partial work is safe to abandon |
| Allow concurrency | Runs are fully independent and idempotent |

Implementations:
- **Single host**: `flock` (Linux) around the command:

```bash
*/5 * * * * flock -n /run/lock/sync.lock /opt/app/bin/sync || echo "previous run still active" >&2
```

- **Kubernetes**: `concurrencyPolicy: Forbid` (skip) or `Replace`.
- **Distributed** (several hosts or replicas): a lock in a shared store — a database advisory lock, a row with a lease, or a key with a TTL in a cache/coordination service. Use leases that expire if the holder dies, and make the lease longer than the worst-case run or renew it while running. Lock-based mutual exclusion is never perfect across a network; keep the work idempotent so the rare double run is harmless.
- **Application replicas**: when every replica embeds a scheduler, either designate one (leader election) or have each job acquire a shared lock first.

## Idempotency and checkpoints

- Process explicit windows or checkpoints, and persist the checkpoint only after the work commits.
- Use upserts, unique constraints, or "already processed" markers so a repeated run does not duplicate effects (two invoices, two emails). Outbound actions such as emails or payments should carry a per-run or per-item idempotency key.
- Support a manual run for a specified window (`--date 2026-03-01`), separate from the scheduled default. This is how you recover from outages and backfill.

## Missed runs and catch-up

When the scheduler, host or job was down at the scheduled time, what should happen?

- **Run once on recovery** (systemd `Persistent=true`, many managed schedulers): fine for "make sure it has run today" jobs.
- **Run every missed interval** (orchestrator catch-up/backfill): needed when each interval is a distinct data window.
- **Skip**: fine for jobs where only current state matters (cache warmers, health pings).
- **Deadline**: if it cannot start within N minutes of schedule, give up and alert (Kubernetes `startingDeadlineSeconds`; similar settings elsewhere). Prevents a flood of stale runs after a long outage.

Choose explicitly; tool defaults differ and sometimes surprise (e.g. an orchestrator catching up a year of daily runs after you deploy a DAG with an old start date).

## Retries, timeouts and failure handling

- **Timeouts**: every job needs a maximum runtime. A hung job holds its lock forever and blocks all future runs. Set the timeout at the scheduler level (kill) and inside the job for external calls.
- **Retries**: retry transient failures with backoff and a cap; do not retry deterministic failures (bad config, bad data) repeatedly. Make sure retries plus the next scheduled run cannot pile up.
- **Exit codes** must reflect failure. A wrapper that always exits 0 (e.g. `cmd; echo done`) hides every failure from the scheduler.
- **Partial failure** in batch jobs: process items independently, record failed items for retry or review, and report a summary; fail the run if the failure rate exceeds a threshold.
- **Job queues**: set visibility timeouts longer than processing time (or extend them), cap delivery attempts, and send poison messages to a dead-letter queue that someone monitors. Workers must handle redelivery (at-least-once).

## Observability and alerting

Minimum for any job that matters:

1. **Success heartbeat (dead man's switch)**: on successful completion, the job pings a monitor (a heartbeat service, a metric with a timestamp, a row in a status table). An alert fires if no success is recorded within the expected interval plus grace. This catches every "did not run" cause at once: scheduler down, job disabled, crontab deleted, host gone, credentials expired before the job could log anything.
2. **Failure alerts** to an owner, with a link to logs.
3. **Structured logs** with run ID, scheduled time, actual start time, window processed, item counts, duration, outcome.
4. **Metrics**: last success timestamp, duration, items processed, failures. Alert on duration trends approaching the interval or timeout.
5. **Output sanity**: zero items processed for a job that always has work is suspicious; alert on unexpected zero or huge counts.

Logging gotchas: cron mails output to the local user by default, which usually goes nowhere. Redirect stdout/stderr to a log system or file with rotation. Never `>/dev/null 2>&1` a job unless something else records its outcome.

## Environment and runtime gotchas

- **Minimal environment**: cron runs with a tiny `PATH`, no shell profile, a different home directory, and often `/bin/sh`. Use absolute paths, set `PATH` and any required environment explicitly, and test with `env -i` to simulate.
- **Working directory** is usually the user's home or `/`; never rely on it.
- **User and permissions**: decide which account runs the job; avoid root unless required; ensure it can read secrets and write outputs.
- **Secrets** come from the platform's secret mechanism, not from the crontab line or a world-readable file.
- **Resource contention**: many jobs at `0 * * * *` across a fleet all start at the same second ("thundering herd"). Spread start minutes or add randomised delay.
- **Clock correctness**: hosts need NTP/time sync; skewed clocks shift schedules and break signed requests.
- **Containers**: ephemeral filesystems lose local state between runs; store checkpoints externally.
- **Deploys during runs**: decide whether deploys wait for running jobs, kill them (job must be interruptible and resumable), or let old versions finish.

## Process

1. **Define the job's contract**: what it does, unit of work (window or checkpoint), how long it should take, how often it must run, what happens if it is late or missed, who owns it.
2. **Choose the mechanism** and timezone.
3. **Write the job** idempotent, with explicit window arguments, timeouts and meaningful exit codes.
4. **Add locking** according to the overlap policy.
5. **Configure** retries, catch-up/deadline behaviour, and history retention in the scheduler.
6. **Instrument**: logs, metrics, success heartbeat, failure alert to the owner.
7. **Validate the schedule** by listing the next fire times in the target timezone, including around a DST change if local time is used.
8. **Test**: run manually with a window; run twice concurrently; kill mid-run and rerun; run in a minimal environment.
9. **Document**: schedule, timezone, owner, how to run manually, how to pause, what to do on alert.

## Debugging "it didn't run" / "it ran twice"

Work from the outside in:

1. Did the scheduler fire? Check scheduler logs/history (cron logs in syslog/journal, CronJob events, managed scheduler execution logs).
2. Is the schedule what you think, in the timezone you think? Print next run times.
3. Did the job start but fail immediately? Look for environment differences (PATH, permissions, missing env vars, working directory).
4. Was it skipped due to a lock held by a hung previous run, or a concurrency policy?
5. Was it suspended, disabled, or deleted by a deploy that replaced the crontab or manifest?
6. For double runs: multiple hosts/replicas with the same schedule, scheduler failover, DST fall-back, retries overlapping the next scheduled run, at-least-once delivery.

## Worked examples

Illustrative configurations; field names and defaults vary by version and provider.

### A wrapper that makes any command observable

```bash
#!/usr/bin/env bash
# run-job: run a command with a lock, a timeout, logging and a success heartbeat.
set -Eeuo pipefail
name=$1; shift
lock="/run/lock/${name}.lock"
log() { printf '%s job=%s %s\n' "$(date -u +%FT%TZ)" "$name" "$*" >&2; }

exec 9>"$lock"
if ! flock -n 9; then log "skipped: previous run still active"; exit 0; fi

start=$(date +%s)
log "start"
if timeout --kill-after=60 "${JOB_TIMEOUT:-3600}" "$@"; then
  log "success duration=$(( $(date +%s) - start ))s"
  curl -fsS --max-time 10 "${HEARTBEAT_URL:?}" >/dev/null || log "warning: heartbeat ping failed"
else
  rc=$?
  log "failure rc=$rc duration=$(( $(date +%s) - start ))s"
  exit "$rc"
fi
```

Used from cron as `15 2 * * * /opt/app/bin/run-job nightly-report /opt/app/bin/nightly-report`. The heartbeat URL is configured in the environment, not in the crontab. (`timeout` and `flock` are Linux utilities; macOS needs alternatives.)

### Kubernetes CronJob settings that matter

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-report
spec:
  schedule: "15 2 * * *"
  timeZone: "Etc/UTC"              # explicit; supported on recent versions
  concurrencyPolicy: Forbid        # skip if the previous run is still going
  startingDeadlineSeconds: 1800    # give up if it cannot start within 30 minutes
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 5
  jobTemplate:
    spec:
      backoffLimit: 2              # pod-level retries
      activeDeadlineSeconds: 3600  # hard timeout for the whole job
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: report
              image: registry.example.com/report:1.4.2
              args: ["--date", "yesterday"]
```

Note that `backoffLimit` retries plus a long `activeDeadlineSeconds` can approach the next scheduled run; size them together.

### Reasoning through a DST question

A digest is scheduled at `30 2 * * *` in `America/New_York`. On the spring-forward day, 02:30 local time does not exist; depending on the implementation it runs at 03:00 or not at all. On the fall-back day, 02:30 occurs twice; it may run twice. Fixes: move it to 06:30 local (outside the transition window), or schedule in UTC and accept the one-hour seasonal shift in local delivery time, or keep local time and make the job idempotent per business date so a second run sends nothing.

### Investigating "the report did not arrive"

1. Heartbeat monitor shows the last success was four days ago — the job has not succeeded since a deploy.
2. Scheduler history shows runs starting and failing within a second.
3. Logs show `command not found: python3`: the new base image puts Python elsewhere, and the job relied on `PATH`.
4. Fix: absolute interpreter path, add a smoke test that runs the job in the image during CI, and rerun the four missed days with explicit `--date` arguments (safe because the job is idempotent per date).

## Pitfalls and anti-patterns

- **No heartbeat**: discovering weeks later that the job stopped.
- **Hand-edited crontab** on one server, lost when the server is replaced.
- **Every replica runs the schedule**: N app instances, N copies of the nightly email.
- **No timeout**: a hung run blocks all subsequent runs via its lock.
- **Checkpoint advanced before work commits**: data lost on failure.
- **"Now"-based logic** without a window argument: impossible to rerun yesterday.
- **Local-time schedules in the DST window**, skipping or doubling runs.
- **Output discarded** to `/dev/null` with nothing else recording outcome.
- **Wrapper scripts that swallow exit codes.**
- **Catch-up floods** after deploying with an old start date or long outage.
- **Interval shorter than worst-case runtime** with no overlap policy.
- **Using a schedule where an event trigger fits**: polling every minute for something that could be a webhook or queue message.

## Verification

- [ ] Next fire times listed and match intent in the declared timezone (including DST edges if relevant).
- [ ] Two simultaneous invocations behave per the overlap policy.
- [ ] Killing the job mid-run, then rerunning, produces correct results with no duplicates.
- [ ] Manual run for an explicit past window works.
- [ ] Job runs successfully in a minimal environment (no profile, minimal PATH, correct user).
- [ ] Timeout is set and tested.
- [ ] Failure produces a non-zero exit and an alert to a named owner.
- [ ] Success heartbeat is in place and its "missing" alert was tested (e.g. by disabling the job in a test environment).
- [ ] Schedule and configuration are in version control.

## Reporting back

Tell the user: what runs, when (with timezone), on which mechanism, what it processes per run, overlap and catch-up behaviour, how failures and missed runs are detected and who is alerted, how to run it manually for a given window, how to pause it, and anything you could not test (e.g. DST behaviour on the real scheduler).
