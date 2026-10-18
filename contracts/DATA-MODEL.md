# Data model and lifecycle

`application.json`: schema_version, application_id, name, aliases, environments (name/base_urls), roles, created_at, updated_at. Register aliases to the same stable ID; ambiguity needs user input.
`workflow.json`: selected stage, flow/version, recording ID, completed/interrupted/abandoned/uncertain answer, clarification cursor, unresolved questions, authorizations. State: discovered → recording → awaiting-completion → clarifying → knowledge-ready → cases-ready → executing → eligible/override-required → automation; performance and analysis are independent requested branches. An interrupted flow returns to recording or stays incomplete.
`flows/index.json`: `flows` array of {id, number, name, version, status}. Version records hold business rules/provenance, steps/expected outcomes, alternatives, prerequisites and evidence. Current index points to immutable version files.
`cases/index.json`: `cases` array of {case_id, case_version, flow_id, flow_version, status}. Full cases in versioned JSON and properly quoted CSV; status active/stale/pending. See skill instructions for fields. Always create this index: automation gate joins it against execution records.
`runs/*.json`: execution schema in records.schema.json. Each attempt stores original outcome, actual/expected assertions, timestamps and evidence paths relative to the application root. Manual execution_kind is manual-browser/manual-api even when an AI drives the manual case through MCP. Automated framework runs do not satisfy the manual prerequisite.
`overrides.json`: overrides array of {flow_id, flow_version, authorized_by, authorized_at, reason, scope: automation, explicit: true}. Only user-authorized explicit entries count; agents cannot grant overrides to themselves.
`reports/analysis-*.json`: defects link case/flow/run versions, cause_scores (0–100 or null), supporting/contrary evidence, severity, recommended validation; thresholds assessed against approved performance profile. Engineering Markdown links this evidence.

Gate: select flows by names, numbers or IDs; reject unresolved entries. Join current cases and manual run first attempts. Count distinct current case IDs with current case versions, first-attempt passed/failed status, timestamps and existing nonempty evidence files. Needs two per current flow version or an explicit version-scoped override. Record eligibility rationale. JSON records are evidence logs, not cryptographically signed attestations.

No synthetic run results are shipped. Scripts do not generate business knowledge/test cases or an entire automation framework without the agent/user context.

Check the gate from the source package (or installed .qa-agent):

```sh
python scripts/check_gate.py --application-root "/path/to/application/qa/customer-portal" --flows "Checkout,FLOW-003"
```

Exit 0 means all selected flows satisfy current evidence/overrides; exit 2 means missing prerequisites, unresolved selection or malformed input. Never grant an override merely to make this command pass. Preserve the user's explicit answer in the version-scoped record.

# Flow identity and illustrated document fields

Flow index entries additionally carry `aliases`, `name_status` (pending/user-supplied/user-confirmed) and `documentation_status` (draft/incomplete/complete-with-gaps/complete). Ask the name before finalizing; a temporary recording/flow ID is sufficient while clarification is pending. A name-only edit preserves ID, number and business version; changed business steps/rules still version the flow and invalidate impacted cases as before.

Each versioned flow JSON stores `name`, `name_source`, `name_confirmed_at` when confirmed, recording IDs, privacy mode and steps containing `step_id`, `action`, `expected_result`, `observed_result`, `source_recording_id`, `source_screenshot`, `document_screenshot`, `screenshot_status` (captured/unavailable) and `screenshot_gap_reason` when unavailable. Keep screenshot provenance when several recordings contribute to one flow. Never equate screenshot presence with a passed business assertion.

The Markdown flow document embeds copied images from `flows/assets/FLOW-NNN/vN/` using paths relative to the document. Record original recording/step references in JSON. Screenshot copies survive recording cleanup and remain until their own deletion is requested; deleting a recording is not a global purge of all derived evidence copies. Keep case/run traceability keyed to stable flow ID/version, not display name alone.

# Summary review and confirmed preferences

Use one combined summary review for proposed flow name, inferred steps, completion status and minor uncertainties. Store `review_status`, `proposed_name`, `proposed_completion`, `minor_uncertainties`, `essential_blockers`, answers and confirmation references in workflow/clarification state. Existing step_cursor is retained for compatibility, not a requirement to question every step.

Confirmed nonsecret defaults live in `qa/preferences.json` (workspace) and `qa/<application-id>/preferences.json` (application overrides), with scope/environment, source confirmation reference/time and freshness conditions. Current user instructions override remembered preferences. Reuse only confirmed applicable settings; do not store credentials or approvals. See docs/INTERACTION.md for review and approval boundaries.

# Native framework execution

qa-test-execution selects manual-flow or native-runner mode before resolving flow records. Selected existing unit/component/contract/integration/end-to-end suites do not require manual flow identity. See NATIVE-EXECUTION.md for handoff and result fields. Native results use native-runs/, automated-* execution kinds, actual runner/report provenance and original attempt outcomes; qa-analysis normalizes them without granting manual gate eligibility. Flow/version references are optional traceability, not invented prerequisites.


# Conditional work continuity

knowledge.md remains the single canonical application knowledge document. Ongoing work may reuse an existing mutable summary or, when useful, work-knowledge/WORK-ID.md and work-knowledge/index.json. Match stable work/incident/assessment IDs and objectives before writing; update the same note on resume, create a separate note for distinct work only when continuity adds value, and skip one-off/redundant notes. See KNOWLEDGE.md for identity, freshness, minimal fields and few-question policy. These notes link versioned flow/test/RCA/architecture evidence; they neither replace immutable history nor carry reusable approvals. No application notes/index are created during toolkit setup.
