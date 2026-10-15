---
name: qa-fix-implementation
description: "Apply only an explicitly approved RCA/tuning proposal, validate the change and prepare a comparable retest without automatic deployment."
---

# qa-fix-implementation

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Verify user approval reference, exact action/target/environment, proposal/patch digest and revision. Stop dependent edits if approval is missing, expired/revoked by the user, or content/target changed; resolve while doing unaffected analysis. Agent-written approval metadata alone is not evidence of human authorization.
Apply the smallest approved local patch, preserve unrelated user changes and follow existing framework/data conventions. If the change creates/updates flow automation, also enforce its manual execution gate. Run relevant checks; record actual results, failures and diff in a change receipt. Ask before new dependencies/extra effects not covered by approval. No automatic commit, CI modification, deployment or production rollback. Handoff to qa-performance-retest and RCA; readiness is not deployment approval.

For record fields and content-bound approval preflight, read `references/RECORDS.md`.
