# QA package gap review

Reviewed 15 October 2026. Scope: existing recorder, skills/agents, gate, installer, adapters and new performance/RCA/integration design. This is a local architecture/code review, not a production incident diagnosis.

Status distinguishes implemented procedures, tested code corrections, larger proposals and environment validation. A procedure is not a runtime enforcement mechanism.

## PE-01 — Performance execution lacked a full engineering lifecycle

Priority: P1. Status: Procedure added.

Evidence: `skills/qa-performance/SKILL.md (v1)`.

Change or suggestion: Added dedicated engineering coordinator and workload/correlation/bottleneck/retest specialists.

Next action: Exercise the lifecycle against an approved application baseline.

## PE-02 — Workload validity and baseline comparability were underspecified

Priority: P1. Status: Procedure added.

Evidence: `skills/qa-performance/SKILL.md (v1)`.

Change or suggestion: Added open/closed models, units, generator saturation, sampling/coordinated-omission caveats and percentile comparison rules.

Next action: Supply documented SLOs and a comparable baseline before pass/fail or capacity claims.

## RC-01 — Cause scores could be mistaken for confirmed root cause

Priority: P1. Status: Procedure added.

Evidence: `skills/qa-analysis/SKILL.md (v1)`.

Change or suggestion: Separated suspected/probable/confirmed with mechanism proof and logs/traces/metrics/code agreement; added structural preflight.

Next action: Validate actual evidence credibility; local JSON checks cannot prove causality.

## RC-02 — Fix review, rollback and post-fix validation had no dedicated roles

Priority: P1. Status: Procedure added.

Evidence: `skills/qa-reporting/SKILL.md and agents/qa-analysis.md (v1)`.

Change or suggestion: Added fix-proposal, approval-bound implementation and performance retest specialists.

Next action: Review a concrete proposal before approving any application change.

## MC-01 — No product-specific MCP responsibilities or deployment boundaries

Priority: P1. Status: Procedure added.

Evidence: `agent-manifest.json (v1)`.

Change or suggestion: Added separate Splunk, Dynatrace, NeoLoad, Jira and Confluence skills/agents and documented vendor templates.

Next action: Choose deployment/version/region/auth references during setup.

## MC-02 — No cross-tool correlation or query completeness contract

Priority: P1. Status: Procedure added.

Evidence: `contracts/CONTRACT.md (v1)`.

Change or suggestion: Added IDs/time windows/entities/revisions/clock uncertainty, explicit budgets, pagination and missing-source handling.

Next action: Confirm bounded query budgets and mappings for each environment.

## MC-03 — Meta-tool actions and uncertain writes needed explicit handling

Priority: P1. Status: Procedure added.

Evidence: `agent-manifest.json and skills/qa-setup/SKILL.md (v1)`.

Change or suggestion: Require nested-action discovery/effect classification, exact approvals, launch/write reconciliation and no blind retries.

Next action: Test connector-specific read/denial/timeout/unknown-write scenarios with mocks or approved fixtures.

## MC-04 — Jira/Confluence publishing lacked duplication, field and concurrency rules

Priority: P2. Status: Procedure added.

Evidence: `skills/qa-reporting/SKILL.md (v1)`.

Change or suggestion: Added duplicate search, issue metadata, page-version-aware updates, visibility/redaction and publication receipts.

Next action: Select site/project/space/destination and approve each concrete write.

## FS-01 — Output boundary was checked after directory creation

Priority: P1. Status: Code fixed.

Evidence: `recorder/src/recorder.ts (v1 mkdir before realpath check)`.

Change or suggestion: Added nearest-existing-ancestor validation before mkdir plus post-check; escaping symlink regression test.

Next action: Use workspace ACLs to protect against concurrent filesystem tampering.

## RE-01 — Page-controlled payloads could overwrite evidence fields or bypass masked resource policy

Priority: P1. Status: Code fixed.

Evidence: `recorder/src/recorder.ts (v1 exposed binding and payload spread)`.

Change or suggestion: Added explicit event-kind/field allowlist, upload size/base64 checks and masked-file omission before persistence.

Next action: Treat recorded page events as untrusted observations, not authenticated attestations.

## RE-02 — Explicit stop reason and event URL could be overwritten by later browser state

Priority: P2. Status: Code fixed.

Evidence: `recorder/src/recorder.ts (v1 page close and queued action)`.

Change or suggestion: Preserve explicit-stop and capture URL/page identity before screenshot queue; added stop-reason assertion.

Next action: Continue reporting screenshot-time races rather than promising event-instant capture.

## IN-01 — Broad source traversal could copy undeclared secrets or a nested target workspace

Priority: P1. Status: Code fixed.

Evidence: `scripts/install.py (v1 source.rglob)`.

Change or suggestion: Install only checksum-listed owned files; reject nested target/source escapes.

Next action: Review distribution list before publishing; checksums are not publisher signatures.

## IN-02 — No safe managed-update path existed for installed definitions

Priority: P2. Status: Code fixed.

Evidence: `scripts/install.py (v1 conflict-only overwrite policy)`.

Change or suggestion: Added install receipt and opt-in --update-managed; update only unchanged previously owned files, preserving user edits.

Next action: Preview updates; manually review legacy installs without ownership receipts.

## GA-01 — Malformed versions, duplicate indexes or external JSON symlinks could undermine evidence checks

Priority: P1. Status: Code fixed.

Evidence: `scripts/check_gate.py (v1 current-case map and JSON loading)`.

Change or suggestion: Reject duplicate indexes, non-integer/boolean versions and out-of-root records; added regression tests.

Next action: Use signed attestations if records need protection from deliberate local forgery.

## RE-03 — Confirmed cleanup could remove evidence from a still-running recorder

Priority: P1. Status: Code fixed.

Evidence: `recorder/src/cli.ts (v1 cleanup)`.

Change or suggestion: Record process ID; refuse cleanup of unfinished active/unknown sessions while retaining exact-path confirmation.

Next action: Use a stronger process/session lock if PID reuse or multi-user hosts matter.

## EN-01 — Approvals and execution prerequisites remain agent policy/local JSON

Priority: P1. Status: Approval needed.

Evidence: `contracts/CONTRACT.md and scripts/engineering_checks.py`.

Change or suggestion: Added scoped content-digest checks, but no host hook or signed authorization service.

Next action: Approve host-specific hooks/read-only tool allowlists or an authenticated policy gateway; define identity and revocation first.

## PR-01 — Screenshot masking cannot guarantee removal of arbitrary customer data

Priority: P1. Status: Approval needed.

Evidence: `recorder/src/recorder.ts screenshot mask logic and docs/RECORDER.md`.

Change or suggestion: Preserved conservative input/API redaction and explicit limitations; production monitoring defaults to aggregates/redacted references.

Next action: Approve application-specific selectors, publication review and fixture-based visual redaction acceptance tests; consider omit-screenshot mode.

## RE-04 — Fast navigation, closed frames and native gestures can leave screenshot/action gaps

Priority: P2. Status: Approval needed.

Evidence: `recorder/src/instrument.ts and docs/RECORDER.md`.

Change or suggestion: Explicit screenshot errors and observed event URL are retained; no claim of exhaustive capture.

Next action: Choose an approved queue/backpressure strategy and optional trace/video capture; define acceptance for shadow DOM/canvas/native dialogs.

## BU-01 — The stored-resource cap does not bound all browser/temp memory/disk or dishonest body lengths

Priority: P2. Status: Approval needed.

Evidence: `recorder/src/budget.ts and response.body use in recorder.ts`.

Change or suggestion: Stored payload budget remains strict; unknown-size/compressed body omissions are documented.

Next action: Approve a bounded streaming capture design and separate screenshot/profile/export budgets if hard process quotas are required.

## RV-01 — Crash recovery and multi-file knowledge updates lack transactional guarantees

Priority: P2. Status: Approval needed.

Evidence: `session.json/events.jsonl and agent-written knowledge/version records`.

Change or suggestion: Completion remains explicitly awaiting clarification; partial-state and resume limitations are documented.

Next action: Approve checkpoint/atomic-write/journal design and retained-profile lock handling; test abrupt process termination.

## LV-01 — Templates and vendor docs do not prove tenant capabilities or access

Priority: P1. Status: Environment validation.

Evidence: `integrations/catalog.json and templates/`.

Change or suggestion: Provided edition/version-aware discovery and bounded read acceptance procedure; no live services queried.

Next action: Connect approved tenants, discover exact schemas and validate read-only fixtures before enabling writes or load execution.

## PL-01 — Native IDE discovery and Windows/Linux behavior remain unverified

Priority: P2. Status: Environment validation.

Evidence: `verification.md and adapters/`.

Change or suggestion: Generated native role adapters and portable fallbacks; validated source/metadata locally.

Next action: Run a cross-platform/client acceptance matrix; verify duplicate-skill discovery and supported secret/auth behavior.

## Recommended next decisions

Prioritize EN-01 (enforce permissions/gates at the host), PR-01 (application-specific redaction acceptance), and LV-01 (bounded live connector acceptance). These need a chosen host/application/environment and approval scope; they are not silently enabled by this package.

Provider source links and deployment caveats are in integrations/SETUP.md. The initial package archive is the v1 source snapshot for the findings marked v1.
