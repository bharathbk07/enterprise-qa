---
name: qa-engineering
description: "Route performance engineering and RCA/fix requests to focused specialists and product-specific MCP roles."
license: MIT
---

# qa-engineering

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Determine performance project vs QA failure vs production incident, selected application/environment, known run/incident IDs and requested output. Route lifecycle work to qa-performance-engineering; causal investigations to qa-rca; fixes to qa-fix-proposal then qa-fix-implementation only after approval. Route integrations individually: qa-mcp-splunk, qa-mcp-dynatrace, qa-mcp-neoload, qa-mcp-jira, qa-mcp-confluence. qa-setup owns connector discovery/setup approval.
Use selected evidence paths and IDs instead of loading all product outputs. For hosts without delegation, apply each specialist sequentially. The main QA orchestrator retains overall workflow.json; this role writes engineering investigation progress only. Record unresolved human questions and handoff state. Do not automatically run load tests or publish findings.
