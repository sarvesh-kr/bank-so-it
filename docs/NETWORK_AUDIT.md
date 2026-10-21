# Networking and cybersecurity R2 — 20 October 2026

This revision supplies **200 questions** following the user's explicit Bank SO IT preparation scope. It replaces the previous 152-item network set. All 664 questions in other subjects remain unchanged, including option order and explanations; the before/after hashes are recorded in [change evidence](network-r2-change-evidence.json).

The target is direct foundational recall and short bank-IT applications. There are **ten short subnet calculations**. No channel-capacity formulas, Hamming calculations, stop-and-wait utilisation, bandwidth-delay products, recovery arithmetic or detailed fragmentation arithmetic are included. Identifying the slowest link is a simple conceptual bandwidth question, not a transfer-time drill.

## Coverage

| Area | Questions |
|---|---:|
| OSI and TCP/IP models | 16 |
| Devices and transmission media | 14 |
| Frames, packets and headers | 13 |
| IPv4, IPv6, classes, private addressing and NAT | 20 |
| Subnetting: two concepts and ten calculations | 12 |
| TCP, UDP and communication | 10 |
| Services and popular ports | 22 |
| Bandwidth and network fundamentals | 8 |
| SSL/TLS, cryptography and encoding | 21 |
| Firewalls and protective controls | 14 |
| Common attacks | 20 |
| Malware and virus types | 16 |
| CIA triad and general security | 14 |
| **Total** | **200** |

Ports include FTP, SSH, Telnet, SMTP, DNS, DHCPv4, HTTP/HTTPS, POP3, IMAP, NTP, SNMP, RDP, TFTP, LDAP and SMB. Explanations distinguish conventional defaults from configurable ports, SMTP transfer from submission, DNS UDP from TCP, FTP control from data, and explicit upgrades from implicit-TLS mail/directory ports.

The set covers phishing variants, pharming, on-path interception, ARP/DNS spoofing, DoS/DDoS, SYN flooding, brute force, spraying, stuffing, replay, injection, XSS and CSRF. Malware coverage includes file/boot/macro/resident/non-resident/polymorphic/multipartite/stealth viruses, worms, Trojans, ransomware, spyware, keyloggers, rootkits, botnets and logic bombs. Categories can overlap: questions identify the behaviour described rather than asserting that every classification is mutually exclusive.

## Accuracy review

Each stem, all five choices, selected key and explanation received a technical review for one best answer, clear assumptions, concise wording and relevance to the supplied topic map. Questions avoid undefined layer claims and misleading absolutes:

- Historical Class A/B/C defaults are distinguished from modern CIDR. Modern subnet counts include all-zero and all-one subnet numbers; RFC 1878 explicitly documents this practice.
- Usable-host calculations exclude network/broadcast addresses in ordinary LAN subnets. /31 and /32 special cases are not used in these drills.
- Conventional OSI presentation functions are distinguished from actual TLS/IPsec placement. SSL is identified as obsolete; HTTPS protection is not portrayed as proof that a business is honest.
- Hashing and encoding are distinguished from encryption. Public/private key roles, digital signatures, salt and message authentication are stated with their scope.
- NAT is not encryption; firewalls, VPNs, certificates and antivirus-related concepts do not promise universal protection.

All ten subnet answers are independently recomputed by `check_quality.py`, including masks, usable hosts, network/broadcast/range, subnet count and required host capacity. Sixteen port questions are checked against a compact snapshot of 24 IANA registry associations; the source CSV checksum and retrieval date are preserved in [registry evidence](../content/review/network-r2-port-registry.json). `check_network.py` enforces the count, coverage and numerical limit.

The complete wording, five choices, answer, explanation, sources and reviewed hash appear in [question-audit.csv](question-audit.csv). Exact content hashes in the review register make unreviewed edits fail CI. The canonical source is [network-r2.txt](../content/curated/network-r2.txt), with explicit stable IDs and a [reference catalog](../content/curated/network-references.json).

References include RFCs, IANA, ITU, NIST, OWASP, the Kurose/Ross networking lectures and selected Norton/Kaspersky explainers. RFC/IANA texts, OWASP guidance, NIST authentication guidance/publication pages and the vendor explainers were retrieved during review. Full NIST PDF downloads were blocked; the malware subtype review also used the retrieved explainers. This is a model-assisted technical review, not an independent human certification or a claim that these are authenticated previous-year questions. The user-provided scope governs this revision; no exact exam topic frequencies are asserted.

## Saved progress

New questions use `network-r2-*` IDs so old answers are not misattributed to different questions. All 152 former current-network IDs are retired, including seven introduced after the original 1,150-question baseline. Old imports cannot restore those stock items. Historical and unfinished attempt snapshots remain intact; current-bank statistics track the replacement set. Other subjects' progress is unchanged.

## Later protocol/API/blockchain/CDN supplement

The [21 October coverage supplement](NETWORK_SERVICES_AUDIT.md) adds 31 conceptual questions to the original 200 without changing those records. Current networking coverage is 231, still with ten subnet calculations. It adds explicit protocol functions/records/secure variants, API basics, blockchain and CDN. The current port checker validates 17 questions using the existing 24 IANA associations.
