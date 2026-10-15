---
name: qa-workload-model
description: "Define realistic performance workloads, documented SLO targets and comparable baseline criteria before load execution."
license: MIT
---

# qa-workload-model

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Derive transaction mix from confirmed business flows and available production aggregates (read-only, redacted). Ask missing business volumes, concurrency/arrival patterns, session length, think time, data cardinality and role mix. Specify open vs closed model, units, peaks, ramp/steady/warmup/cooldown, load/stress/spike/soak/scalability/regression types, dependency assumptions and generator capacity checks.
Map each SLO/threshold to documented source, transaction, metric, percentile/unit/time window, sample count and owner. Record approved baseline/environment/build/data/configuration and confounders. Do not infer transactions/sec from request/sec without a request mix model. Write a versioned workload document/JSON under engineering/workloads and acceptance criteria; unresolved targets block pass/fail conclusions, not all useful analysis. No load execution in this role.
