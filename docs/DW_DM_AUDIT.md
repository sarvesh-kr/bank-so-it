# Data Warehousing & Data Mining R2 audit — 21 October 2026

This revision replaces the previous 52 items with **50 conceptual questions and no numerical exercises**. The scope follows the user's request for OLTP/OLAP, warehouse types, schemas, marts, cubes, tools and important foundational mining concepts. The other **953 question records are exactly unchanged**, including all five earlier subject revisions. [Change evidence](dw-dm-r2-change-evidence.json) compares the records with commit `349d5d4a5cec46503cfc7bc7621e1dae756b9f2f`.

## Coverage

| Area | Questions |
|---|---:|
| Warehouse foundations and types | 8 |
| Dimensional models and schemas | 9 |
| ETL, metadata and data quality | 6 |
| OLAP cubes, operations and types | 11 |
| Data mining concepts and techniques | 14 |
| Common tools and roles | 2 |
| **Total** | **50** |

Coverage includes the classical warehouse characteristics, OLTP versus OLAP, ODS, data marts and dependent/independent sourcing, Inmon/Kimball approaches, star/snowflake/galaxy schemas, facts/dimensions, grain, surrogate keys, semi-additive balances, slowly changing dimensions and conformed dimensions. Loading coverage includes ETL/ELT, staging, identifier reconciliation, metadata/lineage and CDC/incremental loading.

OLAP questions cover cubes and dimension hierarchies, roll-up, drill-down, slice, dice, pivot and MOLAP/ROLAP/HOLAP. Mining questions cover KDD, classification, regression, clustering, association rules, support/confidence/lift definitions, Apriori, decision trees, k-means, agglomerative clustering, anomaly detection and feature scaling. Tool recognition is limited to the broad roles of Informatica PowerCenter and Weka. There are no support/confidence calculations, cube-cell counts, distance calculations, algorithm traces, advanced dimensional variants or vendor-version trivia.

## Accuracy review

Every stem, five options, selected key and explanation was reviewed for a unique best answer under the stated context. Distractors were revised to use nearby concepts where useful. The [per-item ledger](question-audit.csv) and [review register](../content/review/review-register.json) record exact reviewed content hashes. This is model-assisted technical review, not independent human expert certification.

Key conventions:

- Nonvolatile describes predominantly read-oriented analytical use; warehouses can still be loaded, refreshed and corrected. OLTP and OLAP describe workloads, not a rule that they can never share a platform.
- Dependent/independent mart refers to sourcing. Kimball's approach includes integration through conformed dimensions, not disconnected marts.
- Star and snowflake questions use conventional dimensional-design meanings. A fact-table grain describes one business observation; it is not storage size or refresh frequency.
- End-of-day account balances are semi-additive: summing accounts at one date differs from summing successive snapshots. Type 2 version rows are distinguished from Type 1 overwrites and Type 3 limited column history.
- ELT performs transformations after loading. A staging area does not guarantee clean data. CDC identifies changes; incremental loading applies the selected changes.
- Cubes may have more than three dimensions. Slice fixes one dimension to a single member; dice selects a subcube using member sets/ranges. Roll-up and drill-down change detail; pivot changes perspective.
- MOLAP is explicitly identified by storage of both detail and aggregates in multidimensional structures; HOLAP commonly retains relational detail and multidimensional aggregates. ROLAP still supports a multidimensional analytical view.
- Classification predicts categorical labels, regression numeric targets, clustering unlabeled groups and association rules co-occurrences. Support and confidence use different denominators. Lift greater than one is an observed association, not causation or a significance guarantee.
- Apriori pruning assumes a fixed support threshold. Standard k-means uses means rather than medoids. Agglomerative merges and divisive splits. Anomalies warrant investigation; they do not prove fraud. Scaling helps distance-based methods without guaranteeing useful clusters.

## Sources and alignment

[The reference catalog](../content/curated/dw-dm-references.json) attaches Oracle warehouse/mining documentation, Han/Kamber/Pei's author-hosted teaching slides, Kimball's modeling reference, scikit-learn documentation and the vendors' own tool documentation to individual questions. Source bytes were retrieved, hashed and relevant sections inspected; binary PowerPoint text and the Kimball PDF were extracted for review. [Research evidence](dw-dm-research-evidence.json) records the used sources. These sources support technical definitions rather than claims about future exam frequencies.

[RESEARCH.md](RESEARCH.md) records the existing RRB IT preparation outline and recalled-paper analysis. This selection follows the user's conceptual, foundation-first scope; the available material does not establish exact warehouse/mining question frequencies or authenticate these questions as past-paper questions. Numerical checks elsewhere in the app remain unchanged; removing the two older mining/cube calculations reduces the whole-bank independent computed-result checks from 127 to 125.

## Compatibility and validation

[dw-dm-r2.txt](../content/curated/dw-dm-r2.txt) is the canonical source, with stable new IDs `dw-dm-r2-001` through `dw-dm-r2-050`. The loader uses its own random generator so other subjects' option order is preserved. All 65 legacy `dw_dm-001` through `dw_dm-065` IDs are retired, including earlier exclusions, so old attempts cannot attach to replacement questions. Existing historical snapshots and personal edits remain available.

The topic checker enforces counts, conceptual-only kinds, source agreement and legacy retirements. Existing core/backup tests and browser tests cover subject filters, a scored attempt, the dice revision card and references at 320px width, offline persistence and reload-based update migration. The web app and signed Android 2.6 APK share the same bank. See [VALIDATION.md](VALIDATION.md) for release checks and Android testing limits.
