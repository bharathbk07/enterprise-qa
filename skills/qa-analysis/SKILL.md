---
name: qa-analysis
description: "Analyze functional and performance test evidence and score likely failure causes independently from severity."
---

# qa-analysis

Read `references/CONTRACT.md`. Inventory supplied/workspace reports, runner formats (e.g. JUnit/Allure/Playwright/Cucumber), logs and performance results. Normalize without modifying originals. Link application/flow/case versions, environments and attempts; do not merge mismatched runs into misleading totals. Compare expected assertions and approved thresholds with actual values. Missing threshold is unknown, not pass.
For each failure score each cause independently 0–100: test-data, application-api-bug, automation-code, ui-locator-change, environment. Include evidence, contrary evidence and next validation action; scores are judgment-based support/confidence estimates, not measured probabilities and need not total 100. Use null/unknown when evidence is insufficient. Distinguish application UI bugs from locator drift. Severity and confidence are separate. Preserve failed→passed retry as potential flakiness. Produce `reports/analysis-RUN-ID.json` with coverage denominators, passed/failed/blocked/not-executed, exclusions, limitations, defects, performance assessment and prioritized findings. Hand to qa-reporting.

For formal root cause confirmation hand off to qa-rca. Do not average percentiles; do not use independent 0–100 estimates as causal proof. Missing data/thresholds or incomparable baselines remain unknown/inconclusive.
