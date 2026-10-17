---
name: qa-setup
description: "Inspect QA prerequisites and install approved missing skill, agent, browser and recorder components in the selected workspace."
license: MIT
---

# qa-setup

Read `references/CONTRACT.md`. Inspect platform/version, existing skill/agent names, Node (>=22), npm, Playwright version/binaries, recorder build and available dedicated browser launch capabilities and Playwright MCP launch/session configuration. Produce a concrete dependency plan with file paths and commands; ask once before missing component installation/configuration.
Use `scripts/install.py` from the source package: dry-run first, then `--apply` following approval. Without --playwright-loop the installer copies toolkit instructions/adapters only and reports official-agent setup pending; include the protected official-agent phase in setup. Install missing npm dependencies and browsers separately within the approved plan. Do not overwrite changed files or existing agent configuration. If MCP is unavailable, use the bundled recorder for demonstrations or approved local Playwright library launch for UI tests. Verify each launches a dedicated QA-owned process and profile; if execution cannot be supported, mark browser work blocked. Integrated-browser fallback is prohibited. Bundled qa-playwright skill and qa-browser agent are part of every workspace installation. For cloud ChatGPT provide portable instructions and upload guidance, not false local execution claims.

For Splunk/Dynatrace/AppDynamics/Datadog/NeoLoad/Jira/Confluence setup read `references/INTEGRATIONS.md` and `references/ENGINEERING.md`. Ask product deployment/version/region/auth reference; inspect actual tools before claiming capability. Templates are manual merge inputs, not connected servers. Those product integration templates are not activated by the installer; the separate approved official Playwright phase may register its local test MCP server.

Read confirmed workspace/application setup preferences and existing configuration before asking. Ask only missing or changed essential settings; do not repeat the full setup questionnaire. Present nonessential uncertainties together. Preferences do not waive installation/configuration approval.

Install the official Playwright planner, generator and healer during setup in addition to the bundled QA roles. Read `references/PLAYWRIGHT-AGENTS.md`; use the protected local initializer, include its definitions/MCP changes in the existing setup approval, and record native vs reference-only readiness. Do not declare setup complete while that phase is merely pending. Use --playwright-loop with install.py or complete setup_playwright_agents.py separately after preparing the approved local dependencies. Preserve existing framework/seed/fixtures, MCP settings and CI. Unsupported clients receive inactive official references and explicit native limitations.

Include AppDynamics and Datadog in selected-product discovery; reuse confirmed mappings. For unsupported tools/auth failures read `references/EVIDENCE.md` and provide permitted API/export or user-query alternatives. Verify deployment-specific capabilities with the bounded live checklist in `references/INTEGRATIONS.md`; local simulated tests are not live acceptance. JMeter setup follows qa-jmeter and the existing project Java/plugin versions.

qa-architect is the full-stack entry point; qa-orchestrate remains the QA-stage entry. Install only the requested platform definitions, verify specialist discovery and preserve existing workspace setup. Architecture roles do not authorize installation of scanners, cloud resources or test targets.
