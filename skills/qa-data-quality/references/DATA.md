# Data, state and integration correctness

Use the actual database/queue/cache versions and official documentation for their semantics before recommending version-dependent behavior. Existing schema/migration/configuration is evidence of intent; runtime constraints, indexes and isolation need confirmation. Do not infer exactly-once processing or durable delivery from an architecture diagram.

Trace user input and API validation through ownership/authorization, transaction boundaries, persistence, events/consumers, cache/read models and response/UI. Select applicable invariants: uniqueness/referential constraints, tenant isolation, currency precision, timestamp/timezone, null/default behavior, ordering, concurrency/lost updates, idempotent retries, duplicate/out-of-order delivery, reconciliation and retention. Treat unclear business invariants as requirements gaps.

Inspect migration compatibility across mixed versions, backfill/reconciliation ownership, consumer schema compatibility and recoverable rollback. Do not run migrations, event replay, heavy query plans, table exports or cache eviction to inspect a system. EXPLAIN ANALYZE can execute a workload and is not automatically harmless. Use bounded authorized reads and isolated synthetic records; preserve and clean up only records owned by the run.

A failed invariant needs exact schema/build/data conditions, minimal safe input, expected and observed state, environment and evidence without customer values. Differentiate eventual-consistency delay within an agreed window from loss/corruption; no invented convergence deadline. Functional cases retain existing flow/version IDs; strategic remediation flows through solution architecture and concrete approved fixes.
