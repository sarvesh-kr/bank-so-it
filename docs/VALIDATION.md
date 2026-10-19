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

## Android release limitation

The existing APK signature was verified. Its SHA-256 signing-certificate fingerprint is `d3396225849a80c79e30f4d3f1bc886177f9ac6fa618b335ea24dcc46dca0adc`.

No new APK was signed: the original signing key is unavailable. The existing download still has the earlier embedded bank/UI. It accepts the updated question pack through My bank → Import pack, but the new study-coverage UI requires an application rebuild with the existing signing key. No claim of a new device/emulator run is made. The simulated native browser bridge is not a physical Android test.

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

Use the existing release signing key when rebuilding the Android application. Do not substitute a new key for an update to an installed release.
