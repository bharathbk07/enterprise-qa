---
name: qa-reporting
description: "Produce an engineering report from evidenced QA analysis with coverage, defects, thresholds and prioritized recommendations."
---

# qa-reporting

Read `references/CONTRACT.md`. Read the selected analysis JSON and only its referenced evidence. Write `reports/engineering-RUN-ID.md` plus JSON index. Include application/revision/environment/run scope, coverage denominators, outcomes including blocked/not-executed, defects with reproduction and evidence, safe retry history, per-cause scores with caveats, performance percentiles/errors/throughput against approved thresholds, limitations, likely causes and prioritized recommendations with owners when known.
Separate facts from hypotheses; unknown results stay unknown. Do not assert a release is ready unless criteria and sufficient evidence establish it. Include traceability to knowledge rules/flows/cases/runs. Report proposed fixes; apply them only on request. Default output is Markdown/JSON with CSV execution/case records; other formats need a request.

Engineering/RCA reports carry suspected/probable/confirmed labels and the four-source evidence matrix. Jira/Confluence publication routes to their individual MCP specialists and requires explicit write approval.
