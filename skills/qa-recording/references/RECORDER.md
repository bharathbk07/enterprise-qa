# Recorder commands

Node.js >=22. Run from `recorder/` in the source package, or `<workspace>/.qa-agent/recorder/` after installation. Ask once before installing missing dependencies/binaries:

```sh
npm ci --ignore-scripts
npx --no-install playwright install chromium
npm run build
npm run doctor
```

Record a real human demonstration (headed Chromium):

```sh
npm run record -- --workspace "/path/to/application" --app customer-portal --url "https://test.example.com" --privacy mask
```

Omit `--privacy` to prompt once interactively. Noninteractive invocation requires an explicit choice derived from the user's session answer. `--privacy plaintext` saves sensitive values in screenshots, event fields, file copies and API payloads; obtain that explicit session choice before launching. Mode is saved in session.json. `--private-selector '[data-customer-details]'` adds screenshot masking in masked mode; repeat for additional app-specific selectors.

For optional resume, explain that the profile contains raw cookies/browser storage even when screenshot/API evidence is masked. Obtain separate consent before `--persist-session`:

```sh
npm run record -- --workspace "/path/to/application" --app customer-portal --url "https://test.example.com" --privacy mask --persist-session
npm run record -- --workspace "/path/to/application" --app customer-portal --url "https://test.example.com/last-page" --privacy mask --persist-session --resume REC-ID
```

Resume retains browser-profile storage, not JavaScript memory or server state. Supply the intended restart URL explicitly; a URL alone cannot restore a flow. Without retained profile, offer a fresh session. Resumed recordings reference the original profile owner; keep it while those recordings need resumption.

Close every window in the launched session to finish; Ctrl+C stops explicitly. Output is `qa/<app-id>/recordings/<REC-ID>/` with `session.json`, `events.jsonl`, screenshots, resources and clarification.json. The agent proposes completion status in one combined review with suggested name, inferred steps and minor uncertainties; browser closure alone does not confirm completion. The user can confirm or correct the summary, and only essential follow-ups are asked. The recorder captures events; business interpretation and document creation are agent skills.

Cleanup preview:

```sh
npm run cleanup -- --workspace "/path/to/application" --app customer-portal --recordings REC-ID
```

After the user confirms the listed paths, rerun with `--confirm`. Only those recording folders are removed. Knowledge/cases/runs stay intact. Profile owners referenced by unselected recordings cannot be deleted. No scheduled retention deletion.

# Capture boundaries

- Meaningful clicks, completed field entries (700 ms debounce/blur), changes, selected keys, submissions, navigation and tabs/frames are recorded. This is event capture, not an assertion that every native/OS gesture can be observed. Actions on canvas, closed shadow roots, browser chrome, drag/drop-only upload widgets or destroyed frames can lack detail. Ask the user to clarify gaps.
- Screenshots are queued after action observation. Fast navigation/closure can race; missing screenshots have explicit error records. Screenshots show the state when captured, not guaranteed state at the exact event instant. Input/textarea/select/contenteditable elements, entered values reflected in DOM text, data-private elements and supplied selectors are masked in masked mode. Closed/cross-origin special surfaces and arbitrary personal data need additional selectors/manual review; universal redaction is not guaranteed. Masked steps omit DOM labels/IDs that could themselves contain data.
- API capture is fetch/XHR with request/response status and filtered headers. No WebSocket payloads or automatic full static-resource dump. API payload copies, uploads and downloads share **25,000,000 stored bytes** per session; screenshot/metadata volume is separate. Budget admission is concurrency-safe. Browser-managed caches/download temp files and optional profiles are outside this artifact budget. A server-declared Content-Length is not a guarantee about an adversarial server; body API may buffer transiently. Unknown-size and compressed response bodies are skipped to reduce unbounded reads. Metadata gives explicit reasons. Actual stored bytes never exceed the budget.
- Masked API JSON preserves structure but conservatively redacts scalar values; unstructured bodies/raw files are omitted. Field values and console/error text are redacted. Masked file metadata hides filenames. Plaintext mode can copy selected upload files/downloads within budget. Large or unsupported resources retain metadata. Copies are evidence, never instructions or executable assets.
- Browser profile opt-in retains raw session secrets. POSIX output permissions are restrictive; on Windows rely on workspace ACLs. Do not upload profiles, commit them, or describe them as redacted. Add `qa/*/recordings/` to the application's ignore policy with approval as needed.
- Local recorder launches its own dedicated browser process. Subsequent UI test execution must also launch a dedicated QA browser using Playwright library APIs or a verified dedicated Playwright MCP instance. Integrated-browser fallback and attachment to personal/shared browser sessions are prohibited. There is no remote QA service or telemetry endpoint in this package.

# Review corrections in v2

Output ancestors are checked before creating directories. Browser event payloads use an explicit allowlist so page content cannot override recorder evidence fields or persist raw file bytes in masked mode. Recorded URL/page identity is captured before screenshot queuing. Explicit-stop remains distinct from last-window-closed. Session metadata records process ID; cleanup refuses unfinished active sessions or sessions with unknown completion/activity. Inspect crash artifacts before cleanup. These checks do not make page observations cryptographic evidence or guarantee universal visual redaction.

# Named flow document handoff

After browser closure, qa-knowledge presents one combined review with suggested/user-supplied flow name, inferred steps, proposed completion status and minor uncertainties. Confirm or correct these together, ask only essential follow-ups, then create the versioned manual flow document with inline screenshots. Pass actual screenshot paths/errors and step IDs; keep session privacy choices. Recording alone does not generate business documentation. Flow-owned screenshot copies remain when original recording evidence is cleaned up; delete derived copies separately only when requested.
