# Third-party notices

Enterprise QA Agent Kit's repository-authored software, skills and documentation are distributed under LICENSE (MIT). Dependencies and external products have their own licenses and terms. Preserve applicable upstream license/notice files when redistributing their code or binaries; the toolkit's MIT notice does not replace them.

The current recorder/package-lock.json records:

- Playwright and playwright-core 1.64.0: Apache-2.0.
- TypeScript 5.9.3: Apache-2.0.
- @types/node 25.6.0: MIT.
- undici-types 7.19.2: MIT.

These identifiers are taken from the checked-in lockfile, not a complete legal or dependency audit. Review the installed packages' upstream LICENSE/NOTICE files when redistributing those packages. Browser binaries installed by Playwright are separate downloads with their own accompanying notices. The source-only distribution allowlist excludes node_modules, compiled dependencies, downloaded browsers, application recordings and profiles.

Vendor documentation linked by the project remains attributable to its publisher. MCP endpoints, hosted products and associated accounts retain their provider terms and permissions. Product names are used to identify integration targets; no vendor endorsement or service license is supplied by this repository.

The MIT license text follows the Open Source Initiative reference: https://opensource.org/license/mit . The project's copyright notice identifies Bharath Kumar M for 2026.

The protected Playwright agent initializer generates definitions from the user's installed upstream Playwright package at setup time. Those upstream instruction texts are not vendored into this source distribution. When installed, their LICENSE/NOTICE are retained in namespaced files beside the generated definitions, including local Enterprise QA boundary additions. Do not replace the upstream license with the toolkit's MIT notice.
