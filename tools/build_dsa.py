"""Load the curated DSA revision with stable IDs and independent choice shuffling."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parents[1]
WORKED={11,12,24,36,45,46,55,56,67,68,91,92,93,94,106,107,108,119,120,129,130,137,138,149,150}

def load_dsa():
    refs=json.loads((ROOT/'content/curated/dsa-references.json').read_text());rows=[];rng=random.Random(20261021)
    for line in (ROOT/'content/curated/dsa-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        fields=line.split('¦');assert len(fields)==11,line
        id,topic,difficulty,stem,correct,*tail=fields;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'dsa-r2-'+id,'subject':'dsa','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,
            'kind':'worked-dsa' if int(id) in WORKED else 'concept','family':topic+'-'+id if int(id) in WORKED else topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==150
    return rows
