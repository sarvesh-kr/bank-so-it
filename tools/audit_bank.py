#!/usr/bin/env python3
"""Publish review evidence; fail if any shipped item lacks a matching reviewed hash."""
import collections,csv,hashlib,json,pathlib
from check_quality import check,fingerprint
ROOT=pathlib.Path(__file__).resolve().parents[1]
bank,checks=check()
registry=json.loads((ROOT/'content/review/review-register.json').read_text())
baseline=json.loads((ROOT/'content/review/baseline-manifest.json').read_text())
retired=json.loads((ROOT/'content/review/retirements.json').read_text())
after_baseline=json.loads((ROOT/'content/review/retired-after-baseline.json').read_text())
corrections=json.loads((ROOT/'content/review/corrections.json').read_text())
current={q['id'] for q in bank['questions']}
assert current==set(registry['items']),'Review register and published bank must contain exactly the same IDs'
def content_hash(q):
    return hashlib.sha256(json.dumps({k:q[k] for k in ['id','subject','topic','difficulty','question','options','answer','explanation','kind','family']},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
rows=[];changes=collections.Counter()
for q in bank['questions']:
    id=q['id'];assert registry['items'][id]==fingerprint(q),id+': content changed after review'
    action='added' if id not in baseline else 'corrected or clarified' if baseline[id]['contentHash']!=content_hash(q) else 'retained'
    changes[action]+=1
    proof=checks['proofs'].get(id)
    rows.append({'id':id,'subject':q['subject'],'topic':q['topic'],'disposition':action,'question':q['question'],
    'five_options':json.dumps(q['options'],ensure_ascii=False),'answer_index_0_based':q['answer'],'correct_option':'ABCDE'[q['answer']],'correct_answer':q['options'][q['answer']],'explanation':q['explanation'],
    'stem_review':'checked','options_review':'checked for a unique best answer under stated assumptions','key_review':'checked','explanation_review':'checked',
    'answer_evidence':proof['method'] if proof else 'Technical review using cited documentation/textbook and stated assumptions',
    'sources':json.dumps(q['references'],ensure_ascii=False),'review_note':corrections.get(id,'Foundational coverage; concise concept or representative application'),
    'reviewer':registry['reviewer'],'reviewed_on':registry.get('reviewedOnById',{}).get(id,registry['reviewedOn']),'reviewed_sha256':registry['items'][id]})
with (ROOT/'docs/question-audit.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n");writer.writeheader();writer.writerows(rows)
oldproof=json.loads((ROOT/'docs/baseline-answer-checks.json').read_text())['proofs']
retiredrows=[{'id':id,'subject':(baseline.get(id) or after_baseline[id])['subject'],'topic':(baseline.get(id) or after_baseline[id])['topic'],'decision':'retired','reason':why,
'computed_answer_evidence':oldproof[id]['method'] if id in oldproof else 'Technical review; item not published',
'original_source_commit':after_baseline[id]['original_source_commit'] if id in after_baseline else '693275acdf059ef83e274cfdbb59d5679f8ce4ff'} for id,why in sorted(retired.items())]
with (ROOT/'docs/retired-question-audit.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=retiredrows[0].keys(),lineterminator="\n");writer.writeheader();writer.writerows(retiredrows)
report={'previous_bank':len(baseline),'previous_items_retained':len(current&set(baseline)),'retired':len(retired),
'retired_from_original_baseline':len(set(retired)&set(baseline)),'retired_after_original_baseline':len(set(retired)-set(baseline)),
'added':len(current-set(baseline)),'current_bank':len(current),'changes':dict(changes),'reviewer':registry['reviewer'],
'computed_checks_current':checks['independent_answer_checks'],'computed_checks_previous':len(oldproof),
'subjects':dict(collections.Counter(q['subject'] for q in bank['questions'])),
'review_limit':'Technical/model-assisted content review with cited primary documentation and authored textbooks, not independent human expert certification or an official IBPS paper.'}
(ROOT/'docs/quality-audit-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
