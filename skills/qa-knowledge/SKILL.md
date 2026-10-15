---
name: qa-knowledge
description: "Summarize and name recorded flows with minimal clarification, maintain business knowledge, and create illustrated manual flow documents."
license: MIT
---

# qa-knowledge

Read `references/CONTRACT.md`. Resolve stable application identity using URL/environment mappings. Read confirmed preferences, existing knowledge and recording evidence first. Present one concise combined review containing the suggested/user-supplied name, inferred ordered steps, proposed completion status and all minor uncertainties, with 3–4 meaningful choices plus free text. Do not review every recorded step as a separate question. Ask additional guided questions only for ambiguity or essential missing business rules, expected outcomes, scope or required approvals. Continue from stored review state and do not repeat answered questions.
Update `knowledge.md` sections in place and `application.json`. Record domain vocabulary, roles, permissions, entities, lifecycle transitions, business invariants, integrations, side effects, error rules and unresolved questions. Distinguish observed/user-confirmed/assumed rules. On conflicts preserve old rule and ask before replacing.
Write versioned `flows/FLOW-NNN.vN.json` and `flows/FLOW-NNN.vN.md` manual instructions (preconditions, data, numbered actions, expected results, alternatives, evidence). Partial flows retain incomplete status. Preserve current index in `flows/index.json`; changed steps/rules increment version and invalidate affected test mappings. Do not duplicate application knowledge per session.

Before finalizing a flow, use its user-supplied name or include one suggested business name (with optional alternatives/custom input) in the combined review. A confirmation of that displayed review confirms the proposed name; do not ask a second naming question. Ask directly only if the name/purpose remains essentially ambiguous. Never silently accept an inferred name. Resolve new vs existing flow and preserve ID/number, name aliases and prior evidence. A name-only edit does not invalidate execution history or increment business flow version.

Always create the named manual flow document with numbered steps and embedded actual screenshots using `references/FLOW-DOCUMENT.md`. Copy images into versioned flow-owned assets; retain source recording/step provenance in JSON. Verify each copied image exists and every embed resolves. Distinguish expected behavior from observed behavior and label missing screenshots explicitly. Return the Markdown document path, assets directory and readiness/gap summary.

Read `references/INTERACTION.md` for summary review, preference reuse and approval boundaries. Minor uncertainties belong in the combined review; if deferred, retain them as unresolved rather than fabricating expected behavior.
