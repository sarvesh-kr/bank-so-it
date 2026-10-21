# Data Structures & Algorithms R2 audit — 21 October 2026

The DSA topic contains **150 newly curated questions**, replacing the preceding 107. The selection follows the user's sorting/searching, arrays, linked lists, stacks, queues, binary trees, BSTs and heaps scope, with basic hashing, graphs, complexity and algorithm approaches. The other **866 question records are unchanged**, including all networking, DBMS and OS revisions. [Change evidence](dsa-r2-change-evidence.json) records the comparison against commit `d5b77faafa23f9606afdca6f946ac532c36a0c1d`.

## Coverage

| Area | Questions |
|---|---:|
| Complexity and algorithm basics | 12 |
| Arrays and strings | 12 |
| Linked lists | 12 |
| Stacks | 10 |
| Queues | 10 |
| Searching | 12 |
| Sorting | 26 |
| Binary trees and traversals | 14 |
| Binary search trees | 12 |
| Heaps and priority queues | 10 |
| Hashing | 8 |
| Graphs and algorithm approaches | 12 |
| **Total** | **150** |

There are **125 conceptual/application questions and 25 short worked exercises**. Sorting covers bubble, selection, insertion, merge, quick, heap, Shell, counting, LSD radix and bucket sorts. Searching covers linear/binary search, prerequisites, comparison costs, duplicate keys and lower/upper boundaries. Tree coverage distinguishes binary/full/complete/perfect trees, traversal orders, height, BST operations and AVL balance. Graph coverage includes representations, BFS/DFS, topological ordering, MST algorithms, Dijkstra and basic greedy/DP distinctions.

Advanced balancing proofs, long sorting traces, complicated recurrences, suffix structures, specialized graph algorithms and implementation-specific programming puzzles are omitted. Small traces reinforce the core operations without making the bank a collection of repeated numerical variants.

## Answer verification

Every stem, five-choice set, selected key and explanation received a technical review against its attached references. The [per-item audit](question-audit.csv) and [review register](../content/review/review-register.json) record exact reviewed hashes and dates. CI rejects an item changed without renewing its review record.

The [independent checker](../tools/check_dsa.py) parses values from the displayed stems, executes the appropriate operation and compares the result with the authored key. It records intermediate states in [dsa-quality-summary.json](dsa-quality-summary.json).

| Worked area | Cases | Verification |
|---|---:|---|
| Loop counts | 2 | Nested-loop iteration and repeated halving |
| Array addressing | 1 | Base, stride and zero-based index calculation |
| Linked-list changes | 1 | Insert and delete sequence |
| Stacks | 2 | Postfix evaluation and pop order |
| Queues | 2 | FIFO removals and circular index wrapping |
| Searching | 2 | Binary-search probe trace and lower bound |
| Sorting | 4 | Bubble pass, selection step, insertion steps and merging |
| Binary trees | 3 | Inorder, edge-based height and full-tree node count |
| BSTs | 2 | Construct/search path and successor-based deletion |
| Heaps | 2 | Insert/extract using Python's independent heap implementation |
| Hashing | 2 | Linear probing and bucket occupancy |
| Graphs | 2 | Alphabetical-neighbour BFS and Dijkstra distance/path |
| **Total** | **25** | |

For the full-tree count, the checker solves the node/edge constraint rather than trusting the explanation. BST deletion checks the resulting inorder sequence. Heap cases validate the heap property before and after the operation. Graph traversal marks vertices when enqueued; the weighted case uses only nonnegative edges.

## Accuracy conventions

- Big-O is an upper bound and does not inherently mean worst case or a tight bound. Complexity questions request the tightest listed class and state the relevant best/worst/expected/amortized condition. Recursive call-stack space is included.
- Array costs distinguish positional search, shifting and resizing. Array slots can be contiguous even when referenced objects are not. C strlen counts bytes before the null terminator, not buffer capacity or universal Unicode character count.
- Linked-list constant-time insertion assumes the position reference and an allocated node. Tail append assumes a maintained tail. Unlinking without copying payloads needs access to the predecessor in a singly linked list.
- Circular-queue questions state zero-based indices, capacity and an explicit count. They do not assume a universal front/rear equality rule. Two-stack queue costs are amortized, not a promise that every transfer is constant time.
- Binary search assumes sorted random-access data. The trace counts middle-element probes, not language-level relational operations. Basic equality-return search is distinguished from lower and upper bounds. The midpoint question explicitly avoids fixed-width addition overflow.
- Bubble sort's linear best case requires its stated early-exit flag. Selection-sort comparisons remain quadratic on sorted input. Stable merge ties take from the left. Standard swap-based selection sort is not universally stable. Random-pivot quicksort has expected linearithmic time and can still have a quadratic run. Shell-sort performance depends on gaps; counting/radix/bucket claims state their relevant assumptions.
- Tree height counts edges where used; a singleton has height zero. Full/proper, complete and perfect have explicit shape definitions. A generic binary tree's inorder need not be sorted. BST questions use distinct keys and apply ordering to entire subtrees.
- Heaps use zero-based index formulas and complete-tree shape. Heap order is not BST order or complete sorting. Insertion excludes a backing-array resize; bottom-up build is linear. Traces state sift rules because more than one valid heap arrangement can exist.
- Hash lookup's constant bound is expected under suitable hashing/load assumptions. Chaining can have load factor above one. Open-addressing tombstones preserve probe paths; deleting by blindly marking a slot never used can lose reachable keys.
- BFS gives shortest distances by edge count in unweighted graphs. DFS does not generally do so. Topological ordering concerns directed acyclic graphs. MST cost and shortest-path distance are distinct objectives. Standard Dijkstra assumes nonnegative weights. Greedy choices need a correctness argument; DP reuses overlapping subproblems.

## Research and limits

Technical references include Pat Morin's [Open Data Structures](https://opendatastructures.org/ods-java.pdf), Sedgewick and Wayne's [Algorithms companion](https://algs4.cs.princeton.edu/home/), [MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/), OpenDSA's authored textbook sources, the [C11 committee draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), Python/SciPy documentation, Joshua Bloch's binary-search analysis, and supporting CP Algorithms/USACO Guide explanations. The relevant book, standard, lecture transcript and topic pages were retrieved and inspected. Rendered educational pages that were unavailable were replaced by the publishers' accessible textbook source files where applicable.

The [reference catalog](../content/curated/dsa-references.json) attaches sources per item. [Retrieval evidence](dsa-research-evidence.json) records the 29 used reference entries, URLs, retrieved sizes and content hashes. Some entries point to different sections of the same book/page; they are not 29 independent expert reviews.

Exam-alignment evidence remains in [RESEARCH.md](RESEARCH.md). The user's scope and a foundation-first revision level determine the selection, without asserting exact past-paper frequencies. This is model-assisted technical review, not independent human expert certification or an official/authenticated IBPS paper. Automated checks establish the stated worked results; conceptual relevance and unique-best-answer interpretation also depend on the documented review.

## Source and progress compatibility

[dsa-r2.txt](../content/curated/dsa-r2.txt) is the canonical authored source. [build_dsa.py](../tools/build_dsa.py) generates stable IDs `dsa-r2-001` through `dsa-r2-150` and deterministic option shuffling. Legacy generation remains to preserve unrelated subjects' IDs and random state.

All legacy `dsa-001` through `dsa-250` IDs are retired, including earlier retirements. Fresh IDs avoid attaching old attempts to unrelated replacement questions. Old session snapshots and personal edits remain available; stale stock imports cannot restore retired questions to current practice. The same bank ships in the web app and signed Android 2.4 APK.
