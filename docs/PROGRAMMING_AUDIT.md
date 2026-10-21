# Programming & OOP revision — 21 October 2026

This revision replaces 60 older items with **75 focused questions**, comprising 70 concepts and five short executed Python outputs. A concurrent [software/banking revision](SE_BANK_IT_AUDIT.md) replaces 68 questions with 50. All **909 existing question records outside these two subjects are exactly unchanged**, including option order, keys, explanations and references. [Change evidence](programming-r2-change-evidence.json) compares the release with commit `db458fb00b8bf44ac9f0be38300a6a958ab395c3`.

## Coverage

| Subtopic | Questions |
|---|---:|
| OOP foundations | 8 |
| Python types & basics | 12 |
| Python functions & OOP | 8 |
| Python short output | 5 |
| Java runtime & core types | 9 |
| Java classes & interfaces | 11 |
| C pointers & strings | 8 |
| C++ classes & strings | 14 |
| **Total** | **75** |

The 33 common-OOP/Python questions cover class/object, encapsulation, abstraction, inheritance, polymorphism, overloading/overriding, composition and access control; Python integers, list/tuple/dict/set/str/None, range, slices, identity/equality and indentation; `__init__`, `__new__`, `self`, attributes, overriding, argument collection, mutable defaults and exception handling. The five output questions test instance initialization, aliasing, slicing, set uniqueness and overriding using short, deterministic Python 3 programs.

The 20 Java questions cover javac/class files/bytecode, JVM/JDK roles, portability, primitive/reference types, string equality/immutability, argument passing, checked exceptions, interface contracts and modern method/field rules, single class inheritance with multiple interfaces, abstract classes, garbage collection, overloading, overriding, static/final and constructors. Language references use Java SE 21; the selected foundations do not require advanced version-specific features.

The 22 C/C++ questions cover address/dereference, argument passing, arrays, null-terminated strings, strlen/strcat/strcmp and undefined behaviour; C++ access defaults, multiple/multilevel inheritance, virtual/pure-virtual methods, virtual destruction, references, RAII and matching new[]/delete[]; std::string size/length/append/substr/find/c_str. The scope avoids long execution puzzles, advanced template/metaprogramming, compiler trivia and attempts to predict undefined behaviour.

## Technical review

Every stem, five-option set, selected answer and explanation was reviewed. Particular distinctions include:

- Python tuple immutability does not freeze a referenced list. Dict keys and set elements must be hashable; empty braces create a dict. Python strings are Unicode text, and identity is distinct from equality.
- `__new__` creates an instance; `__init__` initializes it and returns None. `self` is a convention, not a reserved word. Mutable defaults are evaluated at function definition and may be shared across calls.
- Java class files contain bytecode and metadata; a compatible JVM/runtime and libraries are still required. JVM implementation is not restricted to interpretation. Modern interfaces can have implemented methods; their fields are public static final.
- Java argument passing copies values, including references. Reassigning a reference parameter differs from mutating a shared object. A final reference does not make its referent immutable; garbage collection is not guaranteed to occur at a chosen time.
- C strings use a null character rather than the digit zero or a null pointer. Strlen excludes the terminator and counts char units, while strcmp guarantees the sign of unequal comparisons rather than exact values of −1 or 1. Null dereference has undefined behaviour, with no portable fixed output or guaranteed crash.
- C++ virtual dispatch, pure virtual functions, appropriate virtual destruction and allocation/deallocation pairs have distinct roles. Reference assignment does not reseat a reference. String size/length count char elements; substr's second argument is a count, find uses npos for failure, and c_str's pointer must not be freed or written through.

[The reference catalog](../content/curated/programming-references.json) attaches precise sources to items. [Research evidence](programming-research-evidence.json) records 24 retrieved reference entries with URLs and hashes: official Python documentation, Oracle Java language/JVM/API/tool specifications, the C committee draft, the C++ working draft and C++ Core Guidelines. Relevant source sections and the extracted C PDF were inspected. An OpenJDK page returned403 and is not used; the JDK/tool item cites Oracle javac and JVM documentation instead.

The whole-bank checker executes each exact displayed Python program in an isolated interpreter and compares output with the selected answer. Additional local C11 and C++17 compiler spot checks exercised string operations, reference assignment and virtual dispatch/destruction; these are supplementary semantic checks rather than a proof of every conceptual claim. No Java compiler execution is claimed; Java items were checked against Oracle specifications. There are no Java or C/C++ output puzzles in the bank.

The user-defined foundation-first Bank SO IT scope and [existing preparation research](RESEARCH.md) guide selection. This is not an assertion of exact past-paper frequencies or authenticated previous-year questions. Technical/model-assisted review is not independent human expert certification.

## Integrity and application checks

Canonical source: [programming-r2.txt](../content/curated/programming-r2.txt). New IDs are `programming-r2-001` through `programming-r2-075`; all 60 previous programming IDs are retired. Legacy source generation remains for reproducibility of other subjects, but its programming questions do not enter current study pools. Old stock imports cannot restore those IDs or overwrite reviewed built-ins; personal edits and old session snapshots retain existing handling.

The checker enforces coverage, canonical-source agreement, the five output items and retirements. Reviewed hashes and [the item ledger](question-audit.csv) cover all shipped questions. Browser coverage includes all eight filters, a scored output attempt and a multiline initialization revision card with answer, explanation and sources at 320px. The same 1,034-question bank is embedded in signed Android 2.8. See [VALIDATION.md](VALIDATION.md).
