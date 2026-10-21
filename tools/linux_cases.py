"""Render reviewed Bash cases; execute each in a fresh isolated working directory."""
import json,pathlib,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def fixtures():return json.loads((ROOT/'content/curated/linux-r2-cases.json').read_text())['cases']
def render(number,intro):return intro+'\n'+fixtures()[str(number)]['script']
def execute(number):
    script=fixtures()[str(number)]['script']
    with tempfile.TemporaryDirectory(prefix='bank-so-it-shell-') as directory:
        result=subprocess.run(['/bin/bash','--noprofile','--norc','-c',script],cwd=directory,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'},input='',capture_output=True,text=True,timeout=5)
    assert result.returncode==0,(number,result.returncode,result.stderr)
    assert not result.stderr,(number,result.stderr)
    return result.stdout.rstrip('\n') or '(empty output)'
