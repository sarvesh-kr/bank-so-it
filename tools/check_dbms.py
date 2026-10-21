"""Execute query/algebra fixtures and verify normalization, tree and RAID examples."""
import itertools,collections,json,pathlib,re
from dbms_cases import fixtures,result,render
ROOT=pathlib.Path(__file__).resolve().parents[1]
def closure(attrs,fds):
    out=set(attrs)
    while True:
        previous=set(out)
        for left,right in fds:
            if set(left)<=out:out.update(right)
        if out==previous:return out
def normal_form(attrs,fds):
    attrs=set(attrs);subsets=[set(v) for n in range(len(attrs)+1) for v in itertools.combinations(sorted(attrs),n)]
    keys=[x for x in subsets if closure(x,fds)>=attrs and not any(closure(x-{a},fds)>=attrs for a in x)]
    prime=set().union(*keys);nonprime=attrs-prime
    second=all(not ((closure(part,fds)-part)&nonprime) for key in keys for part in subsets if part<key)
    third=all(not ((closure(x,fds)-x)-prime) for x in subsets if closure(x,fds)!=attrs)
    bcnf=all(not (closure(x,fds)-x) for x in subsets if closure(x,fds)!=attrs)
    return keys,('BCNF' if bcnf else '3NF' if third else '2NF' if second else '1NF')
def worked(number,q):
    if number==62:return '{'+', '.join(sorted(closure('A',[('A','B'),('B','C')])))+'}'
    if number==68:return normal_form(['S','C','N','G'],[('S','N'),('SC','G')])[1]
    if number==69:return normal_form(['E','D','N'],[('E','D'),('D','N')])[1]
    if number==70:
        keys,nf=normal_form('ABC',[('AB','C'),('C','B')]);assert {frozenset(k) for k in keys}=={frozenset('AB'),frozenset('AC')}
        return nf+' but not BCNF'
    if number==71:
        r1,r2=set('AB'),set('AC');common=r1&r2;c=closure(common,[('A','B')]);assert r1<=c or r2<=c
        return 'Yes, because common attribute A determines R1'
    if number==98:
        m=int(re.search(r'order (\d+)',q['question']).group(1));return str(m-1)
    spec={194:('mirror',2,2,'two'),198:('single-parity',4,2,'four'),199:('dual-parity',6,2,'six'),200:('paired-mirrors',4,2,'four')}
    mode,n,size,word=spec[number];assert word in q['question'] and str(size)+' TB' in q['question']
    blocks=[size]*n
    usable=blocks[0] if mode=='mirror' else sum(blocks[1:]) if mode=='single-parity' else sum(blocks[2:]) if mode=='dual-parity' else sum(min(blocks[i:i+2]) for i in range(0,n,2))
    return str(usable)+' TB'
def check_dbms(bank):
    qs=[q for q in bank['questions'] if q['subject']=='dbms'];by_id={q['id']:q for q in qs};assert set(by_id)=={f'dbms-r2-{i:03}' for i in range(1,201)}
    expected={'DBMS foundations & models':12,'ER modelling & Chen notation':18,'Relations, keys & constraints':16,'Naming & SQL data types':10,'Normalization & dependencies':16,'Relational algebra':14,'Indexes & B/B+ trees':15,'SQL command families':18,'SQL clauses & query logic':17,'SQL output & command practice':32,'Transactions & recovery':20,'Backup & RAID':12}
    assert dict(collections.Counter(q['topic'] for q in qs))==expected
    proofs={};cases=fixtures()['cases']
    authored={int(p[0]):p[3] for line in (ROOT/'content/curated/dbms-r2.txt').read_text().splitlines() if line and not line.startswith('#') for p in [line.split('¦')]}
    for q in qs:
        n=int(q['id'].rsplit('-',1)[1]);answer=q['options'][q['answer']];value=None
        if q['kind'] in ['checked-sql','checked-algebra']:
            value=result(n)
            # Verify that the rendered input still matches the fixture actually executed.
            intro=authored[n]
            assert q['question']==render(n,intro),q['id']
        elif q['kind']=='worked-dbms':value=worked(n,q)
        if value is not None:
            assert answer==value,(q['id'],answer,value);proofs[q['id']]={'method':q['kind'],'independent_result':value}
    assert sum(q['kind']=='checked-sql' for q in qs)==32
    assert sum(q['kind']=='checked-algebra' for q in qs)==6
    assert len(proofs)==48
    report={'questions':200,'coverage':expected,'executed_SQL':32,'evaluated_algebra':6,'other_worked_checks':10,'worked_checks_total':len(proofs),'proofs':proofs}
    (ROOT/'docs/dbms-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return proofs
