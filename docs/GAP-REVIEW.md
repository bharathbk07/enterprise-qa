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


## Reliability follow-up — 17 October 2026

Scope: proactive setup-to-execution review of the current package and official documentation for Dynatrace, Splunk, AppDynamics, Datadog, NeoLoad and JMeter. No user-reported incident, live tenant access or live load run was supplied. The findings below preserve the original review; the implementation status section records the resulting local changes and remaining limits. Preserve the original confirmed-cause standard, dedicated spawned-browser policy and existing approval boundaries.

Confirmed direction: prioritize practical reliability; use MCP first, then an approved official API or local export, then give the user a scoped query/command and request pasted results. Validate fixes with local tests and simulated connector responses; report live checks separately. The user subsequently selected dedicated AppDynamics, Datadog and JMeter skills/agents with shared fallback/evidence guidance.

### RF-01 — No consistent capability fallback or query handoff

Priority P1. Evidence: integrations/SETUP.md steps 4–5 and the three existing product SKILL.md files require discovery but do not define the agreed fallback sequence or a user-run query packet. Suggestion: introduce a shared fallback procedure with product-specific query references. Record the failed/missing capability and selected path. Provide explicit environment, identifiers, UTC window, bounded limits, query dialect/version, expected fields/units, redaction instructions and a paste template. Never ask for tokens or silently switch tenants. A pasted response is user-supplied evidence, not proof of a live tool call. Missing output stays missing; user-run mutations/load still require approval.

### RF-02 — AppDynamics and Datadog are absent from discovery and routing

Priority P1. Evidence: integrations/catalog.json, skill-definition.json, agent-manifest.json and qa-telemetry-correlation name only the existing providers. Suggestion: add scoped product guidance and explicit routing without loading every provider. AppDynamics requires its own Controller/Analytics authentication distinction; Datadog requires site-specific setup and restricted toolsets. Choose focused specialists or references after reviewing these findings. Do not claim either product is connected.

### RF-03 — Documentation freshness lacks an operational refresh decision

Priority P2. Evidence: integrations/catalog.json records 15 October sources; Splunk guidance is explicitly pinned to 1.0 while official 1.3 guidance is available. This alone does not make the deployed 1.0 instructions invalid. Suggestion: retain verified source/version/date per product, compare against the actual deployment during setup, and rediscover on permission/server changes. Keep supported deployment boundaries and unresolved differences explicit rather than replacing all configurations with the newest endpoint.

### RF-04 — Generic discovery guidance has no simulated failure acceptance suite

Priority P1. Evidence: scripts/test_engineering.py exercises records, gates, approvals and installation, but does not test normalized connector outcomes for denied access, expired authentication, throttling, empty/partial results, pagination or uncertain launch outcomes. Suggestion: add deterministic fixture-driven checks for evidence/fallback decisions; preserve reason, completeness and retry budget. Simulations must be labelled synthetic. They cannot certify authentication, vendor schemas or host policy enforcement.

### RF-05 — JMeter is named but its execution contract lacks tool-specific detail

Priority P1. Evidence: skills/qa-performance/SKILL.md and contracts/ENGINEERING.md provide general load guidance, without a JMeter reference or specialist. Suggestion: document existing JMX/plugin/Java dependencies, dynamic correlation, CSV sharing/recycling, assertions, non-GUI execution, injector limits, JTL fields/units, unique result paths, dashboard output requirements and aggregate-sample pitfalls. Use CLI load execution and disable expensive debug listeners, following Apache documentation. Do not assume that JMeter executes browser JavaScript or that a process exit proves SLO compliance. Preserve the existing tool rather than migrate the application.

### RF-06 — Structural profile checks do not establish executable stop criteria

Priority P1. Evidence: scripts/engineering_checks.py requires nonempty thresholds, abort_conditions and generator_limits; it does not validate tool-specific executable mappings or prove an abort mechanism is wired. This is consistent with its structural-only disclaimer. Suggestion: add a pre-execution mapping from each approved threshold/abort condition to a supported runner check, owner or manual stop procedure, and report unmapped conditions before launching. Do not report an abort as enforced merely because it appears in JSON.

### RF-07 — User-pasted evidence needs provenance and completeness handling

Priority P1. Evidence: contracts/ENGINEERING.md covers tool/query provenance but has no explicit handoff for the newly chosen paste fallback. Suggestion: retain user-provided source, time window, collection time, query and filters, omitted fields, counts/continuation markers, units and redaction status. Identify unknown fields without guessing, retain conflicting results separately and request only the missing critical slice. No synthetic trace IDs, invented totals or confirmed RCA from a truncated excerpt.

### RF-08 — Runtime enforcement and client/live acceptance remain unresolved

Priority P1. Evidence: existing EN-01/LV-01/PL-01 and verification.md. Suggestion: keep these findings open. Validate local simulated decisions now; provide a per-product bounded read and denial test checklist for later approved tenant validation. Host hooks or policy gateways require a chosen host and explicit implementation scope; documentation-only changes cannot close enforcement gaps.

### Official sources checked for this follow-up

- Dynatrace: [remote MCP capabilities and permissions](https://docs.dynatrace.com/docs/dynatrace-intelligence/dynatrace-mcp).
- Splunk: [MCP Server for Splunk platform 1.3](https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/1.3/about-mcp-server-for-splunk-platform).
- AppDynamics: [26.7.0 MCP client and authentication](https://help.splunk.com/en/appdynamics-saas/mcp-server-integration/26.7.0/configure-an-mcp-client), [deployment](https://help.splunk.com/en/appdynamics-saas/mcp-server-integration/26.7.0/deploy-the-mcp-server).
- Datadog: [observability MCP server](https://docs.datadoghq.com/mcp_server/), [toolsets and permissions](https://docs.datadoghq.com/mcp_server/tools/). Site-specific setup must be verified for the selected tenant; do not infer a universal URL.
- NeoLoad: [Web meta-tool discovery](https://docs.tricentis.com/neoload-web-v2/en-us/content/ai_integration/mcp_meta_tool.htm), [User Path MCP client actions](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/mcp_actions.htm). These are different capabilities.
- JMeter: [CLI execution](https://jmeter.apache.org/usermanual/get-started.html), [best practices](https://jmeter.apache.org/usermanual/best-practices.html), [dashboard generation](https://jmeter.apache.org/usermanual/generating-dashboard).


### Follow-up implementation status — 17 October 2026

- **RF-01 — Procedure and checker added.** Shared fallback/query packet in contracts/EVIDENCE.md; explicit denial and uncertain-write handling. Next: Validate a bounded permitted read and query handoff for the chosen tenant.
- **RF-02 — Skills and routing added.** Three focused skills/agents and generated client exports; provider registry/templates updated. Next: Verify actual client discovery and selected product capabilities.
- **RF-03 — Sources refreshed.** Six product references dated 17 October; Splunk version boundaries and per-provider source dates retained. Next: Compare actual deployed release and refresh after tool/permission changes.
- **RF-04 — Local synthetic tests added.** Twelve new tests cover normalized evidence outcomes and readiness mappings. Next: Live product/auth/protocol acceptance remains separate.
- **RF-05 — JMeter procedure added.** Dedicated qa-jmeter with JMX/CLI/JTL/dashboard and data/runner guidance. Next: Validate selected JMX/plugins and stop behavior against an approved fixture/profile.
- **RF-06 — Structural mapping check added.** Profile-bound readiness requires every threshold/abort mapping and verification reference; manual controls need owner/cadence/approval reference. Next: Actual runner control wiring/enforcement remains unverified and must be checked before launch.
- **RF-07 — Evidence procedure and checker added.** Pasted results retain user-supplied provenance; failed, empty, partial and conflicting records remain limited. Next: Review real pasted/exported evidence semantics and redaction.
- **RF-08 — Open — host/live validation.** No policy gateway, host hook or live connection was introduced. Next: Select approved host/tenant and complete the bounded acceptance checklist.

These statuses distinguish added guidance, local structural checks and synthetic tests from runtime enforcement and live acceptance. No load run or vendor connection is claimed.


## Full-stack architecture expansion — 17 October 2026

Package 0.3.0 adds eight focused roles for a total of 37: qa-architect, qa-stack-discovery, qa-functional-architecture, qa-security, qa-accessibility, qa-resilience, qa-data-quality and qa-solution-architecture. The user selected end-to-end functional/nonfunctional scope and an assess-first strategy favoring compatible changes, with project strategy clarification when consequential and redesign justified by cost/risk evidence.

Implemented guidance now covers stack/trust-boundary discovery, quality-domain scoping, requirement-to-test traceability, evidence-backed defect reporting, domain-specific verification and enterprise solution tradeoffs/validation. Existing QA/performance/RCA and product roles remain operational entry paths. Added local plan consistency checks with nine synthetic scenarios; these check records, not a real application.

Remaining limitations stay open: native client acceptance, actual scanner/assistive-technology/runner capabilities, authorized target evidence, runtime permission/gate enforcement, screenshot redaction/capture and crash/budget issues documented above. Standards links and generated roles do not establish compliance or enterprise readiness. No real application's architecture, bugs, root causes or solution performance were assessed by installing these definitions.
