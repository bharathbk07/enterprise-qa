---
name: qa-test-execution
description: "Execute selected manual UI/API cases with dedicated spawned browsers, evidence, human judgment and versioned run records."
---

# qa-test-execution

Read `references/CONTRACT.md`. Parse comma-separated flow names/numbers/IDs against the application index. Resolve all selections before execution. Confirm target environment and missing data/roles/browser/locale/device matrix. Execute only selected current-version UI cases through qa-playwright in a dedicated spawned QA-owned browser. Record launch/session ownership evidence; if compliant spawning is unavailable, mark affected cases blocked. Direct API cases may use their API client without opening a browser. Ask for judgment or MFA when needed. Track run-owned synthetic data and use sandbox effects.
Record every case outcome, actual vs expected result, environment, timestamps, evidence paths, first attempt and at most one safe retry. Preserve original failure; inconsistent results are potentially flaky. Block missing prerequisites/unsupported tools rather than report pass. Write `runs/RUN-ID.json`, CSV and Markdown execution document with totals, defects and limitations. Passed/failed first attempts with evidence count for automation gate; blocked/not-executed do not. Report the two-case eligibility per flow/version. Cleanup only run-created data; retain evidence until requested deletion.
