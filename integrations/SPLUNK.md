# Splunk platform evidence

Sources checked 17 October 2026: [MCP platform 1.3 overview](https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/1.3/about-mcp-server-for-splunk-platform), [2.0 connection/settings](https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/2.0/connecting-to-the-mcp-server-and-settings), [Search REST reference](https://help.splunk.com/en/splunk-enterprise/rest-api-reference/9.4/search-endpoints/search-endpoint-descriptions). Verify the deployed version; older 1.0 guidance is not a universal current requirement. Splunk Platform MCP, Observability Cloud and AppDynamics are distinct products/capability sets.

Obtain the endpoint from the installed MCP Server app and use its supported encrypted MCP token, rather than assuming a generic REST token works. Discover allowed tools/indexes, role restrictions and server guardrails. Keep TLS verification enabled; fix trust/certificates through approved setup rather than copying insecure example flags. Retain query timeouts and result budgets regardless of server guardrail availability.

For fallback, use an already approved official Search REST capability or an existing export. Search jobs need bounded lifecycle/status/result handling; a job submission is not the completed result. Do not broaden index permissions, enumerate all indexes or run modifying SPL. To ask the user for a query, replace every placeholder with confirmed mappings before execution:

```text
index=<approved_index> earliest=<start_epoch_seconds> latest=<end_epoch_seconds>
<confirmed_environment_field>="<environment>" <confirmed_service_field>="<service>"
| stats count by <confirmed_severity_field>
| head 50
```

This is an SPL template, not a ready-to-run query. Select a permitted index/window and suitable indexed filters; a final head limit does not bound bytes scanned. Use the approved timeout/scan/call budget too. Request query/job ID, absolute window, row counts, completion/truncation and aggregate results. An absent severity field needs a mapping or a different aggregate, not an invented column. Preserve event versus ingestion timestamps and late-arrival limitations.
