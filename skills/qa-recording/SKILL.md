---
name: qa-recording
description: "Record human flows in a dedicated spawned Chromium browser with step screenshots, console/network evidence and bounded file resources until the last window closes."
license: MIT
---

# qa-recording

Read `references/CONTRACT.md` and `references/RECORDING.md`, `references/BROWSER.md`. Obtain start URL, application ID, workspace, session masking/plaintext choice and optional saved-session storage consent. Use the installed recorder command in `references/RECORDER.md`. Spawn a dedicated headed Chromium process and QA-only profile for the demonstration; headless is only for local verification. Use the bundled recorder, never an integrated browser or attachment to a personal/shared browser. Resume only a retained QA application profile with storage consent, launching a dedicated process again.
Capture meaningful clicks, completed field entry, selections, keyboard actions, submissions, navigation, tabs/popups, console errors and fetch/XHR API evidence. Link tab/frame identifiers and chronological step IDs. Resources share the 25 MB budget. Screenshots are best-effort after action; navigation/rapid actions can race. Preserve screenshot errors and evidence gaps. Native dialogs, closed shadow roots, canvas and cross-origin restrictions may need user descriptions; do not claim exhaustive capture.
When the final window closes or recording is explicitly stopped, return recording path and summary. Hand off to qa-knowledge for one combined review of suggested name, inferred steps, proposed completion status and minor uncertainties. Browser closure alone does not confirm completion. If the user confirms interruption, offer retained-session resume or fresh start; saved URL/profile cannot guarantee restoration of in-memory app state. Ask only essential follow-ups instead of questioning every step.

Retain any user-supplied flow name/objective with the recording handoff. If absent, let qa-knowledge suggest names from clarified actions or ask the user to enter a name; a recording ID is not a confirmed business name. Pass recording ID, ordered step IDs, screenshot paths/errors, privacy choice and naming status directly to the combined review for the illustrated flow document. Never imply that recording alone creates the final named business document.
