# Bank SO IT

A small offline MCQ app for **Bank SO IT professional-knowledge practice**. The web app and Android APK use the **shared interface, question-bank source and scoring logic**.

The web version runs entirely on **GitHub Pages**: no server, database service, API key or paid hosting is required. After one successful online visit it works offline and can be installed from a supported browser. All personal data stays in your browser/device.

## Practice features

- **864 curated practice MCQs**, each with five choices, a correct answer and an explanation.
- Subject-wise or mixed tests; choose 20, 40, 50, all eligible questions, or any custom count.
- Subtopic, difficulty, unseen, wrong-answer and bookmark filters.
- **Quick revision**: searchable answer/explanation cards, source links and an 11-subject coverage selector. Repeated and specialist-depth items have been retired.
- Practice mode with immediate feedback, or Test mode with answers hidden until submission.
- Optional timer and −0.25 penalty; a focused 40-question / 30-minute preset.
- Question navigator, review flags, bookmarks, saved unfinished sessions and detailed results.
- Add/rename subjects, edit questions, and import/export JSON question packs.
- **Progress backup/restore** transfers edits, bookmarks, history and unfinished sessions between browsers or the APK.
- Installable web app with offline caching, plus a small signed Android APK.

| Subject | Questions |
|---|---:|
| Networks & Cybersecurity | 200 |
| DBMS & SQL | 118 |
| Operating Systems | 73 |
| Data Structures & Algorithms | 107 |
| Linux & Shell | 86 |
| Warehousing & Mining | 52 |
| Cloud, AI & ML Basics | 47 |
| Software Engineering & Banking IT | 68 |
| Programming & OOP | 60 |
| Computer Fundamentals & Architecture | 33 |
| Web Technology | 20 |
| **Total** | **864** |

Each retained stem, five-option set, key and explanation received a technical review, with sources and independent checks for computed answers. See the [content audit](docs/CONTENT_AUDIT.md), [per-item ledger](docs/question-audit.csv) and [retirement decisions](docs/retired-question-audit.csv). This is practice material rather than an official previous-year paper. No exact exam topic weights are asserted.

**Networks & Cybersecurity now contains 200 newly curated questions aligned to the user-provided topic map**, with only ten short subnet calculations. The previous 152 network items are retired; the other 664 questions are unchanged. See the [network review and coverage map](docs/NETWORK_AUDIT.md). The earlier cross-subject review is recorded separately in the content audit. Old stock imports cannot overwrite reviewed built-ins or restore retired items; use the editor for personal changes. Earlier session reviews are retained, while current-bank statistics exclude retired questions.

**Android 2.1** bundles the same curated bank and quick revision. It reuses the Android 1.2 release key, so 1.2 installations can update in place. Export a progress backup before installing updates. Installations predating the 1.2 key change still need export, uninstall, reinstall and restore.

## Deploy on GitHub Pages

The repository is now **[sarvesh-kr/bank-so-it](https://github.com/sarvesh-kr/bank-so-it)** and its configured site is **https://so.sarvesh.si/**. Deployment uses GitHub Actions.

1. In **Settings → Pages → Build and deployment**, keep **Source → GitHub Actions** selected.
2. Keep the custom domain **so.sarvesh.si** and **Enforce HTTPS** enabled in Pages settings.
3. Push or merge a pull request into `main`. The **Test and deploy GitHub Pages** workflow rebuilds the bank, runs tests, builds `_site/`, and deploys it after checks pass.
4. To redeploy without a code change, select **Actions → Test and deploy GitHub Pages → Run workflow → main**.

Pull requests and manual workflow runs on other branches only run validation. Only `main` can publish. The workflow uses GitHub's built-in token and Pages deployment identity; no deploy key, personal access token, or signing secret is needed. Repository-root web copies are no longer maintained; shared web/APK source lives under `app/src/main/assets/` and `_site/` is generated during the build.

For a custom subdomain, the DNS CNAME should target the owning account's Pages hostname, **sarvesh-kr.github.io**, without a scheme or path. The Pages custom-domain setting is the source of truth for Actions hosting; a repository `CNAME` file is not required. Keep domain/DNS settings under the owner's control. All app URLs are relative, so custom-domain roots and default Pages repository paths both work.

Collaborators can push code or submit pull requests; the owner or an administrator manages Pages, DNS and environment protection settings. See [deployment details](docs/DEPLOYMENT.md) for setup, transfers and troubleshooting.

## Web app use

Open the Pages URL online once. In **My bank**, the app indicates when offline practice is ready. Install via the browser's **Install app** menu, or **Share → Add to Home Screen** on iPhone/iPad. You can also keep using it in an ordinary tab.

Open or reload the app online to load the latest release. A release discovered while the page is already open does not restart it or apply when you leave a test or editor. Reloading applies the update regardless of the current screen; no Apply update button is needed. Offline visits use the last downloaded release. Saved progress is separate from the offline cache and is retained across updates.

Progress is local and **does not automatically sync** with GitHub, another browser, another device or the APK. Use **My bank → Back up progress**, then **Restore backup** on the destination. Clearing site data or uninstalling the Android app removes its local records. Browsers can also evict local storage; retain backups for important progress. Question-bank export includes questions only; a progress backup includes your personal records.

Timed sessions use the device clock and continue while you are away. If closed at the deadline, the saved attempt submits when reopened. Completed scores are raw practice scores, not IBPS normalized marks.

## Android APK

Download [Bank-SO-IT.apk](downloads/Bank-SO-IT.apk), or use **My bank → Download Android APK** on the web app. Open it on an Android phone and allow that file-opening app to install it if Android prompts.

Requires **Android 7.0+ with an updated Android System WebView**. The APK bundles its own offline assets, contains no native architecture-specific libraries and requests no app permissions. The shared browser features use Android's native file picker and local storage inside the APK.

To build locally:

```sh
export JAVA_HOME=/path/to/jdk
export ANDROID_HOME=/path/to/android-sdk
# Install platforms;android-35 and build-tools;35.0.0 with sdkmanager first.
bash tools/build_apk.sh
```

The result is `dist/Bank-SO-IT.apk`. A private signing key is generated under ignored `signing/` if none exists. **Keep this key private and retain it for future upgrades.** Keys, passwords, private source archives and local progress are excluded from this repository. Increase the manifest's `versionCode` when distributing upgrades.

An optional **Build Android APK** workflow is available. For stable signed upgrades, configure repository secrets `ANDROID_KEYSTORE_BASE64` (the original JKS encoded as Base64) and `ANDROID_KEYSTORE_PASSWORD`; the key alias is `rrb-it-personal`. The workflow fails if either secret is missing, preventing accidental changes to the release signing identity. Signing secrets are never needed by the Pages workflow.

## Develop and test

Python 3, Bash and Node.js 22+ are sufficient for the web build. npm dependencies are development/test tools and are not shipped to browsers or bundled in the APK.

```sh
npm ci
python3 tools/build_bank.py
python3 tools/audit_bank.py
python3 tools/check_apk_assets.py
npm test
npm run build:web
npx playwright install chromium
npm run test:pages
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. HTTPS or localhost is required for service workers. `test:pages` starts its own server and tests a repository subpath, offline practice, persistence, backups, separate project storage, the shared Android bridge, and automatic migration from the previous cached release. If using another installed Chromium, set `CHROME_PATH` to its executable.

## Project layout

- `app/src/main/assets/` — shared UI, pure quiz logic, browser persistence, PWA bootstrap, import validation and the generated question bank.
- `app/src/main/java/` — Android WebView shell, private storage and system file picker.
- `content/curated/network-r2.txt` — current 200-question network/cybersecurity source with explicit IDs and per-item references.
- `content/*.txt` — other concept/scenario sources and legacy generator compatibility inputs.
- `tools/build_bank.py` — deterministic generation plus executable SQL/Bash answer checks.
- `tools/build_web.py` — fresh `_site/` artifact built from an explicit public-file allowlist.
- `web/sw.template.js` — service-worker template, versioned by build content.
- `downloads/` — the signed APK published with the site.
- `.github/workflows/` — Pages testing/deployment and optional APK build.
- `tests/` — content, scoring, backup and browser tests.

The checked-in bank JSON lets the APK and browser share the same data. Edit `content/` or the generator for permanent bank changes, regenerate it, and commit the source changes. Edit UI source under `app/src/main/assets/`; Actions builds the publishable web files automatically. Rebuild the APK and replace the file under `downloads/` when you want the APK to include those changes too. In-app edits stay private to that installation until exported/imported.

## Question import format

```json
{
  "schemaVersion": 1,
  "subjects": [{"id": "programming", "name": "Programming Fundamentals"}],
  "questions": [{
    "id": "programming-001",
    "subject": "programming",
    "topic": "OOP",
    "difficulty": "Easy",
    "question": "Which principle bundles state and behavior?",
    "options": ["Encapsulation", "Paging", "Routing", "Normalization", "Deadlock"],
    "answer": 0,
    "explanation": "Encapsulation groups state and behavior and controls access to implementation."
  }]
}
```

`answer` is zero-based: 0=A through 4=E. Exactly five distinct options are required. A matching ID updates a question; a new ID adds one. Include each referenced subject in the pack. Import is previewed before applying; current and historical sessions retain their original question snapshots. Maximum question-pack size is 4 MB; maximum progress-backup size is 24 MB. The merged bank supports up to 100 subjects and 10,000 questions.

The Android application ID, browser database names and signing alias retain legacy identifiers so existing installations and progress continue to work. Newly exported backups use Bank SO IT naming; older backups remain supported.

See [validation notes](docs/VALIDATION.md) for what has and has not been tested.
