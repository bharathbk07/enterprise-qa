# Official Playwright Test Agents during setup

Source: [Playwright Test Agents](https://playwright.dev/docs/test-agents). The upstream roles are **planner**, **generator** and **healer**. Generate them with the installed Playwright CLI and regenerate after a Playwright upgrade. They complement the toolkit's 37 roles; qa-playwright/qa-browser alone are not the official agent installation.

## Required setup step

qa-setup must include official agent initialization in its concrete setup plan, not merely suggest it as optional reading. First inspect the selected host, existing framework, compatible local Playwright tooling and user customizations. Reuse confirmed preferences and ask only missing essential details. Include missing dependencies, files and MCP changes in the existing once-per-setup approval. Do not install a new application framework or migrate from Selenium/another runner just to obtain agent definitions.

Local Playwright may come from the application's existing Playwright Test dependencies or the installed .qa-agent/recorder package. Prefer the application's compatible version; do not silently upgrade it. If a Playwright Test framework is desired and dependencies are missing, include a compatible pinned @playwright/test package in the approved dependency plan. The helper itself never downloads packages. Installing agent definitions does not make a non-Playwright project runnable as a Playwright Test suite.

## Protected initialization

The helper runs the real local `playwright init-agents` command in a temporary directory with a minimal staging config, then previews exactly what it would install. It does not load the application's executable config or point a generated seed at its testDir. Examples below run from the toolkit source root, or .qa-agent after installation.

```sh
python3 scripts/setup_playwright_agents.py --workspace "/path/to/application" --loop claude
python3 scripts/setup_playwright_agents.py --workspace "/path/to/application" --loop claude --apply
```

Use --loop vscode for VS Code Copilot, --loop claude for Claude Code, or --loop codex for Codex. These loop names are documented by Playwright and verified against the installed 1.64.0 CLI. When needed, add --playwright-cli "/absolute/path/to/node_modules/playwright/cli.js" to select approved existing tooling. No browser launches or application tests occur during definition generation.

You can combine toolkit definition installation with official initialization:

```sh
python3 scripts/install.py --workspace "/path/to/application" --platforms claude-code --playwright-loop claude
python3 scripts/install.py --workspace "/path/to/application" --platforms claude-code --playwright-loop claude --apply
```

The combined preview checks both plans before applying either. Without --playwright-loop, install.py remains a definition-copy phase and explicitly reports official Playwright setup pending. qa-setup must complete the helper phase or clearly report why the chosen host/tooling cannot support it before declaring setup complete. For multiple supported local hosts, repeat helper initialization for their respective loops within the approved plan.

## Host handling

- VS Code Copilot: --loop vscode, official definitions under .github/agents and the local playwright-test server in .vscode/mcp.json.
- Claude Code: --loop claude, official definitions under .claude/agents and the local playwright-test server in .mcp.json.
- Codex: --loop codex, official TOML definitions under .codex/agents with per-agent local MCP configuration. This is separate from the toolkit's portable Codex QA roles.
- Cursor/Antigravity: the referenced guide and installed CLI do not provide cursor/antigravity loop flags. Do not invent them or claim native compatibility. Generate a verified loop in reference-only mode below; separately validate any native adapter before activation.
- ChatGPT without local execution access: retain upload-based analysis/local command instructions. Do not claim a local agent or server was registered by uploading files.

For an unsupported native host, preserve the actual generated upstream definitions as inactive references:

```sh
python3 scripts/setup_playwright_agents.py --workspace "/path/to/application" --loop claude --reference-only
python3 scripts/setup_playwright_agents.py --workspace "/path/to/application" --loop claude --reference-only --apply
```

These files live under .qa-agent/vendor/playwright/claude and do not activate .claude agents/MCP settings. Reference-only installation is not native host acceptance. This helper targets local IDE clients, not GitHub's cloud coding-agent environment; cloud setup needs its own approved environment and CI plan.

## Preservation and refresh

Existing unrelated MCP servers/settings are preserved. A conflicting playwright-test entry or user-edited official definition blocks application of the plan. JSONC/non-JSON settings need manual review rather than destructive conversion. The helper pins each installed MCP invocation to the inspected local CLI, avoiding an implicit npx package download on agent invocation. Reinitialize after dependency upgrades or moving the CLI path.

Use --update-managed during preview/apply to refresh previously generated definitions only when their saved ownership hashes still match. Custom edits remain conflicts. Ownership/version data is kept in .qa-agent/.playwright-agent-state.json. These local receipts are not signed authorization records. All file paths must stay inside the selected workspace.

The upstream initializer may create seed tests, specs scaffolding and CI files. The protected helper reports but does not copy those scaffold files into the application. qa-framework must select/reuse the real application's seed/config/fixtures before live planner/generator/healer use. User-owned seeds/tests/pipelines remain untouched. Generated upstream instruction text retains Playwright's LICENSE/NOTICE in namespaced files beside the installed agents; toolkit MIT licensing does not replace upstream terms.

## Execution boundaries

Generated official definitions include a clearly marked Enterprise QA section. Browser operation still requires a dedicated spawned QA-owned session. Generator/healer changes to flow automation still require two distinct current-version manual cases executed or an explicit scoped override. Real application/configuration fixes follow proposal/approval. Retain original failures and business assertions; never hide product defects by skipping tests or weakening assertions, and do not start an unbounded heal-until-green loop. One safe retry remains the default; further investigation needs its own scope. MCP registration does not itself verify dedicated-browser behavior; verify it before browser use.

## Verify completion

Confirm all three upstream roles, inspected Playwright version, native/reference destination, preserved MCP entries and seed/fixture readiness. Inspect the client's actual loaded agent/tool list; local file generation is not a guarantee of client acceptance. Record verified/blocked capabilities and why. Validate a harmless authorized local fixture before live work; no load, CI modification or external writes solely to prove installation.
