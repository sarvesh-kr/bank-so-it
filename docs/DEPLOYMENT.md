# Hosting and maintenance

## GitHub Pages

This is a static client-side app. The generated web files are checked in at the repository root for **Deploy from a branch → main → / (root)** hosting. Run `npm run publish:pages` after editing the shared assets or rebuilding the bank, and commit the refreshed root files. The build copies only its public-file allowlist and preserves source files and any custom-domain `CNAME`. Branch hosting also makes the public source tree available over HTTP; no signing keys, credentials or personal backups belong in this public repository.

Alternatively, set the repository's Pages source to **GitHub Actions** to publish only `_site/`. The workflow detects the configured source: it validates branch-hosted files in either mode, and runs its deployment job only for the Actions source. It has `contents: read` and `pages: read` for building and grants `pages: write` plus `id-token: write` only to the deployment job. With Actions hosting, pushes to `main` deploy after checks pass; pull requests run checks without deployment. Branch publishing is independent of the validation workflow. Repository creation, pushing workflow files and enabling Pages require the corresponding GitHub integration permissions, even if login succeeds.

To enable Pages using an already authorized GitHub CLI:

```sh
gh api --method POST repos/OWNER/REPOSITORY/pages -f build_type=workflow
```

If Pages is already configured, change its source in Settings → Pages instead. GitHub may take a few minutes to publish the first deployment.

## Storage and offline behavior

A collaborator can fork or copy this repository and enable Pages in their own account. To use a custom domain, set it under that repository's Settings → Pages and follow GitHub's DNS instructions. Enable HTTPS once GitHub provisions the certificate. The app uses relative URLs and needs no hardcoded hostname or repository name. The build preserves and includes that repository's `CNAME` without caching it in the service worker. Do not merge another host's `CNAME` into your own deployment. Moving domains creates a separate browser storage origin; export progress on the old site, then restore it on the new one.

- IndexedDB stores one current state record, scoped to the Pages project path. Two apps under different paths on the same `OWNER.github.io` origin use different databases.
- The APK uses its existing native AtomicFile storage instead of IndexedDB.
- Progress backups have a versioned format and are validated before replacing local state. Restoring is explicit; publishing a new site never restores or overwrites personal progress.
- A service worker precaches an explicit asset list. Each project has its own cache prefix. Updates install into a new versioned cache and wait for activation; they do not mix changed question files with an old UI during an open session.
- Offline data is prepared only after a successful first online visit. A browser can clear or evict stored data. Export backups when progress is important.
- The app stores no GitHub credentials and cannot commit personal edits to the repository. Export a question pack or update the source if a bank change should be shared with everyone.

## Update questions or code

1. Edit the shared source under `app/src/main/assets/`, original questions under `content/`, or the drill generator under `tools/`.
2. Run `python3 tools/build_bank.py`, `npm test`, `npm run publish:pages` and `npm run test:pages`.
3. Commit and push to `main`.
4. Branch hosting publishes the root files when pushed. Actions hosting publishes `_site/` after tests pass.
5. For an APK update, increment Android `versionCode`, rebuild using the original private signing key, and replace `downloads/RRB-IT-Practice-Lite.apk` in the repository.

No APK rebuild is necessary for a browser-only update. APK users can import new question packs without rebuilding the APK.

## Android signing

The original personal signing key remains outside version control. To enable repeatable signed CI builds, its owner can set `ANDROID_KEYSTORE_BASE64` and `ANDROID_KEYSTORE_PASSWORD` as repository Actions secrets. The Pages deployment does not receive them. Never commit a key, its password, or the earlier private source archive that includes signing material.
