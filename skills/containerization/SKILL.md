---
name: containerization
description: >-
  Write, review, and optimise container images and local container setups:
  Dockerfiles/Containerfiles, base image choice, layer ordering and build
  caching, multi-stage builds, image size, running as non-root, signals and
  PID 1, health checks, configuration via environment, Compose for local
  development, and image scanning and signing. Use when someone asks to
  dockerize an app, write or fix a Dockerfile, shrink an image, speed up
  docker builds, set up docker-compose for local dev, harden a container, or
  fix a container that works locally but not in production. Not for
  orchestrating containers in a cluster (see kubernetes).
metadata:
  category: devops
  related: kubernetes, ci-cd-pipelines, secure-coding, dependency-management, cloud-architecture, project-scaffolding
---

# Containerization

A container image is a frozen, portable filesystem plus a start command. A good image is small, rebuilds quickly when code changes, starts and stops cleanly, runs with the least privilege it needs, contains no secrets, and produces the same behaviour on a laptop, in CI, and in production. Most container problems come from treating a Dockerfile as a shell script that "gets the app running" rather than as a build artifact with caching, security, and runtime semantics.

Examples use Docker/BuildKit syntax because it is the most common; the same ideas apply to Podman, Buildah, nerdctl, kaniko, ko, Jib, Cloud Native Buildpacks, and others.

## Scope

Covers: Dockerfile authoring, base images, layer caching, multi-stage builds, image size, users and permissions, signals, health checks, runtime configuration, local development with Compose, image scanning, signing, and registries.

Hands off to:

- Running containers on a cluster (deployments, probes as k8s objects, scaling) → `kubernetes`.
- Building and publishing images in the pipeline → `ci-cd-pipelines`.
- Choosing a container platform vs. serverless vs. VMs → `cloud-architecture`.
- Dependency pinning and updates in general → `dependency-management`.

## Core principles

**1. One process concern per container.** A container should run one main process (which may have worker threads or child processes it manages). Running a web server, a cron daemon, and a database in one container defeats independent scaling, restarts, health checking, and logging. Use separate containers and compose them.

**2. Images are immutable; configuration is injected.** Build one image and configure it per environment through environment variables, mounted config files, or a secret store at runtime. An image baked with `ENV=production` and a database URL cannot be promoted through environments (see `ci-cd-pipelines`, "build once").

**3. Layer order is cache order.** Each instruction creates a layer; a change invalidates that layer and every layer after it. Put what changes least (OS packages, dependency manifests and installs) first and what changes most (application source) last. This alone often turns a 5-minute rebuild into 10 seconds.

**4. Ship only what runs.** Compilers, build tools, test fixtures, package caches, and source for compiled languages have no place in the runtime image. They add size, startup time, and attack surface. Multi-stage builds make this easy.

**5. Least privilege by default.** Run as a non-root user, with a read-only root filesystem where possible, no extra Linux capabilities, and no secrets in the image. Container isolation is not a strong security boundary on its own; root in a container is much closer to root on the host than people assume.

**6. Be a good PID 1.** The container's main process receives signals (SIGTERM on stop) and must shut down gracefully; it also inherits zombie-reaping duty. Exec-form entrypoints and a proper init (or a runtime that handles it) prevent slow, unclean shutdowns.

**7. Reproducible builds.** Pin base images (tag plus digest for production), lock dependencies, and avoid `apt-get upgrade`-style unpinned changes. Otherwise two builds of the same commit differ and debugging becomes guesswork.

## Discovering context first

1. Look for existing `Dockerfile`, `Containerfile`, `*.dockerfile`, `.dockerignore`, `compose.yaml` / `docker-compose.yml`, `devcontainer.json`, `skaffold.yaml`, `Tiltfile`, buildpack configs (`project.toml`), or language-native image builders (Jib, ko).
2. Identify language, runtime version, and package manager from the project files (lockfiles, version files like `.nvmrc`, `.python-version`, `go.mod`, `rust-toolchain.toml`). Match the image's runtime version to what the project pins.
3. Find how the app is started in production today (Procfile, systemd unit, start scripts) and which ports, env vars, and files it needs.
4. Check the target platform: CPU architecture (amd64 vs. arm64 — Apple Silicon laptops and ARM cloud instances make multi-arch builds common), orchestrator, any platform-imposed constraints (e.g. read-only filesystems, required non-root, specific port binding).
5. Check organisational rules: approved base images, internal registries/mirrors, mandatory scanning, labels.
6. Follow existing conventions (naming, label schema, directory layout, how config is passed) unless they are actively harmful; if so, say why.

## Process

1. **Get it running correctly first,** in the simplest working form, verifying the app starts and serves.
2. **Add a `.dockerignore`** before optimising: exclude `.git`, dependency directories (`node_modules`, `.venv`, `target/`), build output, local env files, secrets, logs, editor files. This shrinks the build context, speeds builds, and prevents leaking `.env` files into images.
3. **Restructure for caching:** copy dependency manifests and lockfiles, install dependencies, then copy source.
4. **Split into build and runtime stages.**
5. **Harden:** non-root user, minimal base, no secrets, exec-form entrypoint, health check if appropriate.
6. **Measure:** image size (`docker image ls`, `dive` or similar for per-layer analysis), cold and warm build times, start time.
7. **Scan** for vulnerabilities and fix what matters.
8. **Verify runtime behaviour:** graceful stop, config via env, runs as non-root, works with a read-only filesystem if targeted.

## Base image choice

| Base family | Size (approx) | Pros | Cons | Choose when |
|---|---|---|---|---|
| Full distro (e.g. `debian`, `ubuntu`) | 75–130 MB+ | Familiar, all tools, glibc | Larger, more CVEs to triage | Need many system packages; debugging convenience matters |
| Slim distro (e.g. `debian:*-slim`, language `-slim` tags) | 25–80 MB | glibc compatibility, smaller | Fewer tools | Good default for interpreted languages |
| Alpine | ~5–10 MB | Tiny, simple package manager | musl libc: some binary wheels/native modules break or are slow to build; DNS and locale quirks | Small static-ish apps; team knows musl caveats |
| Distroless / minimal (e.g. Google distroless, Chainguard/Wolfi-based, UBI micro) | 2–30 MB | No shell or package manager, very few CVEs | Harder to debug in place | Production runtime stage for compiled or bundled apps |
| `scratch` | 0 | Nothing but your binary | Need static binary, CA certs, tzdata, user handled manually | Static Go/Rust binaries |
| Language official images (e.g. `python`, `node`, `eclipse-temurin`) | Varies | Correct runtime preinstalled | Pick the slim variant | Most apps; use as build stage at least |

Heuristics:

- For Python with native dependencies, prefer slim glibc images over Alpine; manylinux wheels install instantly on glibc, while on musl they may compile from source for minutes or fail.
- For Go/Rust, build in a full toolchain image and copy the binary into distroless or scratch. Remember CA certificates (for TLS) and timezone data if the app needs them.
- For JVM apps, use a JRE (not JDK) runtime image, or a jlink'd minimal runtime; set container-aware memory flags (modern JVMs respect cgroup limits, but heap percentage settings like `-XX:MaxRAMPercentage` deserve explicit thought).
- For Node, install production dependencies only in the runtime stage (`npm ci --omit=dev` or equivalent) or copy a pruned `node_modules` from the build stage.
- Pin by digest for production reproducibility (`image:tag@sha256:...`) and let an automated dependency tool propose updates; floating tags silently change.

## Layering and caching

Illustrative ordering (Node example; adapt to the project's language):

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev
COPY --from=build /app/dist ./dist
USER node
EXPOSE 8080
CMD ["node", "dist/server.js"]
```

What it demonstrates: manifests before source, a BuildKit cache mount for the package manager download cache (persists across builds without bloating layers), a separate runtime stage with only production dependencies, a non-root user that the base image already provides, and exec-form `CMD`.

Other caching rules:

- Combine related package-manager commands in one `RUN` and clean caches in the same layer (`apt-get update && apt-get install -y --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`). Deleting files in a later layer does not shrink the image; the earlier layer still contains them.
- Never run `apt-get update` in its own layer: the cached update goes stale while later installs change, producing "package not found" errors.
- `COPY . .` early is the most common cache killer. So is a build step that stamps the current time or git SHA into a file early in the build; pass such metadata late or as labels.
- `ARG` values used early invalidate everything after them when they change; place volatile args late.
- In CI, ephemeral runners start with no local cache. Use registry or CI-backed cache export/import (`--cache-to`/`--cache-from` with BuildKit, or the CI system's native Docker cache).

## Multi-stage builds

- Use named stages (`AS build`, `AS test`, `AS runtime`) and `COPY --from=<stage>` to move only artifacts forward.
- A `test` stage can run unit tests during the build (`docker build --target test`), which ensures tests ran against the same dependencies the image uses. Keep it out of the default target so production builds do not require test dependencies.
- A `dev` stage with hot-reload tooling can share the dependency layers with production, keeping local and production images aligned.
- BuildKit builds independent stages in parallel and skips stages not needed for the requested target.

## Size

Size matters for pull time (cold starts, autoscaling speed, node disk pressure), registry cost, and attack surface. Rough targets: compiled apps on distroless/scratch 10–50 MB; interpreted apps on slim bases 100–300 MB; anything over 1 GB deserves investigation unless it legitimately carries large models or toolchains.

Where size usually hides:

- Build tools and compilers left in the runtime image (fix: multi-stage).
- Package manager caches and apt lists (fix: cache mounts or same-layer cleanup).
- Dev dependencies (fix: production-only install).
- Large files copied by an over-broad `COPY` or missing `.dockerignore` (fix: ignore file, targeted copies).
- Files deleted in a later layer (fix: never create them in the image layer, or squash via multi-stage).
- `chown -R` in a separate layer after copying, which duplicates every file (fix: `COPY --chown=user:group`).
- ML models or data baked in. Sometimes correct (immutable, versioned with code); often better pulled at startup or mounted from a volume/object store. Decide based on how often the model changes vs. the code and how cold-start sensitive the workload is.

Use a layer inspection tool (e.g. `dive`, `docker history`) to find the big layers rather than guessing.

## Users, permissions, and hardening

- Create or use a non-root user with a fixed numeric UID/GID (e.g. 10001). Some platforms enforce `runAsNonRoot` and can only verify numeric UIDs. Set `USER` to it in the runtime stage.
- Files the app only reads should be owned by root and not writable by the app user; only directories the app writes (cache, temp, uploads) should be writable. This limits what a compromised process can alter.
- Aim to run with a read-only root filesystem and a writable `tmpfs` or volume for `/tmp` and any runtime write paths. Finding the write paths early is easier than retrofitting.
- Bind to ports above 1024 (e.g. 8080) so the process does not need privileges; map ports at the platform layer.
- Drop all capabilities and add back only what is needed (most web apps need none). Never use `--privileged` for application containers. Never mount the container runtime socket into an application container: it is equivalent to root on the host.
- Set `no-new-privileges` where the runtime supports it.

### Secrets

- **Never** put secrets in `ENV`, `ARG`, or copied files. Build args and env values are visible in image history and metadata; deleted files remain in earlier layers. Anyone who can pull the image gets the secret.
- For build-time secrets (private package registry tokens), use BuildKit secret mounts (`RUN --mount=type=secret,id=npmrc ...`), which are not persisted in layers.
- For runtime secrets, inject from the platform's secret mechanism (orchestrator secrets, cloud secret manager, mounted files) at start. Prefer files over env vars for highly sensitive values when the platform supports it, since env vars leak more easily into crash dumps, debug endpoints, and child processes.
- If a secret has ever been committed to an image that was pushed, rotate it. Deleting the tag is not enough.

## Signals, PID 1, and shutdown

- Use **exec form** (`CMD ["python", "app.py"]`), not shell form (`CMD python app.py`). Shell form runs `/bin/sh -c`, which becomes PID 1 and typically does not forward SIGTERM; the app gets killed hard after the grace period (often 10–30 s), dropping in-flight requests.
- If a wrapper script is needed, end it with `exec "$@"` or `exec your-app` so the app replaces the shell.
- PID 1 does not get default signal handlers in Linux: a process that does not explicitly handle SIGTERM may ignore it. Either handle it in the app or use a minimal init (`tini`, `dumb-init`, or the runtime's `--init` flag), which also reaps zombie processes if the app spawns children.
- Implement graceful shutdown: on SIGTERM stop accepting new work, finish in-flight requests within a bound, close connections, exit 0. Keep the drain time below the platform's termination grace period.
- Log to stdout/stderr, not files inside the container; the platform collects streams. Files inside the container are lost on restart and fill the writable layer.

## Health checks

- An image-level `HEALTHCHECK` is used by Docker/Compose and some platforms; Kubernetes ignores it and uses its own probes (see `kubernetes`). Include one when the image will run under Docker/Compose or on platforms that honour it.
- A health check should be cheap and check the process is able to serve (e.g. an HTTP `/healthz` that returns quickly). Do not make it depend on downstream systems; a database blip would then mark every instance unhealthy and trigger cascading restarts.
- Distroless images have no `curl`; implement the check in the app's own binary (a `--healthcheck` flag) or rely on platform probes.

## Configuration

- Read configuration from environment variables or mounted files at startup, with validation and a clear error if required values are missing. Fail fast at boot rather than at the first request.
- Provide sane defaults for non-sensitive settings; require explicit values for anything environment-specific.
- Document required env vars (in the README, compose file, or a sample env file without real values).
- Use OCI labels (`org.opencontainers.image.source`, `.revision`, `.version`, `.created`) to record provenance; this helps answer "what is running?" during incidents.

## Compose for local development

Compose (Docker Compose, Podman Compose) is the usual tool for running an app with its dependencies locally.

Good practice:

- Define dependencies (database, cache, queue, object-store emulator) as services with pinned versions matching production's major versions.
- Use `depends_on` with health conditions (`condition: service_healthy`) so the app waits for the database to accept connections, not merely for its container to start. Still make the app retry connections on startup; production does not have `depends_on`.
- Mount source code as a bind mount for hot reload in a dev profile/stage; do not bind-mount over dependency directories built inside the image (use an anonymous or named volume for `node_modules`, `.venv`, etc.), or host and container architectures will clash.
- Persist database data in named volumes; document how to reset them (`down -v` deletes volumes, which is destructive — warn before suggesting it on anyone's machine with data they care about).
- Use a `.env` file for local-only values and make sure it is in `.gitignore` and `.dockerignore`. Provide an example file with placeholders.
- Bind exposed ports to `127.0.0.1` for local dev databases so they are not exposed on shared networks.
- Use profiles for optional services (e.g. observability stack, workers) to keep the default `up` fast.
- Compose is primarily a local and simple-host tool. For multi-host production, reliability needs (rolling updates, self-healing across nodes) usually call for an orchestrator or managed container platform.

## Scanning, signing, and registries

- Scan images in CI with a vulnerability scanner (e.g. Trivy, Grype, Docker Scout, the registry's built-in scanner). Fail the build on high/critical findings **that have fixes available** and are in packages actually present in the runtime image; otherwise the gate becomes noise and gets disabled.
- Most findings disappear by switching to a smaller base image or rebuilding to pick up patched packages. Rebuild images on a schedule even without code changes so base-image patches land.
- Triage the rest: is the vulnerable code reachable? Is there a fixed version? Record accepted risks with an expiry date rather than suppressing permanently.
- Generate an SBOM (e.g. Syft, BuildKit's SBOM attestations) and sign images (e.g. cosign/Sigstore, Notation) if consumers or policy require provenance; enforce signature verification at deploy time if you sign.
- Lint Dockerfiles (e.g. hadolint) to catch common mistakes automatically.
- Use immutable tags in the registry where supported, retention policies to cap storage cost, and pull-through caches/mirrors to avoid public registry rate limits.

## Multi-architecture

If developers use ARM laptops and production uses amd64 (or vice versa), build multi-arch images (`docker buildx build --platform linux/amd64,linux/arm64`) or at least build for the production architecture explicitly. Emulated cross-builds (QEMU) can be 5–10× slower; native builders per architecture or cross-compilation (Go, Rust) are faster. An "exec format error" at start almost always means an architecture mismatch.

## Language-specific notes

These are the issues that most often trip up a first Dockerfile in each ecosystem. Defer to the project's existing build tooling where it exists.

- **Python:** set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` (unbuffered output so logs appear immediately). Install into a virtual environment in the build stage and copy the venv into the runtime stage, or build wheels in the build stage and install them in runtime. Use the project's lock tool (pip-tools, Poetry, uv, PDM) rather than unpinned `pip install -r` of a loose requirements file. Run under a production server (gunicorn, uvicorn workers) and size workers to the CPU limit, not the host's CPU count.
- **Node.js:** use `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --immutable` for deterministic installs. Do not run under `npm start` as PID 1 if it swallows signals; invoke `node` directly. Frontend builds usually produce static files best served by a static server or CDN, not a Node container.
- **Go:** `CGO_ENABLED=0` for a static binary that runs on scratch/distroless; cache `GOMODCACHE` and `GOCACHE` with cache mounts. Add `-trimpath` and `-ldflags="-s -w"` for smaller, more reproducible binaries.
- **Rust:** dependency caching needs a trick, because `cargo build` compiles dependencies and source together; tools like cargo-chef or a dummy-main pre-build layer cache dependency compilation. Use musl or distroless/cc depending on whether you need glibc.
- **JVM:** layered jars (Spring Boot layertools) or Jib split dependencies from application classes for better caching. Watch startup time and memory; set heap relative to the container limit and leave headroom for non-heap memory (metaspace, threads, direct buffers), commonly 25–40% of the limit.
- **.NET:** use the SDK image to build and the ASP.NET runtime or `runtime-deps` image to run; restore against the project file before copying source for caching. Consider chiselled/distroless variants for runtime.
- **Ruby/PHP:** native extensions need build headers in the build stage only; copy installed gems/vendor directory to runtime. For PHP, the common pattern is separate PHP-FPM and web-server containers, or an image that bundles both deliberately.

## Debugging containers

| Symptom | Likely causes | First checks |
|---|---|---|
| Exits immediately | Missing config, wrong command, crash on boot | `docker logs`, run interactively with the same command, check exit code (137 = killed/OOM, 139 = segfault, 126/127 = not executable/not found) |
| `exec format error` | Architecture mismatch, or script missing shebang / has CRLF line endings | `docker image inspect` for architecture; check line endings |
| `permission denied` writing files | Non-root user cannot write the directory | Make specific write paths owned by the user; do not fall back to root |
| Works locally, not in prod | Different arch, env vars, read-only fs, missing CA certs, DNS, platform-forced UID | Compare `inspect` output, run locally with prod-like flags (`--read-only`, `--user`, `--cap-drop=ALL`) |
| Slow stop (~10–30 s) | Signal not reaching app (shell form, no handler) | Exec form, `--init`, handle SIGTERM |
| OOM-killed | Limit too low, runtime ignores cgroup limits, memory leak | Check runtime is container-aware, measure RSS under load |
| Builds slow every time | Cache busted early (`COPY . .`, volatile `ARG`), no remote cache in CI | Build twice with `--progress=plain` and see which step reruns |
| Image unexpectedly huge | Dev deps, caches, deleted-later files | Layer inspection tool |

For images without a shell (distroless), debug with an ephemeral debug container sharing the target's process namespace, or a `:debug` variant of the base image used only in non-production.

## Pitfalls and anti-patterns

- **`latest` everywhere.** Builds and deploys drift. Pin.
- **Secrets in layers.** `ARG TOKEN`, `COPY .env`, or `RUN echo $KEY > file && ... && rm file` across layers. Use secret mounts and runtime injection; rotate exposed values.
- **Shell-form CMD/ENTRYPOINT.** Slow, unclean shutdowns. Exec form plus signal handling.
- **Running as root** because "it is just a container". Use a numeric non-root user.
- **Missing `.dockerignore`.** Huge context, leaked files, cache busting from `.git` changes.
- **SSH daemons or process supervisors running multiple services** to make containers behave like VMs. Use separate containers; use `exec` or ephemeral debug containers for access.
- **Writing logs or state inside the container.** Lost on restart, fills disk. Stdout for logs; volumes or external stores for state.
- **Health check that tests dependencies.** Cascading restarts during downstream incidents.
- **Debug tools in the production image "just in case".** Use debug variants or ephemeral debug containers instead.
- **Alpine for Python/native-heavy stacks** without knowing musl implications: slow builds, subtle runtime differences.
- **Works on my machine (ARM), fails in prod (amd64).** Build for the target platform.
- **Timezone/locale/CA-cert gaps in minimal images**: TLS failures to external APIs, wrong times. Copy or install them deliberately.

## Alternatives to hand-written Dockerfiles

Not every project needs a bespoke Dockerfile:

- **Cloud Native Buildpacks** (e.g. `pack`, platform-integrated builders) detect the language and produce a reasonable, patchable image with no Dockerfile. Good for standard web apps and teams without container expertise; less control over layout and size.
- **Language-native builders** (Jib for JVM, ko for Go, `dotnet publish` container support) build optimised layered images without a Docker daemon.
- **Dev containers** (`devcontainer.json`) define a development environment, not a production image; keep them separate but share base versions so behaviour stays aligned.

Choose a hand-written Dockerfile when you need control over the base, system packages, or layout; choose a builder when standardisation and low maintenance matter more.

## Safety notes

- Ask before deleting images, volumes, or running prune commands (`system prune -a --volumes`) on someone's machine or a shared host; volumes may hold the only copy of local data.
- Do not push images to public registries or make repositories public without confirmation; images often contain proprietary code even when secrets are absent.
- Do not disable scanning gates or security options to make a build pass; fix the cause or record a time-bound exception with the user's agreement.

## Verification

- [ ] Image builds from a clean cache, and a source-only change rebuilds in seconds (dependency layers cached).
- [ ] `docker run` with only documented env vars starts the app; missing required config fails fast with a clear message.
- [ ] `docker inspect`/`id` inside the container confirms a non-root numeric UID.
- [ ] `docker stop` completes well within the grace period and the app logs a graceful shutdown (no SIGKILL after timeout).
- [ ] No secrets in `docker history --no-trunc`, image config, or filesystem (search for known secret names).
- [ ] Image size measured and compared with before; big layers explained.
- [ ] Scanner run with no unexplained high/critical fixable findings.
- [ ] Health check passes when healthy and fails when the process cannot serve.
- [ ] Built for the production architecture.
- [ ] Compose stack starts from scratch with one command and the app reaches its dependencies.

Report image size, build times (cold/warm), scan summary, and anything not verified (e.g. "not tested on the production platform's read-only filesystem").

## Worked example: a 1.4 GB Python API image

Situation: a FastAPI service image is 1.4 GB, rebuilds take 6 minutes on every code change, and `docker stop` always takes 10 seconds.

Diagnosis, step by step:

1. `docker history` shows a 900 MB layer from `pip install` that includes compilers (`build-essential`) installed for one native dependency, plus the pip cache.
2. The Dockerfile does `COPY . .` before `pip install -r requirements.txt`, so any source change reinstalls everything — that is the 6 minutes.
3. There is no `.dockerignore`; the context includes `.git` (300 MB) and a local `.venv`.
4. `CMD uvicorn app:app` in shell form means `/bin/sh` is PID 1 and SIGTERM never reaches uvicorn, so the runtime waits the full timeout and then kills it.
5. The container runs as root.

Changes:

- Add `.dockerignore` (`.git`, `.venv`, `__pycache__`, `.env*`, tests data).
- Build stage on `python:3.12-slim` with build tools: copy the lock file, build a venv with a pip cache mount, then copy source.
- Runtime stage on `python:3.12-slim` without build tools: copy the venv and source, create user with UID 10001, `USER 10001`.
- Exec-form `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]`, with the app handling shutdown.
- Pin the base by digest, add a scan step in CI.

Result: ~210 MB image, source-only rebuilds in ~15 seconds, stop completes in under a second, scanner findings drop from 140 to a dozen (mostly unfixable base packages, recorded with review dates).

The reasoning to copy: inspect layers before guessing, fix cache ordering and context first (cheapest, biggest win), then separate build from runtime, then harden and verify shutdown behaviour.
