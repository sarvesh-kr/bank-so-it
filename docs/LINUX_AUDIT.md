# Linux & Shell R2 audit — 21 October 2026

The topic contains **75 newly curated questions**, replacing the preceding 86. The scope follows the user's request for Linux foundations, important commands, users/groups, permissions, shell basics and shell programming. The other **930 records are unchanged**, including the networking, DBMS, OS and DSA revisions. [Change evidence](linux-r2-change-evidence.json) compares the records against commit `34b15ea646bd55d841ff8fe788c560095ceab54e`.

## Coverage

| Area | Questions |
|---|---:|
| Linux foundations and navigation | 10 |
| Files, text and search | 16 |
| Users, groups and permissions | 14 |
| Processes, storage and services | 10 |
| Shell operators and expansion | 10 |
| Bash programming basics | 15 |
| **Total** | **75** |

There are **58 conceptual/application items and 17 executable examples**. Command coverage includes pwd, cd, ls, man/help, mkdir/rmdir, cp/mv/rm, ln, cat/less, head/tail, grep/find, sort/uniq/wc, cut/sed/awk, whoami/id, usermod, sudo, chown/chgrp/chmod, umask, ps/top, kill, fg/bg/jobs, df/du/free, mount, systemctl, tar, ss and ip. Explanations distinguish nearby commands without requiring specialist administration knowledge.

Shell coverage includes PATH, stdout/stderr/stdin, redirection, pipes, conditional execution, quoting, command substitution, exit status, export, globbing, shebangs, assignments, arithmetic, read, tests, conditionals, loops, case, functions and positional parameters. Advanced regular-expression puzzles, lengthy scripts, distro package-manager trivia, kernel tuning and complex sed/awk programs are omitted.

## Executed-answer evidence

The [case fixtures](../content/curated/linux-r2-cases.json) supply the exact scripts displayed in the app. The [checker](../tools/check_linux.py) verifies that displayed text matches the fixture, then runs it through [linux_cases.py](../tools/linux_cases.py). Each script runs in a fresh temporary working directory using Bash with default options, no startup profiles and a controlled C locale/PATH. Output is compared with the independently authored choices, and nonzero final status or unexpected stderr fails the check. Temporary files are removed after each case.

| Area | Cases | Checked results |
|---|---:|---|
| Text utilities | 3 | cut fields, global sed substitution, awk fields |
| File modes | 3 | Symbolic chmod 640, file umask result 644, directory umask result 750 |
| Shell expansion/status | 3 | Single/double quotes, quoted "$@", false followed by "$?" |
| Bash programming | 8 | Integer division, empty-string test, for/while/case, function status, argument count/value, sort/uniq/wc pipeline |
| **Total** | **17** | |

The results and scripts are recorded in [linux-quality-summary.json](linux-quality-summary.json). Cases use ordinary GNU/Linux tools and awk-compatible field semantics; no GNU-awk-specific extension is required. Script outputs preserve meaningful whitespace and internal line breaks; terminal newlines are omitted when comparing the displayed answers. Quiz options and Quick revision preserve internal output line breaks; a browser check verifies the visible two-line quoting answer. The authored source uses ↵ as an output-line separator that the loader converts into an actual newline.

## Review conventions

Every stem, five choices, selected answer and explanation received a technical review against attached manuals. The [per-item ledger](question-audit.csv) and [review register](../content/review/review-register.json) preserve reviewed hashes/dates. CI rejects content that no longer matches its recorded review.

- The kernel and shell have distinct roles. Root directory, root account and /root are not interchangeable. Case-sensitive filenames and conventional filesystem layout are qualified rather than claimed for every Linux configuration.
- Commands are interpreted under their stated GNU/Linux/Bash context. find filename patterns are quoted, grep searches content, uniq handles adjacent duplicates and wc -l counts newline characters. tail -f is distinguished from options used to follow rotated filenames.
- Password-hash placement assumes a conventional local shadow-password setup. usermod -aG appends supplementary groups; -G alone replaces the list and -g changes the primary group. sudo follows configured authorization policy.
- File read/write/execute bits differ from directory listing/search/modification. Symbolic chmod names its target classes explicitly. Umask removes requested mode bits; it does not add execute permission. The creation examples explicitly assume no default ACL because inherited ACLs can change the rules.
- Sticky-directory deletion/renaming restrictions include the file owner, directory owner and suitable privilege, in addition to ordinary permissions. Sticky, setgid inheritance and executable setuid are distinct concepts.
- kill defaults to SIGTERM, which can be handled or ignored; a sent signal does not prove completed termination. systemctl questions specify a systemd host and existing service name; enable is not the same as start.
- Pipes connect stdout to stdin; stderr is separate unless redirected. && checks exit status, not whether output is empty. Command substitution captures stdout, while arithmetic expansion computes integers.
- Single quotes preserve literals, double quotes allow expansion without ordinary splitting/globbing, and quoted "$@" retains separate arguments. Export affects child environments, not the parent or all future logins.
- Bash syntax is named explicitly. Script execution does not assume POSIX sh supports every Bash feature. Shebang selection and execute permission are separate. read -r handles backslashes; IFS controls a different aspect of input processing.
- Numeric/string/file tests, function return status versus printed output, break versus continue, and fixed-format printf versus variable data are distinguished. Script examples are short and use deterministic inputs rather than machine-specific process IDs or directory contents.

## Research basis and limits

Sources include the GNU Bash/GNU utility manuals hosted by man7.org, upstream GNU Coreutils manual and mode-documentation sources, Linux man-pages, shadow-utils, sudo documentation, procps, util-linux, iproute2 and systemd. The relevant manual/source sections were retrieved and inspected. GNU website endpoints were unavailable, so accessible upstream manual source and published manual-page copies were used.

The [reference catalog](../content/curated/linux-references.json) attaches sources to items. [Retrieval evidence](linux-research-evidence.json) records all 25 used reference entries, URLs and content hashes; references are supporting documentation, not independent expert certifications.

Exam-alignment evidence remains in [RESEARCH.md](RESEARCH.md). The user's foundation-first scope determines the selection without invented topic frequencies. This is model-assisted technical review, not independent human expert certification or an official/authenticated IBPS paper. Execution establishes the stated script outputs; conceptual accuracy and unique-best-answer interpretation also depend on review and the explicit assumptions.

## Source and progress compatibility

[linux-r2.txt](../content/curated/linux-r2.txt) is the canonical authored source. [build_linux.py](../tools/build_linux.py) supplies stable IDs `linux-r2-001` through `linux-r2-075` and deterministic choice shuffling. Legacy generation remains to preserve unrelated subjects' IDs and random state.

All legacy `linux-001` through `linux-100` IDs are retired, including earlier retirements. New IDs avoid attaching old attempts to unrelated replacement questions. Old session snapshots and personal edits remain available; stale stock imports cannot restore retired questions into current practice. The same bank ships in the web app and signed Android 2.5 APK.
