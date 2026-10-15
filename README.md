# Enterprise QA agent kit

A modular QA pipeline for web applications and APIs: recorded human flows → business knowledge → manual cases/execution → framework automation → performance → evidence analysis → engineering report.

Two core files: `skill-definition.json` catalogs 26 focused skills; `agent-manifest.json` maps 26 specialist roles. Each skill has a short SKILL.md and loads only the shared contract plus task-specific references. Native agents are generated for Cursor, Claude Code and VS Code Copilot; Codex/Antigravity use skills with portable roles; ChatGPT supports uploaded artifacts and local recorder commands. This package is instructions plus a working recorder, not an unattended implementation of every downstream stage.

Start with [installation](docs/INSTALLATION.md), [recorder commands and boundaries](docs/RECORDER.md), [data model](contracts/DATA-MODEL.md), or [architecture](docs/ARCHITECTURE.md).

Validation from package root:

```sh
python scripts/validate.py
python -m unittest discover -s scripts -p 'test_*.py'
npm --prefix recorder test
```

Example agent requests:

- Use qa-recording to record checkout for application customer-portal.
- Use qa-knowledge to summarize recording REC-ID for one combined review, asking only essential follow-ups.
- Use qa-test-design to create cases for Checkout, FLOW-003.
- Use qa-test-execution to execute Checkout, 3 against the approved sandbox.
- Use qa-framework to document the entire existing automation framework and test-data wiring.
- Use qa-automation to update the existing framework for FLOW-003 after checking the manual execution gate.
- Use qa-performance to create scripts; ask me to confirm the run profile before executing.
- Use qa-analysis then qa-reporting for the selected run, including per-cause evidence scores.

Dependencies and adapters are installed only after an approved concrete plan. Do not store application evidence/profile secrets in source control by default. See verification.md for observed test results and remaining platform limitations.

Performance engineering/RCA extensions: [shared engineering rules](contracts/ENGINEERING.md), [MCP setup/templates](integrations/SETUP.md), and [prioritized gap review](docs/GAP-REVIEW.md). There are dedicated workload, correlation, bottleneck, RCA, proposal, approved implementation and retest specialists. Each of Splunk, Dynatrace, NeoLoad, Jira and Confluence has its own skill and agent.

After intentional package edits run `python scripts/sync_package.py` to synchronize generated references/adapters and the owned distribution checksums. `scripts/engineering_checks.py` structurally validates contexts, run profiles, RCA confirmation records and proposal-bound approvals. These checks do not prove causal truth or grant authorization.

Browser policy: recording and UI execution use only dedicated spawned QA browsers. Integrated IDE/app browsers and personal/shared browser attachments are prohibited. Compliant launch tooling is required; API/protocol testing and result analysis remain browser-independent.

Flow documentation: use the user's flow name or suggest names for confirmation/custom input. Every manual flow document embeds actual step screenshots with action, expected/observed outcomes and provenance. See [flow document guidance](docs/FLOW-DOCUMENT.md). Copied screenshots are owned by the flow version so recording cleanup does not break its images. Missing screenshots remain explicit gaps.

Clarification now defaults to one combined flow review, with confirmed workspace/application preferences reused across sessions. Minor uncertainties are grouped into that review; further questions are reserved for essential gaps and required approvals. See [interaction policy](docs/INTERACTION.md).
