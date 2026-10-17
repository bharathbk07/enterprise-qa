---
name: qa-resilience
description: "Assess service and infrastructure resilience, failure handling and recoverability using measurable reliability objectives and scoped test plans."
license: MIT
---

# qa-resilience

Read `references/CONTRACT.md`, `references/ARCHITECTURE.md` and `references/RESILIENCE.md` for test/solution selection. Inspect available dependency topology, deployment/resource settings, timeout/retry budgets, circuit breaking, queue/backpressure, idempotency, consistency and failure containment. Include health/readiness, scaling behavior, failover/backup/restore and operational runbooks only where evidence exists. Do not invent availability, RTO/RPO or durability targets.
Distinguish a design review, synthetic fault simulation and actual recovery evidence. Derive candidate scenarios from critical user outcomes and failure modes. Before fault injection, failover, restore, destructive data operations or active diagnostics, prepare concrete target/environment/blast-radius, observability, rollback/stop plan and obtain required action approval. Production investigation stays read-only. A restore plan or configured backup is not a demonstrated recovery.
Correlate observed outcomes with workload/build/configuration and record actual recovery time/data loss plus gaps. Use qa-performance-engineering for load and existing monitoring specialists for bounded telemetry. Return risks, evidence and measurable validation plans; route remediation through solution/fix roles. Do not claim resilience from Kubernetes replicas or retry configuration alone.
