# Named manual flow document with screenshots

Use an explicit user-supplied name. Otherwise include a concise suggested name (with alternatives/custom input if useful) in one combined flow review alongside inferred steps, proposed completion status and minor uncertainties. Confirmation of that review confirms the displayed name without a separate naming question. If the purpose remains unclear ask for a name directly. Preserve existing flow identity, aliases and business version for a rename-only change. Do not finalize a pending name.

After the combined review and any essential clarification, create `flows/FLOW-NNN.vN.md` and the corresponding JSON. This is a required deliverable, not just a link to events.jsonl or a list of screenshot paths.

## Document contents

Include confirmed flow name, stable ID/number, version, completion/documentation status, application/environment, actor/role, business objective, prerequisites, data references, privacy mode, source recording IDs and unresolved questions. For each numbered business step include its action/intent, expected result, observed result and recorded step IDs. A screenshot records an observed state; it does not establish the expected business rule.

Copy the actual step screenshot into `flows/assets/FLOW-NNN/vN/`, retaining its original recording and step in JSON. Use unique recording/step-derived filenames so resumed recordings cannot overwrite another step. Preserve existing version assets; resolve collisions by reusing identical content or choosing a distinct name, never replacing another step's evidence. Honor masked/plaintext session choices; never expose a previously masked credential in copies or captions. External publishing still requires the stricter production redaction and explicit approval rules.

Embed each existing copied screenshot immediately below its numbered step, using Markdown image syntax and a descriptive caption/alt text. Example syntax below is a structural template: replace paths only with real verified images, never ship a broken template embed as completed evidence.

```markdown
# <Confirmed flow name>

Flow: <FLOW-ID> · Version: <N> · Status: <completion/documentation status>

## 1. <Business action>

Action: <What the user did and why>
Expected: <User-confirmed expected behavior, or clearly unresolved>
Observed: <What the evidence actually shows>
Evidence: <recording ID / step ID / capture timing caveat if relevant>

![Step 1 — <Observed screen description>](assets/<FLOW-ID>/v<N>/<recording-id>-<step-id>.png)

Caption: <Role, screen/state, and meaningful observation without sensitive values>
```

If the screenshot is unavailable, write an explicit `Screenshot unavailable: <reason>` note in place of the image; preserve the recorder error and offer recapture in a dedicated spawned QA browser. Do not embed an invented screenshot, another step's image or an unresolved file path. Mark the document incomplete or complete-with-gaps as appropriate; offer the documented draft with gaps rather than claiming full visual coverage.

## Verification and handoff

Verify every image source/copy exists and each relative image path resolves from the Markdown file. Map every captured step to the correct business step; combine several recorded events only with clear step-ID mapping. Ensure headers/JSON/index agree on confirmed name, ID/version, completion and documentation status. Do not silently copy images across applications or environments. Return the illustrated document and asset paths, and list remaining naming/expectation/screenshot gaps. Human review and business clarification remain the knowledge agent's responsibility; the recorder captures evidence only.
