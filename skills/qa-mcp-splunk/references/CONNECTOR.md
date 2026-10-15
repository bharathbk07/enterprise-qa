# Splunk connector

Copy the endpoint from the Splunk MCP Server app. The cited 1.0 guidance requires an encrypted MCP token, not a generic REST token; verify the deployed version. Tool availability is administrator-controlled. Do not disable TLS verification.

Source: [official setup](https://help.splunk.com/en/splunk-enterprise/mcp-server-for-splunk-platform/1.0/connecting-to-the-mcp-server-and-settings). Documentation verified 15 October 2026; no live tenant validation performed.

Use the shared engineering contract for scope, bounded reads, approval, redaction and error handling. Templates under `.qa-agent/integrations/templates/` are manual-merge drafts; they do not connect or install a server. Current client/version/edition and actual tools must be checked during setup.
