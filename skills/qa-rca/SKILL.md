---
name: qa-rca
description: "Investigate QA failures and production incidents, establish causal mechanisms and distinguish suspected/probable/confirmed causes."
license: MIT
---

# qa-rca

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Define symptom, business impact, incident/test window, environment, affected revision and reproduction. Preserve incident timeline and recent deploy/config/data changes. Gather bounded logs/traces/metrics plus relevant code/framework evidence through selected specialists; include contrary observations and alternative causes.
Construct causal chain from trigger→mechanism→failure and contributing factors. Require mechanism proof plus agreement across all four source classes for confirmed; missing/contradictory evidence keeps suspected/probable. Record 0–100 independent support scores by cause (or null), severity and uncertainty separately. Use scripts/engineering_checks.py to validate the record before assigning confirmed. Never call correlation or tool-generated confidence a proven cause. Write versioned engineering/rca JSON/Markdown with evidence links, gaps and next experiments; send concrete fix creation to qa-fix-proposal. Production analysis remains read-only.

For record fields and content-bound approval preflight, read `references/RECORDS.md`.
