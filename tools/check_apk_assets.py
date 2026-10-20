#!/usr/bin/env python3
"""Reject stale Android downloads; signature verification is a release-build step."""
import hashlib,json,pathlib,xml.etree.ElementTree as ET,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
assets=ROOT/'app/src/main/assets'
apk=ROOT/'downloads/Bank-SO-IT.apk'
release=json.loads((ROOT/'docs/android-release.json').read_text())
assert hashlib.sha256(apk.read_bytes()).hexdigest()==release['sha256'],'APK checksum does not match release record'
expected={f'assets/{p.name}':p for p in assets.iterdir() if p.is_file()}
with zipfile.ZipFile(apk) as archive:
    actual={n for n in archive.namelist() if n.startswith('assets/') and not n.endswith('/')}
    assert actual==set(expected),'APK has missing or obsolete shared assets'
    for name,path in expected.items():assert archive.read(name)==path.read_bytes(),'Stale APK asset: '+name
    bank=json.loads(archive.read('assets/bank.json'))
assert len(bank['questions'])==release['questions']
assert len(bank['subjects'])==release['subjects']
manifest=ET.parse(ROOT/'app/src/main/AndroidManifest.xml').getroot()
namespace='{http://schemas.android.com/apk/res/android}'
assert manifest.attrib[namespace+'versionName']==release['version']
assert int(manifest.attrib[namespace+'versionCode'])==release['versionCode']
print(json.dumps({'APK_assets_match':True,'questions':release['questions'],'version':release['version'],'bytes':apk.stat().st_size}))
