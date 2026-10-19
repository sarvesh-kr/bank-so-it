# Content review — 19 October 2026

The supplied HTML contained 1,150 questions. The existing project had 950 questions in five subjects. This change adds **200 rewritten questions in three missing subjects**, retaining the original 950 project questions and their IDs. The published bank now has 1,150 questions.

## Coverage and study priorities

| Subject | Full bank | Focused revision |
|---|---:|---:|
| Networks & Cybersecurity | 250 | 146 |
| DBMS & SQL | 250 | 111 |
| Operating Systems | 100 | 71 |
| Data Structures & Algorithms | 250 | 105 |
| Linux & Shell | 100 | 100 |
| Data Warehousing & Data Mining | 65 | 50 |
| Cloud, AI & ML Basics | 65 | 48 |
| Software Engineering & Banking IT | 70 | 61 |
| **Total** | **1,150** | **692** |

Focused revision is the default in new sessions. It includes foundations and representative exercises. **All questions** includes 458 optional-depth or extra-drill items. These questions remain accessible, including through mistake and bookmark revision. Optional items are labelled in the question display.

Examples of optional depth include Hamming-code and Nyquist calculations, detailed fragmentation calculations, advanced dimensional modelling, neural-network training details, segment/Fenwick trees and extra numerical variants of the same skill. Basic subnetting, SQL outputs, process/memory concepts, sorting, graph algorithms and banking security stay in focused revision. A moderate calculation is not automatically irrelevant.

This is an editorial preparation priority, not an official IBPS syllabus or a guarantee about future questions. Equal subject sampling is a practice-balancing choice. Programming languages/OOP, web technology and computer architecture still need separate coverage; this bank is not a complete syllabus mock.

## What changed in the supplied questions

All 200 new-subject items were rewritten into short questions with five choices and a concise explanation. A source ID links each replacement to its input slot; a replacement may narrow or change the concept rather than preserve every claim in the source. Compound questions, answer-length clues, unsupported superlatives and changing transaction limits were removed where encountered.

Notable corrections and replacements:

- Warehouse data can be corrected; “nonvolatile” does not mean every row is permanently unchangeable. Data marts need not always be warehouse subsets.
- Association support means co-occurrence. Z-score scaling is not robust to outliers.
- Serverless does not guarantee particular billing or scale-to-zero behaviour. Multiple availability zones do not guarantee zero data loss.
- Generative AI is not exclusively deep learning. RAG does not guarantee truthful answers; federated learning does not guarantee privacy.
- Lowering a fixed score threshold cannot decrease recall, but precision need not change monotonically.
- Verification and validation are distinguished by purpose, not simply static versus dynamic execution. Cyclomatic complexity is not a universal minimum branch-coverage test count.
- Removed the incorrect universal NEFT minimum, NPCI incorporation claim, conflation of *99# with UPI 123PAY, and conflation of contactless-card, UPI Lite and e-mandate limits.
- CERT-In incident reporting is identified separately from RBI requirements. Payment-data localisation is limited to the relevant payment-system scope, with the foreign-leg qualification.
- Removed universal claims about bank gateway architecture, PAM product features, mandatory approval flows and exact maintenance-cost percentages.
- Replaced RRB ownership ratios and credit-score cut-offs with relevant IT controls and data-quality questions.

## Per-question records and limits

- [question-audit.csv](question-audit.csv): one row for **each of the 1,150 production questions**, with selected answer, explanation, study priority, disposition and review evidence.
- [attachment-disposition.csv](attachment-disposition.csv): one row for **each of the 1,150 supplied questions**, identifying the 200 replacements and 950 excluded input items. Wording flags are screening signals, not proof of factual error.
- [attachment-manifest.json](attachment-manifest.json): counts and a SHA-256 fingerprint of the safely extracted input JSON.
- [bank-validation.json](bank-validation.json): generated structural and execution-check results.

The attachment's 950 items in already-existing subjects were **not bulk-imported**. Keeping the project's existing bank avoids doubling those subjects with another, frequently verbose question set. This is a subject-level scope decision, not a claim that every source question is an exact duplicate or that every additional subtopic is already covered.

**The excluded 950 source answer keys have not all been independently fact-checked. They are not endorsed for study.** Specific observed problems, including Bash `set -e` exceptions and password-locking versus account-access restrictions, are recorded in the input ledger. This review does not certify the entire original HTML bank as accurate.

For the production bank, concept/selected-answer review is distinguished from computational evidence: the generator executes 150 SQL answers in SQLite and 30 shell answers in Bash, and regenerates 305 numerical/trace questions from reviewed formulas and algorithms. The 200 additions were reviewed during rewriting. Structural checks verify unique IDs/stems, five distinct choices, valid answer indices and explanations. None of these checks is a substitute for an independent subject expert's certification of all concepts or a proof that every distractor is ideal.

Existing question text, option order, correct-answer index and explanations are unchanged for the original 950 project records. Added study-priority metadata does not alter scoring. Active attempts retain their original snapshots.

## Research basis

The [2024 candidate-recalled Scale II analysis](https://www.bankersadda.com/ibps-rrb-officer-scale-2-exam-analysis-2024/) describes moderate professional knowledge and mentions sorting, graphs, SQL commands, IP addressing, protocols, cyberattacks and OS segmentation. This supports conceptual questions and short applications, but supplies neither authenticated complete papers nor dependable topic weights. [ixamBee's preparation outline](https://www.ixambee.com/exams/ibps-rrb-officer-scale-ii-exam-syllabus) provides broader indicative coverage; it is not an official topic specification. Check the current [IBPS notification and examination handout](https://www.ibps.in/) for the applicable pattern.

Primary references for the sensitive corrections:

- [NIST SP 800-145: cloud definition](https://csrc.nist.gov/pubs/sp/800/145/final).
- [RBI: Storage of Payment System Data, 6 April 2018](https://rbi.org.in/Scripts/NotificationUser.aspx?Id=11244).
- [CERT-In: directions dated 28 April 2022](https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf) and [official implementation FAQs](https://www.cert-in.org.in/PDF/FAQs_on_CyberSecurityDirections_May2022.pdf).
- [NPCI: UPI 123PAY](https://www.npci.org.in/what-we-do/upi-123pay/live-members/).
- [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html).
- [GNU Bash manual: the set builtin and its exceptions](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).
- [scikit-learn: precision and recall](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics).

Regulatory questions identify their source and scope. Volatile transaction limits are avoided rather than presented as timeless facts.

## Build and delivery

Run `python3 tools/build_bank.py`, then `python3 tools/audit_bank.py`. To recreate the input comparison with a local extracted snapshot, add `--attachment audit/attachment-original.json`. Raw input snapshots are not published in the site or repository.

The web build uses the updated shared assets. The existing signed APK download has not been replaced: its signing key is absent. Existing APK users can download the latest `bank.json` using the web app's question-pack link and import it through **My bank → Import pack**. That updates question content; the older APK does not acquire the new study-coverage UI through a data import. A signed application update requires the existing release key.
