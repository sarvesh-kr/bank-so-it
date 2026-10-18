# Hosting and maintenance

## GitHub Pages

This is a static client-side app. `_site/` is the only directory published. It contains the shared browser assets, the 950-question bank, a generated versioned service worker, the install manifest/icons and the signed APK. It contains no signing key, private backup, server credentials or build/source archive.

Set the repository's Pages source to **GitHub Actions**. The Pages workflow has `contents: read` for building and grants `pages: write` plus `id-token: write` only to the deployment job. Pushes to `main` deploy after checks pass; pull requests run checks without deployment. Repository creation, pushing workflow files and enabling Pages require the corresponding GitHub integration permissions, even if login succeeds.

To enable Pages using an already authorized GitHub CLI:

```sh
gh api --method POST repos/OWNER/REPOSITORY/pages -f build_type=workflow
```

If Pages is already configured, change its source in Settings → Pages instead. GitHub may take a few minutes to publish the first deployment.

## Storage and offline behavior

- IndexedDB stores one current state record, scoped to the Pages project path. Two apps under different paths on the same `OWNER.github.io` origin use different databases.
- The APK uses its existing native AtomicFile storage instead of IndexedDB.
- Progress backups have a versioned format and are validated before replacing local state. Restoring is explicit; publishing a new site never restores or overwrites personal progress.
- A service worker precaches an explicit asset list. Each project has its own cache prefix. Updates install into a new versioned cache and wait for activation; they do not mix changed question files with an old UI during an open session.
- Offline data is prepared only after a successful first online visit. A browser can clear or evict stored data. Export backups when progress is important.
- The app stores no GitHub credentials and cannot commit personal edits to the repository. Export a question pack or update the source if a bank change should be shared with everyone.

## Update questions or code

1. Edit the shared source under `app/src/main/assets/`, original questions under `content/`, or the drill generator under `tools/`.
2. Run `python3 tools/build_bank.py`, `npm test`, `npm run build:web` and `npm run test:pages`.
3. Commit and push to `main`.
4. The workflow publishes the web update after tests pass.
5. For an APK update, increment Android `versionCode`, rebuild using the original private signing key, and replace `downloads/RRB-IT-Practice-Lite.apk` in the repository.

No APK rebuild is necessary for a browser-only update. APK users can import new question packs without rebuilding the APK.

## Android signing

The original personal signing key remains outside version control. To enable repeatable signed CI builds, its owner can set `ANDROID_KEYSTORE_BASE64` and `ANDROID_KEYSTORE_PASSWORD` as repository Actions secrets. The Pages deployment does not receive them. Never commit a key, its password, or the earlier private source archive that includes signing material.
