"""Load the user-scoped DBMS revision; execute worked cases in a separate checker."""
import json,pathlib,random
from dbms_cases import fixtures,render
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load_dbms():
    refs=json.loads((ROOT/'content/curated/dbms-references.json').read_text());cases=fixtures()['cases'];rng=random.Random(20261021);rows=[]
    worked={62,68,69,70,71,98,194,198,199,200}
    for line in (ROOT/'content/curated/dbms-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦');assert len(p)==11,line
        id,topic,difficulty,stem,correct,*tail=p;wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';');number=int(id)
        if id=='072':keys.append('advanced-normal')
        if topic=='ER modelling & Chen notation' and number in [13,14,15,16,17,18]:keys.append('chen')
        kind='concept'
        if str(number) in cases:kind='checked-sql' if cases[str(number)]['type']=='sql' else 'checked-algebra';stem=render(number,stem)
        elif number in worked:kind='worked-dbms'
        options=[correct]+wrong;assert len(set(options))==5,stem;rng.shuffle(options)
        rows.append({'id':'dbms-r2-'+id,'subject':'dbms','topic':topic,'difficulty':difficulty,'question':stem,'options':options,'answer':options.index(correct),'explanation':explanation,'kind':kind,'family':topic+'-'+id if kind!='concept' else topic,'references':[{'title':refs[k][0],'url':refs[k][1]} for k in keys]})
    assert len(rows)==len({q['id'] for q in rows})==len({q['question'] for q in rows})==200
    return rows
