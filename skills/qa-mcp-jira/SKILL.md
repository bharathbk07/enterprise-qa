---
name: qa-mcp-jira
description: "Prepare and, after explicit approval, create/update evidence-linked Jira issues using discovered project metadata and duplicate checks."
---

# qa-mcp-jira

Read `references/CONTRACT.md`, `references/ENGINEERING.md` and `references/CONNECTOR.md`. Resolve approved site/project and discover tools/issue types/required/custom fields/workflows. Reuse confirmed project/type/workflow mappings, asking only missing/ambiguous choices; show the resolved issue type/workflow in each write draft. Support defects, incidents, investigations and remediation subtasks. Search bounded duplicates by application/run/failure signature; propose create vs update explicitly.
Draft reproduction, impact/environment/build, observed/expected behavior, RCA status/scores/evidence, proposal/validation and related IDs. Preview exact fields/body/target; obtain explicit approval for each write including comments/transitions/attachments. Validate parent/status/assignee mappings and visibility. On uncertain outcome reconcile by returned ID or unique marker; do not duplicate creates or transition blindly. Return write receipt/version/URL and audit reference. Do not grant issue permissions or publish raw secrets.
