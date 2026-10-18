---
name: qa-orchestrate
description: "Coordinate a requested QA workflow across recording, knowledge, tests, automation, performance and reporting without loading unrelated stages."
license: MIT
---

# qa-orchestrate

Identify the requested stage, application and selected flows. Read `references/CONTRACT.md`. Consult `agent-manifest.json` at the package root or installed `.qa-agent/agent-manifest.json` for roles. Load only the relevant specialist skill. Carry forward the user's choices and authorization; do not force the whole lifecycle on a request for one stage.
Route: setup → qa-setup; browser operations → qa-playwright; capture → qa-recording; clarify/update knowledge → qa-knowledge; inspect framework → qa-framework; design cases → qa-test-design; execute cases → qa-test-execution; framework changes → qa-automation; load scripts/runs → qa-performance; diagnose results → qa-analysis; engineering document → qa-reporting.
After capture, use the combined flow review to confirm the proposed completed/interrupted status together with its name, steps and minor uncertainties; do not ask a separate completion question. For interruption offer saved-session resume (only if available) or a fresh session. Browser closure is not proof of flow completion. Track selected stage state and unresolved questions in `workflow.json`. Stop only at required human input or a concrete tool limitation; finish independently authorized work. Warn/override gate belongs before automation mutations.

Performance-engineering or incident/RCA requests route to qa-engineering. Tool-level performance execution stays with qa-performance. Connector setup stays with qa-setup. Do not load the new specialist collection wholesale.

Recording-to-knowledge handoff must resolve a user-supplied or user-confirmed flow name and produce an illustrated manual flow document. Route naming and screenshot-to-step mapping to qa-knowledge; retain gaps/readiness in workflow.json. Do not mark documentation complete when only recording metadata or screenshot links without the required inline images exist.

Use summary-first clarification from `references/INTERACTION.md`: one combined review resolves flow name, steps, completion and minor uncertainties. Reuse confirmed preferences; ask additional questions only for essential gaps or required approval. Do not run a fixed discovery questionnaire or ask specialists to repeat answered questions.

Broader full-stack quality/solution architecture requests go to qa-architect with the existing application context and a concrete scope. Do not forward a delegated recording/testing task back to the architect; complete it and return its artifacts. Existing QA-only entry usage remains supported.

When repeated or ongoing work would benefit from durable context, read `references/KNOWLEDGE.md` and route the scoped update/resume to qa-knowledge knowledge mode. Reuse the same application/work note; separate genuinely distinct work only when useful. Pass the matched work ID/path and source deltas in handoffs. Do not create notes for every request, force recording, or repeat known questions.
