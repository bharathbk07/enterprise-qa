# Dynatrace evidence

Sources checked 17 October 2026: [remote MCP server and permissions](https://docs.dynatrace.com/docs/dynatrace-intelligence/dynatrace-mcp), [DQL reference](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-query-language). Use supported Latest Dynatrace environments; verify Managed/classic differences. The remote operational MCP server differs from app-development documentation MCP and the optional open-source local server.

The official remote guide documents platform bearer and confidential OAuth options. Match MCP gateway and selected storage/agent permissions to actual tools; do not grant the entire published scope list by default. Generating/explaining DQL and executing DQL are different capabilities. Current documented analysis output has a record cap; discover the actual response/truncation metadata rather than assuming every query is complete.

Resolve entity IDs and actual environment/field mappings before DQL reads. For fallback use an already permitted official query API for that deployment or an existing export. If neither is available, provide a DQL query for the user to run in the selected environment/notebook with explicit timeframe and scan/result limits. Starting shape, adapted to actual schema:

```text
fetch logs
| filter dt.entity.service == "<confirmed-service-entity-id>"
| summarize events = count(), by: {loglevel}
| limit 50
```

This is a template: dt.entity.service/loglevel must be verified for the data. Set absolute start/end and supported scan limits in the execution UI/API; limit only bounds returned rows, not scanned data. Ask for the query, environment, event window, returned counts/truncation and redacted aggregate table. Metrics/spans require their corresponding data source and permissions; do not translate SPL mechanically into DQL.

Record metric resolution, sampling, ingestion delay and topology/revision differences. Automated problem/AI explanations remain hypotheses until supporting evidence meets the shared RCA standard. No live tenant or permission acceptance is claimed.
