"""Load the explicitly curated, stable-ID network replacement without changing other subjects."""
import json,random,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]

def load_network():
    catalog=json.loads((ROOT/'content/curated/network-references.json').read_text())
    rows=[];rng=random.Random(20261020)
    numerical={65:'usable-hosts',66:'usable-hosts',67:'prefix-mask',68:'prefix-mask',69:'network-address',70:'network-address',71:'broadcast-address',72:'host-range',73:'subnet-count',74:'minimum-host-capacity'}
    for line in (ROOT/'content/curated/network-r2.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        fields=line.split('¦');assert len(fields)==11,line
        id,topic,difficulty,stem,correct,*tail=fields
        wrong,explanation,keys=tail[:4],tail[4],tail[5].split(';')
        options=[correct]+wrong;assert len(set(options))==5,stem
        rng.shuffle(options)
        rows.append({'id':'network-r2-'+id,'subject':'network','topic':topic,'difficulty':difficulty,'question':stem,
            'options':options,'answer':options.index(correct),'explanation':explanation,
            'kind':'worked-drill' if int(id) in numerical else 'concept','family':numerical.get(int(id),topic),
            'references':[{'title':catalog[key][0],'url':catalog[key][1]} for key in keys]})
    assert len(rows)==229
    assert len({r['id'] for r in rows})==len({r['question'] for r in rows})==229
    return rows
