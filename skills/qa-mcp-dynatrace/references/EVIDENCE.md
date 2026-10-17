# Connector fallback and evidence handoff

Use this procedure for missing product capabilities, transport/authentication failures, API/export alternatives and results pasted by the user. It applies to read evidence and separately approved runner operations. It does not grant access, authorize load or replace the original RCA confirmation standard.

## Select a path

1. Inspect the configured MCP tool catalog, version, input schemas and allowed scope. Do not treat missing tools as empty data. Record unavailable, denied, expired-auth, rate-limit, timeout and unknown-outcome distinctly.
2. If MCP cannot supply the needed evidence, use an already permitted official product API or existing local export. New credentials/configuration still follow setup approval. Inspect export identity/window/version before combining it with live evidence. A permission denial is not permission to seek broader credentials or bypass policy through another transport.
3. If neither path is usable, provide a scoped product query or command for the user to execute, then ask them to paste a bounded redacted result. One request should include the query and all necessary return fields. Do not ask for credentials, full raw production logs or one result at a time.

Give the reason for switching paths and the capability/evidence limitation. Reuse confirmed environment mappings and budgets. Query examples must be adapted to actual fields/IDs, syntax, edition and limits; never execute unresolved placeholders. JMeter is a CLI/export path unless a separately verified connector exists; do not invent an official JMeter MCP server.

## Failure decisions

- Denied or expired authentication: stop that access path. Report the required scope or supported login repair without requesting secrets in chat. An already permitted sanitized export may still be analyzed.
- Read throttling/transient timeout: honor Retry-After and finite remaining call/time budgets. Do not retry outside the window or expand scope automatically. Record partial data and attempts. A blocked connection is not a zero-error result.
- Launch/write timeout or unknown outcome: reconcile by existing run/object ID or an approved bounded status lookup before any further launch/write. Never blindly retry. Do not use a user command as a workaround to the same approval boundary.
- Empty successful result: report no matching observations for that query/window. It does not prove no incident or no traffic. Check filters/retention/sampling without broadening beyond the approved scope.
- Pagination/truncation: record counts, continuation and omitted fields. Fetch only within the remaining budget; otherwise preserve partial evidence and explain which conclusions are unsupported.

## User query/command packet

Include purpose; product/edition/query language; application/environment/tenant; actual selected IDs; explicit timezone-aware start/end; exact query/command with no secret values; row/page/scan/time/call bounds supported by the tool; expected output columns and units; and instructions for the user to remove tokens, cookies and personal/customer data before pasting. For a load command include the approved profile/run identifier and stop plan; asking for output does not approve execution.

Ask for a result header plus only the relevant aggregate rows/error/summary:

```text
Product/version and tenant/environment reference:
Query/command or saved query ID:
Event window and timezone:
Collected at:
Rows returned / total known / truncated / next page:
Units, rollup and sampling/retention limitations:
Redaction performed / omitted fields:
Result or exact error (sanitized):
```

Generate a real scoped SPL, DQL, Datadog search/metric request, AppDynamics metric/snapshot selection, NeoLoad run export or JMeter command from the selected product reference. When essential IDs/fields are unknown, ask one guided question for the missing mapping; do not fabricate a runnable query. A confirmed preference is not an access grant.

## Normalized evidence record

Retain originals when safe and requested; default monitoring artifacts are redacted aggregates plus source references. A normalized local JSON envelope has provider (`splunk`, `dynatrace`, `appdynamics`, `datadog`, `neoload`, `jmeter`), channel (`mcp`, `api`, `export`, `user-paste`), operation (`read`, `launch`, `write`), status (`ok`, `denied`, `auth-expired`, `rate-limited`, `timeout`, `unavailable`, `unknown-outcome`), application_id, environment, source_reference, query_reference, start_utc, end_utc, collected_at, redaction_reviewed (boolean), complete (boolean), row_count (nonnegative integer), truncated (boolean), next_page (string or null), and limitations (array of strings). Record query content/hash in the referenced artifact; identifiers must be secret-free. Include version, units, rollup, sampling, retention and linkage when applicable. `retry_after_seconds`, `remaining_calls` and `remaining_seconds` are optional read retry inputs; a retry candidate must fit the remaining call and time budget.

Run `python3 scripts/evidence_checks.py --record evidence.json` from the toolkit or `.qa-agent` root. This helper checks local envelope consistency and suggests the next step; it does not contact products, sanitize raw data, attest truth, authenticate a user or enforce permissions. Its `valid` flag is structural, never a successful run/approved operation. Incomplete or failed responses cannot support an overall pass or confirmed cause. Follow the shared RCA standard even for structurally complete evidence.

Pasted output is labelled user-supplied; never record it as a direct MCP/API execution receipt. Record unknown units/retention/collection times as gaps and ask only if they affect the requested conclusion. Do not force the user to invent missing provenance to satisfy a validator. Snippets remain useful for limited hypotheses while completeness is unknown.
