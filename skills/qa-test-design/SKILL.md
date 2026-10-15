---
name: qa-test-design
description: "Create versioned manual UI/API test scenarios with at least 20 distinct cases for each selected business flow."
license: MIT
---

# qa-test-design

Read `references/CONTRACT.md`. Use current confirmed flow rules, not recording guesses. Cover all selected dimensions where applicable; ask for missing expected behavior. At least 20 distinct meaningful cases per flow, more as needed. For a simple/partial flow with insufficient rules, record pending cases or seek clarification instead of fabricating assertions.
Each JSON/CSV case has application/flow ID and version, case ID/version, title, objective, category, priority, role, prerequisites, test data references, environment/browser/locale/viewport targets, actions, expected assertions, rule/evidence links, side effects, cleanup ownership and pending expectations. Encode multiline steps correctly in CSV. Case IDs are stable across revisions; version changed cases. Produce coverage mapping and excluded/not-applicable reasons. Preserve earlier versions; do not claim complete coverage without a defined rule inventory.
