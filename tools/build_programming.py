"""Load the focused programming/OOP revision with stable IDs and independent choices."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_programming():
    refs=json.loads((ROOT/'content/curated/programming-references.json').read_text());rows=[];rng=random.Random(20261025)
    for line in (ROOT/'content/curated/programming-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        fields=line.split('¦');assert len(fields)==11,line
        id,topic,difficulty,stem,correct,*tail=fields;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        stem=stem.replace('\\n','\n');options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'programming-r2-'+id,'subject':'programming','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':'executed-python' if topic=='Python short output' else 'concept','family':topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==75
    return rows
