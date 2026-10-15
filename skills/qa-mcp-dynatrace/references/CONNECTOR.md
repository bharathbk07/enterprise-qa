# Dynatrace connector

Use the documented environment-specific endpoint for supported Latest Dynatrace deployments; verify edition support. Platform bearer tokens or confidential OAuth are documented. Grant only needed MCP/data permissions; do not paste the full broad permission list by default.

Source: [official setup](https://docs.dynatrace.com/docs/dynatrace-intelligence/dynatrace-mcp). Documentation verified 15 October 2026; no live tenant validation performed.

Use the shared engineering contract for scope, bounded reads, approval, redaction and error handling. Templates under `.qa-agent/integrations/templates/` are manual-merge drafts; they do not connect or install a server. Current client/version/edition and actual tools must be checked during setup.
