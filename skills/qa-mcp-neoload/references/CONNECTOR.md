# Neoload connector

NeoLoad Web meta endpoint discovers action schemas on demand. US URL shown; EU is https://neoload-v2-eu.saas.neotys.com/mcp-server/mcp-v2. Set NEOLOAD_AUTH_HEADER to the API-token header value required by the deployment. Classify the nested action before execution. This differs from testing MCP servers via NeoLoad User Path client actions.

Source: [official setup](https://docs.tricentis.com/neoload-web-v2/en-us/content/ai_integration/mcp_meta_tool.htm). Documentation verified 15 October 2026; no live tenant validation performed.

Use the shared engineering contract for scope, bounded reads, approval, redaction and error handling. Templates under `.qa-agent/integrations/templates/` are manual-merge drafts; they do not connect or install a server. Current client/version/edition and actual tools must be checked during setup.
