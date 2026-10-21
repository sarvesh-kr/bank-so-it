# DBMS & SQL R2 audit — 21 October 2026

The DBMS topic contains **200 newly curated questions**, replacing all 118 items in the preceding release. The user's topic list governs this revision: concise fundamentals and short applications suited to Bank SO IT professional-knowledge practice. The other **746 questions are unchanged**, including the 200-question networking revision. [Change evidence](dbms-r2-change-evidence.json) records that comparison against commit `516b7b71c9530d23fb5aecb8633f9c86271ecf08`.

## Coverage

| Area | Questions |
|---|---:|
| DBMS foundations and models | 12 |
| ER modelling and Chen notation | 18 |
| Relations, keys and constraints | 16 |
| Naming and SQL data types | 10 |
| Normalization and dependencies | 16 |
| Relational algebra | 14 |
| Indexes and B/B+ trees | 15 |
| SQL command families | 18 |
| SQL clauses and query logic | 17 |
| SQL output and command practice | 32 |
| Transactions and recovery | 20 |
| Backup and RAID | 12 |
| **Total** | **200** |

The questions include model distinctions, schema/instance, ER shapes and cardinality, candidate/primary/foreign keys, naming conventions, numeric and date types, functional dependencies, normal forms, basic algebra operators, B/B+ trees, dense/sparse/composite indexes, SQL command families, joins, NULL, aggregation, subqueries, transactions, concurrency anomalies, logging, checkpoints, backup chains and RAID. 4NF and 5NF receive brief definitions. Long decomposition proofs, elaborate tree insertions and specialist SQL puzzles are omitted in favour of revision value.

## Answer and explanation checks

Each stem, five-choice set, selected answer and explanation received a technical review against its attached references. The [per-item ledger](question-audit.csv) and [review register](../content/review/review-register.json) record the reviewed hashes and dates. CI rejects unreviewed content changes. There are **152 conceptual/application questions and 48 independently checked worked exercises**:

- **32 SQL cases** execute in isolated SQLite databases with the displayed schema, rows and statements. They cover sorting, DISTINCT, NULL, aggregates, GROUP BY/HAVING, joins, subqueries, UNION/UNION ALL, LIKE, INSERT/UPDATE/DELETE, ALTER, views, rollback/savepoints and real primary-key, CHECK and foreign-key failures. Foreign-key enforcement is explicitly enabled. Ordering is explicit wherever row order matters.
- **Six relational-algebra cases** evaluate selection, projection, Cartesian product, union, difference and natural join as sets. Tuple displays use a stated comparison order; relations have no inherent row order.
- **Ten further worked cases** independently check attribute closure, normal-form classification, lossless decomposition, maximum B-tree keys and RAID capacities. Candidate keys are enumerated rather than accepted from the answer key.

The authored choices are compared with the computed results; the checker also ensures the query/table text shown in the app matches the executed fixture. See [dbms-quality-summary.json](dbms-quality-summary.json), [fixtures](../content/curated/dbms-r2-cases.json) and [checker](../tools/check_dbms.py).

## Accuracy conventions

- ER shape questions explicitly use **Chen notation**. An entity is a rectangle, relationship a diamond, attribute an oval, multivalued attribute a double oval and derived attribute a dashed oval. Double participation lines mean total participation; weak entities and their identifying relationships use double shapes. Cardinality examples state their business assumptions.
- A candidate key is minimal by attribute inclusion. Normal-form questions distinguish prime attributes and superkeys. The 3NF-but-not-BCNF exercise enumerates both candidate keys.
- SQL command labels use the common examination taxonomy when SELECT is called DQL. This is a classification convention, not a claim that every vendor uses the same labels.
- Every executable SQL exercise names **SQLite**. Identifier case/quoting questions name PostgreSQL where appropriate. TIMESTAMP is qualified as standard SQL/PostgreSQL. Primary-key rules refer to the relational model/standard SQL; SQLite's historical exceptions are not generalized.
- CHECK rejects FALSE rather than every UNKNOWN result. Foreign-key NULL behaviour is qualified. No universal claim is made about TRUNCATE rollback, identity reset or logging; those depend on the implementation.
- B-tree order is defined in the numerical question. B/B+ tree terminology uses textbook conventions. Composite-index guidance avoids a universal prohibition on non-leading-column use, accounting for implementations with skip scans.
- Recovery questions distinguish atomicity and durability, write-ahead logging, checkpoints and undo/redo needs. The explanation acknowledges ARIES repeating history before undoing unfinished transactions.
- RAID capacity examples state equal drive sizes and exclude spares/overheads. RAID 10 uses explicitly paired mirrors. RAID is not a backup; logical deletion and ransomware can affect every live replica. Differential and incremental backup questions define their bases and dependencies.

## Research basis and limits

The exam-alignment evidence remains the preparation outline and recalled analysis documented in [RESEARCH.md](RESEARCH.md). They support foundational DBMS/SQL coverage; they are not an authenticated full paper or an exact topic-weight table. The user's detailed scope determines this selection.

Technical sources include the authors' [Database System Concepts slides](https://www.db-book.com/slides-dir/index.html), particularly relational modelling, ER design, normalization, storage/RAID, indexing, recovery and formal query languages. Relevant slide PDFs were retrieved and inspected. [PostgreSQL documentation](https://www.postgresql.org/docs/current/) supplies command/constraint/type/concurrency details; [SQLite documentation](https://www.sqlite.org/docs.html) supplies the executable dialect; [Linux RAID documentation](https://docs.kernel.org/admin-guide/md.html) supports RAID distinctions. Chen shape references also use [Lucidchart's notation guide](https://www.lucidchart.com/pages/ER-diagram-symbols-and-meaning). Sources are attached to individual questions in the [reference catalog](../content/curated/dbms-references.json).

One retrieved public ER guide reversed the total/partial participation line convention. It was excluded; the textbook explicitly confirms double lines for total participation. Source disagreement was resolved rather than copied into the bank.

This is a documented model-assisted technical review, not independent human expert certification or an official IBPS paper. The executable checks verify the stated worked results; conceptual relevance and uniqueness also depend on the review and stated assumptions.

## Source and progress compatibility

[dbms-r2.txt](../content/curated/dbms-r2.txt) is the canonical authored source. [build_dbms.py](../tools/build_dbms.py) supplies stable IDs `dbms-r2-001` through `dbms-r2-200` and deterministic choice shuffling. Legacy source rows remain only to preserve other subjects' generation IDs and random sequence.

All prior `dbms-001` through `dbms-257` IDs are retired, including ones retired by earlier reviews. Fresh IDs prevent old attempts being credited to unrelated replacement questions. Old session snapshots and personal edits remain available; retired stock questions cannot re-enter current practice through an old stock import. The same bank ships in the web app and signed Android 2.2 APK.
