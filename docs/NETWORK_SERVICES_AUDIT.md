# Protocol, API, blockchain and CDN coverage supplement — 21 October 2026

Networking now contains **229 questions**. All 200 earlier records are exactly unchanged; **29 new conceptual questions** fill gaps identified by the user's protocol/API/blockchain/CDN checklist. There are no additional numerical exercises. The original ten subnet calculations remain unchanged. [Change evidence](network-supplement-change-evidence.json) compares records with commit `42206bfdb77f1ae551d2695f9b9a31c8a496bc20`.

## Checklist and additions

| Requested area | Existing coverage | New coverage |
|---|---|---|
| DNS | Purpose, TCP/UDP 53, A/MX, attack scenarios | AAAA, CNAME, PTR |
| DHCP | UDP 67/68 and DORA | Configuration purpose and relay agents |
| SMTP | TCP 25, submission distinction in explanation | Mail sending/transfer role |
| POP/POP3 | TCP 110 and TLS 995 in explanation | Retrieval, optional rather than automatic deletion |
| IMAP | TCP 143 and server mailbox synchronization | Paired implicit-TLS port question: 993/995 |
| SSH | TCP 22 and secure remote-access explanation | Secure remote login and host-key identity |
| FTP | Control/data channels and ports | Plain FTP confidentiality limitations; SFTP versus FTPS |
| HTTP/HTTPS | 80/443, TLS, certificates, trust limits, HTTP/3 distinction | API methods, representations and status semantics |
| Email TLS | Secure variants noted in explanations | Implicit TLS versus STARTTLS |
| APIs | Limited material elsewhere in the bank | Interface/endpoint basics, REST, formats, GET/PUT, 401/403, OAuth, rate limits and confidential keys |
| Blockchain | No prior questions | Distributed ledger, hash links, permissions, consensus, smart contracts and Bitcoin relationship |
| CDN | Prior cloud question removed during the concurrent cloud revision | Edge delivery/caching and no-store versus private/no-cache |

The additions contain 12 protocol/service items, nine API items, six blockchain items and two CDN items, with IDs `network-r2-201` through `network-r2-229`.

## Accuracy conventions

Every new stem, five options, answer and explanation was reviewed against its attached references. DNS records distinguish addresses, aliases, mail routing and reverse lookup. DHCP relay does not imply routers forward every broadcast. POP3 does not require deleting every retrieved message. SMTP sends/transfers; POP3 and IMAP access mailboxes. SSH host identity still needs verification. SFTP is carried over SSH and differs from FTP secured with TLS. STARTTLS is an upgrade and does not guarantee protected fallback when policy permits an unprotected connection.

The existing IANA snapshot includes TCP 993/995. The network checker now independently checks 17 port questions against 24 retrieved associations, including the new implicit-TLS pair. No new unchecked port facts were introduced.

REST is an architectural style, not a mandatory JSON format. HTTP methods have intended semantics independent of encryption. HTTP 401 concerns valid authentication credentials; 403 is refusal and does not universally prove authentication succeeded. OAuth provides delegated authorization rather than a complete authentication protocol. Rate limiting does not replace authorization, and deliberately confidential API keys must not be confused with publishable identifiers.

Blockchain is tamper-evident/resistant under system assumptions rather than an absolute guarantee of immutability or truthful inputs. Consensus coordinates ledger agreement; not all chains use proof of work. Permissioning concerns participation rights. Smart-contract code can contain bugs and does not automatically establish legal enforceability. Blockchain uses extend beyond Bitcoin.

CDNs deliver suitable content through distributed edge locations; not every customer-specific response should be publicly cached. HTTP `no-store` forbids storage by HTTP caches, whereas `private` alone excludes shared caches and `no-cache` requires validation before reuse. Cache controls do not replace access control.

## Sources, scope and compatibility

Sources include IETF RFCs, the existing IANA snapshot, Fielding's REST dissertation, OWASP, OpenSSH/OpenBSD, MDN and NIST IR 8202. Relevant sections were retrieved and inspected, including the extracted NIST PDF. [Research evidence](network-supplement-research-evidence.json) records source URLs and hashes. The source catalog preserves existing reference entries so the earlier 200 questions' reviewed hashes and option order remain unchanged.

This is foundational Bank SO IT practice following the user's checklist, without claims of exact question frequencies or authenticated past-paper provenance. [NETWORK_AUDIT.md](NETWORK_AUDIT.md) records the original 200-question revision; [CLOUD_AI_ML_AUDIT.md](CLOUD_AI_ML_AUDIT.md) records the concurrent 50-question cloud/AI update. The full release has 1,035 questions; 756 existing records outside these two subjects are unchanged.

No existing network IDs are replaced. Personal edits and historical snapshots remain available. Reviewed-hash enforcement, topic counts, port checks, new-topic browser filters, a CDN/no-store revision card, and the production Chromium/WebKit download/update tests cover this release. The same bank is bundled in signed Android 2.7.
