# Full-stack functional and nonfunctional architect

Start with **qa-architect** for an end-to-end application quality assessment or enterprise solution design. It covers frontend, APIs/services, databases/caches/queues, external integrations, infrastructure/delivery and observability. It coordinates testing, bug investigation, RCA and evidence-backed remediation without replacing the focused specialists or changing the application's technology stack merely to use this toolkit.

## Assessment and strategy

Use existing application knowledge, source/configuration, reports, architecture diagrams and confirmed preferences first. Assess current architecture before recommending structural change. Prefer compatible improvements; propose redesign only when evidence justifies benefit, operating cost, migration risk and organizational capacity, with a smaller alternative. If missing project strategy matters, ask one guided question with 3–4 choices and free text. Reuse the confirmed answer rather than repeating intake for each specialist.

No source or live access is required for every task: assess the supplied subset and state the missing evidence. A narrow bug/performance/accessibility request does not force a full architecture discovery cycle. Existing flow recording, naming and screenshot requirements apply when that workflow is requested.

## Focused responsibilities

- **qa-architect:** requested scope, selected domains, artifact ownership, combined assessment and canonical quality plan.
- **qa-stack-discovery:** implementation/deployment evidence and end-to-end component/data/trust-boundary mapping.
- **qa-functional-architecture:** business invariants, state/contracts, risk-based test layers and traceability; existing QA roles create and execute cases.
- **qa-security:** scoped threat/control review and safe verified findings, with no implied active scanning permission.
- **qa-accessibility:** selected criterion/version, automated versus manual evidence, human/assistive-technology gaps and remediation.
- **qa-resilience:** failure containment, reliability objectives, recovery and operational readiness; no automatic fault injection.
- **qa-data-quality:** integrity/consistency/isolation, transactions, events, migrations and owned test data.
- **qa-solution-architecture:** compatible remedies, justified structural alternatives, tradeoffs, phased delivery and acceptance.

Existing qa-orchestrate owns recording/manual/automation stages. qa-engineering coordinates performance, RCA, concrete fix proposal and approved implementation. Monitoring specialists retain Splunk, Dynatrace, AppDynamics, Datadog and NeoLoad responsibilities; qa-jmeter remains the JMeter runner specialist. qa-analysis normalizes results and qa-reporting assembles the evidenced report. Hosts without native specialist agents perform selected roles sequentially. No unnecessary spawning or loading of every skill is required.

## Outputs and validation

Store selected artifacts in qa/<application-id>/architecture/ and link canonical knowledge, flows/cases/runs and engineering/rca/fixes. Produce a current-state map, functional/nonfunctional quality plan, findings with reproductions/evidence, solution decisions and prioritized delivery/validation actions only where requested. Excluded/deferred domains, unknown acceptance, incomplete evidence and untested scenarios remain visible. Do not create invented assessments during installation.

Use contracts/ARCHITECTURE.md for quality-plan fields. Local consistency check:

```sh
python3 scripts/architecture_checks.py --record "/path/to/application/qa/application-id/architecture/quality-plan.json"
```

The checker validates traceability, states and references in the record. Valid JSON is not proof that references are truthful, a solution was measured or a system is enterprise-ready. Proposed/accepted/implemented/validated states are distinct. An accepted design does not approve a code/configuration change or deployment. Validate fixes through the existing approved implementation process and relevant functional/nonfunctional tests.

## Examples of requests

- Use qa-architect to assess this application's current stack and propose a risk-based functional/nonfunctional quality plan.
- Use qa-stack-discovery to trace checkout through frontend, authorization, services, events, data and external dependencies.
- Use qa-functional-architecture to map these confirmed business rules to test layers and uncovered cases.
- Use qa-security to review this application's authorization and tenant isolation from source; draft active checks separately if needed.
- Use qa-accessibility to assess the selected flow against our specified WCAG version/level, marking unavailable manual checks.
- Use qa-resilience to review timeout/retry/recovery risks and prepare an experiment plan without running it.
- Use qa-solution-architecture to recommend compatible fixes for these evidenced findings and explain when a larger change is justified.

## Enterprise quality boundaries

A useful enterprise solution states measurable business/quality goals, affected boundaries, security/privacy/accessibility, performance/capacity, reliability/recovery, operability/observability, maintainability, compatibility, cost assumptions and rollout/rollback ownership. These are decision criteria, not a fixed compliance checklist. Do not invent SLOs, legal obligations, recovery targets, cost savings or an approved release decision.

Standards references were checked on 17 October 2026: [OWASP ASVS](https://owasp.org/projects/asvs), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), and [SRE SLO guidance](https://sre.google/workbook/implementing-slos/). Use only applicable, versioned requirements; links do not confer compliance. Domain notes contain focused verification guidance, not copied standards.

Production investigation remains read-only by default. Approved scope is required for load, active security tests, fault injection, failover/restore and data/infrastructure changes. Dedicated spawned browsers remain mandatory for UI operations. Existing automation prerequisites, one safe retry, original-failure retention, RCA evidence standard, privacy and publication approvals remain intact. Local helpers and prompts do not enforce every host's external actions; client/platform/live acceptance is still required.

## Existing native tests and focused references

qa-test-execution now has native-runner mode for selected existing unit/component/contract/integration/end-to-end tests. It inspects the workspace CLI/configuration, executes only the selected tests and preserves runner exit, source reports and first-attempt outcomes under native-runs/. A missing manual flow index does not block this mode. Native runs do not satisfy the manual prerequisite for flow automation. See [NATIVE-EXECUTION.md](../contracts/NATIVE-EXECUTION.md).

Common instructions now retain identity, evidence, permissions and essential browser boundaries. Recording, detailed browser ownership, manual flows, automation and setup rules are loaded from the selected mode reference. Structured plan fields are in [ARCHITECTURE-RECORDS.md](../contracts/ARCHITECTURE-RECORDS.md); security/accessibility/domain reviews need not load the full schema. A validated solution must verify every requirement attached to its source findings, alongside any additional regression checks.

See the [illustrative checkout walkthrough](EXAMPLE-WALKTHROUGH.md) for a complete usage example covering cases, execution, RCA, solution design and honest report states.
