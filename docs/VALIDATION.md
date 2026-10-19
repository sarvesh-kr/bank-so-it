# Validation record — 19 October 2026

## Current question-bank update

- 1,150 unique questions across eight subjects; five distinct choices and a valid answer index for each.
- 65 warehousing/mining, 65 cloud/AI/ML and 70 software engineering/banking IT additions.
- 692 focused-revision questions; 458 optional-depth or extra-drill questions.
- All original 950 project records retain their IDs, stems, choices, answer indices and explanations. Only study metadata was added to those records.
- Generation executes 150 SQL answers in SQLite and 30 shell answers in Bash, and regenerates 305 numerical/trace answers.
- Per-question evidence and review limits are documented in [CONTENT_AUDIT.md](CONTENT_AUDIT.md). Automated checks do not certify conceptual accuracy independently.

## Checks completed

- `python3 tools/build_bank.py`: bank generation and structural checks passed.
- `python3 tools/audit_bank.py --attachment audit/attachment-original.json`: 1,150 production ledger rows and 1,150 input dispositions generated.
- `npm test`: all 11 core/backup tests passed, including focused/all filtering, legacy pack compatibility, metadata preservation, eight-subject sampling, scoring and invalid imports.
- `npm run build:web`: generated a static site of approximately 828 KB including the existing APK; audit CSVs and raw input are not included in the site.
- `CHROME_PATH=/usr/bin/chromium npm run test:pages`: passed. Each new subject supports a scored attempt; coverage selection changes eligible counts. Also checked root/subpath hosting, offline reload, scoring/review, IndexedDB persistence, backup/restore, path isolation, cached APK, simulated native storage and responsive layouts.
- `CHROME_PATH=/usr/bin/chromium npm run test:ui`: passed editing, imports, inert HTML handling, exports, timer expiry, one-time submission after restart, progress persistence and responsive layouts.
- JavaScript syntax and Git whitespace checks passed. Home screenshot inspected.

## Android 1.2 release

The old APK download was replaced with a newly signed 152,751-byte Android 1.2 APK (version code 3), as requested. APK Signature Schemes v2 and v3 pass verification. All embedded assets match the updated shared source, including 1,150 questions, eight subjects and focused revision. See [android-release.json](android-release.json) for the APK and public certificate fingerprints.

The release uses a new signing identity. Old installations require exporting progress, uninstalling the old APK, installing 1.2 and restoring the backup. The private key is excluded from Git and retained in a private backup. GitHub denied repository-secrets access (HTTP 403), so Actions signing secrets have not been configured. The Android workflow now fails if persistent signing secrets are absent rather than silently creating another key.

No physical-device or emulator test was completed for this release. Signature, archive-content and browser/shared-interface checks do not replace device testing.

## Reproduce

```sh
python3 tools/build_bank.py
python3 tools/audit_bank.py
npm test
npm run build:web
CHROME_PATH=/usr/bin/chromium npm run test:pages
# In another terminal for the UI suite:
python3 -m http.server 8765 --bind 127.0.0.1 --directory _site
# Then:
CHROME_PATH=/usr/bin/chromium npm run test:ui
```

Reuse the new Android 1.2 release key for future upgrades. Keep the private signing backup safe.
