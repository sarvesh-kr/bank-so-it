"""Enforce software/banking scope, five short scenarios and canonical-source agreement."""
import collections,json,pathlib
from build_se_bank import load_se_bank
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'SDLC & requirements':9,'Design, delivery & maintenance':6,'Testing foundations & types':12,'Testing techniques & principles':5,'IT service management & resilience':5,'Vendor management & outsourcing':4,'Banking systems & payments':4,'Banking IT scenarios':5}
def check_se_bank(bank):
    qs=[q for q in bank['questions'] if q['subject']=='se_bank_it'];assert {q['id'] for q in qs}=={f'se-bank-r2-{i:03}' for i in range(1,51)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'se_bank_it-{i:03}' in bank['retiredQuestionIds'] for i in range(1,77))
    authored={q['id']:q for q in load_se_bank()}
    for q in qs:
        assert q['kind']==('scenario' if q['topic']=='Banking IT scenarios' else 'concept'),q['id']
        if q['kind']=='scenario':assert q['question'].startswith('Scenario:') and len(q['question'].split())<=65,q['id']
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
    (ROOT/'docs/se-bank-quality-summary.json').write_text(json.dumps({'questions':50,'conceptual_questions':45,'banking_scenarios':5,'coverage':COVERAGE,'numerical_exercises':0,'review':'Every stem, five options, answer and explanation reviewed using attached technical references; structural checks alone do not certify conceptual correctness or exam frequency.'},indent=2)+'\n')
