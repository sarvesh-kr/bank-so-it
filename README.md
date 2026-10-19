# RRB IT Practice

A small offline MCQ app for **IBPS RRB Officer Scale II — IT**. The web app and Android APK use the **shared interface, question-bank source and scoring logic**.

The web version runs entirely on **GitHub Pages**: no server, database service, API key or paid hosting is required. After one successful online visit it works offline and can be installed from a supported browser. All personal data stays in your browser/device.

## Practice features

- **1,150 practice MCQs**, each with five choices, a correct answer and an explanation.
- Subject-wise or mixed tests; choose 20, 40, 50, all eligible questions, or any custom count.
- Subtopic, difficulty, unseen, wrong-answer and bookmark filters.
- **Focused revision (692 questions)** by default; choose **All questions** to include 458 optional-depth or extra-drill items.
- Practice mode with immediate feedback, or Test mode with answers hidden until submission.
- Optional timer and −0.25 penalty; a focused 40-question / 30-minute preset.
- Question navigator, review flags, bookmarks, saved unfinished sessions and detailed results.
- Add/rename subjects, edit questions, and import/export JSON question packs.
- **Progress backup/restore** transfers edits, bookmarks, history and unfinished sessions between browsers or the APK.
- Installable web app with offline caching, plus a small signed Android APK.

| Subject | Questions |
|---|---:|
| Computer Networks & Cybersecurity | 250 |
| DBMS & SQL | 250 |
| Operating Systems | 100 |
| Data Structures & Algorithms | 250 |
| Linux & Shell Basics | 100 |
| Data Warehousing & Data Mining | 65 |
| Cloud, AI & ML Basics | 65 |
| Software Engineering & Banking IT | 70 |
| **Total** | **1,150** |

These are original practice questions and worked drills informed by published analyses, not official previous-year questions. The preset covers the eight included subjects; the wider IT syllabus includes other areas. See [research and content approach](docs/RESEARCH.md).

See the [content audit](docs/CONTENT_AUDIT.md) for corrections, study priorities, sources and review limits.

**Existing APK:** the signed download still bundles the earlier 950-question bank. Download `bank.json` from the web app and use **My bank → Import pack** in the APK to update its questions. The new study-coverage filter requires a rebuild with the existing release signing key, which is not present in this workspace.

## Deploy on GitHub Pages

The repository is now **[sarvesh-kr/rrb-it-practice](https://github.com/sarvesh-kr/rrb-it-practice)** and its configured site is **https://so.sarvesh.si/**. Deployment uses GitHub Actions.

1. In **Settings → Pages → Build and deployment**, keep **Source → GitHub Actions** selected.
2. Keep the custom domain **so.sarvesh.si** and **Enforce HTTPS** enabled in Pages settings.
3. Push or merge a pull request into `main`. The **Test and deploy GitHub Pages** workflow rebuilds the bank, runs tests, builds `_site/`, and deploys it after checks pass.
4. To redeploy without a code change, select **Actions → Test and deploy GitHub Pages → Run workflow → main**.

Pull requests and manual workflow runs on other branches only run validation. Only `main` can publish. The workflow uses GitHub's built-in token and Pages deployment identity; no deploy key, personal access token, or signing secret is needed. Repository-root web copies are no longer maintained; shared web/APK source lives under `app/src/main/assets/` and `_site/` is generated during the build.

For a custom subdomain, the DNS CNAME should target the owning account's Pages hostname, **sarvesh-kr.github.io**, without a scheme or path. The Pages custom-domain setting is the source of truth for Actions hosting; a repository `CNAME` file is not required. Keep domain/DNS settings under the owner's control. All app URLs are relative, so custom-domain roots and default Pages repository paths both work.

Collaborators can push code or submit pull requests; the owner or an administrator manages Pages, DNS and environment protection settings. See [deployment details](docs/DEPLOYMENT.md) for setup, transfers and troubleshooting.

## Web app use

Open the Pages URL online once. In **My bank**, the app indicates when offline practice is ready. Install via the browser's **Install app** menu, or **Share → Add to Home Screen** on iPhone/iPad. You can also keep using it in an ordinary tab.

The service worker caches the interface, questions and downloadable APK. New versions prepare in the background. Close all app tabs and reopen to activate an update, or use **Apply available update** in My bank after finishing your current session. Your saved progress is separate from the offline cache and is retained across updates.

Progress is local and **does not automatically sync** with GitHub, another browser, another device or the APK. Use **My bank → Back up progress**, then **Restore backup** on the destination. Clearing site data or uninstalling the Android app removes its local records. Browsers can also evict local storage; retain backups for important progress. Question-bank export includes questions only; a progress backup includes your personal records.

Timed sessions use the device clock and continue while you are away. If closed at the deadline, the saved attempt submits when reopened. Completed scores are raw practice scores, not IBPS normalized marks.

## Android APK

Download [RRB-IT-Practice-Lite.apk](downloads/RRB-IT-Practice-Lite.apk), or use **My bank → Download Android APK** on the web app. Open it on an Android phone and allow that file-opening app to install it if Android prompts.

Requires **Android 7.0+ with an updated Android System WebView**. The APK bundles its own offline assets, contains no native architecture-specific libraries and requests no app permissions. The shared browser features use Android's native file picker and local storage inside the APK.

To build locally:

```sh
export JAVA_HOME=/path/to/jdk
export ANDROID_HOME=/path/to/android-sdk
# Install platforms;android-35 and build-tools;35.0.0 with sdkmanager first.
bash tools/build_apk.sh
```

The result is `dist/RRB-IT-Practice-Lite.apk`. A private signing key is generated under ignored `signing/` if none exists. **Keep this key private and retain it for future upgrades.** Keys, passwords, private source archives and local progress are excluded from this repository. Increase the manifest's `versionCode` when distributing upgrades.

An optional **Build Android APK** workflow is available. For stable signed upgrades, configure repository secrets `ANDROID_KEYSTORE_BASE64` (the original JKS encoded as Base64) and `ANDROID_KEYSTORE_PASSWORD`; the key alias is `rrb-it-personal`. Without those secrets, the workflow creates a temporary key and its APK cannot upgrade the existing signed installation. Signing secrets are never needed by the Pages workflow.

## Develop and test

Python 3, Bash and Node.js 22+ are sufficient for the web build. npm dependencies are development/test tools and are not shipped to browsers or bundled in the APK.

```sh
npm ci
python3 tools/build_bank.py
npm test
npm run build:web
npx playwright install chromium
npm run test:pages
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. HTTPS or localhost is required for service workers. `test:pages` starts its own server and tests a repository subpath, offline practice, persistence, backups, separate project storage, and the shared Android bridge. If using another installed Chromium, set `CHROME_PATH` to its executable.

## Project layout

- `app/src/main/assets/` — shared UI, pure quiz logic, browser persistence, PWA bootstrap, import validation and the generated question bank.
- `app/src/main/java/` — Android WebView shell, private storage and system file picker.
- `content/*.txt` — original concept/scenario questions.
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

See [validation notes](docs/VALIDATION.md) for what has and has not been tested.
