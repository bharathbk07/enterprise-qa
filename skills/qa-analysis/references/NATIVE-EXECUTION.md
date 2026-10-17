# Native unit, component, contract, integration and end-to-end execution

Use qa-test-execution in native-runner mode for selected existing framework tests or framework checks requested by a functional-quality/architecture task. This mode does not require flows/index.json, a manual flow name, or a recording. Manual UI/API cases retain the separate manual-flow mode and gate rules. Test-code creation still goes to qa-automation or an approved fix workflow as appropriate; execution does not authorize edits or dependency changes.

## Handoff and operation

The caller supplies application/environment, source revision, requested test layer, affected requirements/components, selected test paths/IDs/tags, working directory, expected runner/report format, data/fixture and external-effect limits, and any relevant approval reference. Inspect existing package commands, runner configuration, fixtures/hooks, plugins, targets, retries and reports first. Discover the command from the actual workspace; do not guess a runner or install a new framework. A missing flow index does not block a selected existing unit test. Missing runner/dependency or an ambiguous selection is a concrete blocker or essential clarification.

Run only the selected tests with the existing CLI in its working directory and record literal argv without secret values. Inspect commands/hooks before execution; integration/contract tests can call external systems. Use local/sandbox fixtures and existing effect/approval policies. UI-based runners must spawn a dedicated QA-owned browser; never attach an integrated/personal/shared session. Keep the original attempt and at most one safe agent retry; account for runner-configured retries before launching. Do not hide or erase retries in imported reports.

Collect actual runner exit code, raw report/log references, discovered/executed/skipped/failed counts, test IDs, assertions and environment/revision. Zero exit or a successful collection is not evidence that selected tests ran. Empty collection, unsupported report semantics and blocked/skipped tests are explicit, not passes. Preserve first failure even if a safe retry passes, labelling potential flakiness. Native execution may be independently requested without a manual flow; it never satisfies the manual two-case prerequisite.

## Result contract

Store under qa/<application-id>/native-runs/RUN-ID.json, with source artifacts in native-runs/assets/RUN-ID/. Keep these records out of the manual runs/ glob. Fields:

- schema_version `1.0`, application_id, environment, run_id, source revision, runner, working_directory, command (argv array), started_at, ended_at (timezone-aware), runner_exit_code (actual integer or null when not executed), status (passed/failed/blocked/not-executed).
- execution_kind: automated-unit, automated-component, automated-contract, automated-integration or automated-e2e.
- report_references (paths relative to the application artifact root), limitations (string array), and tests (array of {test_id, status, attempts: [{status, evidence_references}]}). test status preserves the first attempt; keep later attempts separately. Optional requirement_ids, source_test_path and existing flow/case/version references are traceability, not fabricated prerequisites.

The status is the assessment preserving original failures, while runner_exit_code records the tool's actual exit (which can be zero after an internal retry). Export attempts where supported; when an imported report cannot expose original attempts, record that limitation without inventing them. Block unsupported normalization rather than declaring an unknown test passed. If selected tests did not run, use blocked/not-executed with the reason; collection/runtime failure may be failed with its source log and nonzero exit.

From the source package or installed .qa-agent directory:

```sh
python3 scripts/native_run_checks.py --record "/path/to/native-runs/RUN-ID.json" --application-root "/path/to/application/qa/application-id"
```

The optional root verifies evidence paths exist, are nonempty and stay inside the application artifact root; omit only for reference-only/upload analysis and report that path checks were not performed. This helper validates the agent's normalization, not runner protocol truth, test quality or user authorization. Execution remains the agent's actual CLI operation. qa-analysis consumes native runs with their layer/selection/revision and counts; qa-architect links their requirement results into the quality plan. Preserve source reports and avoid merging different revisions/targets.
