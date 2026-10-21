# Software Engineering & Banking IT revision — 21 October 2026

This revision replaces 68 older items with **50 focused questions: 45 concepts and five short banking IT scenarios**. There are no numerical exercises. The concurrent [programming revision](PROGRAMMING_AUDIT.md) replaces 60 with 75. All **909 question records outside software/banking and programming are exactly unchanged**, including option order, answers, explanations and references. [Change evidence](se-bank-r2-change-evidence.json) compares the bank with commit `db458fb00b8bf44ac9f0be38300a6a958ab395c3`.

## Coverage

| Subtopic | Questions |
|---|---:|
| SDLC & requirements | 9 |
| Design, delivery & maintenance | 6 |
| Testing foundations & types | 12 |
| Testing techniques & principles | 5 |
| IT service management & resilience | 5 |
| Vendor management & outsourcing | 4 |
| Banking systems & payments | 4 |
| Banking IT scenarios | 5 |
| **Total** | **50** |

SDLC coverage includes waterfall, risk-driven spiral, V-model, incremental versus iterative delivery, prototyping, Agile, Scrum ownership, functional/non-functional requirements and traceability. Design/delivery covers cohesion/coupling, UML sequence diagrams, version control, CI, delivery versus deployment and maintenance categories.

The 17 testing questions cover verification/validation, static/dynamic testing, unit/component, integration, system, UAT, black/white-box, confirmation/regression, smoke, load/stress, authorization security and alpha/beta testing. Techniques/principles cover equivalence partitioning, boundary analysis, branch coverage, risk-based prioritization and the limits of testing.

Service operations cover incidents versus problems, impact/urgency, controlled changes, RTO/RPO and continuity versus IT disaster recovery. Four vendor questions cover risk-based due diligence, contractual SLA/security/audit terms, the bank's retained accountability and exit/transition planning. Banking foundations cover CBS, RTGS/NEFT, SWIFT messaging and PCI DSS scope. Wider payment-product trivia, volatile limits/reporting deadlines and project-estimation arithmetic are omitted from this compact revision.

## Five scenarios

1. Business users assess loan rules and workflows through UAT.
2. An approved safe workaround restores a non-security CBS outage while problem investigation continues.
3. A failed release reaches approved rollback criteria; recovery includes service and data-consistency checks.
4. A DR exercise meets RTO but misses RPO; the objectives are assessed separately without calculations.
5. An uncertain transfer is retried under an explicitly supported idempotency contract, reusing its original key and intent.

Each scenario asks for one short practical decision and states the conditions needed for a unique best answer. Scenario stems are at most 65 words. The idempotency example does not imply that all payment interfaces implement the same contract or that a timeout proves failure.

## Accuracy review and sources

Every stem, all five options, key and explanation received a technical review. Particular checks include:

- Agile does not prohibit planning or documentation; Scrum Product Owner accountability remains even when work is delegated.
- Verification/validation are purposes, not a strict static/dynamic division. Confirmation testing is distinct from regression testing.
- Black/white-box techniques are not synonyms for manual/automated testing. Full branch coverage is not proof of full path coverage or absence of defects.
- Smoke tests are shallow initial checks, and load/stress tests have distinct objectives. Alpha/beta environment definitions follow the official ISTQB glossary; the question makes no fixed claims about sequence, duration or defect percentages.
- Restoring a non-security outage need not await permanent root-cause resolution. The scenario specifies a safe approved workaround; cybersecurity containment and evidence obligations are not displaced.
- Controlled changes and emergency processes retain authorization and records. Rollback does not automatically undo business transactions.
- Recovery speed and recoverable-data age are separate objectives. Vendor oversight continues after outsourcing; contracts and exit planning need appropriate security, audit, performance and continuity provisions.
- RTGS/NEFT settlement mechanisms are distinct; SWIFT messaging alone does not move funds. PCI DSS scope is payment-account-data security rather than every banking regulation.

[The reference catalog](../content/curated/se-bank-references.json) attaches sources to each item. Sources include the official ISTQB CTFL 4.0.1 syllabus and glossary, IEEE SWEBOK v4, OMG UML 2.5.1, Agile Manifesto, Scrum Guide, Git, AWS, NIST SP 800-218/800-53/800-34/800-61, Atlassian service-management documentation, Microsoft performance guidance, RBI FAQs, RBI outsourcing directions, SWIFT, PCI SSC and IBM core-banking material. [Research evidence](se-bank-research-evidence.json) records 26 retrieved documents with checksums and one official glossary entry checked through indexed excerpts. Direct glossary HTML exposed a JavaScript shell; an older ASTQB PDF link redirected to an index. Unused NPCI candidate responses did not expose usable text; no UPI question remains in this compact topic. Vendor controls use retrieved RBI outsourcing guidance as a technical reference, without asserting that its legal applicability covers every type of bank. These limitations are recorded rather than counted as successful document downloads.

[RESEARCH.md](RESEARCH.md) records the existing Bank SO IT preparation scope and recalled-paper limits. This selection follows the user's foundation-first exam preparation request. It does not assert exact question frequencies or authenticate these as previous-year questions. The technical/model-assisted review is not independent human expert certification.

## Integrity and application checks

Canonical source: [se-bank-r2.txt](../content/curated/se-bank-r2.txt). New IDs are `se-bank-r2-001` through `se-bank-r2-050`; all 76 legacy IDs are retired, including eight already absent and six supplement IDs added after the original baseline. Old stock imports cannot reintroduce them or overwrite reviewed built-ins. Personal edits and historical test snapshots retain existing handling.

The topic checker enforces the 50-question scope, five scenario IDs, short stems, source agreement and retirements. Reviewed hashes and [the per-item ledger](question-audit.csv) cover all shipped items. Browser checks cover each subtopic filter, a scored scenario attempt, and the DR scenario's answer, explanation and source link at 320px. Existing reload, offline, progress and Chromium/WebKit download tests remain in place. The same bank is embedded in signed Android 2.8. See [VALIDATION.md](VALIDATION.md).
