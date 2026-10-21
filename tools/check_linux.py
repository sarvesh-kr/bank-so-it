"""Execute all displayed Bash cases and reject unreviewed fixture/stem drift."""
import collections,json,pathlib
from linux_cases import fixtures,render,execute
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'Linux foundations & navigation':10,'Files, text & search':16,'Users, groups & permissions':14,'Processes, storage & services':10,'Shell operators & expansion':10,'Bash programming basics':15}
CASES={24,25,26,37,38,39,55,56,58,63,66,68,69,70,71,72,75}
def check_linux(bank):
    qs=[q for q in bank['questions'] if q['subject']=='linux'];assert {q['id'] for q in qs}=={f'linux-r2-{i:03}' for i in range(1,76)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    assert set(map(int,fixtures()))==CASES
    authored={int(p[0]):p[3] for line in (ROOT/'content/curated/linux-r2.txt').read_text().splitlines() if line and not line.startswith('#') for p in [line.split('¦')]}
    proofs={}
    for q in qs:
        number=int(q['id'].rsplit('-',1)[1]);assert q['kind']==('checked-linux' if number in CASES else 'concept')
        if number not in CASES:continue
        assert q['question']==render(number,authored[number]),q['id']
        expected=execute(number);assert expected==q['options'][q['answer']],(q['id'],expected,q['options'][q['answer']])
        proofs[q['id']]={'method':'Bash/GNU execution in an isolated temporary directory','independent_result':expected,'script':fixtures()[str(number)]['script']}
    assert len(proofs)==17
    report={'questions':75,'coverage':COVERAGE,'concepts_and_applications':58,'executed_examples':17,'permission_mode_examples':3,'dialect':'Bash, GNU/Linux tools, C locale, default shell options; permission cases assume no default ACL','proofs':proofs}
    (ROOT/'docs/linux-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return proofs
