---
name: qa-bottleneck-analysis
description: "Diagnose latency, saturation, capacity and scalability bottlenecks using correlated workload and system evidence."
license: MIT
---

# qa-bottleneck-analysis

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Inspect the selected workload/run/correlation evidence and generator health. Trace transaction critical paths across browser/network/API/dependencies/database/cache/queue/infrastructure. Investigate CPU/run queues, memory/GC/leaks, connection/thread pools, lock contention, queue lag/backpressure, database waits/plans (read-only where permitted), cache hit/eviction, network errors and downstream limits when evidence supports them.
Separate symptoms, limiting resource, triggering condition and contributing factors. Distinguish frontend/application UI faults from test locator drift. Check load-generator limits, coordinated omission, autoscaling behavior and sampling before attributing capacity. Do not average percentiles or compare incompatible metric units. Produce ranked hypotheses with supporting/contrary evidence and next causal validation experiment. Formal confirmed labels belong to qa-rca; tuning mutations belong to approved fix implementation.
