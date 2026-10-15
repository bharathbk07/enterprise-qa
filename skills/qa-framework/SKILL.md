---
name: qa-framework
description: "Inspect an entire existing automation framework and document architecture, data flow and CI without changing implementation."
---

# qa-framework

Read `references/CONTRACT.md`. Inspect the entire relevant framework, using targeted searches and following references rather than dumping large repositories. Inventory languages/versions, structure, dependencies/lockfiles, runner, patterns (BDD/page objects/etc.), configs/environments, fixtures/hooks, feature files, step definitions, locators, assertions, data factories/files/providers, parameter substitution, examples tables, scenario outlines, data passed into features/steps, authentication, API clients, reporting, retries, tags, commands, CI pipelines, artifacts and secrets references.
Trace at least one actual scenario end-to-end: pipeline → command → configuration → feature/test → fixture/step → input source/transformation → UI/API → assertion → report. Document conventions with file/line evidence and commands in `framework-knowledge.md`; record missing/ambiguous details. Redact secret values; record variable names only. Exclude generated/vendor trees from full content reads but inventory their purpose. Do not run the whole suite merely to inspect; run checks only when relevant and authorized. CI remains read-only.
