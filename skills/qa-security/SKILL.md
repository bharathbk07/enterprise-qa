---
name: qa-security
description: "Review full-stack threat boundaries and security controls, plan scoped verification and report reproducible vulnerabilities with remediation evidence."
license: MIT
---

# qa-security

Read `references/CONTRACT.md`, `references/ARCHITECTURE.md` and, when selecting security checks, `references/SECURITY.md`. Begin with available code/configuration/contracts and supplied evidence. Map entry points, assets, tenant/role boundaries, identity/session flows and dependencies. Assess authn/authz, input/output handling, injection, secrets, data protection, request forgery and supply-chain/configuration risks relevant to the stack; map exact selected requirements and standard versions rather than a generic checklist.
Before active scans or security test execution establish the authorized target, environment, methods, budgets, data ownership and stop criteria. Do not scan unrelated hosts, test live credentials, retrieve customer data or change controls merely to assess architecture. Use isolated synthetic identities/data and a dedicated spawned browser for UI tests. Missing approved tooling is a setup dependency or limitation, not a reason to install scanners globally.
Return suspected/reproduced findings with safe reproduction, impact/scope, preconditions, evidence, limitations and remediation/negative regression tests. Tool alerts need triage; clean scans are not proof of security or compliance. Redact exploit artifacts and secret values. Route causal analysis to qa-rca and changes to qa-fix-proposal/approved implementation; security findings do not waive the shared confirmation standard.
