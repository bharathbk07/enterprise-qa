# Useful knowledge and work continuity

Use this guidance when reusable facts or ongoing work would otherwise be rediscovered. Do not create a knowledge file for a one-off lookup, generic answer, empty task or repetition of an existing useful artifact. Installing the toolkit does not create application/work knowledge. Read only the relevant sections/index entries, not every prior investigation.

## Choose the existing home first

- **Same application:** update qa/<application-id>/knowledge.md for durable business/system understanding. Another environment, session, date or monitoring tool does not create another application knowledge file. Keep environment/revision qualifiers when behavior differs.
- **Same flow/framework:** update or link the existing versioned flow or framework knowledge under its existing rules. Do not replace immutable evidence/version history with a new summary.
- **Same ongoing work:** resume the mapped mutable work note and update it in place. A stable investigation/assessment/incident ID or explicit user continuation is the strongest match. Retesting, another session/environment or a different tool stays in that work when the objective/identity is unchanged.
- **Different work, same application:** create a separate work note only when a distinct objective/investigation needs continuity. Link related work and shared application knowledge; do not copy them wholesale.
- **Different application:** resolve/create its own stable application identity and canonical knowledge. Do not merge applications because they share a domain name, component name or similar issue title.

Use an existing mutable investigation summary if it already serves this purpose. Otherwise use qa/<application-id>/work-knowledge/WORK-ID.md. Create/update work-knowledge/index.json only when a work note actually exists. No compulsory per-task log or second knowledge system. A recorded flow already documented adequately does not automatically need a work note.

## Resolve identity with few questions

First inspect confirmed application mappings, current request/continuation, supplied work/issue IDs and the relevant work index/artifacts. Use objective/type/flow or component links to distinguish related work. A matching title or URL alone is insufficient. Avoid duplicate date-named notes on resume and avoid silently merging separate incidents.

When there is one strong existing match, continue it without asking for a filename or reconfirming unchanged context. When the match is genuinely ambiguous or a merge would change scope, ask one guided question with 3–4 meaningful choices plus free text, for example: continue the suggested work; create separate work in this application; choose another existing work/application; defer saving. Show the candidate ID/objective so the answer is concrete. Ask only the next essential question; no fixed intake questionnaire or mandatory final note-approval prompt. Keep minor uncertainties together and continue independent work. Business-rule conflicts and action approvals retain their existing rules.

## Store what changes the next decision

A compact work note contains work ID/title, application/objective/type, relevant environments/revisions, status, updated_at and source references; then confirmed facts/constraints, current hypothesis and confidence, decisions with reasons, attempts/results as evidence links, rejected approaches and why, unresolved critical questions and next action/owner. Keep observed, user-confirmed, assumed, suspected and validated states distinct. Do not convert a candidate cause or proposed solution into established knowledge.

The optional index has schema_version and works entries with work_id, application_id, title/objective/type, external_issue_refs, related flow/component IDs, environments, status, note_path and updated_at. Paths are relative to the application artifact root and must remain inside it; derive safe internal IDs rather than treating external titles/IDs as file paths. It points to the note; it does not duplicate its content.

Update only relevant sections, preserve useful earlier decisions and link superseded facts to their replacement evidence. Keep raw runs, immutable versions, original failures and approvals in their existing artifact homes. For app-wide reusable facts, update the appropriate canonical knowledge section and link the work; keep session-specific hypotheses in the work note. Assign one writer per shared file; other specialists return proposed deltas with sources. Re-read before writing and preserve unrelated concurrent edits.

## Resume and privacy

On resume give a short “known / changed or stale / next” summary. Check that remembered facts still fit the current application, environment, revision, tool capabilities and source freshness; reverify only what affects the task. If source evidence is missing or conflicting, retain the uncertainty instead of repeating an old conclusion as fact. Do not silently replace a confirmed business rule.

Save redacted durable facts and evidence references, not credentials, cookies, raw customer data, browser profiles, whole transcripts or reusable permission grants. A remembered target/tool/preference, earlier run approval or proposed fix is not fresh execution/implementation authorization. Current instructions and existing approval rules take precedence. Work-note continuity requires neither browser recording nor screenshots; those remain required only for the separate recorded manual-flow workflow. This is an agent procedure, not an automatic knowledge database or transactional writer.
