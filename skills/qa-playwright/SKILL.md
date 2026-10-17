---
name: qa-playwright
description: "Operate browser/API tests using dedicated spawned Playwright browsers and inspect API traffic."
license: MIT
---

# qa-playwright

Read `references/CONTRACT.md` and `references/BROWSER.md`. Discover the client's actual browser launch/tool schema. Spawn a dedicated QA-owned browser process using Playwright library launch APIs or a dedicated Playwright MCP instance that launches its own browser. Verify session ownership and QA-only profile before actions. An integrated IDE/app browser or a new tab/context in a shared process is not permitted. Never attach to a personal/shared or unrelated pre-existing browser through extensions or CDP. If compliant spawning is unavailable, mark browser work blocked and provide local launcher/setup instructions. Use live role/label/test-ID locators; never reuse stale element references blindly.
Inspect network request lists/details and console errors using available developer tools. Supplement observed traffic with workspace OpenAPI/Postman/API docs and user-confirmed expectations. Observed success is not an API contract. Never export unmasked MCP output in a masked session. If tools cannot sanitize evidence before persistence, use the recorder's filtered outputs or metadata only.
Do not equate MCP-driven automation with passive human recording. Use qa-recording for user demonstrations. Mark CAPTCHA/MFA or judgment-dependent assertions blocked pending human assistance. New browser/locale/device targets require user selection and approved missing dependencies; viewport emulation is not a physical mobile test.

Record browser launch mode, session/run identity and available ownership evidence with execution artifacts. Reuse only this session’s tabs/windows. Retained QA application profiles require storage consent and a newly spawned process on resume; never use a personal browser profile. Close only the owned session.

Setup includes the official Playwright planner/generator/healer, distinct from qa-browser. Read `references/PLAYWRIGHT-AGENTS.md` when initializing or verifying their MCP/host readiness. Verify dedicated-browser ownership before use; registration alone is not browser acceptance.
