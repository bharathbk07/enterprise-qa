---
name: qa-performance
description: "Create or update k6/JMeter performance scripts and execute only a confirmed load profile for selected application flows."
---

# qa-performance

Read `references/CONTRACT.md`. Preserve existing k6/JMeter/NeoLoad conventions; ask tool choice when none exists or selection is ambiguous. Derive workload from selected business/API flows and evidence; parameterize auth via environment/secret references, correlate dynamic tokens/IDs, avoid record-and-replay with stale values. Account for role/data variation, think time, checks and data ownership.
For script creation ask only necessary missing design inputs. Before any execution ask missing target/environment, VUs or arrival/request rate, stages/duration, request mix, warmup, thresholds (latency percentiles, error rate, throughput), resource limits, abort criteria and permitted side effects. Present and confirm complete run profile, storing approval timestamp/profile hash. Script generation is not run approval. Run only within approved limits, stop on configured abort conditions. Write scripts plus run instructions and preserve raw results; hand to qa-analysis.

Full engineering work routes to qa-performance-engineering; NeoLoad tool operations route to qa-mcp-neoload. When applying engineering run profiles also read `references/ENGINEERING.md`.
