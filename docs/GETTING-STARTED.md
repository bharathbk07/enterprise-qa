# Getting started

## Choose the operation

For agent instructions only, review the relevant SKILL.md and shared contract; no browser/npm installation is needed merely to read the kit. For recording, prepare the TypeScript recorder. For native skill/agent discovery, install the selected workspace adapter. MCP configuration is a separate approved setup step.

## Obtain the source

```sh
git clone https://github.com/bharathbk07/enterprise-qa.git
cd enterprise-qa
```

Use Python 3.11+, Node.js 22+ and npm. On Windows select the corresponding Python launcher and quote paths that contain spaces. Use the commands from the actual repository root or recorder directory as shown; do not run them against an application folder that lacks these files.

## Install workspace definitions

Preview first:

```sh
python3 scripts/install.py --workspace "/path/to/application" --platforms cursor
```

Choose cursor, claude-code, vscode-copilot, codex, antigravity or chatgpt-portable; a comma-separated subset or all is accepted. Inspect the paths/conflicts. After approving the plan, repeat with --apply. Files go to the workspace's .qa-agent package and supported native skill/agent directories. Existing user edits are protected. See INSTALLATION.md for adapter details and managed updates.

## Record a demonstration

From this repository root:

```sh
cd recorder
npm ci --ignore-scripts
npx --no-install playwright install chromium
npm run build
npm run doctor
npm run record -- --workspace "/path/to/application" --app customer-portal --url "https://test.example.com" --privacy mask
```

Only install missing components after the user's approved setup plan when operating as an agent. Use an approved application URL. The browser is a dedicated spawned Chromium process; integrated browsers and personal/shared attachments are not used. Perform the flow and close every window to stop. A masked session still requires deliberate consent before retaining an authenticated profile. See RECORDER.md for plaintext choice, file capture limits, resume and cleanup.

## Turn the recording into QA artifacts

Invoke qa-knowledge with the actual recording ID/path. It proposes the flow name, inferred steps, completion status and minor uncertainties together for one guided review. Confirm or correct the summary. It asks further questions only for essential ambiguity or required approval, then maintains application knowledge and creates the manual flow document with actual embedded screenshots. The recorder itself does not infer business expectations or automatically render that final document.

Use qa-test-design for manual cases and qa-test-execution for selected flows. qa-automation checks current-version manual evidence before framework edits. qa-performance-engineering and qa-rca route their focused specialists. External actions, load profiles, fixes and publications preserve their explicit approval requirements.

## Verify and troubleshoot

From the repository root, after dependency preparation:

```sh
python3 scripts/validate.py
npm --prefix recorder run build
python3 -m unittest discover -s scripts -p 'test_*.py'
npm --prefix recorder test
```

A browser test needs local socket and process-launch permissions. Missing executable: run npm run doctor inside recorder and prepare the approved Chromium dependency. Changed source checksum: review intentional edits, run scripts/sync_package.py from the repository root, inspect its diff and validate again. Do not regenerate checksums to conceal unknown changes. For discovery/authentication problems, follow INSTALLATION.md or ../integrations/SETUP.md and report your client/version without secrets. Check SUPPORT.md and SECURITY.md at the repository root before opening a report.
