# Production download routing fix — 21 October 2026

## Confirmed defect

The service worker returned cached `index.html` for **every navigation request in its scope**, before looking for a matching static asset. Browsers that handled a download link as navigation received the 1,265-byte app document instead of the APK. Opening `bank.json` as a document had the same problem, and nonexistent file paths incorrectly returned HTTP 200 with the app document.

Production reproduction confirmed all three responses were `text/html` from the service worker. Chromium's ordinary download-attribute path returned the correct files, which is why a direct-fetch check was insufficient to validate browser download behavior.

The earlier browser suite checked APK bytes using `fetch()` and tested generated progress-backup downloads. It did not test the APK anchor's navigation path. This was a coverage gap; passing those tests did not establish that every download path worked.

## Fix

Known static assets take precedence over application navigation. Only the app's root URL falls back to its cached shell; its index file is already an explicitly cached asset. Unknown paths retain network/404 behavior and fail offline rather than receiving an unrelated HTML document. Query strings do not change a known file into an app route.

Navigation requests for the APK and question pack receive explicit attachment filenames and correct MIME types. JSON fetches used by app startup retain normal semantics. Rebuilt responses remove transport encoding and length headers because Fetch exposes decoded bytes. The APK link also declares its filename explicitly. A stale question-count value was removed from the page description.

Question content, scoring and saved progress are unchanged. The signed Android 2.6.1 build retains the existing signing identity and contains matching shared assets.

## Regression and wider checks

[downloads.test.js](../tests/downloads.test.js) uses a compressed-response static server and exercises the actual My bank anchors with and without the download attribute. Each downloaded APK/JSON file must match the served artifact's SHA-256 and expected filename. The matrix covers Chromium and WebKit, root and repository-subpath hosting, online and offline operation: **32 file downloads**. It also verifies CSS document navigation, real missing-file errors and app reloads.

The regression was run against the actual pre-fix worker template from commit `e308ae7b8fcb398351f7b4598d851b446c096e18` and failed on the navigation-style APK download, then passed with the fix. Download tests are now a required step before Pages deployment.

The wider checks include core/backup tests, 125 independent whole-bank computed-result checks, Pages quiz/revision/download-cache/persistence flows, update migration, editor/import/export tests and deadline submission. Those checks cover defined scenarios; they are not a claim that the entire platform is free of undiscovered bugs. Desktop WebKit engine testing is not a substitute for testing every iOS/Safari version or Android device.
