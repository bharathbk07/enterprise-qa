---
name: qa-telemetry-correlation
description: "Align test/incident runs with bounded logs, traces and metrics across products while reporting missing links and clock uncertainty."
license: MIT
---

# qa-telemetry-correlation

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Build correlation context with run/incident IDs, environment/application, services/entities, build/deployment, UTC window plus original timezone, trace/request IDs and optional approved run markers. Ask bounded query/export budgets, then use only the requested Splunk/Dynatrace/NeoLoad specialists.
Normalize event time vs ingestion/collection time, clock offsets, trace sampling and retention. Keep source-specific IDs/URLs/query hashes, units, pagination/row limits and completeness. Record exact/mapped/time-only/missing linkage and gaps; never convert co-occurrence to causal confirmation. Avoid joining same-named services across tenants/environments. Write engineering/correlations records with evidence matrix and uncertainties for bottleneck/RCA specialists.
