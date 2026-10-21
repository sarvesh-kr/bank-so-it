# Bank SO IT

A small offline MCQ app for **Bank SO IT professional-knowledge practice**. The web app and Android APK use the **shared interface, question-bank source and scoring logic**.

The web version runs entirely on **GitHub Pages**: no server, database service, API key or paid hosting is required. After one successful online visit it works offline and can be installed from a supported browser. All personal data stays in your browser/device.

## Practice features

- **1,081 curated practice MCQs**, each with five choices, a correct answer and an explanation.
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
| Networks & Cybersecurity | 231 |
| DBMS & SQL | 200 |
| Operating Systems | 100 |
| Data Structures & Algorithms | 150 |
| Linux & Shell | 75 |
| Warehousing & Mining | 50 |
| Cloud, AI & ML Basics | 50 |
| Software Engineering & Banking IT | 50 |
| Programming & OOP | 75 |
| Computer Fundamentals & Architecture | 75 |
| Web Technology | 25 |
| **Total** | **1,081** |

Each retained stem, five-option set, key and explanation received a technical review, with sources and independent checks for computed answers. See the [content audit](docs/CONTENT_AUDIT.md), [per-item ledger](docs/question-audit.csv) and [retirement decisions](docs/retired-question-audit.csv). This is practice material rather than an official previous-year paper. No exact exam topic weights are asserted.

**Computer Fundamentals & Architecture now has 75 focused questions**, covering hardware/data/logic, CPU/I/O, memory hierarchy, processes/threads/states, scheduling, paging and deadlock/synchronization. The separate 100-question OS topic remains unchanged; four short architecture cases are independently checked. See the [architecture audit](docs/ARCHITECTURE_AUDIT.md). **Web Technology now has 25 questions** on HTML/forms/CSS, JavaScript/DOM, HTTP/services, browser security, formats and storage; all JSON syntax choices are parsed. See the [web audit](docs/WEB_AUDIT.md). All 981 records outside these two topics are unchanged. Earlier [programming](docs/PROGRAMMING_AUDIT.md), [software/banking/vendor management](docs/SE_BANK_IT_AUDIT.md), [cloud/AI/ML](docs/CLOUD_AI_ML_AUDIT.md), [network supplement](docs/NETWORK_SERVICES_AUDIT.md) and other topic audits document their revisions. Old stock imports cannot overwrite reviewed built-ins or restore retired items; personal edits and historical session snapshots retain their existing handling.

**Android 2.9** bundles the same curated bank and quick revision. It reuses the Android 1.2 release key, so 1.2 installations can update in place. Export a progress backup before installing updates. Installations predating the 1.2 key change still need export, uninstall, reinstall and restore.

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
npx playwright install chromium webkit
npm run test:pages
npm run test:downloads
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. HTTPS or localhost is required for service workers. `test:downloads` checks real APK/question-pack link clicks and navigation downloads in Chromium and WebKit, online and offline, at root and repository paths. `test:pages` starts its own server and tests a repository subpath, offline practice, persistence, backups, separate project storage, the shared Android bridge, and automatic migration from the previous cached release. If using another installed Chromium, set `CHROME_PATH` to its executable.

## Project layout

- `app/src/main/assets/` — shared UI, pure quiz logic, browser persistence, PWA bootstrap, import validation and the generated question bank.
- `app/src/main/java/` — Android WebView shell, private storage and system file picker.
- `content/curated/architecture-r2.txt` — current 75-question integrated architecture/OS-foundations source with four short checked cases.
- `content/curated/web-r2.txt` — current 25-question web source with independently checked JSON syntax.
- `content/curated/programming-r2.txt` — current 75-question OOP/Python/Java/C/C++ source with five executed Python outputs.
- `content/curated/se-bank-r2.txt` — current 50-question software/banking source with five short scenarios and explicit references.
- `content/curated/cloud-ai-ml-r2.txt` — current 50-question conceptual cloud/AI/ML source with explicit IDs and references.
- `content/curated/dw-dm-r2.txt` — current 50-question conceptual warehousing/mining source with explicit IDs and references.
- `content/curated/network-r2.txt` — current 231-question network/cybersecurity source with explicit IDs and per-item references.
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
