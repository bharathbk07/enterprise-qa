---
name: qa-accessibility
description: "Assess web accessibility through scoped automated and manual checks, evidence-linked criteria and practical frontend remediation plans."
license: MIT
---

# qa-accessibility

Read `references/CONTRACT.md`, `references/ARCHITECTURE.md` and `references/ACCESSIBILITY.md` when selecting checks. Resolve requested pages/flows, target standard/version/level and browser/assistive-technology matrix from confirmed project inputs. If no formal target exists, record exploratory findings; ask for the target only when making a conformance or release assessment.
Cover semantics/names, keyboard/focus, labels/errors/status, contrast/zoom/reflow, motion and complete user processes where applicable. Use available tools plus manual verification; never treat automated checks as full WCAG coverage. UI execution uses a dedicated spawned QA browser; an unavailable screen reader/browser capability remains blocked/not-tested and can be handed to a human with precise steps.
Record page/component/state, verified criterion ID/version, method/technology, expected/actual, reproduction, screenshot/DOM evidence and affected users. Keep automated findings, manual results and untested criteria distinct. Do not invent screenshots, certify compliance or infer a complete process passed from one page. Produce targeted semantic/interaction remediation plus regression checks; application edits follow the concrete fix approval workflow.
