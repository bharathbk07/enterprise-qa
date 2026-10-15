---
name: qa-mcp-confluence
description: "Prepare application knowledge, performance/RCA documents and runbooks, then publish version-aware Confluence changes after explicit approval."
license: MIT
---

# qa-mcp-confluence

Read `references/CONTRACT.md`, `references/ENGINEERING.md` and `references/CONNECTOR.md`. Resolve space/page/document type from the current request and confirmed application preferences; ask only missing/ambiguous values. Show the exact destination in each publication draft for explicit write approval; resolve IDs, permissions and existing version. Support derived application knowledge, plans, baselines, reports, incident history and approved remediation runbooks. Local knowledge remains canonical unless user chooses otherwise.
Preserve unrelated content and existing application page mapping; prepare redacted content/diff plus Jira/evidence links within visibility scope. Validate supported content format and convert deliberately; Markdown is not universally accepted by tools. Preview exact target/action/content/version and obtain approval. Use conditional version-aware updates if supported; on conflict re-read/rebase and obtain approval for changed content. If conditional updates are unavailable, flag the concurrency limitation and confirm before writing. Reconcile unknown create results rather than duplicating pages. Return receipt/page version/source report digest.
