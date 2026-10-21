# Web Technology revision — 21 October 2026

This revision replaces 20 older items with **25 focused questions**. The concurrent [architecture revision](ARCHITECTURE_AUDIT.md) replaces 33 with 75. All **981 records outside the two subjects are exactly unchanged**, including all network/API questions. [Change evidence](web-r2-change-evidence.json) compares the release with commit `64602727828aff726ad5adeed2163c283d932e08`.

## Coverage

| Subtopic | Questions |
|---|---:|
| HTML, forms & CSS | 8 |
| JavaScript & DOM | 5 |
| HTTP & web services | 4 |
| Browser security & sessions | 5 |
| Data formats & browser storage | 3 |
| **Total** | **25** |

HTML/CSS covers language roles, external stylesheets, hyperlinks, form destination/method, password masking, class selectors, padding/margin and media queries. JavaScript/DOM covers browser behaviour, the document model, event listeners, const bindings and strict equality. HTTP/web services covers statelessness, Content-Type, common status codes and SOAP versus REST. Browser security covers origins, CORS, XSS, CSRF and cookie flags. Formats/storage covers JSON syntax, XML well-formedness versus validation and local/session storage.

All questions use concise foundations or short applications. There are no framework-specific coding exercises, long JavaScript traces or new networking calculations. The broader protocol/API material remains in Networks rather than being recreated wholesale here.

## Technical review

Every stem, five-option set, selected answer and explanation was checked against its attached reference. Important distinctions include:

- Markup, presentation and behaviour have different roles. HTML action/method attributes do not configure encryption; password masking does not protect transport by itself.
- DOM APIs manipulate a document model rather than implementing HTTP. JavaScript is distinct from Java; const does not deeply freeze objects, and strict equality is distinct from coercive equality or assignment.
- HTTP statelessness does not forbid server-side records or login sessions. Content-Type describes a representation rather than authorization or safety. Status codes identify outcomes, not a general proof of network reachability.
- SOAP is a messaging framework using XML technologies; REST is an architectural style and is not JSON-only.
- Origins compare scheme, host and effective port. CORS governs browser response sharing rather than granting payment authority or blocking every nonbrowser request.
- XSS and CSRF are distinct mechanisms. Cookie Secure and HttpOnly protect different aspects of handling; neither replaces authorization or all other browser-security controls.
- All five JSON choices are parsed independently; exactly the selected one is valid with the stated string key and number value. XML syntax alone does not establish conformance to a specified schema/DTD.
- Web Storage is client-side state, not authoritative account storage or automatically sent cookie headers. Local storage retention can be affected by user actions, browser policy and quotas; session storage is scoped to a page session.

[The reference catalog](../content/curated/web-references.json) attaches sources to items. [Research evidence](web-research-evidence.json) records 23 retrieved entries with URLs and hashes: WHATWG HTML/DOM/Web Storage, W3C XML/XML Schema/SOAP, IETF HTTP/JSON, OWASP, MDN and Fielding's REST dissertation. Relevant sections were inspected.

The user-defined Bank SO IT foundation-first scope and [existing preparation research](RESEARCH.md) guide selection. These are not authenticated past-paper questions; neither exact topic frequency nor a complete official granular syllabus is asserted. Technical/model-assisted review is not independent human expert certification.

## Integrity and app checks

Canonical source: [web-r2.txt](../content/curated/web-r2.txt), IDs `web-r2-001` through `web-r2-025`. All 20 previous web IDs are retired. The checker enforces scope, canonical-source agreement, retirements and unique JSON validity; reviewed hashes and [the item ledger](question-audit.csv) cover all shipped questions. Old stock imports cannot reintroduce retired material or overwrite reviewed built-ins; existing personal edits and historical snapshots retain their handling.

Browser checks cover all five topic filters, scoring, literal HTML displayed as text in a revision answer, a source-linked stylesheet revision card at 320px, and the JSON answer/explanation. Existing CSP/import/offline/update/download checks remain in place. The web app and signed Android 2.9 use the same 1,081-question bank. See [VALIDATION.md](VALIDATION.md).
