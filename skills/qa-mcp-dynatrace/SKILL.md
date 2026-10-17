---
name: qa-mcp-dynatrace
description: "Discover Dynatrace MCP tools and retrieve bounded DQL, entity, problem, metric and trace evidence for engineering investigations."
license: MIT
---

# qa-mcp-dynatrace

Read `references/CONTRACT.md`, `references/ENGINEERING.md` and `references/CONNECTOR.md`. Confirm supported Dynatrace deployment, environment, MCP capabilities, entity mappings and auth/permission references. Discover actual DQL/problem/entity/trace/metric tools and nested schemas; available tools vary by tenant/permissions.
Use explicit environment/time windows and connector-supported scan/row/page/time/call budgets. Resolve entity IDs before joining service names. Check metric units, timeseries aggregation, trace sampling, ingestion delay and topology/revision changes. Treat automated problem explanations as evidence/hypotheses, not causal proof. Return redacted aggregates and trace/entity/source IDs; preserve gaps. Do not alter alerting, instrumentation, settings or run active diagnostics without action-specific approval. Link to common correlation context.

For official product-specific setup and query/export handoffs read `references/CONNECTOR.md`. On missing capabilities, connection failure or pasted results read `references/EVIDENCE.md`; follow MCP → permitted official API/export → scoped user query and pasted results. Preserve permission boundaries and label user-supplied evidence.
