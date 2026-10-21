"""Load the focused web-technology revision using independent, stable option ordering."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_web_topic():
    refs=json.loads((ROOT/'content/curated/web-references.json').read_text());rows=[];rng=random.Random(20261027)
    for line in (ROOT/'content/curated/web-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦');assert len(p)==11,line
        id,topic,difficulty,stem,correct,*tail=p;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'web-r2-'+id,'subject':'web','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':'checked-json' if id=='023' else 'concept','family':topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==25
    return rows
