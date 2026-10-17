---
name: qa-jmeter
description: "Inspect, create or update JMeter JMX plans, prepare approved CLI load runs and assess JTL/dashboard evidence without migrating existing tools."
license: MIT
---

# qa-jmeter

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Read `references/JMETER.md` for JMX inspection, execution and JTL semantics. Use this specialist only when JMeter is selected or already present; qa-performance coordinates tool choice and the approved run profile. Preserve existing JMX structure, Java/plugin versions, properties, CSV data ownership and CI. Never load an untrusted JMX/plugin merely to inspect it; inspect XML as data first.
Prepare correlated dynamic tokens, separate sessions, business assertions, realistic pacing and the approved open/closed workload. Record precise non-GUI command, property references, generator readiness, unique output paths and monitoring. Map every threshold and abort condition to a verified implementation or named approved manual procedure before execution; `scripts/engineering_checks.py --kind readiness` checks that mapping against the profile digest, not its actual enforcement. Obtain complete run-profile approval; execute once, reconcile uncertain starts, stop only within the approved abort plan and retain partial results.
Interpret JTL/dashboard errors, counts, elapsed/connect/latency units and transaction samples without double counting. Process completion is not an SLO pass. Hand analysis to qa-analysis and causal hypotheses to qa-rca. For missing execution access or user-run results read `references/EVIDENCE.md`; provide commands for the user and request bounded redacted output, never claim a run occurred. Protocol testing needs no browser; any browser-based runner must spawn a dedicated QA-owned browser.

For profile-bound readiness fields read `references/RECORDS.md`.
