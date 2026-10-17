---
name: qa-performance-engineering
description: "Coordinate full performance engineering from SLO/workload design through monitoring, bottlenecks, tuning proposals and retesting."
license: MIT
---

# qa-performance-engineering

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Establish business goals, documented SLOs/SLAs, approved baseline, architecture and target test types. Delegate detailed workload specification to qa-workload-model; tool-specific scripts/runs to existing qa-performance or qa-mcp-neoload. Build a plan with test/data/environment ownership, instrumentation readiness, monitoring queries, limits and required approvals.
Use qa-telemetry-correlation for run↔logs/traces/metrics alignment, qa-bottleneck-analysis for capacity/latency mechanisms, qa-rca for formal root cause conclusions, qa-fix-proposal for tuning changes and qa-performance-retest for comparison after approved changes. Do not treat tool execution as engineering completion. Ask missing targets rather than invent defaults; validate generator health and baseline comparability. Report open constraints and hand only established analysis to qa-reporting.

Route selected JMeter operations to qa-jmeter and AppDynamics/Datadog evidence to their matching specialists. On access failures or pasted evidence read `references/EVIDENCE.md`; retain scope/completeness through correlation. Require threshold/abort implementation mapping and profile-bound readiness before execution, without claiming the local check enforces runtime controls.

For profile-bound readiness record fields read `references/RECORDS.md`.
