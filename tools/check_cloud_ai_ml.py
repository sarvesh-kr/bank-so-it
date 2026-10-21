"""Enforce the reviewed cloud/AI/ML scope and canonical-source agreement."""
import collections,json,pathlib
from build_cloud_ai_ml import load_cloud_ai_ml
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'Cloud foundations & models':10,'Virtualization, storage & operations':10,'Cloud security & banking controls':5,'AI & learning foundations':8,'ML algorithms & evaluation':12,'AI applications & responsible use':5}
def check_cloud_ai_ml(bank):
    qs=[q for q in bank['questions'] if q['subject']=='cloud_ai_ml'];assert {q['id'] for q in qs}=={f'cloud-ai-ml-r2-{i:03}' for i in range(1,51)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'cloud_ai_ml-{i:03}' in bank['retiredQuestionIds'] for i in range(1,66))
    authored={q['id']:q for q in load_cloud_ai_ml()}
    for q in qs:
        assert q['kind']=='concept',q['id']
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
    (ROOT/'docs/cloud-ai-ml-quality-summary.json').write_text(json.dumps({'questions':50,'cloud':25,'ai_ml':25,'coverage':COVERAGE,'numerical_exercises':0,'review':'Every stem, five options, key and explanation reviewed against attached references; structural checks alone do not certify conceptual accuracy.'},indent=2)+'\n')
