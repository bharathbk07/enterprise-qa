# Engineering records and local preflight

All records live under `qa/<application-id>/engineering/`. Use versioned investigation/workload/profile/proposal IDs and source timestamps. Missing data is explicit; no real incidents/results are bundled.

Context record: application_id, environment, investigation_id, start_utc, end_utc, original_timezone, baseline_window, run/tool/trace/request/service/entity IDs, revision, clock_uncertainty and query_budget {max_rows, max_pages, max_calls, timeout_seconds, optional scan budget supported by the connector}. Evidence references also record source tool/query, collected_at, completeness/pagination, sampling, retention and redaction policy.

Profile: context identity/window, tool k6/jmeter/neoload, target_ids, workload_id, load {model open/closed, value, unit}, duration_seconds/stages, thresholds linked to documented SLOs, abort_conditions, generator_limits and monitoring_plan. The preflight checks structure, not safe load ceilings. Complete profile confirmation and real user authorization are separately required.

RCA: investigation_id, application_id, environment, cause, classification suspected/probable/confirmed, mechanism_evidence (reference array), evidence_matrix {logs, traces, metrics, code}, missing_sources, contradictions, cause_scores (each original five categories 0–100 or null), severity, provenance and next validation. Confirmed fails preflight without all four classes and mechanism references or with unresolved gaps. A structurally valid record cannot prove that the evidence is truthful or causal.

Fix proposal: proposal_id/version, action, target, environment, base_revision, affected_paths, evidence, exact patch/config payload or patches [{path, sha256}], risks, rollback and validation_plan. Approval: explicit true, authorized_by, trusted authorization_reference, authorized_at (timezone-aware), action, target, environment and proposal_digest. Digest uses canonical JSON with sorted keys and compact separators; include all content-bearing references/hashes. The implementation agent must match approval to a real user instruction; it cannot create approval for itself.

CLI checks:

```sh
python scripts/engineering_checks.py --kind context --record context.json
python scripts/engineering_checks.py --kind profile --record profile.json
python scripts/engineering_checks.py --kind rca --record rca.json
python scripts/engineering_checks.py --kind approval --record approval.json --proposal proposal.json --artifact-root "/path/to/application/qa/app/engineering/fixes"
```

`--artifact-root` is required by approval preflight when patch files are referenced; each relative path must stay within that root and match its hash. Exit 2 means missing/mismatched structure or content. This does not provide signed approvals, revocation enforcement or interception of every client's mutation tools.

Jira/Confluence drafts retain content digest, destination IDs, expected version, evidence links, redaction review and requested action. After a write, retain returned ID/URL/version and verified outcome. Unknown outcomes remain unknown until reconciliation.

Readiness record: profile_digest (same canonical digest as the unchanged profile), controls (array). Every profile thresholds[i] and abort_conditions[i] must have exactly one mapping with criterion `thresholds:i` / `abort_conditions:i`, mechanism `native` / `external` / `manual`, implementation_reference, verification_reference, verified_at (timezone-aware). A manual mapping also requires owner, observation_interval_seconds (positive), and explicit_manual_approval_reference. References point to actual runner configuration/validation evidence or a concrete approved human procedure, not self-certified truth. The helper validates mappings and the profile first; it cannot inspect external configurations or enforce runtime behavior.

```sh
python3 scripts/engineering_checks.py --kind readiness --record readiness.json --proposal profile.json
python3 scripts/evidence_checks.py --record evidence.json
```

For fallback/query packets and evidence-envelope fields read contracts/EVIDENCE.md from the installed package, or the selected skill's references/EVIDENCE.md. No raw credentials in provenance. Failed/partial/pasted output retains its actual source channel and limitations.
