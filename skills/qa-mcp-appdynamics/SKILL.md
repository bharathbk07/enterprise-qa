---
name: qa-mcp-appdynamics
description: "Investigate AppDynamics application, transaction, snapshot and metric evidence through discovered MCP tools or scoped official API/export fallbacks."
license: MIT
---

# qa-mcp-appdynamics

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. For product setup, authentication and evidence selection read `references/CONNECTOR.md`. Resolve Controller/account, application, tier/node and business transaction IDs, deployment and UTC window before querying. Keep Controller and optional Analytics credentials separate; Analytics availability is not implied by APM access.
Discover actual tool schemas and read capabilities. Correlate transaction snapshots, call graphs, errors, backend/database timings and metric rollups without equating a sampled snapshot to all traffic. Preserve resolution, sample selection and missing visibility. Vendor diagnosis is a hypothesis until qa-rca establishes the agreed mechanism/evidence standard. Infrastructure or Virtual Appliance administration is outside this read-only monitoring role.
On missing capabilities, connection failure or pasted results read `references/EVIDENCE.md`: MCP → approved official API/local export → scoped user-run query/command and pasted results. Do not bypass a permission denial. Return source IDs, bounded query details, completeness, redacted aggregates and the next validation request. No instrumentation/configuration changes or active diagnostics without concrete approval.
