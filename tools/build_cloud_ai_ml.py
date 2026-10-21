"""Load the focused cloud/AI/ML revision with stable IDs and independent choice RNG."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_cloud_ai_ml():
    refs=json.loads((ROOT/'content/curated/cloud-ai-ml-references.json').read_text());rows=[];rng=random.Random(20261023)
    for line in (ROOT/'content/curated/cloud-ai-ml-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦');assert len(p)==11,line
        id,topic,difficulty,stem,correct,*tail=p;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'cloud-ai-ml-r2-'+id,'subject':'cloud_ai_ml','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':'concept','family':topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==50
    return rows
