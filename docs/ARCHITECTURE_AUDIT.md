# Computer Fundamentals & Architecture revision — 21 October 2026

This revision replaces 33 older items with **75 questions**, following the user's request for architecture plus processes/threads/states, memory, scheduling, paging and deadlock. The concurrent [Web Technology revision](WEB_AUDIT.md) replaces 20 with 25. All **981 existing question records outside these two subjects remain exactly unchanged**, including the separate 100-question OS topic. [Change evidence](architecture-r2-change-evidence.json) compares the release with commit `64602727828aff726ad5adeed2163c283d932e08`.

## Coverage

| Subtopic | Questions |
|---|---:|
| Data representation & digital logic | 10 |
| CPU, instruction cycle & I/O | 12 |
| Memory hierarchy & storage | 10 |
| Processes, threads & states | 12 |
| Scheduling & performance | 9 |
| Paging & virtual memory | 12 |
| Deadlock & synchronization | 10 |
| **Total** | **75** |

The first 32 questions cover bits/units/binary/hexadecimal, gates and state-holding circuits, UTF-8, stored-program organization, ALU/control/registers/ISA, load-store design, address capacity, pipelines/hazards, DMA/interrupts/boot, caches and locality, SRAM/DRAM, flash, volatility and cache blocks.

The remaining 43 address the user-listed OS foundations through concise definitions and short applications: process instances and thread sharing, independent thread execution contexts, concurrency/parallelism, basic process states, PCB/context/mode transitions, dispatch and preemption, FCFS/SJF/SRTF/RR/aging, response time, address spaces/TLB/protection/offsets, demand paging, dirty pages, fragmentation/segmentation/thrashing/replacement, privileged mappings, resource-deadlock conditions, ordering/avoidance/graphs, starvation/livelock, races, semaphores/mutexes and recovery.

There are **71 conceptual/application questions and four short checked cases**: KiB conversion, unsigned binary conversion, address-count calculation and an SRTF next-task decision. No long scheduling timelines, complex paging arithmetic, cache geometry calculations or Banker's matrices were added.

## Relation to the OS topic

The user's requested scope overlaps the existing 100-question OS topic. That topic is preserved exactly. This integrated set combines hardware with those essential foundations; it is not 75 entirely distinct concepts absent from the rest of the bank. Existing detailed OS exercises remain in the OS pool. New stems are unique across the complete bank, and the revision avoids adding further long drills for the same algorithms.

## Accuracy checks

Every stem, five choices, key and explanation received a technical review. Explicit assumptions keep simplified models separate from implementation details:

- Octet and KiB terminology is unambiguous; the conversion is unsigned and the address-count example states byte addressing.
- PC/IR roles use a basic instruction-cycle model. ISA differs from microarchitecture, and pipelining improves throughput without guaranteeing lower latency for each instruction.
- DMA reduces CPU copying rather than eliminating all CPU/OS involvement. The loader's role is distinguished from runtime scheduling.
- Powered SRAM and DRAM have different refresh mechanisms. Ordinary RAM is volatile; flash-based firmware need not be immutable.
- Cache misses, TLB misses and nonresident/protection faults are different events. A resident read-only page can still fault on a prohibited write; a TLB miss does not itself require demand-page disk I/O.
- Shared thread address spaces do not imply shared register values or identical stacks. Mode changes need not select a new process, and a context switch does not inherently copy or swap out all process memory.
- Process states, ready eligibility and actual CPU dispatch are distinguished. RR assumptions and the single-CPU SRTF comparison are stated.
- Page/frame offsets are preserved, dirty pages require suitable preservation before reuse, and fragmentation categories are not conflated. FIFO recency differs from LRU, while theoretical optimal replacement needs future references.
- The global ordering example specifies its two lock types. Banker's availability alone is insufficient; unsafe is not synonymous with already deadlocked. Cycles have different implications for single- and multiple-instance resources.
- Starvation, livelock, races and deadlock have distinct meanings. Correct use and participating accesses are stated for mutex protection; recovery requires appropriate resource cleanup.

[References](../content/curated/architecture-references.json) are attached per item. [Research evidence](architecture-research-evidence.json) records 28 retrieved sources with checksums: authored OSTEP chapters, University of Illinois Chicago course notes, MIT Computation Structures, NIST binary prefixes, Unicode, Microsoft boot-stage guidance and University of York architecture explanations. Relevant passages and extracted PDFs were inspected. Failed guessed MIT/NIST paths were replaced with valid official paths; UEFI specification retrieval returned403 and was not counted as successful evidence.

The existing [exam preparation research](RESEARCH.md) supports concise degree-level foundations and applications, rather than predicted weights. User scope governs this integrated selection; these are not authenticated previous-year questions and no exact topic frequency is claimed. The technical/model-assisted review is not independent human expert certification.

## Integrity and app verification

Canonical source: [architecture-r2.txt](../content/curated/architecture-r2.txt), IDs `architecture-r2-001` through `architecture-r2-075`. All 33 previous architecture IDs are retired. The checker parses the displayed inputs independently for the four cases and enforces coverage, canonical-source agreement and retirements. [The item ledger](question-audit.csv) and reviewed hashes cover every shipped record.

Browser coverage checks all seven filters, a scored attempt and a TLB revision card with its answer, explanation and source at 320px. Existing offline/update/storage/download regressions remain in place. The same bank ships in signed Android 2.9; see [VALIDATION.md](VALIDATION.md).
