#!/usr/bin/env python3
"""Write per-item review evidence; never present structural checks as fact-checking.

Optional --attachment accepts the safely extracted JSON array, not executable HTML.
The input-source comparison is separate from the reviewed production question bank.
"""
import argparse, collections, csv, hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--attachment', type=pathlib.Path)
args = parser.parse_args()
bank = json.loads((ROOT/'app/src/main/assets/bank.json').read_text())
questions = bank['questions']
docs = ROOT/'docs'

def write_csv(name, rows):
    with (docs/name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

methods = {
    'concept': 'Concept and selected answer reviewed; structural checks are not an independent expert certification',
    'worked-drill': 'Formula/trace generator reviewed and regenerated with stated assumptions',
    'executed-SQL': 'Answer executed in SQLite during bank generation; dialect stated in question',
    'executed-shell': 'Answer executed in Bash with C locale during bank generation',
}
rows = []
for q in questions:
    assert len(q['options']) == len(set(q['options'])) == 5
    assert type(q['answer']) is int and 0 <= q['answer'] < 5
    assert q['studyScope'] in ('core', 'extended')
    assert q['explanation'].strip()
    rows.append({
        'id': q['id'], 'subject': q['subject'], 'topic': q['topic'],
        'question': q['question'], 'correct_answer': q['options'][q['answer']],
        'study_scope': q['studyScope'], 'priority_reason': q['studyReason'],
        'disposition': 'Rewritten addition' if q.get('sourceId') else 'Retained',
        'review_evidence': methods[q['kind']],
        'attachment_reference': q.get('sourceId', ''),
        'explanation': q['explanation'],
    })
write_csv('question-audit.csv', rows)

# Specific concerns observed in the input. These are not asserted to be the only
# errors in input items that were excluded rather than imported.
notes = {
    'dw_dm_2': 'Nonvolatile does not prohibit all corrections or dimension updates; replacement tests a warehouse characteristic.',
    'dw_dm_9': 'Grain is not the first step of every dimensional-design process; ask its meaning instead.',
    'dw_dm_24': 'Removed combined niche SCD taxonomy; replaced with a simple retention concept.',
    'dw_dm_35': 'Clarified co-occurrence support; event intersection must not be confused with event union.',
    'dw_dm_39': 'Z-score scaling is not robust to outliers.',
    'dw_dm_48': 'A placeholder requires later reconciliation; do not silently associate facts with the wrong member.',
    'dw_dm_65': 'Removed unsupported universal CIMS/ADF regulatory-automation claims; replaced with reporting reconciliation.',
    'cloud_ai_ml_3': 'Shared responsibilities vary by service model; no universal key-management allocation.',
    'cloud_ai_ml_7': 'Serverless billing and scale-to-zero behaviour are provider-dependent.',
    'cloud_ai_ml_12': 'Corrected payment-system data scope and foreign-leg qualification; primary RBI source provided.',
    'cloud_ai_ml_13': 'Multiple zones do not guarantee zero recovery-point loss.',
    'cloud_ai_ml_21': 'Generative AI is not exclusively deep learning.',
    'cloud_ai_ml_33': 'AUC is a ranking measure, not accuracy at a chosen classification threshold.',
    'cloud_ai_ml_35': 'KNN storage, preprocessing and indexing costs are not universally constant.',
    'cloud_ai_ml_39': 'Apply resampling within training folds to prevent information leakage.',
    'cloud_ai_ml_41': 'Backpropagation computes gradients; the optimizer applies updates.',
    'cloud_ai_ml_44': 'RAG does not guarantee truthful output.',
    'cloud_ai_ml_45': 'Feature explanations are not exact causal proof or a universal regulatory mandate.',
    'cloud_ai_ml_54': 'Service mesh does not require one particular sidecar architecture.',
    'cloud_ai_ml_58': 'Removed unsupported fixed percentage cost-saving claim.',
    'cloud_ai_ml_59': 'Federated learning can leak information through model updates.',
    'cloud_ai_ml_63': 'Lowering a threshold cannot decrease recall but does not guarantee a monotonic change in precision.',
    'se_bank_it_6': 'Scrum Sprints are one month or less, not necessarily two to four weeks.',
    'se_bank_it_13': 'Verification/validation differ in purpose, not simply static versus dynamic execution.',
    'se_bank_it_18': 'Independent-path count is not a universal minimum branch-coverage test count.',
    'se_bank_it_22': 'Removed unsupported universal maintenance-percentage claim.',
    'se_bank_it_24': 'Avoided ambiguous MTBF conventions by giving explicit uptime and downtime.',
    'se_bank_it_27': 'Removed nonstandard CORE backronym.',
    'se_bank_it_28': 'Removed incorrect universal NEFT minimum; replacement tests gross/net settlement.',
    'se_bank_it_29': 'Removed incorrect NPCI incorporation statute claim.',
    'se_bank_it_31': 'UPI 123PAY is distinct from *99# USSD; avoided changing payment limits.',
    'se_bank_it_35': 'ISO 20022 is more than a wire-format label.',
    'se_bank_it_38': 'Separated CERT-In reporting from RBI requirements and limited the question to covered entities/incidents.',
    'se_bank_it_43': 'Some surviving mutants are equivalent; survival does not always prove missing tests.',
    'se_bank_it_52': 'Replaced disputed/version-sensitive maturity-level trivia with model purpose.',
    'se_bank_it_55': 'Replaced credit-score thresholds and approval implications with data-quality practice.',
    'se_bank_it_58': 'Replaced general-financial-awareness shareholding ratios with relevant banking-channel security.',
    'se_bank_it_59': 'Avoided misleading blanket Positive Pay thresholds; retained control purpose.',
    'se_bank_it_61': 'Separated dynamic transaction protection from absolute unclonability and conflated EMV mechanisms.',
    'se_bank_it_62': 'Removed conflation of contactless-card, UPI Lite and e-mandate limits.',
    'se_bank_it_63': 'Bank gateway architecture is not universal.',
    'se_bank_it_65': 'Backup strategies improve resilience but do not guarantee recovery or imply a universal exact mandate.',
    'se_bank_it_66': 'Removed unsupported universal mandate for specific PAM product features.',
    'linux_17': 'Sticky-directory removal rules also involve directory owner and privileged users; original not imported.',
    'linux_63': 'Bash errexit has conditional-context exceptions; original not imported.',
    'linux_95': 'Password locking does not disable all login methods; original not imported.',
}
if args.attachment:
    raw = args.attachment.read_bytes()
    supplied = json.loads(raw)
    targets = {q['sourceId']: q for q in questions if q.get('sourceId')}
    rows = []
    for q in supplied:
        target = targets.get(q['id'])
        long_item = len(q['q']) > 350 or max(map(len, q['o'])) > 300
        flags = []
        if long_item: flags.append('Long/compound wording')
        if re.search(r'\b(always|never|guarantee|guarantees|mandatory|mandates)\b', q['q']+' '+q['o'][q['a']]+' '+q['e'], re.I):
            flags.append('Absolute/regulatory wording needs qualification')
        rows.append({
            'attachment_id': q['id'], 'subject': q['subject'], 'subtopic': q['subtopic'],
            'disposition': 'Replaced by concise reviewed item' if target else 'Not imported: existing subject retained',
            'production_id': target['id'] if target else '',
            'scope': target['studyScope'] if target else 'Excluded input',
            'screening_flags': '; '.join(flags),
            'specific_note': notes.get(q['id'], 'Single-concept rewrite; removed answer-length cues and unsupported absolutes where applicable.' if target else 'No bulk merge of the overlapping five subjects. This decision does not certify the supplied answer key or claim exact question equivalence.'),
            'accuracy_status': 'Use the rewritten production item, not the original answer/explanation' if target else 'Original answer not independently certified; excluded from production',
        })
    write_csv('attachment-disposition.csv', rows)
    (docs/'attachment-manifest.json').write_text(json.dumps({
        'extracted_json_sha256': hashlib.sha256(raw).hexdigest(),
        'input_items': len(supplied), 'rewritten_additions': len(targets),
        'excluded_input_items': len(supplied)-len(targets),
        'specific_concerns_recorded': len(notes),
        'scope_note': 'Disposition for every input item; excluded original answers are not independently certified.',
    }, indent=2)+'\n')
print(json.dumps({'production_rows':len(questions), 'study_scopes':dict(collections.Counter(q['studyScope'] for q in questions)), 'input_comparison_written':bool(args.attachment)}))
