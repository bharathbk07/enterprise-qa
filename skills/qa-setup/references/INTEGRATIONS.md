# Integration setup and discovery

Templates are manual-merge drafts, not working connections or a custom MCP server implementation. No actual tenant, credentials, issue/page destination or run profile is supplied. Source registry records the verified official guidance and its version/date. Credentials remain in the client secret facility/environment; templates contain references only. Do not disable TLS checks or install unreviewed proxy packages.

## Procedure

1. Inspect existing client tools/connections first. During setup ask product/edition/version, SaaS vs self-hosted, region, endpoint, site/workspace, authentication reference, allowed data scope and desired operations, one question at a time with 3–4 options/free text.
2. Compare the chosen connector's official deployment/client support. Confirm URL from the product/admin; do not extrapolate an endpoint to an unsupported on-prem edition. Verify TLS, permissions and the client's secret interpolation before adding configuration. Keep remote server allowlists and least-privilege credentials in the client/admin system where supported.
3. Present exact missing dependency/configuration plan, then ask once before installation/configuration. For these product integrations, the installer copies templates only; it never merges them into active MCP settings. The separate approved official Playwright agent phase can register its own local test server. Preserve existing settings and avoid duplicate Jira/Confluence connections when one Rovo connection suffices.
4. Authenticate through the approved client flow, discover actual tools and nested action schemas, and record capabilities/version/freshness. Native availability is not proof that every advertised action is authorized. An execute wrapper can contain writes; classify its action semantics. Set concrete query/time/page/scan/row/call budgets before read tests.
5. Validate a bounded permitted read against a known harmless object/window and save a redacted receipt. Do not launch a test or create an issue/page merely to validate connectivity. Label unverified/unavailable capabilities and refresh discovery after connector changes.
6. For write/launch operations draft the exact payload/profile/target first, obtain explicit approval, execute once, verify/reconcile outcome and save receipt. On rate limits honor supported backoff within scope; on uncertain writes do not retry blindly. Pagination/partial results must be recorded.

## Client templates

Cursor: `templates/cursor.mcp.example.json` uses documented mcpServers/url shape, deliberately URL-only. Token-auth products remain incomplete until the installed client's supported secret/header mechanism is verified; URL-only does not authenticate Splunk/NeoLoad. Merge approved entries into the selected workspace `.cursor/mcp.json`. [Client documentation](https://cursor.com/help/customization/mcp).

VS Code Copilot: `templates/vscode-copilot.mcp.example.json` uses servers/http plus password inputs. Merge into `.vscode/mcp.json` only after approval. Interactive inputs may not forward to all Agent Host harnesses; use that harness's supported secret mechanism if necessary. [Configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Claude Code (including its VS Code extension): `templates/claude-code.mcp.example.json` uses HTTP entries and product-specific `${VAR}` secret references. Merge into `.mcp.json` after approval. Verify variables are present in the actual process; do not use Claude/cloud provider credentials as product tokens. [Environment expansion](https://code.claude.com/docs/en/mcp#environment-variable-expansion-in-mcpjson).

Codex: `templates/codex.config.example.toml` uses documented bearer-token environment references/custom header environment references. Entries start disabled; replace environment/endpoint values and approve activation before enabling. Merge into the chosen configuration scope deliberately, not automatically. [Official MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). This draft does not invent tool allowlists: discover exact names, then configure the supported host policies.

Antigravity: use its current native MCP setup UI/schema for the verified endpoint/auth; no undocumented JSON configuration schema is supplied. ChatGPT: use the supported connector/admin flow; absent local tool access, analyze uploaded redacted artifacts. The Atlassian plugin was discoverable during this review; discovery is not a claim of connection. Other products have documented vendor MCP options even when not returned in this app's plugin directory.

## Provider boundaries

Splunk: get endpoint from the MCP Server app; version-specific guidance uses encrypted MCP tokens. Verify the deployed MCP/version and permitted indexes before setup. [Official connection guide](https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/2.0/connecting-to-the-mcp-server-and-settings).

Dynatrace: documented remote endpoint and token/OAuth options apply to supported Latest Dynatrace environments; do not assume classic/managed parity. [Official MCP guide](https://docs.dynatrace.com/docs/dynatrace-intelligence/dynatrace-mcp).

NeoLoad Web: official region-specific meta endpoint enables discovery of actions on demand, reducing eager tool loading. Verify edition/version/workspace and API-token format. [Meta endpoint guide](https://docs.tricentis.com/neoload-web-v2/en-us/content/ai_integration/mcp_meta_tool.htm).

Jira/Confluence: separate specialist roles share the Atlassian Cloud Rovo endpoint. OAuth plus existing permissions govern access; Data Center needs a separately verified connector. [Rovo MCP](https://developer.atlassian.com/cloud/rovo-mcp/).


## Product references and fallback

Select only the product in the request: [Splunk](SPLUNK.md), [Dynatrace](DYNATRACE.md), [AppDynamics](APPDYNAMICS.md), [Datadog](DATADOG.md), [NeoLoad](NEOLOAD.md), or [JMeter runner](JMETER.md). AppDynamics and Datadog have separate focused skills/agents. JMeter has its own runner specialist; no JMeter MCP endpoint is invented. Shared fallback and user query/result handoff are in [contracts/EVIDENCE.md](EVIDENCE.md). These are instructions and disabled/manual-merge drafts, not authenticated connections.

AppDynamics templates select a deployed HTTP server and Controller token only; optional Analytics Events auth is configured separately when needed. Datadog templates intentionally use a placeholder site endpoint and no assumed token header: confirm the selected site's current endpoint/client authentication and then approve configuration. Do not activate unresolved .invalid destinations. A reference URL does not verify tenant availability. Product-specific documentation dates in catalog.json do not advance Atlassian's prior verification date.

## Bounded live acceptance still required

For each selected product record actual client/server/version, scope and credential reference, discovered read/action schemas, selected application/entity IDs, and timestamp. Within the approved environment/time/result budget perform a known harmless read, verify field units/window/counts/pagination and save only a redacted receipt. Verify scope restriction/permission denial without seeking broader access. Do not launch load, create dashboards/issues, change instrumentation or bypass TLS to prove connectivity. AppDynamics must distinguish APM from optional Analytics; Datadog must identify the actual site; NeoLoad must distinguish Web control from User Path MCP-client tests; JMeter needs separate target/profile approval even for a smoke run.

Exercise or document remaining cases: expired auth, 429/Retry-After, timeout, partial/truncated output and read budget exhaustion. Write/launch unknown-outcome reconciliation can first be simulated; it must not be induced against a live service merely for acceptance. Refresh receipts after server/tool/permission/deployment changes. Local tests in scripts/test_evidence.py cover normalized synthetic envelopes and decision suggestions only; they are not vendor protocol tests, authentication tests or an enforcement gateway.
