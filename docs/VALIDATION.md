# Bank SO IT validation — 20 October 2026

## Question quality

The current bank contains 816 questions across 11 subjects. The review assigned a retain, correct or retire decision to all 1,150 previous records, retired 470, corrected or clarified 163 retained items, and added 136 foundations. Each shipped stem, five-option set, answer and explanation has a reviewed content hash and references. See [CONTENT_AUDIT.md](CONTENT_AUDIT.md), [the per-item ledger](question-audit.csv) and [retirement decisions](retired-question-audit.csv).

The independent checker verifies 88 current results: 40 worked calculations/traces, 15 SQL results, 16 Bash outputs, 10 Python outputs and seven further calculations. All 485 computed results in the previous bank were also checked. SQL and scripts are executed; other small cases are independently calculated or enumerated. Technical relevance and conceptual interpretation received a model-assisted review using cited documentation and authored textbooks. This is not independent human expert certification or an authenticated past paper.

## Completed checks

- Bank generation, reviewed-hash enforcement and independent answer checks passed.
- All 15 core/backup tests passed, including retirements, stale stock imports, reference validation, answer shuffling, scoring, sampling and legacy/new backup compatibility.
- Pages browser tests passed for scored attempts in the added subjects, quick revision/search/references, offline reload and practice, saved answers, results/review, progress backup/restore, separate project storage, cached APK, root/subpath hosting and responsive layouts.
- The automatic-update integration test starts with the actual pinned pre-update client from commit `693275a`. Loading it discovers the new release without a manual action. Progress, bookmarks, unfinished answers and original question snapshots survive the transition. New clients defer reloading during tests and question edits; leaving those screens applies the release automatically. The latest cached version works offline. Cache cleanup preserves sibling applications. The server also simulates a fresh HTTP asset cache to check that release downloads bypass stale browser entries.
- UI and expiry tests cover editing/import/export, inert imported HTML, saved sessions, timer expiry and exactly-once submission after restarting an expired test. Layouts and screenshots were inspected.
- JavaScript syntax and Git whitespace checks passed.

The static site is approximately 893 KB including its APK. Test tooling, raw source inputs, audit ledgers and signing material are excluded from the deployed site.

## Android 2.0

The public download is [Bank-SO-IT.apk](../downloads/Bank-SO-IT.apk): 160,943 bytes, version code 4, with all 816 questions and the same interface as the web app. APK Signature Schemes v2 and v3 verify. Every embedded shared asset matches source. [android-release.json](android-release.json) records its checksum and public signing-certificate fingerprint.

The existing Android 1.2 key and application ID are retained for in-place upgrades. The private key, password and backup remain excluded from Git. The signing certificate's original subject and internal storage identifiers are compatibility identifiers; the displayed app, downloads, exports, manifest and documentation use Bank SO IT. New backups use the new product format and old backups remain accepted.

Native interactions were tested through a simulated Android bridge in Chromium. A physical device/emulator installation has not been tested. GitHub denied access to configure signing secrets, so the optional Android workflow still requires its owner to supply the existing key via repository secrets; the published APK was signed locally. Pages deployment does not require these secrets.
