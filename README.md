# Enterprise QA Agent Kit

[MIT license](LICENSE) · [Getting started](docs/GETTING-STARTED.md) · [Contributing](CONTRIBUTING.md) · [Support](SUPPORT.md)

A modular, open-source QA toolkit for web applications and APIs. It connects recorded human flows to application knowledge, illustrated flow documents, manual test cases, automation, performance engineering, root cause analysis and engineering reports.

The kit contains **26 focused skills and 26 agent roles**, platform adapters and a TypeScript Playwright recorder. The skills describe agent workflows; the recorder is executable capture software. It is not an unattended runtime for every QA stage. See [verification](verification.md) for what has actually been tested.

## What it does

- Records human demonstrations in dedicated spawned Chromium browsers, including step screenshots, console errors and bounded API/file evidence.
- Reviews a suggested flow name, inferred steps, completion status and minor uncertainties in one question. Further questions are reserved for essential gaps or required approvals; confirmed application/workspace preferences are reused.
- Maintains one application knowledge document and versioned manual flow documents with actual screenshots embedded per step.
- Designs at least 20 meaningful manual cases per flow where business rules support them, executes selected cases and preserves evidence. Missing rules remain unresolved rather than invented.
- Inspects an existing automation framework, including feature files, data wiring and pipelines. Automation updates require two distinct current-version manual executions per flow or an explicit scoped override.
- Supports performance engineering, workload modeling, telemetry correlation, bottleneck analysis, evidence-based RCA, reviewable fix proposals and approved implementation/retesting.
- Provides separate Splunk, Dynatrace, NeoLoad, Jira and Confluence skills and documented MCP setup templates. Templates do not establish live connections.

## Platform support

Native skill/agent adapters are provided for Cursor, Claude Code and VS Code GitHub Copilot. Codex and Google Antigravity use discoverable skills with portable role instructions; ChatGPT can analyze uploaded artifacts and provide local recording commands when it lacks local execution access. Available tools and native discovery depend on the client/version. Cross-platform/client acceptance remains incomplete; see [installation](docs/INSTALLATION.md) and [verification](verification.md).

## Quick start

Prerequisites: Git, Python 3.11+, Node.js 22+, npm and an approved application/test environment. Chromium and recorder dependencies are needed for browser recording, not merely for reading the skills.

```sh
git clone https://github.com/bharathbk07/enterprise-qa.git
cd enterprise-qa
python3 scripts/install.py --workspace "/path/to/application" --platforms cursor
```

The command previews the workspace files. Review the plan, then repeat with `--apply` to install approved definitions. Select only the platforms you need; `--platforms all` is also available. Installation copies owned files and refuses unapproved overwrites. It does not install npm packages, configure active MCP connections or change global IDE settings.

To prepare and use the recorder, run from this repository:

```sh
cd recorder
npm ci --ignore-scripts
npx --no-install playwright install chromium
npm run build
npm run doctor
npm run record -- --workspace "/path/to/application" --app customer-portal --url "https://test.example.com" --privacy mask
```

Ask the user before missing-component installation/configuration when an agent executes these setup actions. Use a permitted test environment. Close every window in the launched session to finish. See [recorder guidance](docs/RECORDER.md) for plaintext evidence, opt-in saved profiles, resource budgets, resume and cleanup. Python may be named `python` or `py` on your system; use a Python 3.11+ interpreter.

## Typical agent requests

- Use qa-orchestrate to record and document the checkout flow.
- Use qa-knowledge to summarize recording REC-ID for one combined review and create the illustrated flow document.
- Use qa-test-design to create cases for Checkout, FLOW-003.
- Use qa-test-execution to execute Checkout, 3 against the approved sandbox.
- Use qa-framework to inspect the entire framework and test-data wiring.
- Use qa-performance-engineering to plan a workload, correlate telemetry and investigate bottlenecks.
- Use qa-rca to investigate RUN-ID and prepare a fix proposal for approval.

## Project structure

`skill-definition.json` catalogs the skills; `agent-manifest.json` maps roles to those skills. Both are portable catalogs, not native host runtime configuration. `skills/` and `agents/` contain focused definitions; `adapters/` contains client-specific exports; `contracts/` defines shared rules and data records; `recorder/` contains executable capture code; `integrations/` contains MCP setup guidance; `scripts/` contains install, synchronization and validation helpers.

Application artifacts belong in the tested workspace under `qa/<application-id>/`, not in the toolkit source. Keep credentials, raw production data and browser profiles out of Git and public issues. Recording's 25 MB budget applies to stored resource payloads, separately from screenshots/profile storage. Screenshot redaction and event coverage have documented limits.

## Development and verification

After preparing recorder dependencies, run from the repository root:

```sh
python3 scripts/validate.py
npm --prefix recorder run build
python3 -m unittest discover -s scripts -p 'test_*.py'
npm --prefix recorder test
```

The browser tests launch Chromium against a loopback-only fixture. Environments that disallow local sockets or process launch cannot run them without an appropriate execution environment. Keep generated references/adapters and owned checksums synchronized with `python3 scripts/sync_package.py` after intentional source changes. Review the diff before regenerating checksums; they are not publisher signatures or a security boundary.

## Documentation

- [Getting started](docs/GETTING-STARTED.md), [installation and updates](docs/INSTALLATION.md), [recorder](docs/RECORDER.md)
- [Flow documents](docs/FLOW-DOCUMENT.md), [fewer-question interaction](docs/INTERACTION.md), [data model](contracts/DATA-MODEL.md)
- [Architecture](docs/ARCHITECTURE.md), [engineering rules](contracts/ENGINEERING.md), [MCP setup](integrations/SETUP.md)
- [Gap review](docs/GAP-REVIEW.md), [verification](verification.md), [changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md), [security reporting](SECURITY.md), [support](SUPPORT.md), [community conduct](CODE_OF_CONDUCT.md)

## License

MIT License. Copyright (c) 2026 Bharath Kumar M. See [LICENSE](LICENSE). License copies accompany independently installable skill/agent bundles. Third-party packages, browser binaries and hosted services retain their respective notices/terms; see [third-party notices](THIRD_PARTY_NOTICES.md).
