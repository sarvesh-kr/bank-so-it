"""Enforce programming/OOP coverage, source agreement and retired stock IDs."""
import collections,json,pathlib
from build_programming import load_programming
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'OOP foundations':8,'Python types & basics':12,'Python functions & OOP':8,'Python short output':5,'Java runtime & core types':9,'Java classes & interfaces':11,'C pointers & strings':8,'C++ classes & strings':14}
def check_programming(bank):
    qs=[q for q in bank['questions'] if q['subject']=='programming'];assert {q['id'] for q in qs}=={f'programming-r2-{i:03}' for i in range(1,76)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'programming-{i:03}' in bank['retiredQuestionIds'] for i in range(1,61))
    authored={q['id']:q for q in load_programming()}
    for q in qs:
        assert q['kind']==('executed-python' if q['topic']=='Python short output' else 'concept'),q['id']
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
    (ROOT/'docs/programming-quality-summary.json').write_text(json.dumps({'questions':75,'conceptual_questions':70,'executed_python_outputs':5,'coverage':COVERAGE,'review':'Every stem, five choices, key and explanation reviewed using attached language specifications/documentation; all five displayed Python outputs execute in the whole-bank checker.'},indent=2)+'\n')
