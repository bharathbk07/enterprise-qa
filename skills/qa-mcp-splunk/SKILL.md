---
name: qa-mcp-splunk
description: "Discover approved Splunk MCP capabilities and retrieve bounded environment-scoped log/search evidence for performance or RCA."
---

# qa-mcp-splunk

Read `references/CONTRACT.md`, `references/ENGINEERING.md` and `references/CONNECTOR.md`. Confirm product edition/MCP version, deployment, tenant, endpoint, auth reference, allowed indexes/sourcetypes, environment and field mappings. Discover actual tools/nested schemas; do not assume every Splunk product shares an MCP server.
Construct read-oriented SPL/search with explicit start/end, index/environment/service/run/trace filters and bounded result/page/scan/time/call limits supported by the connector. Do not include data-writing/administrative commands in investigation queries. Prefer aggregates and source links; redact safe excerpts before saving. Record query, tool/source reference, timestamps, pagination and missing/late events. Search execution can consume resources; stay inside approved budget. Mutations require exact approval. Return evidence to correlation/RCA; do not independently declare root cause.
