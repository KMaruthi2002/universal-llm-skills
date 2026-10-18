---
name: kubernetes
description: >-
  Deploy, configure, operate, and debug workloads on Kubernetes (any
  distribution or managed service, e.g. EKS, GKE, AKS, OpenShift, k3s):
  Deployments, StatefulSets, Jobs, Services, Ingress/Gateway, ConfigMaps and
  Secrets, resource requests and limits, liveness/readiness/startup probes,
  autoscaling, rollouts and rollbacks, disruption budgets, RBAC, manifests
  with Helm or Kustomize, and debugging pods that crash, hang, or will not
  schedule. Also covers when not to use Kubernetes at all. Use when someone
  asks to deploy to k8s, write manifests or a Helm chart, fix
  CrashLoopBackOff, Pending, OOMKilled, or ImagePullBackOff, tune probes or
  resources, set up ingress, or decide whether they need Kubernetes.
metadata:
  category: devops
  related: containerization, ci-cd-pipelines, infrastructure-as-code, cloud-architecture, observability, incident-response, release-management
---

# Kubernetes

Kubernetes is a control loop: you declare desired state as objects, and controllers work continuously to make reality match. Nearly every confusing Kubernetes behaviour makes sense once you ask "which controller is reconciling this, and what does it think the desired state is?" This skill covers deploying and running workloads well, debugging them when they misbehave, and the honest question of whether Kubernetes is the right tool.

## Scope

Covers: workload objects, configuration and secrets, resources, probes, scheduling, scaling, networking and ingress, rollouts, disruption, basic RBAC and security context, packaging (Helm, Kustomize), GitOps, and debugging.

Hands off to:

- Building the image → `containerization`.
- Provisioning the cluster and cloud resources → `infrastructure-as-code`, `cloud-architecture`.
- Pipeline that deploys to the cluster → `ci-cd-pipelines`.
- Metrics, logs, traces, and alerting → `observability`.
- A live outage → `incident-response`.

Cluster administration in depth (control-plane operations, etcd, CNI internals, multi-cluster federation) is beyond this skill; treat it as specialist territory and lean on the provider's documentation.

## When not to use Kubernetes

Kubernetes has real fixed costs: cluster upgrades every few months (minor versions are supported for roughly a year), add-on management (ingress controller, cert manager, DNS, autoscaler, CSI drivers, observability agents), RBAC and network policy design, and a team that understands it. Consider alternatives when:

| Situation | Usually better fit |
|---|---|
| One to a handful of stateless services, small team | Managed container platform (e.g. Cloud Run, App Runner, Azure Container Apps, Fly.io, Render) or a PaaS |
| Event-driven, spiky, short tasks | Serverless functions |
| A single app on one or two hosts | VMs with a process manager, or Compose on a host |
| Static site or SPA | Object storage plus CDN |
| Team has no one to own the platform | Anything managed |

Kubernetes earns its cost when you have many services, need a uniform deployment and operations model across them, need fine control over scheduling/networking, have portability requirements across clouds or on-prem, or already have a platform team. If the user is asking "should we move to Kubernetes?", answer that question explicitly with these factors before writing manifests (see `technical-decision-making`).

## Core principles

**1. Declarative, reconciled state.** Apply desired state; do not script imperative sequences. `kubectl edit` or `kubectl scale` in production creates drift from the source of truth and will be reverted (or worse, not reverted) by the next deploy. Keep manifests in version control and apply them through a pipeline or GitOps controller.

**2. Pods are cattle.** Pods are rescheduled, evicted, and replaced at any time: node upgrades, autoscaling, spot reclamation, OOM. Design workloads to tolerate termination at any moment: stateless processes, graceful shutdown, external state, idempotent jobs.

**3. Requests are for scheduling; limits are for enforcement.** The scheduler places pods based on *requests*. The kernel enforces *limits*: exceeding a memory limit gets the container OOM-killed; exceeding a CPU limit gets it throttled. Wrong requests cause bad packing or noisy neighbours; wrong limits cause mysterious kills and latency.

**4. Probes tell Kubernetes what "healthy" means, so get them right.** Readiness controls traffic; liveness controls restarts; startup protects slow boots. Misconfigured probes are a leading cause of self-inflicted outages.

**5. Labels and selectors are the wiring.** Services, Deployments, network policies, disruption budgets, and monitors all find pods by label. A typo or an overly broad selector silently routes traffic to the wrong pods or none.

**6. Least privilege everywhere.** Service accounts with minimal RBAC, non-root containers, no host access, network policies where the cluster enforces them. A compromised pod with cluster-admin is a compromised cluster.

## Discovering context first

1. **Find the manifests and how they are rendered:** raw YAML directories, `kustomization.yaml` with overlays, Helm charts (`Chart.yaml`, `values*.yaml`), jsonnet/cdk8s/Pulumi, or a GitOps repo watched by Argo CD or Flux. Changes must go through that mechanism, not `kubectl apply` from a laptop.
2. **Identify cluster(s), distribution, and version.** Managed vs. self-hosted, Kubernetes minor version (API availability differs), which ingress/gateway controller, which CNI (does it enforce NetworkPolicy?), storage classes, autoscalers (cluster autoscaler, Karpenter, provider-native), service mesh if any.
3. **Check your kubectl context before every command.** `kubectl config current-context` and the namespace. Running a command against production when you meant staging is one of the most common serious mistakes.
4. **Look at existing conventions:** label schema (e.g. `app.kubernetes.io/*`), namespace layout, resource defaults (LimitRange/ResourceQuota), how secrets are provisioned (external secrets operator, sealed secrets, CSI secret store, cloud-native), policy engines (Kyverno, Gatekeeper, Pod Security admission) that will reject non-compliant manifests.
5. **Learn the workload's real behaviour:** memory and CPU under load, startup time, shutdown time, whether it holds state or long connections.

## Core objects and when to use each

| Need | Object | Notes |
|---|---|---|
| Stateless, replicated service | Deployment | Default for web/API/workers |
| Stable identity or per-replica storage (databases, brokers, consensus systems) | StatefulSet | Ordered start, stable names, volume per replica. Consider a managed service or an operator first |
| One per node (log shippers, node agents) | DaemonSet | Mind resource cost × node count |
| Run to completion | Job | Set `backoffLimit`, `activeDeadlineSeconds`, `ttlSecondsAfterFinished` |
| Scheduled run | CronJob | Set `concurrencyPolicy` (usually `Forbid`), `startingDeadlineSeconds`, history limits; times are in the controller's time zone unless `timeZone` is set |
| Stable in-cluster address | Service (ClusterIP) | Load-balances to ready pods matching the selector |
| External L4 load balancer | Service type LoadBalancer | Usually one cloud LB each — cost adds up |
| HTTP routing, TLS, host/path rules | Ingress or Gateway API | Gateway API is the newer, more expressive standard; use what the cluster's controller supports |
| Non-secret config | ConfigMap | Mounted files or env |
| Secret values | Secret | Base64 is encoding, not encryption — see below |
| Keep minimum replicas during voluntary disruption | PodDisruptionBudget | Needed for safe node drains |
| Autoscale replicas | HorizontalPodAutoscaler | Requires requests set and metrics available |

## Resources: requests and limits

**Setting requests:** measure. Start from observed usage under realistic load (p90–p95 of usage over a representative period) plus headroom. Without data, start modest and review after a week of metrics. Tools like the Vertical Pod Autoscaler in recommendation mode or cost tools can suggest values.

**Memory:**

- Set the memory limit; memory is incompressible, and an unbounded container can take down its node.
- A common, safe pattern is memory request == memory limit for latency-sensitive services (predictable, avoids eviction surprises). Allow limit > request only with clear reasons.
- Language runtimes must know the limit: configure JVM heap percentages, Node `--max-old-space-size`, Go `GOMEMLIMIT`, worker counts. Leave headroom for non-heap memory.
- `OOMKilled` (exit code 137 with that reason) means the container exceeded its limit, not that the node ran out.

**CPU:**

- Always set CPU requests; they determine scheduling and the CPU share under contention.
- CPU limits are contested among practitioners. Limits cause CFS throttling, which shows up as latency spikes even when average CPU is low, especially for multi-threaded runtimes. Many teams set CPU requests but no CPU limits for latency-sensitive services, relying on requests for fairness; others require limits for cost control or multi-tenant isolation. Choose deliberately, and if you set limits, monitor throttling metrics.
- Size worker/thread counts to the CPU request/limit, not to the node's core count (many runtimes see the host's cores).

**QoS classes:** Guaranteed (requests == limits for all resources), Burstable, BestEffort (none set). Under node pressure, BestEffort pods are evicted first. Never run production workloads as BestEffort.

## Probes

| Probe | Question it answers | Failure effect | Typical design |
|---|---|---|---|
| Startup | Has the app finished booting? | Keep waiting; kill after threshold | Generous: `failureThreshold × periodSeconds` ≥ worst-case boot time |
| Readiness | Can this pod take traffic right now? | Removed from Service endpoints; not restarted | Checks the app can serve; may consider critical local dependencies briefly |
| Liveness | Is the process wedged beyond recovery? | Container restarted | Cheap, local, only fails on true deadlock |

Rules:

- **Liveness must not check dependencies.** If the database is down and liveness fails, Kubernetes restarts every pod in a loop, turning a dependency outage into a total outage and a thundering herd on recovery.
- **Readiness checking dependencies is a judgment call.** If every pod depends on the same database, failing readiness on all of them removes all endpoints, producing connection refused instead of a meaningful error. Usually prefer readiness that reflects the pod's own ability to serve, and handle dependency failures in the app (errors, circuit breakers).
- Use a startup probe for slow-starting apps instead of large `initialDelaySeconds` on liveness.
- Keep probe endpoints fast and unauthenticated on an internal port or path; set `timeoutSeconds` realistically (default 1 s is tight for some apps under load).
- Omitting liveness is acceptable if the process crashes rather than hangs; a bad liveness probe is worse than none.

## Graceful shutdown and disruption

When a pod terminates: it is marked terminating, removed from endpoints (asynchronously), the `preStop` hook runs, SIGTERM is sent, and after `terminationGracePeriodSeconds` (default 30) SIGKILL follows.

- Endpoint removal propagates to load balancers and proxies with delay. Without care, traffic still arrives after SIGTERM. A short `preStop` sleep (a few seconds) is a common mitigation; the app should also keep serving in-flight requests while draining.
- Set the grace period above the app's maximum drain time. Long-running jobs or connections may need minutes.
- **PodDisruptionBudgets** protect against voluntary disruptions (node drains, upgrades, autoscaler scale-down). `maxUnavailable: 1` or `minAvailable: N-1` is typical. A PDB that allows zero disruptions (`minAvailable` equal to replicas) blocks node drains forever and stalls cluster upgrades.
- Spread replicas across nodes and zones (`topologySpreadConstraints` or pod anti-affinity). Three replicas on one node is one node failure from an outage.
- Run at least 2 replicas (3 for important services across 3 zones) for anything that must survive a node loss.

## Configuration and secrets

- Use ConfigMaps for non-secret config; Secrets for credentials. Mount as files when the app can reload them; env vars are fixed at container start, so changing a ConfigMap does not affect running pods using env until they restart. Trigger rollouts on config change (e.g. a checksum annotation in the pod template, which Helm and Kustomize generators can manage).
- **Kubernetes Secrets are base64-encoded, not encrypted** by default in manifests. Anyone with read access to Secrets in a namespace can read them. Ensure encryption at rest is enabled for etcd (managed providers often do; verify), restrict `get/list` on Secrets via RBAC, and never commit plain Secret manifests to git.
- Common patterns for getting secrets in: an external secrets operator syncing from a cloud secret manager or vault; sealed/encrypted secrets in git (Sealed Secrets, SOPS); CSI secret store drivers mounting secrets directly. Follow whichever the cluster already uses.
- Prefer workload identity (federating the pod's service account to cloud IAM) over static cloud credentials in Secrets.

## Scaling

- **HPA** scales replicas on CPU, memory, or custom/external metrics. CPU-based HPA targets utilisation relative to *requests*, so wrong requests produce wrong scaling. Set `minReplicas` to survive a zone loss and handle baseline traffic; set `maxReplicas` to protect downstream systems and budget.
- Scale on the signal that represents load: request rate or concurrency for web services, queue depth/lag for consumers (event-driven autoscalers such as KEDA help here). Memory is rarely a good scaling signal since it often does not fall when load drops.
- Tune scale-down stabilisation to avoid flapping; scale up fast, down slowly.
- **Cluster/node autoscaling** adds nodes when pods are Pending for lack of resources. Pods with no requests do not trigger it correctly. Very large requests may not fit any node type.
- Don't run HPA and VPA on the same resource metric for the same workload; they fight.
- Remember downstream limits: scaling a service from 10 to 100 pods multiplies database connections. Use connection pooling and cap replicas accordingly.

## Networking

- Services select pods by labels and route only to **ready** pods. "No endpoints" usually means a selector mismatch or no ready pods.
- In-cluster DNS: `service.namespace.svc.cluster.local`. Cross-namespace calls need the namespace in the name.
- For HTTP ingress, use one shared Ingress/Gateway controller with many routes rather than a LoadBalancer Service per app (cost, certificate management). Automate TLS certificates (e.g. cert-manager with ACME, or the cloud's certificate service).
- **NetworkPolicy** only takes effect if the CNI enforces it. Start with default-deny per namespace plus explicit allows once you know traffic flows; adding default-deny to a running namespace without mapping flows first will cause an outage. Remember to allow DNS egress.
- Keep long-lived connections (gRPC, HTTP/2, WebSockets) in mind: Kubernetes Service load balancing is per connection, so long-lived connections pin to pods and new pods get no traffic after scale-up. Use client-side load balancing, a mesh, or periodic connection recycling.

## Rollouts

- Deployment `RollingUpdate` with `maxSurge` and `maxUnavailable` controls pace. `maxUnavailable: 0, maxSurge: 25%` keeps full capacity during rollout at the cost of temporary extra pods.
- A rollout is only as safe as its readiness probe: if new pods report ready while broken, the rollout completes and takes down the service. Pair with `minReadySeconds` and post-deploy checks.
- Set `progressDeadlineSeconds` so stuck rollouts are reported as failed; make the pipeline wait on `kubectl rollout status` (or the GitOps health status) and fail the deploy on timeout.
- Rollback: `kubectl rollout undo` works but creates drift from git; in GitOps setups, revert the commit instead. Keep `revisionHistoryLimit` reasonable.
- For canary and blue/green, use a progressive delivery controller (e.g. Argo Rollouts, Flagger) or a mesh/gateway with traffic splitting; plain Deployments only approximate canaries by replica ratio. See `ci-cd-pipelines` for strategy choice.
- Pin images by immutable tag or digest. `imagePullPolicy: Always` with `latest` makes every pod restart a potential surprise upgrade.

## Packaging: raw YAML, Kustomize, Helm

| Approach | Strength | Weakness | Choose when |
|---|---|---|---|
| Raw YAML | Transparent, no tooling | Duplication across environments | Very small setups |
| Kustomize | Overlays per env, no templating language, built into kubectl | Limited logic | Your own apps with a few environments |
| Helm | Parameterised, distributable, release history | Templated YAML is hard to read and debug; values sprawl | Distributing apps to others; installing third-party software |
| Code-based (cdk8s, Pulumi, jsonnet) | Real language, abstraction | More tooling, team must know it | Large platforms with many similar services |

Whatever the tool, render and review the final YAML (`helm template`, `kustomize build`) before applying, and diff against the live cluster (`kubectl diff`, Argo CD/Flux diff). Pin chart versions for third-party charts.

**GitOps** (Argo CD, Flux): the cluster pulls desired state from git and reconciles. Benefits: audit trail, drift correction, easy rollback by revert. Consequence: manual `kubectl` changes are reverted, so fix things in git.

## Security context

Default to, in each container:

- `runAsNonRoot: true` with a numeric `runAsUser`.
- `allowPrivilegeEscalation: false`.
- `readOnlyRootFilesystem: true` with `emptyDir` mounts for writable paths.
- `capabilities: drop: ["ALL"]`.
- `seccompProfile: RuntimeDefault`.

Avoid `hostNetwork`, `hostPID`, `hostPath` mounts, and privileged containers for applications. Give each workload its own ServiceAccount with only the RBAC it needs; set `automountServiceAccountToken: false` if it does not call the API. Use the cluster's Pod Security admission level (`restricted` where possible).

## Debugging

Start broad, then narrow. Always confirm context and namespace first.

```text
kubectl get pods -n <ns> -o wide          # status, restarts, node
kubectl describe pod <pod> -n <ns>        # events: scheduling, probes, pulls, OOM
kubectl logs <pod> -n <ns> [-c <ctr>] [--previous]   # --previous for crashed containers
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl top pod -n <ns>                   # needs metrics-server
kubectl get endpoints/endpointslices <svc> -n <ns>
kubectl debug -it <pod> --image=<debug-image> --target=<ctr>   # ephemeral container
```

| Status / symptom | Usual causes | Check |
|---|---|---|
| `Pending` | Insufficient CPU/memory for requests, node selectors/taints, unbound PVC, quota | `describe` events; requests vs. allocatable; PVC status |
| `ImagePullBackOff` / `ErrImagePull` | Wrong name/tag, private registry auth, rate limits, arch mismatch | Events; pull secret / node identity; tag exists |
| `CrashLoopBackOff` | App exits on start: config missing, bad command, dependency unreachable at boot, liveness killing it | `logs --previous`; exit code; probe events |
| `OOMKilled` | Memory limit too low or leak; runtime unaware of limit | `describe` last state; memory metrics over time |
| `CreateContainerConfigError` | Missing ConfigMap/Secret or key | Events name the missing object |
| Running but not receiving traffic | Readiness failing, selector mismatch, wrong targetPort, NetworkPolicy | Endpoints list; labels; port names |
| Intermittent 502/503 during deploys | No graceful drain, readiness too optimistic | preStop, grace period, `minReadySeconds` |
| Latency spikes, low avg CPU | CPU throttling from limits | Throttling metrics; raise/remove CPU limit |
| Evicted pods | Node memory/disk pressure, BestEffort/Burstable pods | Node conditions; ephemeral storage use |
| Stuck `Terminating` | Finalizers, app ignoring SIGTERM, unreachable node | Finalizers on object; node status |

Resist "fixes" that hide problems: deleting a crashing pod only reschedules it; raising a liveness timeout to stop restarts may mask a real hang; removing limits to stop OOMs may move the failure to the node.

## Namespaces and multi-tenancy

- Use namespaces to separate teams, applications, or environments, and attach ResourceQuotas and LimitRanges so one tenant cannot starve others and pods without explicit resources still get defaults.
- Namespaces are a soft boundary: they scope names, RBAC, and quotas, but workloads still share nodes and the kernel. Hard multi-tenancy (untrusted tenants) needs separate node pools, sandboxed runtimes, or separate clusters.
- Keeping production and non-production in separate clusters (not just namespaces) limits blast radius from misapplied manifests, noisy experiments, and cluster-level upgrades.

## Safety rules

- **Confirm the context and namespace** and state them before any mutating command. Prefer read-only investigation (`get`, `describe`, `logs`) until a change is agreed.
- **Do not run mutating commands against production** (`apply`, `delete`, `scale`, `rollout undo`, `drain`, `cordon`, `patch`, `edit`) without explicit user confirmation that names the cluster, namespace, and objects.
- **Deleting namespaces, PVCs, or StatefulSets can destroy data irreversibly** (depending on reclaim policy). Check `persistentVolumeReclaimPolicy` and backups first.
- Never print Secret contents into logs, chat, or files. If you must verify a secret exists, check keys, not values.
- Avoid `kubectl apply` from a laptop when GitOps manages the namespace; it will either be reverted or cause drift. Change git.
- Watch cost: LoadBalancer Services, large node pools, and high `maxReplicas` all bill; mention the expected effect when changing them.

## Stateful workloads, Jobs, and cluster upgrades

### Stateful workloads

Running stateful systems on Kubernetes is feasible but demands operational maturity. Before deploying a database or broker in-cluster, confirm:

- A mature operator exists and the team understands it (backups, failover, version upgrades, scaling).
- Storage class performance (IOPS, latency) and topology are adequate; volumes are usually zonal, so a pod bound to a volume cannot move to another zone.
- Backups are automated, stored outside the cluster, and **restores have been tested**.
- `persistentVolumeReclaimPolicy` is `Retain` for important data, so deleting a claim does not delete the disk.

If any of these are missing, a managed database is usually the safer choice, and the application connects to it from the cluster.

### Jobs and CronJobs

- Jobs retry failed pods up to `backoffLimit`; make job logic idempotent because a pod can run partially and then be retried, or run twice if a node is lost mid-run.
- CronJobs can miss runs (controller downtime) or, with `concurrencyPolicy: Allow`, overlap when a run is slow. Use `Forbid` for jobs that must not overlap and alert on missed or failed runs (see `scheduled-jobs`).
- Set `ttlSecondsAfterFinished` so completed Jobs and their pods do not accumulate.
- For database migrations, prefer a dedicated Job or pipeline step that runs before the new version rolls out, over init containers in every replica racing to migrate.

### Cluster upgrades

Managed providers deprecate minor versions on a schedule; falling behind forces rushed upgrades. Before upgrading:

- Scan manifests and Helm releases for removed APIs in the target version.
- Check add-on compatibility (ingress controller, CNI, CSI drivers, operators, mesh).
- Confirm PDBs allow drains and workloads have multiple replicas.
- Upgrade non-production clusters first and let them soak.
- Upgrade one minor version at a time; skipping is generally unsupported.

## Worked example: CrashLoopBackOff after a "config-only" change

Situation: after a deploy that only changed an environment variable, new pods enter `CrashLoopBackOff`; old pods are still serving because `maxUnavailable: 0`.

Investigation: `kubectl describe pod` shows the container was restarted by the liveness probe, not by an app crash. `kubectl logs --previous` shows the app booting normally and running a cache warm-up that now takes ~45 seconds because the changed variable points to a larger dataset. The liveness probe has `initialDelaySeconds: 10`, `periodSeconds: 10`, `failureThreshold: 3`, so the container is killed at ~40 seconds, before it finishes booting, every time.

Fix: add a startup probe with `failureThreshold × periodSeconds` comfortably above worst-case boot (e.g. 30 × 5 s), leave the liveness probe tight for detecting hangs after boot, and add a readiness probe that only passes after warm-up. Apply through the same pipeline, watch the rollout complete, and confirm restarts stay at zero.

The reasoning to copy: read the *reason* for the restart (events and last state) before changing the app; distinguish "the app died" from "Kubernetes killed it"; and be glad the rollout settings kept old pods serving — that is why `maxUnavailable: 0` and a progress deadline matter.

## Pitfalls and anti-patterns

- No requests set → bad scheduling, broken HPA, BestEffort evictions.
- Liveness probe that checks the database → cascading restart loops.
- Single replica, or all replicas on one node/zone.
- PDB with zero allowed disruptions → blocked upgrades.
- `latest` tags → unknown versions, surprise upgrades on restart.
- Plain Secrets committed to git.
- Manual hotfixes with `kubectl edit` that git then overwrites, re-breaking production on the next deploy.
- Running databases in-cluster without the operational maturity (backups, upgrades, storage performance) to do so; managed databases are usually the better default.
- Ignoring API deprecations until the cluster upgrade removes them; check manifests against the target version before upgrading (tools like pluto or kubent help).
- One giant namespace with shared service account and no quotas.

## Verification

- [ ] Rendered manifests reviewed and diffed against the live state.
- [ ] Pods reach Ready; `rollout status` succeeds within the deadline.
- [ ] Requests/limits based on measured usage; no OOMKills or heavy throttling under representative load.
- [ ] Probes behave correctly: kill a dependency and confirm pods are not restart-looping; make the app unready and confirm it leaves endpoints.
- [ ] Deleting a pod causes no user-visible errors (graceful shutdown works).
- [ ] Replicas spread across nodes/zones; PDB allows at least one disruption; a test drain succeeds in non-production.
- [ ] Containers run non-root with the restricted security context, and policy admission accepts them.
- [ ] Secrets come from the agreed mechanism; none in git or logs.
- [ ] Rollback tested (git revert or rollout undo in staging).

Report cluster and namespace touched, what was applied and how, observed behaviour, and anything not verified.
