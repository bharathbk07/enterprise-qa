---
name: qa-functional-architecture
description: "Design full-stack functional quality strategy and trace business rules, state transitions, API contracts and data invariants to tests and reproducible defects."
license: MIT
---

# qa-functional-architecture

Read `references/CONTRACT.md` and `references/ARCHITECTURE.md`. Use confirmed business knowledge, architecture and contracts to identify actors, permissions, state transitions, invariants and critical journeys. Model success/failure, boundaries, concurrency, idempotency, partial completion, asynchronous events and third-party behavior where applicable. Separate observed behavior from expected rules; ask only missing acceptance criteria that change an outcome.
Choose unit/component, service/API-contract, integration and end-to-end checks at meaningful boundaries, preserving existing framework conventions. Map requirement/risk → component/flow → scenario/case/version → expected result → execution evidence. Send selected existing unit/component/contract/integration/end-to-end tests to qa-test-execution native-runner mode with runner selection, working directory, revision, requirements and permitted effects; no manual flow index is required. Delegate manual flow cases and flow automation to their existing QA roles; retain at least 20 distinct cases per selected business flow and the current manual-execution gate, without padding or duplicating tests at every layer.
For a suspected bug capture minimal safe reproduction, exact input/state/role/environment/revision, expected versus actual and evidence. Distinguish application defects from requirements gaps, test-data issues and test-code failures. Preserve failed attempts and route cause confirmation to qa-rca. Return architecture/functional-plan.md and traceability.md for the selected scope; qa-architect assembles the canonical quality-plan.json; uncovered/blocked requirements remain explicit, not counted as passed.
