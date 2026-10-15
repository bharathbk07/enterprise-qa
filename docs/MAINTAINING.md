# Maintainer checklist

Canonical repository: https://github.com/bharathbk07/enterprise-qa . Maintainer attribution: Bharath Kumar M. License: MIT. Toolkit package version is in skill-definition.json/agent-manifest.json; recorder/package.json has a separate runtime version.

## Review and release preparation

1. Keep canonical skills/agents/contracts/docs coherent. Preserve dedicated browser ownership, combined review, screenshot evidence and explicit approval rules.
2. Update CHANGELOG.md and relevant toolkit/package metadata when a release iteration changes. Verify factual claims against actual checks; do not convert planned validation into passed results.
3. Review new files for credentials, application data, authentication profiles, local paths and unexpected vendored content. The distribution list is a packaging aid, not a secret scanner.
4. Run scripts/sync_package.py after intentional edits. It synchronizes shared references, native adapters, license copies and owned checksums. Review the generated diff; it must include LICENSE and required notices in installable/distributable bundles.
5. Run relevant checks in CONTRIBUTING.md. Verify optional client/live-connector acceptance separately; no external load or writes solely for routine release validation.
6. Review source archives for license/community docs and excluded local/generated artifacts. Preserve upstream notices if adding third-party code/binaries. Do not bundle node_modules or application evidence by accident.
7. Publish commits, tags, releases or documentation only through the repository's approved workflow. Preparing these files does not configure branch protection, GitHub Actions, issue labels, Discussions, private reporting or release tags.

## GitHub settings to review manually

Enable and verify private vulnerability reporting, or publish a monitored private reporting address and update SECURITY.md. Enable Issues if using the supplied forms. Review repository description/topics, maintainer permissions and a suitable branch-review policy. Do not claim these settings have been enabled merely because templates exist. No new CI workflow is included in this documentation update; pipeline changes require their own request.

## License handling

Root LICENSE is canonical. The synchronizer copies it into each independently installable skill and agent bundle and includes those files in distribution.json. SKILL.md frontmatter and portable catalogs identify MIT; recorder metadata/lockfile identify the repository package license while dependency notices remain separate. Do not remove copyright/permission text from copied bundles.
