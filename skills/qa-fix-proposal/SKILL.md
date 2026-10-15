---
name: qa-fix-proposal
description: "Prepare an evidence-backed code/configuration fix or tuning proposal with reviewable patch, rollback and validation before implementation approval."
---

# qa-fix-proposal

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Use the selected RCA/bottleneck conclusion, affected revision and actual code/configuration. Create proposal artifacts under engineering/fixes without changing application code: exact affected files/settings, unified patch or precise commands, scope, evidence, risks/blast radius, rollback steps and regression/performance acceptance/abort plan. Flag uncertain causes and unvalidated patch assumptions.
Bind proposal digest to all content-bearing patch/config files and target revision so later edits invalidate approval. Present the concrete proposal and request explicit implementation approval; do not seek approval for an unspecified future fix. Any external deploy/configuration action requires separately identified scope. Hand the unchanged approved proposal to qa-fix-implementation, or leave it ready for review.

For record fields and content-bound approval preflight, read `references/RECORDS.md`.
