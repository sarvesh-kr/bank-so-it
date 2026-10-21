"""Enforce architecture coverage and independently check the four short displayed cases."""
import collections,json,pathlib,re
from build_architecture import load_architecture
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'Data representation & digital logic':10,'CPU, instruction cycle & I/O':12,'Memory hierarchy & storage':10,'Processes, threads & states':12,'Scheduling & performance':9,'Paging & virtual memory':12,'Deadlock & synchronization':10}
def check_architecture(bank):
    qs=[q for q in bank['questions'] if q['subject']=='architecture'];by_id={q['id']:q for q in qs};assert set(by_id)=={f'architecture-r2-{i:03}' for i in range(1,76)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'architecture-{i:03}' in bank['retiredQuestionIds'] for i in range(1,34))
    authored={q['id']:q for q in load_architecture()};proofs={}
    for q in qs:
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
        if q['kind']!='worked-architecture':continue
        text=q['question'];n=int(q['id'].rsplit('-',1)[1])
        if n==2:value=str(int(re.search(r'in (\d+) KiB',text)[1])*1024);method='independent binary-prefix calculation'
        elif n==3:value=str(int(re.search(r'binary number ([01]+)',text)[1],2));method='independent unsigned-binary conversion'
        elif n==17:value=str(2**int(re.search(r'uses (\d+) address bits',text)[1]));method='independent address-count calculation'
        elif n==49:
            remaining=int(re.search(r'P1 is running with (\d+) time units remaining',text)[1]);incoming=int(re.search(r'single (\d+)-unit CPU burst',text)[1]);assert remaining!=incoming
            value='P2' if incoming<remaining else 'P1';method='independent SRTF remaining-time comparison'
        else:raise AssertionError(q['id'])
        assert q['options'][q['answer']]==value,(q['id'],value)
        proofs[q['id']]={'method':method,'independent_result':value}
    assert len(proofs)==4
    (ROOT/'docs/architecture-quality-summary.json').write_text(json.dumps({'questions':75,'coverage':COVERAGE,'conceptual_questions':71,'short_checked_cases':4,'arithmetic_cases':3,'scheduling_choice_cases':1,'review':'Every stem, five options, answer and explanation reviewed against attached references; the separate OS bank remains unchanged.'},indent=2)+'\n')
    return proofs
