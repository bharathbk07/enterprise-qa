# Workspace installation

The toolkit-definition phase does not change global IDE settings or active MCP configuration. An explicitly selected --playwright-loop additionally previews/installs official Playwright definitions and their local MCP registration while preserving unrelated settings. The portable manifests are catalogs consumed by the orchestrator, not native executable agent configurations.

1. Select the application workspace and platform(s). Run the installer dry-run with Python 3.11+:

```sh
python scripts/install.py --workspace "/path/to/application" --platforms all
```

Allowed platform IDs: cursor, claude-code, vscode-copilot, codex, antigravity, chatgpt-portable. Use a comma-separated list for a smaller installation. Review destinations/conflicts and the concrete dependency plan. Ask once before installation/configuration, then apply:

```sh
python scripts/install.py --workspace "/path/to/application" --platforms all --apply
```

2. Installer copies package resources to `.qa-agent/`; bundled QA Playwright skill and browser agent are included. It copies workspace skills/agents into native locations where verified by documentation. It refuses changed-file overwrites and paths escaping the workspace. No npm/browser installation occurs inside this command. With --playwright-loop the protected official-agent phase also applies the reviewed local MCP entry; without it that phase is reported pending.
3. Follow RECORDER.md for `npm ci`, missing Chromium installation, build and doctor in `.qa-agent/recorder/`. Use existing compatible browsers where available. Missing Node/MCP/skill dependencies require a concrete plan and the once-per-setup approval. Do not blindly install from unreviewed repositories. Bundle-owned qa-playwright/qa-browser are provided, not a claim that a third-party Playwright skill/agent was installed.
4. Reload/inspect each client's skills/agent picker. Run a smoke request on a permitted fixture. Native file generation is verified locally; runtime integration in every product must be verified on that product/version. Existing Playwright tooling is sufficient only when it can spawn a dedicated QA-owned browser process; verify launch/session ownership. Configure missing approved dedicated launch tooling as needed.

# Platform adapters

Cursor: `.cursor/skills/` and `.cursor/agents/*.md`; native specialist prompts use selected skill paths. [Official skills](https://cursor.com/help/customization/skills) and [subagents](https://cursor.com/docs/subagents).

Claude Code, including its VS Code extension: `.claude/skills/` and `.claude/agents/*.md`. [Skills](https://code.claude.com/docs/en/skills), [subagents](https://code.claude.com/docs/en/sub-agents).

VS Code GitHub Copilot: `.agents/skills/` and `.github/agents/*.agent.md`. The active assistant/harness controls available tools. [Agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills), [custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents). VS Code is an editor, not a single agent runtime. This adapter covers Copilot; Claude/Codex extensions use their respective adapters. With all adapters installed, some hosts discover duplicate compatible definitions; select the relevant platform subset if duplicates appear.

Codex: `.agents/skills/`, with portable roles in `.qa-agent/agents/`. Native specialist registration is not configured; use sequential roles unless the installed runtime supplies supported delegation. [Official skill locations](https://learn.chatgpt.com/docs/build-skills).

Google Antigravity: `.agents/skills/`, portable role prompts under `.qa-agent/agents/`; no undocumented custom agent registration invented. [Official skills](https://antigravity.google/docs/skills?app=antigravity-ide). Read adapters/antigravity/instructions.md and use sequential roles if needed.

ChatGPT: adapters/chatgpt-portable/instructions.md provides upload-based operation when local workspace/browser access is absent. Upload relevant knowledge/results and a selected skill plus its contract. Give local recording commands for browser work. This is portable prompt use, not automatic custom-agent registration or unrestricted local execution.

# Optional Playwright MCP

Inspect whether compliant dedicated browser launch tooling already exists first. If not, ask approval to configure an official Playwright MCP server using the client's documented MCP configuration mechanism. [Official server and client setup](https://github.com/microsoft/playwright-mcp). Example command from the official server setup is `npx @playwright/mcp@latest`; prefer a verified pinned version for repeatable enterprise installation. Do not silently add it to settings or assume every client exposes identical tools. The recorder itself needs only the Playwright npm library and Chromium, not MCP.

# Acceptance checks

Use `qa-orchestrate` to capture a local fixture and clarify the completion state. Verify selected privacy policy, screenshot gaps, bounded resources, knowledge update, at least 20 meaningful cases, and flow selection. Test gate with two distinct current-version manual cases and with one case (override required). Change flow version and verify old runs cease to satisfy the prerequisite. Check that missing browser capabilities produce blocked/not-executed outcomes. Validate performance profile confirmation separately. These are platform acceptance checks, not evidence that each has already passed.

# Updating a managed installation

The v2 installer uses `distribution.json`, a reviewed source allowlist with checksums, instead of copying arbitrary package-directory files. Run `scripts/sync_package.py` after intentional package edits to regenerate references/adapters and checksums, then validate. Do not use it to bless unknown changes without review.

An approved install records `.qa-agent/.install-state.json`. To preview an update, add `--update-managed`; add `--apply` only after approving the concrete plan. Changed package files may replace previously installed files only when their existing content still matches the saved ownership hash. User edits remain conflicts. A v1 installation without a receipt needs manual review/migration; there is no blanket overwrite. No obsolete-file deletion or active MCP settings update occurs automatically.

Performance/RCA extensions and MCP setup: read `contracts/ENGINEERING.md` and `integrations/SETUP.md`. Product-specific roles are separate; Jira/Confluence can share one verified Atlassian connection. The installer copies draft templates into `.qa-agent/integrations/templates/` but never activates them.

# Dedicated browser requirement

Browser ownership: all recording and UI test execution must use a dedicated browser process spawned for the QA session, locally or on an approved dedicated runner. Use Playwright library launch APIs or a verified Playwright MCP instance that launches its own QA-owned browser. The same session may own multiple tabs/windows. Never use an IDE/app integrated browser, personal/shared browser, browser-extension attachment, or a pre-existing unrelated CDP/debugging session. Creating a fresh tab/context in a shared process does not satisfy this requirement. Verify launch mode, session ownership and QA-only profile before browser actions; record available launch/session evidence with the run. A retained profile may be reused only if created for this application by QA and the user consented to storage; resume launches a dedicated process again. If no compliant launcher is available, mark browser-dependent work blocked and provide the approved local launch/setup path; do not silently switch backends. Direct API/protocol tests and uploaded-result analysis do not require a browser. Close only processes/windows owned by this QA session.

The bundled recorder already uses Playwright launch APIs. Setup must reject integrated-browser or shared-session fallback for UI tests. No IDE or MCP settings are changed by this policy update.

# Source and redistribution

Clone https://github.com/bharathbk07/enterprise-qa.git and run these commands from the toolkit source root. For the complete first-run sequence see GETTING-STARTED.md. Root LICENSE (MIT, copyright 2026 Bharath Kumar M), community documents and independent skill/agent license copies are part of the owned distribution. See ../CONTRIBUTING.md for development and ../docs/MAINTAINING.md for release preparation.

# Official Playwright Test Agents

Full setup includes the upstream planner/generator/healer, not only qa-playwright/qa-browser. After preparing compatible local Playwright dependencies, use setup_playwright_agents.py or install.py --playwright-loop with the selected documented loop. See [PLAYWRIGHT-AGENTS.md](PLAYWRIGHT-AGENTS.md) for preview/apply commands, reference-only handling for other hosts, conflict protection, preserved seed/CI files, license notices and refresh after upgrades. Include this phase in the existing concrete setup approval instead of asking redundant questions.


# Full-stack architect discovery

qa-architect is the full-stack entry point; qa-orchestrate remains the QA workflow entry. The kit now has 37 focused skills/roles, including stack, functional, security, accessibility, resilience, data and solution architecture. Use the same dry-run/managed-update installer; no framework, infrastructure or scanner migration is performed by installing definitions. Verify the selected client's discovery and run a bounded source-only assessment before claiming live execution capabilities. See FULLSTACK-ARCHITECT.md.

# Preflight snapshots and guarded apply

Toolkit and official Playwright installation capture destination content/path/mode and receipt snapshots. Apply rechecks the complete batch, then rechecks each destination after staging its bytes. New files use exclusive publication; existing files use atomic replacement. Cooperating installers are serialized by .qa-agent-install.lock. Sources and ownership receipts changed after preflight require a new plan; user edits are not accepted as owned simply because they appeared during planning. Existing file symlinks require manual review.

On a detected late change the action fails rather than overwriting it. Inspect results and re-plan; a failure after earlier files were written can leave a partial batch, so this is not a multi-file transaction or automatic rollback. A crash can leave the lock/staging artifacts; inspect ownership/process state before manually removing those exact artifacts. Arbitrary external editors do not honor the installer lock: content rechecks narrow the final check-to-replace window, but are not an OS-level compare-and-swap guarantee against concurrent adversarial writers. Keep the target installation quiet during apply. Native client/platform acceptance remains separate.
