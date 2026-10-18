---
name: qa-engineering
description: "Route performance engineering and RCA/fix requests to focused specialists and product-specific MCP roles."
license: MIT
---

# qa-engineering

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Determine performance project vs QA failure vs production incident, selected application/environment, known run/incident IDs and requested output. Route lifecycle work to qa-performance-engineering; causal investigations to qa-rca; fixes to qa-fix-proposal then qa-fix-implementation only after approval. Route integrations individually: qa-mcp-splunk, qa-mcp-dynatrace, qa-mcp-appdynamics, qa-mcp-datadog, qa-mcp-neoload, qa-mcp-jira, qa-mcp-confluence. qa-setup owns connector discovery/setup approval.
Use selected evidence paths and IDs instead of loading all product outputs. For hosts without delegation, apply each specialist sequentially. The main QA orchestrator retains overall workflow.json; this role writes engineering investigation progress only. Record unresolved human questions and handoff state. Do not automatically run load tests or publish findings.

Use qa-jmeter for selected JMeter execution details. For failed/unavailable access or user-pasted evidence read `references/EVIDENCE.md`; keep source/channel, window and completeness through the handoff.

For full-stack assessment or solution-design scope beyond this engineering investigation, use qa-architect or qa-solution-architecture once with concrete findings/context. Do not bounce delegated RCA/performance tasks between coordinators. Existing confirmation and fix approvals remain unchanged.

When repeated or ongoing work would benefit from durable context, read `references/KNOWLEDGE.md` and route the scoped update/resume to qa-knowledge knowledge mode. Reuse the same application/work note; separate genuinely distinct work only when useful. Pass the matched work ID/path and source deltas in handoffs. Do not create notes for every request, force recording, or repeat known questions.
