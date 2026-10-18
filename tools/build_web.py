#!/usr/bin/env python3
"""Produce a self-contained GitHub Pages artifact from the same APK assets."""
from pathlib import Path
import argparse,hashlib,json,shutil
parser=argparse.ArgumentParser(description=__doc__)
mode=parser.add_mutually_exclusive_group()
mode.add_argument('--publish-root',action='store_true',help='Refresh the checked-in files for main / (root) Pages hosting.')
mode.add_argument('--check-root',action='store_true',help='Fail when the checked-in Pages files need refreshing.')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'app/src/main/assets'
OUT=ROOT/'_site'
OUT.mkdir(exist_ok=True)
# Only explicitly listed public files enter the site; signing keys and source archives never do.
files=['index.html','style.css','core.js','app.js','storage.js','backup.js','platform.js','bank.json','manifest.webmanifest','icon-192.png','icon-512.png']
for name in files:shutil.copyfile(ASSETS/name,OUT/name)
(OUT/'downloads').mkdir(exist_ok=True)
release=ROOT/'downloads/RRB-IT-Practice-Lite.apk'
if not release.exists():raise SystemExit('Missing downloads/RRB-IT-Practice-Lite.apk; build and copy the signed APK first.')
shutil.copyfile(release,OUT/'downloads/RRB-IT-Practice-Lite.apk')
files.append('downloads/RRB-IT-Practice-Lite.apk')
(OUT/'.nojekyll').write_text('')
(OUT/'scope.json').write_text('{"app":"rrb-it-practice"}')
files.append('scope.json')
digest=hashlib.sha256(b''.join((OUT/f).read_bytes() for f in sorted(files))).hexdigest()[:16]
template=(ROOT/'web/sw.template.js').read_text()
(OUT/'sw.js').write_text(template.replace('__BUILD_HASH__',digest).replace('__PRECACHE__',json.dumps(files)))
(OUT/'build.json').write_text(json.dumps({'version':digest,'questions':len(json.loads((OUT/'bank.json').read_text())['questions'])}))
public_files=files+['.nojekyll','sw.js','build.json']
# Only copy/check public build outputs. Preserve collaborators' source files and CNAME.
if args.publish_root:
 for name in public_files:
  (ROOT/name).parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(OUT/name,ROOT/name)
 print('Updated main-branch Pages files at repository root.')
if args.check_root:
 stale=[name for name in public_files if not (ROOT/name).exists() or (ROOT/name).read_bytes()!=(OUT/name).read_bytes()]
 if stale:raise SystemExit('Run npm run publish:pages and commit the refreshed files: '+', '.join(stale))
# A custom domain configured in GitHub Settings remains specific to this repository.
if (ROOT/'CNAME').exists():shutil.copyfile(ROOT/'CNAME',OUT/'CNAME')
elif (OUT/'CNAME').exists():(OUT/'CNAME').unlink()
print(f'Built GitHub Pages artifact: {OUT} ({sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()):,} bytes)')
