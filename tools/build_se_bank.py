"""Load the focused software-engineering/banking-IT revision with independent choice RNG."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_se_bank():
    refs=json.loads((ROOT/'content/curated/se-bank-references.json').read_text());rows=[];rng=random.Random(20261024)
    for line in (ROOT/'content/curated/se-bank-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        fields=line.split('¦');assert len(fields)==11,line
        id,topic,difficulty,stem,correct,*tail=fields;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'se-bank-r2-'+id,'subject':'se_bank_it','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':'scenario' if int(id)>=46 else 'concept','family':topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==50
    return rows
