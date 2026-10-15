# Security reporting

## Reporting a potential vulnerability

Do not open a public issue containing exploit details, credentials, browser profiles, customer data or unredacted logs. Use GitHub private vulnerability reporting when the repository's Security tab offers "Report a vulnerability":

https://github.com/bharathbk07/enterprise-qa/security/advisories/new

The presence of this link is not a claim that private reporting is enabled. If that option is unavailable, use a private contact channel explicitly published by the maintainer on their GitHub profile. This repository does not currently publish a dedicated security email address. Do not send sensitive information through public issues while a private channel is unavailable.

Include the affected revision/version, minimal synthetic reproduction, impact, environment and relevant redacted evidence. Avoid testing against other users' systems or live production services. Disclose only enough detail for investigation through the private route.

## Maintenance status

The project is early-stage. This policy does not promise a response/remediation SLA, audited security, or a supported release lifetime. Report the exact affected commit and any regression information. Maintainer acceptance and validation are required before a security fix is described as complete.

## Using the toolkit

- Keep credentials, authentication profiles and production data outside source control and public reports.
- Mask recording evidence unless a session-specific plaintext choice is explicitly authorized. Retained QA profiles store raw session state even when screenshots are masked.
- Production telemetry defaults to redacted aggregates/source references. Review evidence before publishing.
- Dedicated-browser ownership, local evidence checks and approval instructions are not a signed policy enforcement gateway. Host permissions and deployment controls remain necessary.
- Refer to docs/RECORDER.md and docs/GAP-REVIEW.md for known privacy, capture, quota and recovery limitations.

## Maintainer setup

Before advertising an operational private reporting route, enable and verify GitHub private vulnerability reporting or publish a monitored private address, then update this policy. Do not publish private report contents in release notes before an appropriate disclosure decision.

GitHub setup reference: [configure private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).
