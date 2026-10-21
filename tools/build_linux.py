"""Load the Linux/Bash fundamentals revision without changing other subjects' RNG."""
import json,pathlib,random
from linux_cases import fixtures,render
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_linux():
    refs=json.loads((ROOT/'content/curated/linux-references.json').read_text());cases=fixtures();rows=[];rng=random.Random(20261021)
    for line in (ROOT/'content/curated/linux-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦');assert len(p)==11,line
        id,topic,difficulty,stem,correct,*tail=p;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';');number=int(id)
        options=[x.replace('↵','\n') for x in [correct]+wrong];correct=options[0];assert len(set(options))==5,stem;rng.shuffle(options)
        checked=str(number) in cases
        if checked:stem=render(number,stem)
        rows.append({'id':'linux-r2-'+id,'subject':'linux','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':'checked-linux' if checked else 'concept','family':topic+'-'+id if checked else topic,
            'references':[{'title':refs[key][0],'url':refs[key][1]} for key in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==75
    return rows
