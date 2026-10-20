# Exam-focused quality audit — 20 October 2026

The current bank contains **864 questions across 11 subjects**. The [network R2 audit](NETWORK_AUDIT.md) replaces the previous 152 networking/cybersecurity items with **200 newly curated questions** following the user’s detailed topic list. The other 664 items are unchanged.

The earlier cross-subject review began with 1,150 questions and produced an 816-item bank: 680 retained and 136 additions, with 470 retirements and 163 retained items corrected or clarified. Those figures describe that earlier release. The current ledger contains 622 retirements across both revisions, including seven IDs added after the original baseline.

## Review criteria

Each retained stem, all five options, selected key and explanation was checked for technical correctness, a unique best answer under stated assumptions, useful degree-level coverage and manageable revision time. The review uses primary technical documentation, authored textbooks, official banking references and independent calculation/output checks. The reviewer is Codex; this is not an independent human expert certification or an official IBPS question paper.

Bank SO IT covers foundational bank specialist IT knowledge. The initial exam-alignment target was RRB Officer Scale II IT: short conceptual distinctions, standard SQL, basic calculations/traces and practical banking IT controls. A question need not mention a bank to be relevant: networks, programming, operating systems and algorithms are part of the technical preparation scope. Obscure implementations, deep formulas, repeated numeric substitutions and unsupported rules do not earn places merely to preserve a question quota.

## What changed

- In the initial cross-subject review, removed repeated datasets/drills and specialist depth such as Nyquist/Hamming calculations, detailed fragmentation calculations, suffix structures, advanced dimensional patterns and detailed model-training mechanics. Retirement is a revision-priority decision, not a claim that a topic is forbidden by an official syllabus.
- Corrected Big-O questions so they request the tightest listed bound. A loose upper bound must not create another defensible answer.
- Clarified next-hop routing assumptions, MTU contents, zero-day terminology, exhaustive password guessing, SQL window ordering, transaction boundaries, page-fault context and SCAN versus LOOK.
- Clarified C string length as bytes, Java reference/value distinctions, Python floor division, graph assumptions and random-forest construction. Avoided undefined-behaviour output puzzles.
- Shortened lengthy keys and replaced many unrelated or giveaway distractors with meaningful competing concepts.
- Added Programming/OOP (60), Computer Fundamentals/Architecture (33), Web Technology (20), and 23 short questions filling gaps in existing subjects.
- Kept regulatory questions anchored to their source and scope. Avoided changing payment-limit trivia and unsupported universal RBI mandates.

## Coverage

| Subject | Questions |
|---|---:|
| Networks & Cybersecurity | 200 |
| DBMS & SQL | 118 |
| Operating Systems | 73 |
| Data Structures & Algorithms | 107 |
| Linux & Shell | 86 |
| Warehousing & Mining | 52 |
| Cloud, AI & ML Basics | 47 |
| Software Engineering & Banking IT | 68 |
| Programming & OOP | 60 |
| Computer Fundamentals & Architecture | 33 |
| Web Technology | 20 |
| **Total** | **864** |

The new areas cover C/C++/Java/Python fundamentals, OOP, exceptions, short Python outputs, CPU/registers/buses, representation and logic, memory hierarchy, HTML/CSS/JavaScript/DOM, HTTP, origins, JSON and XML. The app's Quick revision page provides searchable answer/explanation cards and a subject coverage selector. These are the mapped core areas of the selected IT preparation outline, not a guarantee of every possible future question.

## Evidence for every item

- [question-audit.csv](question-audit.csv): all 864 shipped stems, five options, selected answers, explanations, references, review decisions and reviewed hashes.
- [retired-question-audit.csv](retired-question-audit.csv): all 622 retired IDs, topics and reasons, linked to the previous production commit.
- [baseline-answer-checks.json](baseline-answer-checks.json): independently checked all 485 computed answers in the previous production bank: 305 numerical/trace, 150 SQL and 30 Bash answers.
- [quality-checks.json](quality-checks.json): 78 checks in the current bank: 30 numerical/trace, 15 SQL, 16 Bash, 10 Python and seven additional calculations embedded in conceptual questions.
- [quality-audit-summary.json](quality-audit-summary.json): counts and dispositions.
- [review-register.json](../content/review/review-register.json): exact content hashes approved in this technical review. CI rejects an item changed after review or missing from the register.

The independent checker reconstructs SQL datasets, reruns scripts, enumerates small search/path/subarray cases and computes numeric results without trusting the selected key. These checks establish the stated computed results. Conceptual uniqueness, interpretation and relevance require the documented technical review; an automated five-option/index check alone does not establish them.

The old attachment-disposition files concern the earlier HTML import and remain historical records. This audit concerns the production bank at commit `693275acdf059ef83e274cfdbb59d5679f8ce4ff`, then the revised bank. Excluded answers in the original uploaded HTML are not endorsed by this audit.

## Scope and research limits

The [2024 RRB Scale II recalled-paper analysis](https://www.bankersadda.com/ibps-rrb-officer-scale-2-exam-analysis-2024/) reports a moderate IT section and themes including SQL, networks/security, OS, sorting and graphs. Its accessible indexed material provides themes rather than an authenticated complete paper or reliable topic frequencies. The [RRB IT preparation outline](https://www.ixambee.com/exams/ibps-rrb-officer-scale-ii-exam-syllabus) adds broader subject coverage including languages, web and architecture. It is a preparation-provider outline, not an official topic-weight table. GBO computer-awareness and Scale I SO analyses were not treated as RRB Scale II IT papers.

The [official 2025 RRB notification](https://www.ibps.in/wp-content/uploads/CRP-RRBs-XIV_Final_AD_1.9.25.pdf) has indexed examination-table information supporting the professional-knowledge pattern, but full-PDF retrieval returned errors in this environment. Check the current [IBPS notification and call-letter handout](https://www.ibps.in/) for the applicable format and any changes. The app's 40-question/30-minute setting is a practice preset; equal subject sampling is not a prediction of topic weights.

References are attached to individual questions. The network revision uses explicit RFC/IANA/NIST/OWASP references and selected security-publisher explanations, documented in NETWORK_AUDIT.md. They include IETF/ITU/IANA, NIST/OWASP, PostgreSQL/SQLite, GNU/systemd, the authors of OSTEP and Open Data Structures, MIT, Kimball, language specifications/documentation, WHATWG/W3C, RBI/CERT-In/NPCI/SWIFT and PCI SSC. The full reference-selection rules are in [review_sources.py](../tools/review_sources.py).

## Preserving useful progress

Retired questions are absent from every current study pool. Old stock-pack imports cannot bring them back or overwrite reviewed built-ins. Existing personal edits remain personal study material. Prior session snapshots are preserved, while current-bank statistics exclude retired items. The Android release reuses the private Android 1.2 signing key, enabling an in-place update from 1.2.
