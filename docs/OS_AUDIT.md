# Operating Systems R2 audit — 21 October 2026

The OS topic contains **100 newly curated questions**, replacing the preceding 73. The user's request determines the scope: process states, architecture, memory, scheduling, deadlocks and other useful OS fundamentals, with short applications suited to final revision. The other **873 question records are unchanged**, including all 200 DBMS and 200 networking items. [Change evidence](os-r2-change-evidence.json) records that comparison against commit `7d7afbb42e9b0a3d415c32b3c7a249e3d432c84d`.

## Coverage

| Area | Questions |
|---|---:|
| OS roles and architecture | 10 |
| Processes and states | 14 |
| Threads and IPC | 8 |
| CPU scheduling | 14 |
| Synchronization | 12 |
| Deadlocks | 12 |
| Memory allocation and addressing | 10 |
| Virtual memory and replacement | 10 |
| Files, storage and I/O | 10 |
| **Total** | **100** |

There are **90 conceptual/application questions and ten short worked exercises**. Coverage includes user/kernel mode, system calls, interrupts, monolithic/microkernel/layered designs, real-time systems, virtualization, process transitions, PCBs, context switches, fork/exec, zombies/orphans, user/kernel thread mapping, IPC, FCFS/SJF/SRTF/RR/priority/MLFQ scheduling, aging, locks/semaphores/monitors, race conditions, deadlock conditions/prevention/avoidance/recovery, address translation, paging/segmentation/TLBs, fragmentation, locality, thrashing, replacement, copy-on-write, files/links/allocation, DMA, buffering/caching, spooling and disk scheduling.

Long scheduling tables, complex resource matrices, multilevel page-table bit puzzles, detailed disk geometry and kernel implementation internals are omitted. Short recognition and distinction questions receive more space than numerical variants.

## Worked-answer evidence

The [checker](../tools/check_os.py) parses the inputs from the actual displayed question, independently simulates or calculates the result, then compares it with the authored answer. It records traces in [os-quality-summary.json](os-quality-summary.json).

| ID | Exercise | Verified result |
|---|---|---|
| os-r2-043 | FCFS average waiting time | 5 time units |
| os-r2-044 | SJF average turnaround time | 6 time units |
| os-r2-045 | Round Robin completion of P2 | 7 |
| os-r2-046 | SRTF completion of P2 | 7 |
| os-r2-069 | Banker's safe sequence | P2, P1, P3; the only safe choice listed |
| os-r2-079 | Page/frame address translation | 7268 |
| os-r2-080 | Internal fragmentation | 2 KiB |
| os-r2-089 | FIFO faults, including initial loads | 5 |
| os-r2-090 | LRU faults on the same references | 4 |
| os-r2-100 | SSTF total head movement | 50 tracks |

Scheduling simulations track service one time unit at a time. Banker's analysis enumerates all completion orders; there are two safe sequences in the state, but only one appears among the choices. Page simulations distinguish FIFO insertion order from LRU access order. The disk case checks that no equal-distance tie requires an unstated rule.

## Review conventions

Each stem, five-choice set, selected key and explanation received a technical review using the attached sources. The per-item [audit ledger](question-audit.csv) and [register](../content/review/review-register.json) preserve reviewed hashes and dates. CI rejects later content changes without renewed review.

- Process-state questions distinguish Ready from Waiting and preemption from blocking. Ready Suspended explicitly belongs to an extended model. Zombie, orphan and fork/exec questions specify Unix/POSIX/Linux where relevant.
- Architecture questions distinguish privilege boundaries from mere software organization. Modular monolithic kernels remain monolithic; a microkernel does not mean every OS service disappears.
- CPU exercises state arrivals, queue order, burst assumptions and zero overhead. Turnaround, response and waiting are distinct measures. SJF's optimum claim is qualified to simultaneous arrivals and known bursts.
- Mutex ownership is not equated with general semaphore signaling. Semaphore wait is described by its permit behaviour, avoiding implementation-dependent negative-counter rules. Condition waits release/reacquire the mutex and require predicate rechecking.
- A resource graph cycle is sufficient for deadlock only under the stated single-instance condition. Unsafe does not mean already deadlocked. Banker's Need is Maximum minus Allocation; completed processes return their allocated resources.
- Address translation preserves the page offset. KiB means 1,024 bytes. Internal and external fragmentation are distinct; paging does not require contiguous frames for an entire process.
- A TLB miss is not automatically a page fault, and a page fault need not read from disk. FIFO hits do not refresh insertion order; LRU hits do refresh recency. Belady's anomaly is not attributed to LRU.
- File permissions are not encryption. Hard links share an inode; directory entries hold filenames. DMA still requires setup/completion handling. SCAN and LOOK use explicit endpoint conventions.

## Research basis and limits

Technical sources include Remzi and Andrea Arpaci-Dusseau's [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/), [UIC Operating Systems notes](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/), [POSIX/Linux manuals](https://man7.org/linux/man-pages/) and [Linux kernel documentation](https://docs.kernel.org/). Relevant PDFs/pages were retrieved and checked. The [reference catalog](../content/curated/os-references.json) attaches sources to each question; [retrieval evidence](os-research-evidence.json) records URLs and retrieved-content hashes.

The preparation scope and recalled-paper evidence remain documented in [RESEARCH.md](RESEARCH.md). They support foundational OS preparation without establishing exact question frequencies or an authenticated complete paper. The selection follows the user's explicit request. This is a model-assisted technical review, not independent human expert certification or an official IBPS paper. Automated calculations verify worked results; conceptual relevance and uniqueness also depend on review and stated assumptions.

## Source and progress compatibility

[os-r2.txt](../content/curated/os-r2.txt) is the canonical authored source. [build_os.py](../tools/build_os.py) supplies stable IDs `os-r2-001` through `os-r2-100` with deterministic option shuffling. Older source rows remain only to preserve generation IDs and random state for other subjects.

All legacy `os-001` through `os-103` IDs are now retired, including earlier retirements. Fresh IDs prevent old attempts being counted against unrelated replacement questions. Old session snapshots and personal edits remain available; stale stock imports cannot restore retired questions to current practice. The web app and signed Android 2.3 APK contain the same bank.
