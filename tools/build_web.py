#!/usr/bin/env python3
"""Produce a self-contained GitHub Pages artifact from the same APK assets."""
from pathlib import Path
import hashlib,json,shutil
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
print(f'Built GitHub Pages artifact: {OUT} ({sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()):,} bytes)')
