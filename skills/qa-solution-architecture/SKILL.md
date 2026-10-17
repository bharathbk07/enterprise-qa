---
name: qa-solution-architecture
description: "Propose compatible enterprise solutions and justified redesign options with measurable quality goals, tradeoffs, delivery stages and rollback plans."
license: MIT
---

# qa-solution-architecture

Read `references/CONTRACT.md` and `references/ARCHITECTURE.md`. Ground recommendations in the assessed current stack, business constraints, reproducible findings/RCA, quality targets and evidence gaps. Start with compatible improvements. If the project's change strategy is missing and consequential, give one combined assessment and ask the user to choose compatible improvement, structural change, phased modernization or a custom direction. Reuse that confirmed strategy until conditions change.
For each material recommendation explain the mechanism, affected frontend/API/data/integration/infrastructure boundaries, tradeoffs, operating cost assumptions, security/accessibility/resilience impacts, maintainability and migration/testing needs. Recommend redesign only with evidence that benefits justify cost, risk and organizational capacity; include a smaller alternative. Do not invent budgets, throughput, staffing or compliance obligations or default every application to microservices/multi-region.
Write architecture/decisions and solutions artifacts with chosen/deferred alternatives, source findings, measurable acceptance, rollout/rollback or recovery plan, observability and validation ownership. Costs/capacity remain estimates with source assumptions. Separate proposed, accepted, implemented and validated. Hand concrete code/config patches to qa-fix-proposal, followed by explicit approved implementation; strategy acceptance does not approve deployments or external writes. Return recommendations and limitations for qa-reporting, never an unsupported enterprise-readiness certification.
