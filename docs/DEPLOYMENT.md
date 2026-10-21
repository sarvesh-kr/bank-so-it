# Hosting and maintenance

## GitHub Pages via Actions

Repository: **sarvesh-kr/bank-so-it**. Custom subdomain: **so.sarvesh.si**. The repository owner has configured Pages with `build_type: workflow`, the custom domain, and HTTPS enforcement.

The app is static. The workflow builds a fresh `_site/` artifact from the shared Android/browser assets and publishes only that artifact. The artifact contains the UI, 1016-question bank, versioned service worker, icons, install manifest and signed APK. Root-level generated web copies are no longer needed or checked in.

### Owner setup

1. Under Settings → Pages, select **GitHub Actions** as the source.
2. Set the custom domain to **so.sarvesh.si**. Its DNS CNAME should point to **sarvesh-kr.github.io**. Do not point it to the former owner's hostname or include a URL path. Domain verification can also be managed in the owning account's Pages settings.
3. Enable **Enforce HTTPS** after certificate provisioning. The certificate and HTTPS were already enabled when this flow was configured.
4. If the `github-pages` environment requires review or restricts branches, allow `main` and have the designated reviewer approve deployments. The workflow does not change these protections.

Actions hosting uses the domain configured in Pages settings; no repository `CNAME` file is required. If one is added later, the build preserves it in the artifact, but it does not replace the Pages setting. DNS and repository settings remain administrator tasks; ordinary collaborators do not need admin access to submit code or trigger authorized workflows.

### Publishing changes

Pushes to `main` and manual runs on `main` build, test and deploy. Pull requests and manual runs on other branches only validate. The workflow has `contents: read` for checkout and grants `pages: write` plus `id-token: write` only to the deployment job. It uses the built-in Actions token; no personal token, SSH deploy key or Android signing secret is needed for the web deployment.

After a transfer, update local remotes with `git remote set-url origin https://github.com/sarvesh-kr/bank-so-it.git`. The workflow resolves the repository dynamically and contains no hardcoded owner. Check workflow runs in Actions; the deployment job shows the published URL. A missing Pages configuration fails visibly rather than silently skipping publication. If the job waits for approval, an authorized environment reviewer must approve it. If a Pages API call returns 403, the owner should check workflow permissions and repository policy.

## Storage and offline behavior

A collaborator can fork or copy this repository and enable Pages in their own account. To use a custom domain, set it under that repository's Settings → Pages and follow GitHub's DNS instructions. Enable HTTPS once GitHub provisions the certificate. The app uses relative URLs and needs no hardcoded hostname or repository name. Actions reads the custom domain from Pages settings. An optional repository `CNAME` is included without being cached by the service worker; do not merge another host's `CNAME` into your own deployment. Moving domains creates a separate browser storage origin; export progress on the old site, then restore it on the new one.

- IndexedDB stores one current state record, scoped to the Pages project path. Two apps under different paths on the same `OWNER.github.io` origin use different databases.
- The APK uses its existing native AtomicFile storage instead of IndexedDB.
- Progress backups have a versioned format and are validated before replacing local state. Restoring is explicit; publishing a new site never restores or overwrites personal progress.
- A service worker precaches an explicit asset list. Each project has its own cache prefix. Updates cache the complete release before automatic activation. The browser checks for releases when opened or reloaded. An existing page is not restarted by activation, tab visibility changes or screen navigation. Reloading applies the release from any screen, including a test or editor; saved progress is retained. Offline visits retain the last cached release. Legacy cache namespaces are cleaned only within the same app scope.
- Offline data is prepared only after a successful first online visit. A browser can clear or evict stored data. Export backups when progress is important.
- The app stores no GitHub credentials and cannot commit personal edits to the repository. Export a question pack or update the source if a bank change should be shared with everyone.

## Update questions or code

1. Edit the shared source under `app/src/main/assets/`, original questions under `content/`, or the drill generator under `tools/`.
2. Run `python3 tools/build_bank.py`, `npm test`, `npm run build:web` and `npm run test:pages`.
3. Commit and push to `main`.
4. Actions publishes `_site/` after tests pass, preserving the configured custom domain.
5. For an APK update, increment Android `versionCode`, rebuild using the original private signing key, and replace `downloads/Bank-SO-IT.apk` in the repository.

The release check deliberately requires the published APK to match shared assets; rebuild and replace it whenever shared UI or bank assets change. APK users can import new question packs without rebuilding the APK.

## Android signing

The original personal signing key remains outside version control. To enable repeatable signed CI builds, its owner can set `ANDROID_KEYSTORE_BASE64` and `ANDROID_KEYSTORE_PASSWORD` as repository Actions secrets. The Pages deployment does not receive them. Never commit a key, its password, or the earlier private source archive that includes signing material.
