"""Enforce the reviewed conceptual warehouse/mining scope and source agreement."""
import collections,json,pathlib
from build_dw_dm import load_dw_dm
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'Warehouse foundations & types':8,'Dimensional models & schemas':9,'ETL, metadata & data quality':6,'OLAP cubes, operations & types':11,'Data mining concepts & techniques':14,'Common tools & roles':2}
def check_dw_dm(bank):
    qs=[q for q in bank['questions'] if q['subject']=='dw_dm'];assert {q['id'] for q in qs}=={f'dw-dm-r2-{i:03}' for i in range(1,51)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert all(f'dw_dm-{i:03}' in bank['retiredQuestionIds'] for i in range(1,66))
    authored={q['id']:q for q in load_dw_dm()}
    for q in qs:
        assert q['kind']=='concept',q['id']
        for field,value in authored[q['id']].items():assert q[field]==value,(q['id'],field)
    report={'questions':50,'coverage':COVERAGE,'numerical_exercises':0,'review':'Every stem, five choices, key and explanation technically reviewed against attached sources; structural checks do not certify conceptual accuracy.'}
    (ROOT/'docs/dw-dm-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
