---
name: cloud-architecture
description: >-
  Design and review systems on public clouds (AWS, Google Cloud, Azure, and
  smaller providers alike): choosing compute (VMs, containers, managed
  container platforms, serverless), managed data and messaging services,
  network topology, identity and access (IAM), multi-AZ and multi-region
  resilience, disaster recovery targets, cost management, well-architected
  trade-offs, and vendor lock-in. Use when someone asks how to host or
  deploy an app on the cloud, which cloud service to use, how to make a
  system highly available, how to cut a cloud bill, how to structure
  accounts, VPCs, or IAM, or whether to go multi-cloud or serverless. Not for
  writing the infrastructure code itself (see infrastructure-as-code) or
  application-level system design.
metadata:
  category: devops
  related: system-design, software-architecture, infrastructure-as-code, kubernetes, containerization, observability, secure-coding, authentication-and-authorization, technical-decision-making, architecture-review
---

# Cloud Architecture

Cloud architecture is the practice of choosing and arranging rented building blocks — compute, storage, databases, networks, identity, queues — so a system meets its requirements for reliability, security, performance, and cost, and can be operated by the team that owns it. Clouds offer hundreds of services; the skill lies in using as few as possible, choosing the most managed option the requirements allow, and being honest about trade-offs that the marketing pages skip.

Provider-specific names are given as examples across AWS, Google Cloud, and Azure; the reasoning is the same on any provider.

## Scope

Covers: requirement gathering for cloud designs, compute and data service selection, network topology, account/project structure, IAM, availability and disaster recovery, scaling, cost, lock-in and portability, and reviewing existing cloud designs.

Hands off to:

- Writing Terraform/Pulumi/CloudFormation → `infrastructure-as-code`.
- Application-level component and data-flow design → `system-design`, `software-architecture`.
- Kubernetes specifics → `kubernetes`; image building → `containerization`.
- Monitoring and SLOs → `observability`.
- Formal design review of an existing architecture → `architecture-review`.

## Core principles

**1. Requirements before services.** Availability target, recovery objectives, latency, data residency, compliance, expected load and its shape, team skills, and budget decide the architecture. Choosing services first and justifying them later produces over-built, expensive systems.

**2. Prefer managed, and the higher-level the better — until it stops fitting.** Each step up (VM → managed containers → serverless; self-run database → managed database) hands patching, scaling, and failover to the provider. Teams are usually short of operations time, not compute. Step down only for a concrete reason: cost at scale, a missing capability, performance requirements, or portability requirements.

**3. Design for failure, at every layer.** Instances die, zones have outages, regions occasionally do, dependencies throttle, and deploys break things. Decide explicitly which failures the system survives automatically, which it recovers from manually, and which it accepts. "Highly available" without stating the failure domain means nothing.

**4. Identity is the perimeter.** In the cloud, IAM decides who can do what to every resource, and misconfigured identity is the most common root of serious breaches. Least privilege, short-lived credentials, and separation of environments into accounts are the foundation; network controls are defence in depth.

**5. Cost is an architectural property.** Cloud bills reflect design choices: data transfer paths, always-on capacity, storage tiers, request patterns. Estimate cost during design, attribute it with tags, and review it like any other metric.

**6. Simplicity is a reliability and security feature.** Every additional service, region, and network path is something to secure, monitor, pay for, and understand at 3 a.m. Add complexity only when a requirement demands it.

**7. Reversibility shapes how much to agonise.** Choosing an instance size is easy to change; choosing a primary database, a region for data residency, or an identity model is not. Spend design effort in proportion to the cost of changing the decision later.

## Discovering context first

Gather, from the user and the existing environment:

- **Workload:** what it does, request patterns (steady, diurnal, spiky, batch), latency sensitivity, read/write ratio, data volume and growth.
- **Targets:** availability (e.g. 99.9% ≈ 43 min/month downtime; 99.95% ≈ 22 min; 99.99% ≈ 4.3 min), RTO (how long to recover), RPO (how much data loss is acceptable).
- **Constraints:** existing provider and commitments (credits, enterprise agreements, reserved capacity), data residency and compliance (e.g. GDPR, HIPAA, PCI DSS, SOC 2), approved services lists, network connectivity to on-prem.
- **Team:** size, operational skills, on-call capacity. A design that needs a platform team the user does not have is a bad design for them.
- **Budget:** order of magnitude per month, and whether predictability or minimum cost matters more.
- **Existing estate:** account/project structure, landing zone, networking, IAM conventions, IaC tool, tagging standards, observability stack. Extend what exists; a second, parallel way of doing things doubles the operational load.

If key targets are unknown, propose sensible defaults explicitly ("assuming 99.9% availability, RPO of 5 minutes, single region") and let the user correct them, rather than silently designing for the extreme.

## Compute choices

| Option | Examples | Operational burden | Scaling | Cost profile | Choose when |
|---|---|---|---|---|---|
| Functions (FaaS) | Lambda, Cloud Functions/Cloud Run functions, Azure Functions | Lowest | Per request, to zero | Pay per invocation; can be costly at sustained high throughput | Event-driven, spiky, glue code, low-to-moderate steady traffic |
| Serverless containers | Cloud Run, App Runner, Azure Container Apps, Fargate | Low | Per request or per task, often to zero | Pay for running time | Web services and workers packaged as containers; default for many apps |
| Managed Kubernetes | EKS, GKE, AKS | Medium–high (cluster, add-ons, upgrades) | Pods and nodes | Node-based; efficient at scale | Many services, need for uniform platform, portability, or k8s ecosystem |
| VMs / instance groups | EC2 + ASG, Compute Engine MIGs, VM Scale Sets | Medium–high (OS patching, images) | Instance-level, minutes | Cheapest per unit at steady load, especially with commitments/spot | Legacy apps, special OS/kernel needs, licensed software, steady heavy workloads |
| PaaS | Elastic Beanstalk, App Engine, App Service, Heroku-style platforms | Low | Platform-managed | Moderate | Conventional web apps; team wants minimal infra |
| Batch / HPC / GPU | AWS Batch, Cloud Batch, Azure Batch, GPU instances | Medium | Job queues | Spot/preemptible friendly | Large parallel jobs, ML training |

Decision factors worth stating:

- **Execution duration and statefulness:** functions have time limits (commonly up to 15 minutes or less) and no local state between invocations.
- **Cold starts:** scale-to-zero platforms add latency on the first request (from tens of milliseconds to seconds depending on runtime and image size). Keep a minimum instance count for latency-sensitive paths if needed, at a cost.
- **Concurrency and downstream limits:** functions can scale to thousands of concurrent executions, which can overwhelm a database with connections. Use connection pooling proxies or cap concurrency.
- **Cost crossover:** pay-per-request is cheap at low utilisation and expensive at sustained high utilisation. As a rough rule, once a service is busy most of the day, provisioned containers or VMs with commitments tend to be cheaper. Do the arithmetic with real request counts and durations rather than assuming.

## Data and messaging services

- **Relational by default** for transactional business data (managed PostgreSQL/MySQL such as RDS/Aurora, Cloud SQL/AlloyDB, Azure Database). Choose specialised stores for specialised needs, not novelty. See `database-design`.
- **Key-value/document** (DynamoDB, Firestore/Bigtable, Cosmos DB) for very high scale with known access patterns; design keys around queries up front, since ad-hoc querying is limited and some pricing models charge per request.
- **Object storage** (S3, Cloud Storage, Blob Storage) for files, backups, data lakes, static assets. Effectively unlimited and durable; use lifecycle rules to move cold data to cheaper tiers and to expire what is not needed.
- **Caches** (managed Redis/Memcached/Valkey) to cut latency and database load; plan for cache loss as a normal event.
- **Queues and streams:** queues (SQS, Pub/Sub, Service Bus) decouple producers from consumers and absorb spikes; streams (Kinesis, Kafka/MSK/Confluent, Event Hubs) when ordering, replay, or multiple independent consumers are needed. Design consumers to be idempotent: at-least-once delivery is the norm.
- **Search and analytics:** managed search engines and warehouses (e.g. OpenSearch, BigQuery, Redshift, Snowflake, Synapse/Fabric) for their purpose; do not run analytics on the transactional primary.
- **Managed vs. self-hosted:** self-hosting a database on VMs or Kubernetes saves money only when you count none of the engineering time for backups, failover, upgrades, and tuning.

## Networking

- **Address planning:** choose non-overlapping private CIDR ranges across environments, regions, and on-prem from the start; overlapping ranges make later peering or VPN connections painful or impossible. Leave room to grow.
- **Subnet tiers:** public subnets only for load balancers and NAT/egress; application and data tiers in private subnets with no direct inbound internet access.
- **Ingress:** managed load balancers or API gateways, TLS terminated with managed certificates, a WAF in front of public HTTP endpoints where risk justifies it, a CDN for static and cacheable content.
- **Egress:** NAT gateways are convenient but charge per GB processed and per hour; high-volume egress to cloud services through NAT is a classic surprise bill. Use private endpoints/service endpoints (PrivateLink, Private Service Connect, Private Endpoints) for provider services, and gateway endpoints where free ones exist (e.g. for object storage on some providers).
- **Connectivity between networks:** peering for a few networks; hub-and-spoke via transit gateways/virtual WAN/network connectivity centres for many. VPN or dedicated interconnect for on-prem.
- **Security groups / firewall rules:** reference other groups or service identities rather than IP ranges where possible; never open management ports (SSH, RDP, database ports) to the internet. Use bastion-less access (session managers, identity-aware proxies).
- **DNS:** private DNS zones for internal names; low TTLs on records you may need to fail over.

## Account and project structure

- Use the provider's organisation hierarchy (AWS Organizations with OUs, Google Cloud organisation and folders, Azure management groups and subscriptions).
- **Separate accounts/projects/subscriptions per environment** at minimum (production apart from non-production), and often per team or workload. This is the strongest isolation boundary: IAM mistakes, quota exhaustion, and runaway costs stay contained.
- Central accounts for shared concerns: logging/audit (write-only from other accounts, tamper-resistant), security tooling, networking hub, shared services.
- Apply guardrails at the organisation level: deny disabling audit logs, restrict regions where data must stay, block public object storage by default, require encryption.
- Landing-zone frameworks (e.g. AWS Control Tower, Google Cloud landing zone blueprints, Azure landing zones) provide a starting structure; adopt the parts that fit.

## Identity and access management

- **Humans:** federate to the organisation's identity provider with SSO and MFA; no long-lived personal access keys. Grant roles to groups, not individuals. Use just-in-time elevation for production admin access.
- **Workloads:** attach roles/service accounts to compute (instance profiles, workload identity, managed identities). Never embed static keys in code, images, or config. CI/CD uses federated OIDC identities scoped to repository and environment.
- **Least privilege in practice:** start with narrowly scoped managed or custom policies; use access analysers and last-used data to remove unused permissions. Avoid wildcards on actions and resources in production policies, especially `*:*`.
- **Resource policies** (bucket policies, key policies, queue policies) are a second access path; review them alongside identity policies. Public access should require an explicit, reviewed exception.
- **Break-glass access:** a tightly controlled emergency admin path, monitored and alarmed on use.
- **Audit:** organisation-wide audit logging (CloudTrail, Cloud Audit Logs, Azure Activity Log) into the central log account with retention matching policy.

## Availability and disaster recovery

Failure domains, from smallest to largest: process → instance → zone → region → provider/global control plane.

| Pattern | Survives | Typical RTO / RPO | Relative cost | Notes |
|---|---|---|---|---|
| Single instance | Process crash (with restart) | Minutes–hours / since last backup | 1× | Fine for dev and non-critical internal tools |
| Multi-AZ (zones) | Instance and zone failure | Seconds–minutes / ~0 with synchronous replication | ~1.3–2× | **Default for production.** Managed databases offer multi-AZ options |
| Backup & restore to another region | Region loss (slowly) | Hours / hours | ~1.1× | Cheapest DR; test restores regularly |
| Pilot light / warm standby in second region | Region loss | Tens of minutes / minutes | ~1.3–1.8× | Data replicated asynchronously; compute scaled down until failover |
| Active-active multi-region | Region loss, with low latency globally | Near zero / near zero to seconds | 2×+ and much more complexity | Requires conflict handling or partitioned data; justify carefully |

Guidance:

- Multi-AZ covers the overwhelmingly common failures and is cheap relative to its benefit. Multi-region roughly doubles cost and multiplies complexity (data replication, consistency, failover orchestration, testing). Choose it only when the business impact of a regional outage, or latency/residency needs, justify it.
- RPO is set by replication: synchronous replication (within a region) gives ~0 data loss at a latency cost; cross-region replication is usually asynchronous, so some loss on failover is expected.
- **Backups are only real if restores are tested.** Schedule restore drills; measure the actual RTO.
- Keep backups isolated (separate account, immutable/locked storage) so ransomware or a compromised admin cannot delete them along with production.
- Avoid hidden single points of failure: a single NAT gateway, a single-zone cache, one region's DNS or identity dependency, a control plane you need during failover.
- **Static stability:** design so that during an impairment the system keeps working with what it already has, without needing to create new resources (provisioning APIs are often the first thing degraded in a regional event).
- Use timeouts, retries with exponential backoff and jitter, and circuit breakers for dependencies; unbounded retries turn small outages into big ones.

## Scaling

- Make the stateless tier horizontally scalable behind a load balancer; push state into managed data stores and caches.
- Autoscale on load-representative metrics (requests, concurrency, queue depth) with sensible minimums and maximums. Maximums protect downstream systems and budgets.
- Know your quotas and limits (instances per region, IPs, API rate limits, concurrent function executions). Request increases before launch, not during it.
- Load-test before significant launches to find the real bottleneck, which is usually the database or a third-party API, not compute.

## Cost management

Where cloud money goes, and the levers:

| Driver | Lever |
|---|---|
| Always-on overprovisioned compute | Rightsize from utilisation data; autoscale; schedule non-prod to shut down out of hours (often a 60–70% saving for those environments) |
| Steady baseline usage at on-demand prices | Commitments (reserved instances, savings plans, committed use discounts) for the stable baseline only, typically 1-year first |
| Interruptible work on on-demand | Spot/preemptible instances for batch, CI, and fault-tolerant workers (large discounts, can be reclaimed at short notice) |
| Data transfer | Keep chatty components in the same zone/region where resilience allows; private endpoints instead of NAT; CDN for egress to users; watch cross-region replication |
| Storage growth | Lifecycle policies, tiering, expiry; delete orphaned snapshots and volumes |
| Managed service premiums | Right tier for the workload; serverless vs. provisioned choice based on utilisation |
| Logging and metrics | Retention limits, sampling, dropping noisy logs, controlling metric cardinality (see `observability`) |
| Forgotten resources | Tagging with owner/environment, regular cleanup, TTLs on experiment environments |

Practices:

- Estimate monthly cost during design using the provider's pricing calculator; state assumptions (requests/month, GB stored, GB transferred).
- Tag everything with owner, environment, and cost centre; enforce tags via policy; review cost by tag monthly.
- Set **budgets and anomaly alerts** in every account, including sandboxes. A misconfigured loop or leaked credential can run up thousands per day.
- Treat commitment purchases as financial decisions for the user; describe options and trade-offs, do not purchase.

## Vendor lock-in and portability

Lock-in is a spectrum and a trade: higher-level managed services deliver more value and more coupling.

- **Cheap portability:** containers, standard protocols (HTTP, SQL, S3-compatible APIs, OpenTelemetry), open-source databases on managed hosting, IaC with modules that isolate provider specifics.
- **Accept lock-in deliberately** where the managed service saves substantial effort and the switching cost is acceptable. Write down the decision and what exit would require.
- **Multi-cloud for its own sake** usually means the lowest common denominator plus two sets of expertise, IAM models, and network integrations. It is justified by concrete needs: regulatory requirements, specific best-of-breed services, acquisitions, or negotiation leverage at large scale. Multi-cloud for resilience is rarely cheaper or more reliable than multi-region on one provider.
- **Data gravity** is the real lock-in: moving large datasets is slow and egress is expensive. Consider where data lives before anything else.

## Well-architected trade-offs

The major providers publish "well-architected" frameworks with similar pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, and sustainability. Use them as a checklist of questions, not as a mandate to maximise every pillar. The pillars conflict:

- Reliability vs. cost: multi-region doubles spend.
- Security vs. operability: tighter network isolation complicates debugging and deploys.
- Performance vs. cost: provisioned capacity vs. scale-to-zero cold starts.
- Simplicity vs. resilience: every redundancy mechanism adds components that can fail.

State which pillar wins for each major decision and why, given the requirements.

## Common workload shapes

Starting points, not prescriptions; adjust to requirements and the existing estate.

| Workload | Typical starting shape | Watch out for |
|---|---|---|
| Static site / SPA | Object storage + CDN + managed certificates; API separately | Cache invalidation on deploy; SPA routing fallbacks |
| Web app + API | Serverless containers or PaaS, managed relational DB (multi-AZ), cache, CDN | DB connection limits as instances scale; cold starts |
| Event-driven processing | Queue or stream → functions or container workers → data store | Idempotency, poison messages (dead-letter queues), retry storms |
| Scheduled batch / ETL | Scheduler → batch jobs or containers on spot → object storage / warehouse | Job overlap, partial failures, cost of always-on clusters |
| Data platform / analytics | Object storage lake + managed warehouse + orchestration | Egress and query costs; governance and access control on shared data |
| ML inference | Managed model endpoints or GPU containers with autoscaling | GPU cost when idle, cold-start time of large models, quota for GPU types |
| Internal tools | PaaS or serverless containers behind SSO / identity-aware proxy | Accidentally public endpoints |
| Real-time (WebSockets, games) | Containers or VMs with sticky/long-lived connections, regional placement | Connection draining on deploy, per-connection load balancing |

## Process for a new design

1. **Capture requirements and constraints** (see discovery). Write down assumed targets if not given.
2. **Sketch the simplest architecture that could meet them,** using the most managed services available on the user's provider.
3. **Walk failure scenarios:** instance dies, zone fails, database fails over, dependency slow, deploy goes bad, credentials leak, region fails. Note what happens and whether it meets targets.
4. **Walk the security model:** who and what can access each resource; what is public; where secrets live; how audit works.
5. **Estimate cost** at expected and 10× load.
6. **Identify the hard-to-reverse decisions** (region, primary data store, identity, account structure) and present options with trade-offs for those.
7. **Document the design** briefly: diagram, components and why, failure behaviour, security model, cost estimate, open questions, and decisions recorded (see `technical-decision-making`).
8. **Hand off implementation** to IaC (`infrastructure-as-code`) and pipelines (`ci-cd-pipelines`).

For reviewing an existing design, run steps 3–5 against what exists and list findings by risk.

## Choosing a provider (when not already decided)

Most organisations should not agonise: the major clouds are broadly comparable for mainstream workloads. Deciding factors, roughly in order of weight:

1. Existing skills, contracts, and estate (including identity — an organisation deep in one productivity suite often finds its sibling cloud easier to integrate).
2. Specific services that matter for this workload (data analytics, ML tooling, a particular managed database).
3. Region availability where users and data must be.
4. Pricing for the dominant cost driver of this workload, from a concrete estimate rather than list-price comparisons.
5. Support and compliance offerings required.

Smaller providers and PaaS platforms can be simpler and cheaper for small workloads; weigh their narrower service range and regional footprint.

## Encryption, data residency, and compliance

- Enable encryption at rest everywhere (it is usually default and free with provider-managed keys). Use customer-managed keys when policy requires control over key rotation, access, or revocation; this adds key-management responsibilities and the risk of locking yourself out of your own data if keys are deleted.
- Encrypt in transit: TLS for all external traffic and, increasingly, for internal traffic too.
- Data residency: choose regions deliberately, restrict allowed regions via organisation policy, and check where backups, replicas, logs, and support tooling store data — residency is often violated by a log pipeline or a global service, not the primary database.
- Compliance frameworks (PCI DSS, HIPAA, SOC 2, ISO 27001, FedRAMP and regional equivalents) mostly require evidence: access controls, audit logs, encryption, change management, vulnerability management. Use services within the provider's compliance scope for the regulated parts, and keep the regulated scope small by isolating it in its own accounts and network.

## Moving existing systems to the cloud

Common migration strategies (often summarised as the "R"s):

| Strategy | What it means | When it fits |
|---|---|---|
| Rehost (lift and shift) | Move VMs as they are | Deadline-driven exits from data centres; first step before optimising |
| Replatform | Small changes to use managed services (managed DB, containers) | Most applications; good effort-to-value ratio |
| Refactor / re-architect | Redesign for cloud-native services | High-value systems where scaling or agility justifies the effort |
| Repurchase | Replace with SaaS | Commodity capabilities (email, CRM, ticketing) |
| Retain | Leave on-prem for now | Hard dependencies, recent hardware investment, regulatory reasons |
| Retire | Switch off | Surprisingly many apps in an inventory are unused |

Migrate in waves, starting with low-risk systems to build skills and landing-zone maturity; move data with the application that owns it; plan the cutover (replication, freeze window, DNS switch, rollback path) as carefully as the target design. See `legacy-modernization` for the application side.

## Worked example: hosting a new SaaS product

Requirements given: B2B web app with an API, ~2,000 users at launch, growth uncertain, team of four developers with no dedicated ops, target 99.9%, RPO 5 minutes, single-country customers, budget "a few hundred to low thousands per month".

Reasoning:

- 99.9% with a small team points to managed, multi-AZ, single region. Multi-region is not justified by the targets and would consume the team.
- Compute: the app is containerised and request-driven; serverless containers (e.g. Cloud Run, App Runner, Container Apps) give autoscaling, zero patching, and per-use cost. Kubernetes would add a platform to run with no benefit at this scale.
- Data: managed PostgreSQL with a multi-AZ standby (synchronous, RPO ≈ 0 within the region), automated backups with point-in-time recovery (meets RPO 5 minutes for logical errors), and daily snapshot copies to a separate account.
- Async work: a managed queue plus a worker service on the same container platform.
- Files: object storage with versioning; CDN for static assets.
- Network: private database with no public IP, connection from the container platform through the provider's private connectivity option; NAT only if workers call external APIs, sized and watched for cost.
- Identity: SSO for the team, workload identities for services, OIDC for CI; production in its own account.
- Cost estimate: modest — dominated by the multi-AZ database instance and the baseline minimum instances kept warm to avoid cold starts — comfortably inside the budget, with budget alerts at 50/80/100%.
- Hard-to-reverse choices flagged for the user: region (residency, latency), PostgreSQL as primary store, and the container platform (moderate lock-in, mitigated by standard container images).

The approach to copy: derive every choice from a requirement, choose the most managed option that meets it, and state the next step if growth demands it (e.g. read replicas, then splitting heavy workloads) instead of building it now.

## Safety notes

- Do not create, resize, or delete cloud resources, change IAM, or open network access in a real account without explicit user confirmation that names the account and resources. Prefer generating IaC for review over direct console/CLI changes.
- Flag designs that make data public, use wildcard IAM, expose management ports, or disable audit logging, even if the user did not ask about security.
- Call out cost risks explicitly (NAT data processing, cross-region transfer, provisioned throughput, GPU instances, unbounded autoscaling, verbose logging) with rough magnitudes.
- Never ask the user to paste long-lived cloud credentials into a conversation; recommend federated, short-lived access and use only what they provide through proper channels.
- Do not purchase commitments, reserved capacity, or marketplace products; present the analysis and let the user decide.

## Pitfalls and anti-patterns

- **Lift-and-shift with no adjustment,** then surprise that the cloud is more expensive than the data centre. Rightsizing and managed services are where savings come from.
- **Over-engineering for scale that may never come:** microservices, multi-region, and Kubernetes for an app with ten users. Start simple; design so the likely next step is possible.
- **Single-AZ production** because the defaults were single-AZ.
- **Everything in one account** with shared admin credentials.
- **Long-lived access keys** in CI variables, laptops, and code.
- **Public buckets and open security groups** "temporarily".
- **NAT gateway egress for everything,** including traffic to the provider's own storage service.
- **Untested backups** and DR plans that exist only as documents.
- **Ignoring quotas** until launch day.
- **No budgets or alerts,** discovering a runaway bill at month end.
- **Chatty cross-zone or cross-region designs** that pay transfer costs on every request.
- **Treating multi-cloud as resilience** without the operational investment to fail over.

## Verification

- [ ] Requirements and assumed targets are written down; each major component maps to a requirement.
- [ ] Failure walk-through done for instance, zone, dependency, bad deploy, and (if in scope) region failures; behaviour meets RTO/RPO.
- [ ] No single points of failure for in-scope failure domains (check NAT, caches, DNS, identity).
- [ ] IAM reviewed: workload identities, no long-lived keys, least privilege, no unintended public resources.
- [ ] Network: private tiers private, no management ports open, egress paths and costs understood.
- [ ] Cost estimate with stated assumptions; budgets and anomaly alerts planned.
- [ ] Backups isolated and a restore test planned or performed.
- [ ] Hard-to-reverse decisions are explicit, with alternatives considered.
- [ ] Design fits the team's operational capacity.

Report the design, the trade-offs chosen and why, the cost estimate, known risks, and open questions requiring the user's decision.
