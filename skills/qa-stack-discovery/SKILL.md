---
name: qa-stack-discovery
description: "Map an existing frontend, API/service, data, integration and infrastructure stack with implementation evidence and deployment uncertainty."
license: MIT
---

# qa-stack-discovery

Read `references/CONTRACT.md` and `references/ARCHITECTURE.md`. Inspect relevant source/configuration/lockfiles/contracts/deployment descriptors and supplied diagrams using targeted searches. Record frontend routing/state/rendering, APIs/auth, services/jobs, databases/migrations, caches/queues, integrations, hosting/IaC/networking, CI and observability. Identify versions, ownership, trust boundaries and data classifications through references, never secret values. Do not infer a running topology from a manifest alone; label observed, documented and unverified deployment state.
Trace a selected real business request from UI or API entry through authorization, service logic, persistence/events/external dependencies and observable response/assertions. Include failure paths, consistency boundaries, revisions and file/line evidence. If code/access is missing, use provided artifacts and report the specific gap. Do not run installs, full suites, SQL workloads or infrastructure plans merely for discovery. Reuse framework-knowledge.md for testing implementation details; maintain architecture/stack.md and context.json without creating another business knowledge file. Return relevant risk hotspots to the architect and testing roles.
