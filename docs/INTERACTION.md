# Fewer questions, guided review

## Default interaction

Read the user's current instructions, confirmed preferences, existing application knowledge and recording evidence before asking anything. Do not ask a standard questionnaire when the answer is already available. Reuse confirmed facts/preferences with their application/environment scope; do not infer new authorization from them.

After recording, prepare one concise review containing:

- User-supplied or suggested flow name, with a custom-name correction available.
- Inferred numbered business steps linked to screenshots/evidence; distinguish observations from unconfirmed expectations.
- Proposed completion status, clearly awaiting the user's confirmation; closing the browser is not proof of completion.
- All nonessential uncertainties, with any suggested resolution explicitly shown or marked unresolved.

Ask one guided question, with 3–4 concrete options and free text. For a recorded flow whose completeness is uncertain, useful options are: Confirm summary and flow completed; Confirm steps but flow was interrupted; Correct the summary/name; Keep a draft and review later. Adapt choices to actual evidence rather than forcing generic options. Include the review in the question context or immediately accessible summary so approval applies to a concrete result.

A confirmation covers the displayed name, steps, completion and minor resolutions together. Do not follow it with separate name/completion/step confirmations. If the user corrects only one field, preserve already confirmed answers; ask again only if a material change or unresolved essential detail requires it.

## Follow-ups

Ask additional questions only when genuine uncertainty affects a business rule, expected test outcome, execution scope, required data/role, safety of an effect or required approval. Use one targeted guided question at a time, with 3–4 meaningful options plus free text. Do not invent business rules to avoid a necessary question.

Minor uncertainties belong in one combined review, not a series of prompts. If the user defers them, list them as unresolved in the draft and continue independent work. Do not silently turn unanswered suggestions into confirmed facts. Step-by-step review is available when explicitly requested, rather than the default.

## Remembering confirmed preferences

Use `qa/preferences.json` for confirmed workspace defaults and `qa/<application-id>/preferences.json` for application overrides. Application-specific confirmed values take precedence over workspace defaults; current explicit user instructions take precedence over both. Before reuse check environment, application ID, source/provenance and whether the setting is stale or contradicted by discovered configuration. Ask only about the affected setting, not every saved preference.

Each saved setting records key/value, scope (including environment when needed), confirmation source/reference, confirmed_at and optional revision/freshness condition. Store only explicitly confirmed nonsecret values. Never save credentials, raw sensitive data or reusable approval grants. Examples of reusable values: document format, flow review style, selected framework/tool, preferred browser targets and known environment IDs. New run load/duration/threshold values still need complete-profile confirmation.

A useful preference object contains `schema_version`, `scope`, `settings` and per-setting `value`, `confirmed_at`, `confirmation_reference`, and `valid_for`. Settings without trustworthy confirmation stay suggestions and cannot silently override confirmed configuration.

## Approval boundaries

Combining flow review does not authorize a new recording privacy choice, retained-profile storage, automation prerequisite override, performance run, RCA fix, external configuration change or Jira/Confluence write. Keep their required scope-specific approvals. Include already known values in the concrete proposed action instead of asking for them again. Do not re-request permission for an unchanged action already covered by explicit authorization. Never treat elapsed time or unanswered review as consent.

## Persisted review state

`workflow.json`/`clarification.json` track summary review status, proposed and confirmed name/completion, inferred step/evidence mapping, minor uncertainties, essential blockers, answers and confirmation references. Keep the existing step cursor for compatibility, but it no longer means every recorded step must trigger a question. Drafts remain draft when name/completion or essential rules are unconfirmed. Dedicated spawned-browser and inline screenshot requirements remain unchanged.


## Work continuity without another questionnaire

For the same ongoing work, use its matched work ID and mutable note; do not ask the user to repeat context or choose a new filename. Create a separate note only for distinct work whose context will be reused, and skip one-off answers. Check existing application knowledge, work/issue IDs, scoped preferences and source freshness before questioning. If identity/scope is genuinely ambiguous, ask one guided question with the proposed existing work and meaningful alternatives/free text, then continue with the answer. Do not turn note maintenance into a mandatory flow review or new approval step. See the installed knowledge role's KNOWLEDGE.md reference for full continuity rules.
