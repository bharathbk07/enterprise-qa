---
name: qa-mcp-neoload
description: "Discover NeoLoad Web MCP actions and read results or execute an explicitly approved NeoLoad run profile."
license: MIT
---

# qa-mcp-neoload

Read `references/CONTRACT.md`, `references/ENGINEERING.md` and `references/CONNECTOR.md`. Confirm NeoLoad edition/version/region/workspace/project/scenario, token reference, controllers/generators/license availability and connector support. Distinguish NeoLoad Web MCP server from NeoLoad User Path MCP client actions.
Discover meta-tool actions/schema on demand when available; classify the discovered action before execution. Read scenarios/results and compare run IDs/time windows. For create/update/launch/stop operations obtain exact approval; a stop included in the approved run's abort plan remains authorized. Check scenario/version, load model/stages/data/secrets/generators/thresholds/abort criteria and external effects, then launch once and capture returned run ID. If outcome is uncertain, reconcile status before any retry. Use bounded status reads; no infinite polling. Preserve partial/aborted results and generator saturation. Return normalized evidence, never equate protocol and browser timings.

Browser-based scenarios must use dedicated browsers spawned by the approved QA/load runner. Never substitute an IDE/app integrated browser or attach a shared personal session. Protocol-only scenarios and result reads need no browser. Verify the chosen runner capability before browser-based execution.
