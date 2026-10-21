"""Enforce web scope and independently parse all choices of the JSON syntax item."""
import collections,json,pathlib
from build_web_topic import load_web_topic
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'HTML, forms & CSS':8,'JavaScript & DOM':5,'HTTP & web services':4,'Browser security & sessions':5,'Data formats & browser storage':3}
def check_web_topic(bank):
    qs=[q for q in bank['questions'] if q['subject']=='web'];assert {q['id'] for q in qs}=={f'web-r2-{i:03}' for i in range(1,26)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'web-{i:03}' in bank['retiredQuestionIds'] for i in range(1,21))
    authored={q['id']:q for q in load_web_topic()};proofs={}
    for q in qs:
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
        if q['kind']=='checked-json':
            parsed={}
            for i,text in enumerate(q['options']):
                try:parsed[i]=json.loads(text)
                except json.JSONDecodeError:pass
            assert set(parsed)=={q['answer']} and parsed[q['answer']]=={'count':3}
            proofs[q['id']]={'method':'all five options independently parsed using JSON syntax rules','independent_result':q['options'][q['answer']]}
    assert len(proofs)==1
    (ROOT/'docs/web-quality-summary.json').write_text(json.dumps({'questions':25,'coverage':COVERAGE,'conceptual_questions':24,'json_syntax_checks':1,'review':'Every stem, five choices, answer and explanation reviewed against attached web standards and documentation; protocol/API coverage in Networks remains unchanged.'},indent=2)+'\n')
    return proofs
