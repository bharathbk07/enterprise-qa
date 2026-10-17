---
name: qa-test-execution
description: "Execute selected manual UI/API cases or existing native unit, component, contract, integration and end-to-end tests with truthful evidence and separate provenance."
license: MIT
---

# qa-test-execution

Read `references/CONTRACT.md`. Select the mode from the requested work before looking for flow records. Never require a recording or manual flow index to execute an existing native test. Inspect the actual runner, selection, hooks/fixtures, target and effects before execution; use qa-framework findings when available. Missing tooling is a concrete blocker/setup task, not permission to install or migrate a framework.

For manual-flow mode read `references/FLOWS.md`. Parse comma-separated flow names/numbers/IDs against the application index, resolving all selections first. Execute only selected current-version cases. Confirm missing environment/data/roles/locale/device settings. UI work goes through qa-playwright; read `references/BROWSER.md` before browser execution. Direct API cases may use their client without a browser. Ask for human judgment/MFA only when necessary. Track owned synthetic data and sandbox effects.

Write manual runs/RUN-ID.json, CSV and Markdown with case/flow versions, expected/actual, environment, timestamps, evidence and attempts. Preserve first failure and at most one safe retry; inconsistent outcomes are potentially flaky. Read `references/AUTOMATION.md` when reporting manual gate eligibility: only distinct current-version first-attempt manual passed/failed cases with evidence qualify. Cleanup only run-created data and retain evidence until requested deletion.

For native-runner mode read `references/NATIVE-EXECUTION.md`. Accept selected existing tests/paths/tags and layer directly; run the workspace's inspected CLI command in its working directory. Record actual exit code, source reports, runner test IDs, first outcomes/attempts, selection, environment/revision and limitations under native-runs/. Do not call an empty collection, skipped/blocked tests or zero exit alone a pass. UI-based native tests retain dedicated-browser ownership. Native results have automated-* kinds, do not enter manual runs/ and never satisfy the two-case manual prerequisite. Hand native results to qa-analysis and requirement results to the calling architect.
