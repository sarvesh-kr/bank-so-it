# Validation record

Build date: 18 October 2026.

## Question bank

- Exact totals: Networks & Cybersecurity 250, DBMS & SQL 250, OS 100, DSA 250, Linux & Shell 100.
- 950 unique IDs and unique complete stems.
- Every question has five distinct options, a valid zero-based correct index, a topic, level and explanation.
- 150 SQL-output answers computed by executing the stated queries against their stated datasets in SQLite.
- 30 shell-output answers computed by executing the stated scripts in Bash with C locale.
- Numerical and trace drills compute their keys and working from the stated inputs.
- Correct option positions vary, and session creation shuffles options while preserving the answer text.
- Original conceptual content was reviewed while authoring but has not had independent human expert review. Difficulty labels are editorial estimates.

## Pure quiz logic tests

Seven tests passed in `tests/core.test.js`:

1. Bank validation and exact subject counts.
2. Sampling 1, 20, 40, 50 and all 950 questions without repeats; balanced subjects and preserved answer mapping.
3. Rejection of invalid requested counts.
4. Correct/incorrect/unanswered scoring, negative totals, optional zero penalty and zero-attempt accuracy.
5. Subject, topic, difficulty, unseen, latest-wrong and bookmark filters.
6. Rejection of malformed answer keys, duplicate IDs/options, missing subjects/explanations and reserved IDs.
7. Merge-by-ID updates while retaining unrelated questions and leaving the base bank unchanged.

## Browser interaction tests

Passed in Chromium through Playwright:

- Home loads 950 questions and five subjects.
- Practice selects correct/wrong answers, reveals explanations, locks checked answers, bookmarks and flags.
- Unfinished attempt survives a reload and resumes with its selected answers.
- Navigator indicates answered and flagged questions.
- Results correctly score one correct, one wrong and one blank as 0.75/3.
- Review distinguishes selected wrong answers from the correct answer.
- Timed preset is 40 questions / 30 minutes; Test mode hides explanations before submission.
- Timer expiry submits saved answers.
- Expired persisted attempts submit exactly once after reopening, without duplicating progress.
- Invalid custom question counts are rejected.
- Adding a subject and question updates the bank and survives a reload.
- Malformed JSON packs are rejected; valid packs merge.
- Imported HTML is displayed as inert text, not executable content.
- Exported bank is valid JSON with all custom questions.
- Layouts fit 320, 390 and 768 CSS-pixel widths without horizontal overflow.
- Research/about and progress pages load.
- No browser JavaScript or content-security-policy errors in the tested flows.

## Android artifact

- Compiled against Android API 35, minimum API 24 (Android 7.0).
- APK Signature Scheme v2 and v3 verification passes.
- Release APK is not marked debuggable.
- No `uses-permission` declarations, including no Internet permission.
- Architecture-neutral Java bytecode and assets; no bundled native libraries or browser engine.
- The exported activity, label, version, screen support and SDK metadata were inspected with Android build tools.

Native emulator verification is recorded separately in `android-smoke.txt` when available. Browser checks alone do not verify every Android file-picker or device-specific behavior. No physical-phone or Play Store certification testing was performed.

## Reproduce

```sh
python3 tools/build_bank.py
node --test tests/core.test.js
# Serve app/src/main/assets on localhost:8765, then:
node tests/ui.test.js
node tests/expiry.test.js
bash tools/build_apk.sh
```

For a non-default Chromium installation, set `CHROME_PATH` to its executable. The app uses Android's existing System WebView, which should be kept up to date.

## Web / GitHub Pages edition 1.1

The shared UI now includes IndexedDB browser storage, install manifest/icons, a scope-specific service worker, offline APK download, and versioned progress backup/restore. The native shell keeps its AtomicFile storage and uses the same question and interface assets.

Ten core/backup tests passed. The Pages browser test starts a local server under `/rrb-it-practice/` and verifies all 950 questions, relative-path loading, manifest scope, service-worker control, an offline reload with a saved attempt, correct/wrong/blank scoring and review, progress export/restore and reload, separate state under another project path, offline APK fetch, responsive widths, and a simulated Android JavaScript storage bridge. No browser JavaScript errors were observed in that run. Malformed backups are rejected and completed scores are recomputed from stored answers.

The signing key and private delivery archives were excluded from the staged repository. The new APK was rebuilt and signature-verified. The simulated bridge check is not an actual Android device test; the earlier native-runtime limitation still applies.
