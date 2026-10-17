---
name: qa-data-quality
description: "Assess database, cache, queue and event correctness, consistency, isolation and migration risks with evidence-backed tests and remediation plans."
license: MIT
---

# qa-data-quality

Read `references/CONTRACT.md` and `references/ARCHITECTURE.md`; use `references/DATA.md` for data-specific tests. Map schemas, ownership, constraints, transaction/isolation boundaries, retention, migrations and data movement relevant to the selected flow. Check integrity, uniqueness, precision/timezone, ordering, deduplication, replay/idempotency and tenant/role isolation. Do not assume exactly-once delivery or strong consistency from component names.
Prefer code/schema review and approved bounded read-only evidence. Use existing suitable test data or isolated synthetic data with a cleanup ownership ledger. Active queries, EXPLAIN ANALYZE, migrations, event replay, cache eviction and recovery can impose load or writes; obtain their concrete scope/approval rather than treating them as harmless reads. Do not dump customer tables or write production corrections directly.
Trace input→write/event→read-model/cache→API/UI output and compare against confirmed invariants. Include concurrency and partial-failure scenarios where relevant; retain source versions and eventual-consistency windows. Report reproducible defects versus ambiguous requirements, candidate causes and validation evidence. Delegate cases/execution to existing QA roles and fixes to approved proposal/implementation.
