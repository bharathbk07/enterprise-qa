---
name: qa-mcp-datadog
description: "Investigate Datadog APM, logs and metrics through the observability MCP server or scoped official API/export fallbacks."
license: MIT
---

# qa-mcp-datadog

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Read `references/CONNECTOR.md` for site, authentication, toolset and data semantics. Use the observability MCP server for this role, not the separate local Code Security server. Confirm organization/site, environment, service/version tags and time window. Discover actual tools and nested schemas; expose only needed toolsets.
Use bounded log/APM/metric reads. Preserve metric type, unit, query aggregation/rollup, APM indexing/sampling, retention, trace IDs and pagination. Distinguish monitor state from actual user impact. Do not sum a distribution as though it were a counter or average precomputed percentiles. Toolset filtering reduces exposed tools; it is not an authorization boundary. Do not create monitors, incidents, downtimes, workflows or configuration changes without exact approval.
For missing capabilities, failures or pasted evidence read `references/EVIDENCE.md`. Prefer approved official APIs/exports, otherwise provide a bounded site-specific user query and request pasted redacted results. Never silently change organizations/sites or bypass denied access. Return evidence/completeness for correlation/RCA; no independent confirmed-cause claim.
