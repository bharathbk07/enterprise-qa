# Example: assess and test an order checkout flow

**Illustrative guide — no application was tested to create this document.** Harbor Orders, its business rules and candidate defect below are fictional. All application test outcomes are **not-executed**. No screenshots, telemetry, approvals or performance measurements are supplied. The commands/prompts demonstrate how to use the toolkit; replace placeholders with your authorized workspace and targets before execution.

This example follows current-state discovery → functional/nonfunctional planning → manual testing → automation → performance → RCA → enterprise solution → approved fix → validation/reporting. For a narrow request, use only the relevant stage.

## 1. Start with the architect

Example project inputs:

- Application ID: `harbor-orders`; web checkout and order API, with a relational store, queue and external payment sandbox.
- Environment: a permitted isolated staging environment, whose actual endpoint must be supplied.
- Business goal: submit an order once, preserve correct totals, and recover safely when a payment response is delayed.
- Strategy: assess the current implementation first and prefer compatible improvements. Ask about structural change only if a material decision needs it.
- Unknown inputs: real implementation/revision, accepted performance targets, supported browsers/locales, recovery objectives and available evidence.

Start with:

> Use qa-architect to assess the existing Harbor Orders workspace. Map checkout across frontend, authorization, API, persistence, queue and payment integration. Produce a scoped functional/nonfunctional quality plan and prioritize compatible improvements. Inspect source and supplied reports first; do not launch load, active scans, fault injection or external writes.

qa-stack-discovery inspects the actual source/configuration and traces a selected request. It distinguishes configured topology from observed deployed state. The architect asks only essential missing questions and reuses confirmed project answers. It links the existing application knowledge rather than creating another knowledge file for staging.

## 2. Confirm scope and business rules

For this fictional example, assume the product owner supplied these rules:

1. Only an authenticated customer may submit their own cart; one tenant cannot access another tenant's cart/order.
2. The server computes totals and rejects tampered prices and invalid quantities.
3. Available stock must cover the accepted quantity; rejected orders do not charge payment.
4. Repeating the same order operation with the same idempotency key and payload returns the original result without another order or payment. Reusing that key for a different payload is rejected.
5. A payment timeout leaves a visible pending/reconciling state; retry must not blindly create another charge.
6. Successful and failed outcomes are available through the UI and API, with usable keyboard/focus and error/status feedback.

These rules are example premises, not discoveries about a real system. Ask the actual owner to confirm or correct relevant rules before using them as test assertions.

Functional architecture maps rules to UI, service/API-contract, integration and native tests. Select performance, security, data integrity, accessibility and resilience work according to risk and available tools. Unavailable targets or unspecified acceptance criteria remain explicit gaps.

## 3. Record and document the manual flow

> Use qa-recording for the checkout demonstration in a dedicated spawned Chromium session. Ask once for this recording's masking/plaintext choice. Ask separately before storing an authenticated profile. After closure, summarize the suggested flow name, steps, completion and minor uncertainties in one review.

An example combined review is:

> Suggested name: **Submit Checkout Order**. Inferred steps: open cart → review server-calculated total → submit order → observe confirmation or pending payment. Proposed completion: uncertain until you confirm. Was this the completed flow, interrupted, or should the summary be corrected?

Offer meaningful choices and free text. On interruption offer a retained-session resume only if available, or a fresh dedicated session. Browser closure does not itself confirm completion.

The knowledge role then creates the actual versioned flow document with inline step screenshots and provenance. A step might be drafted as:

```text
Step 3 — Submit order
Expected: one order operation is accepted; payment follows the confirmed business rule.
Observed: not recorded in this illustrative guide.
Screenshot: unavailable — no demonstration was captured.
Readiness: draft; actual action screenshot and business clarification are required.
```

When real evidence exists, embed its copied flow-owned screenshot beside the step. Do not use a stock/generated image or a link to a nonexistent screenshot. This guide is not a completed manual flow document.

## 4. Design at least 20 meaningful cases for the flow

The following sample cases derive from the example rules. The actual application may require more. Every case below starts **not-executed**; no execution or evidence is claimed. Full JSON/CSV cases also need IDs/versions, data/role, steps, assertions, cleanup and traceability.

| Case | Scenario | Expected result from the example rules |
| --- | --- | --- |
| CASE-001 | Valid authenticated checkout | Exactly one accepted order with the correct server total. |
| CASE-002 | Unauthenticated submit | Access is rejected; no order/payment is created. |
| CASE-003 | Session expires before submit | Authentication handling is explicit; no unauthorized order/payment. |
| CASE-004 | Another customer's cart ID | Access denied without exposing or modifying that cart. |
| CASE-005 | Another tenant's cart/order ID | Tenant boundary is preserved. |
| CASE-006 | Client changes a unit price | Server ignores/rejects tampering and uses authoritative pricing. |
| CASE-007 | Client changes the submitted total | Incorrect total cannot authorize an incorrect charge. |
| CASE-008 | Quantity is zero | Validation rejects the order without a charge. |
| CASE-009 | Quantity is negative | Validation rejects the order without changing stock. |
| CASE-010 | Quantity exceeds available stock | Order is rejected; no payment is charged. |
| CASE-011 | Quantity exactly equals available stock | Valid order succeeds; remaining stock is correct. |
| CASE-012 | Two customers compete for the final item | No oversell; the unsuccessful operation is not charged. |
| CASE-013 | Same key and identical payload replayed | Original operation/result is returned; no duplicate order/payment. |
| CASE-014 | Concurrent requests share one key/payload | At most one order operation and payment are created. |
| CASE-015 | Same key with a different payload | Conflict is rejected; original order remains intact. |
| CASE-016 | Payment provider times out | Pending/reconciling status is visible; no blind new charge. |
| CASE-017 | Customer retries while payment is pending | Existing operation is reconciled without duplication. |
| CASE-018 | Payment declines | Failure is shown consistently; no successful order is falsely reported. |
| CASE-019 | Keyboard-only successful checkout | Required controls, focus and confirmation can be used/understood. |
| CASE-020 | Checkout validation/error state | Relevant errors and status are available through the UI and API. |

For actual accessibility assessment, map verified criteria to the project's selected standard/version/level and include human/assistive-technology checks. For expired sessions, concurrency and payment failures, use owned synthetic data and sandbox controls; do not create those effects against a real payment provider merely to exercise a case.

## 5. Execute manual cases or existing native tests

Manual request:

> Use qa-test-execution in manual-flow mode for flow Submit Checkout Order in the approved sandbox; within that flow, execute only CASE-013 and CASE-014. Preserve actual first outcomes, assertions and evidence. Use a dedicated spawned browser for UI actions.

Select the flow by comma-separated names/numbers/IDs. Case IDs in this prompt narrow the execution within that selected flow; resolve the actual current case records first. At least two distinct current-version manual cases must actually finish passed/failed with evidence for the flow automation prerequisite. The sample's 20 planned cases currently provide **zero** eligible executions. Missing evidence, blocked cases and older versions do not qualify.

Native request, independent of manual flow setup:

> Use qa-test-execution in native-runner mode to run the selected existing idempotency unit and contract tests. Inspect the repository's real CLI, configuration and fixtures; use only the selected tests. Do not create a flow index or change code to run them. Record the actual command, revision, exit and raw reports.

Native results belong under `native-runs/` with `automated-*` kinds. They do not count as manual executions. A zero exit, empty collection or skipped test is not sufficient for a pass. Preserve the original failure if a permitted safe retry passes.

## 6. Update automation after the prerequisite

> Use qa-framework to document the current runner, fixtures, feature/step wiring, test-data sources and CI. Then use qa-automation for the selected checkout cases after checking current-version manual execution eligibility. Preserve the existing framework and CI.

If fewer than two eligible manual cases exist, show the missing evidence and warn. Proceed only after actual required execution or an explicit user-approved flow/version-scoped override. This document supplies neither. Do not manufacture an override, weaken an assertion, or label a product defect passed to make a suite green.

## 7. Plan performance and nonfunctional verification

> Use qa-performance-engineering to model the checkout workload and monitoring. Preserve the existing k6/JMeter/NeoLoad tool. Ask for missing targets and confirm the complete load profile before execution.

A reviewable profile identifies environment/target, scenario version, concurrent users or arrival rate, transaction mix, stages/duration, data ownership, latency/error/throughput targets, injector limits, monitoring and abort criteria. This guide does not invent those real project values. Closed-model user counts must be positive integers; open rates use their appropriate units.

Map each threshold/abort condition to a verified runner/external mechanism or an explicitly approved manual procedure with owner/cadence. Local readiness JSON alone does not wire the stop mechanism. Native unit tests, browser recordings and protocol load timings measure different things.

For security, begin with the selected source/control review. For resilience, review timeout/retry/idempotency/recovery behavior before proposing fault experiments. Active scans, load, fault injection, failover/restore and real external effects retain their concrete approval requirements.

## 8. Correlate telemetry or request pasted results

Use only the monitoring product actually available: Splunk, Dynatrace, AppDynamics or Datadog; NeoLoad supplies its selected run/result evidence. Carry application/environment, explicit UTC window, source revision, run/service/entity/trace IDs, units, sampling, pagination and completeness through handoffs.

Fallback sequence:

1. Discover and use the permitted MCP read capability.
2. If unavailable, use an already permitted official API or existing local export.
3. If neither is usable, provide the exact scoped product query/command and ask the user to paste bounded redacted results.

For example, give the selected Splunk query only after resolving its real allowed index/environment/service fields and time limits. Request the query/job reference, window, collection time, aggregate rows/counts and truncation. Do not provide an all-time wildcard search or ask for tokens/raw customer records. A denied path cannot be bypassed through a broader credential. Pasted output stays labelled user-supplied, not a direct MCP execution receipt.

## 9. Investigate a candidate defect

**Hypothetical investigation subject, not a reproduced bug:** two concurrent checkout requests may both create an order if an idempotency check and creation are separated without appropriate coordination.

- Requirement: same key/payload must produce one operation.
- Possible impact: duplicate order/payment; actual exposure remains unverified.
- Next checks: selected concurrency reproduction in the approved sandbox, source transaction/idempotency logic, bounded order/payment logs, traces and metrics.
- Current evidence: none supplied by this guide. Finding is a candidate only; no measured frequency or fabricated confidence score is assigned.
- Alternative explanations: different keys, a client bug, replayed events, misleading UI rendering, test-data collision or an already-correct backend.

qa-rca constructs the causal chain with supporting and contrary evidence. A time correlation or duplicate-looking UI row is not mechanism proof. Under this toolkit's agreed standard, confirmed RCA needs reproducible/direct mechanism evidence plus agreement across logs, traces, metrics and code; missing classes keep the cause suspected/probable. Reproducing a symptom does not automatically confirm its cause.

## 10. Propose a compatible enterprise solution

Only if the actual evidence supports the mechanism, qa-solution-architecture could compare:

- An atomic idempotency claim/uniqueness approach in the existing persistence layer, plus payload identity and existing-operation response handling.
- A more structural operation-state design if coordination spans asynchronous workers/external payment states and the existing model cannot safely represent it.

These are design candidates, not patches for an unknown database or payment API. Review concurrency/transaction boundaries, provider behavior, authorization/tenant scoping, retention, deployment compatibility and failure recovery before choosing.

The proposal should identify affected code/configuration, existing-data compatibility, contention/cost assumptions, telemetry, rollout, rollback/recovery and measurable acceptance. For this example, acceptance would retain the original idempotency/concurrency requirements and legitimate success/decline/pending behavior; an unrelated health check cannot validate the fix. Do not call a smaller fix sufficient or a redesign necessary without evidence.

qa-fix-proposal prepares the concrete patch/commands and validation plan. Implementation begins only after approval of that unchanged proposal; strategy acceptance is not deployment permission. No code, configuration, migration, Jira issue or Confluence page is changed by this sample.

## 11. Keep the report honest

A report at this guide's current state would say:

```text
Application: Harbor Orders (fictional example)
Assessment: planning illustration
Scope: checkout functional/nonfunctional quality and candidate idempotency investigation
Manual cases: 20 proposed; 0 executed
Automation prerequisite: not satisfied; no override supplied
Native test results: not supplied
Performance: targets/run approval/results not supplied
Finding: hypothetical candidate, not reproduced
RCA: insufficient evidence; no confirmed cause
Solution: candidate options only; no implementation approval or applied patch
Validation: not performed
Release/enterprise readiness: no conclusion
Screenshots: not captured; manual flow document remains draft
```

For a real report replace each field only with observed or confirmed evidence. Keep cases, first attempts, versions, source reports, thresholds, incomplete domains and open risks visible. Publish to Jira/Confluence only after previewing the destination/content and obtaining the required write approval.

## 12. Optional structured planning example

The JSON below is a **synthetic planning record**, not a test run or approval. Acceptance comes from the fictional rules above; every verification remains not-executed. It intentionally yields an incomplete assessment.

```json
{
  "application_id": "harbor-orders",
  "environment": "example-only",
  "assessment_id": "EXAMPLE-PLAN-001",
  "revision": "not-supplied-example",
  "requested_outcome": "Plan checkout idempotency verification; do not execute",
  "strategy": "undecided",
  "strategy_reference": "",
  "domains": {
    "functional-correctness": {"status": "selected", "rationale": "Example checkout business rules."},
    "performance": {"status": "deferred", "rationale": "Actual SLO and workload profile are missing."},
    "security": {"status": "deferred", "rationale": "Actual target/control scope is missing."},
    "accessibility": {"status": "deferred", "rationale": "Actual UI and project target are missing."},
    "data-integrity": {"status": "deferred", "rationale": "Actual schema/consistency behavior is missing."},
    "resilience-recoverability": {"status": "deferred", "rationale": "Actual failure/recovery objectives are missing."},
    "maintainability-operability": {"status": "deferred", "rationale": "Actual stack and operating evidence are missing."}
  },
  "requirements": [
    {
      "id": "EXAMPLE-REQ-IDEMPOTENCY",
      "domain": "functional-correctness",
      "source_reference": "Fictional business rule 4 in this guide",
      "acceptance": "Concurrent identical requests with one key create at most one order operation and payment.",
      "components": ["example-checkout-api", "example-order-store"],
      "verification_method": "Selected sandbox concurrency case and existing native tests after scope is confirmed",
      "outcome": "not-executed",
      "evidence_references": []
    }
  ],
  "findings": [],
  "solutions": []
}
```

If you copy this record to a separate local file, `scripts/architecture_checks.py` checks its structure. Expect `valid: true` and `recorded_summary: incomplete`; that is not execution, approval or a release pass. Do not place example records into a real application's evidence history as though they were observed results.

## Further reading

- [Full-stack architect guide](FULLSTACK-ARCHITECT.md)
- [Native execution contract](../contracts/NATIVE-EXECUTION.md)
- [Evidence/query handoff](../contracts/EVIDENCE.md)
- [Architecture record fields](../contracts/ARCHITECTURE-RECORDS.md)
- [Manual flow/screenshot guidance](FLOW-DOCUMENT.md)
- [Installation and managed updates](INSTALLATION.md)
- [Verification and remaining limitations](../verification.md)


## Continuing this kind of work later

For a real ongoing checkout investigation, qa-knowledge can update its existing work note with sourced findings, decisions, evidence links and the next action. A second session or a different monitoring tool does not start a duplicate note. A separate accessibility investigation may have its own note if ongoing context will be useful, linked to the same application's canonical knowledge. An isolated query need not create any file. No real Harbor Orders work note is created by this illustrative guide. See [knowledge continuity](../contracts/KNOWLEDGE.md).
