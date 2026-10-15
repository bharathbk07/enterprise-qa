---
name: qa-automation
description: "Create or update a local automation framework for selected flows after manual execution evidence or an explicit prerequisite override."
license: MIT
---

# qa-automation

Read `references/CONTRACT.md`. Load qa-framework findings and current flow/case records. Before edits, use the gate helper `scripts/check_gate.py` in source package or installed `.qa-agent/scripts/check_gate.py`. Two distinct cases for every selected current flow must have actual first-attempt passed/failed evidence. If insufficient, warn with missing counts and request an explicit override scoped to flow/version; write `overrides.json`. Do not treat an old override as applying to a new version.
Preserve existing framework, dependencies, BDD/feature conventions and data wiring. If no framework exists, ask user to choose framework/language. Implement selected test intent with durable locators, assertions and data references; preserve user work. Update framework knowledge and traceability. Apply local changes, run relevant checks, present diff and observed results. No unsolicited migration, Git commit or CI changes. Do not invent successful execution when browser/environment is unavailable.

For generated browser automation, preserve the framework while ensuring its runner spawns a dedicated QA browser. Do not generate integrated-browser steps or attach to personal/shared sessions. If existing configuration requires a shared browser, propose the minimal approved dedicated-launch configuration before execution.
