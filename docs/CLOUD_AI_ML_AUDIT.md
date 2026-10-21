# Cloud, AI & ML Basics R2 audit — 21 October 2026

This revision replaces 47 older items with **50 conceptual questions**, split equally between cloud and AI/ML. There are **no numerical exercises**. All **956 existing question records outside this topic are exactly unchanged**. The same release also adds 29 new networking items; see the [network supplement](NETWORK_SERVICES_AUDIT.md). [Change evidence](cloud-ai-ml-r2-change-evidence.json) compares all non-cloud records with commit `42206bfdb77f1ae551d2695f9b9a31c8a496bc20`.

## Coverage

| Area | Questions |
|---|---:|
| Cloud foundations and models | 10 |
| Virtualization, storage and operations | 10 |
| Cloud security and banking controls | 5 |
| AI and learning foundations | 8 |
| ML algorithms and evaluation | 12 |
| AI applications and responsible use | 5 |
| **Total** | **50** |

Cloud coverage includes NIST characteristics; elasticity, resource pooling and metering; IaaS/PaaS/SaaS; private/public/community/hybrid deployment; hypervisors, Type 1/2, containers, images and Kubernetes; scaling, load balancing, serverless, object storage, RPO/RTO, shared responsibility, least privilege, encryption and bank outsourcing/exit controls.

AI/ML coverage includes the AI/ML/deep-learning relationship; supervised, unsupervised and reinforcement learning; classification/regression; features/labels; training/inference; expert systems; logistic regression, decision trees, random forests, naive Bayes, k-NN and SVM; overfitting, underfitting distinctions, class imbalance, dataset splits, leakage and fraud metrics; NLP, CNNs, generative AI, hallucinations and responsible banking use.

The focus is concise definitions, distinctions and short application scenarios. Exclusions include metric calculations, optimization/gradient derivations, model-training code, PCA calculations, detailed neural architecture, distributed-systems design patterns, vendor pricing/version trivia and detailed operational commands. Related concepts already present in warehousing/mining remain useful in their subject context, without repeating identical question stems.

## Technical review

Every stem, all five options, selected answer and explanation was reviewed against attached documentation or editorial technical references. Nearby concepts were used as distractors where practical. [The per-item ledger](question-audit.csv) records all questions, references and reviewed hashes; [the review register](../content/review/review-register.json) rejects changes made after review.

Review conventions include:

- NIST's five characteristics and service/deployment definitions are explicit. Private cloud need not be on premises; public cloud does not mean unrestricted data access. Hybrid follows NIST's connected, distinct-infrastructure definition; several subscriptions alone do not establish it.
- Elasticity includes releasing resources as demand falls. Horizontal scaling adds instances; vertical scaling enlarges one. Load balancing distributes traffic and is distinct from adding capacity.
- Conventional containers share a host kernel; VMs have guest kernels. A container image is a template and an instance can be running or stopped. Kubernetes and serverless do not eliminate application/security responsibilities.
- RPO concerns acceptable data loss in time and RTO a restoration-time target. They are objectives, not guarantees. Shared responsibility varies by service and agreement. Data encryption requires suitable key/access controls.
- Banking cloud questions concern due diligence, applicable requirements, oversight, audit/access, continuity and exit planning. They do not claim all banking data has one universal location rule or that outsourcing transfers accountability away from the bank.
- ML/deep learning are nested within the broader AI field. Supervised targets can be categories or numbers. Features and targets, training and inference, and rule-based inference and learned models are distinguished.
- Random forest is explicitly bootstrap-based in the question; naive Bayes assumes conditional independence given the class. k-NN is specified as a classifier. SVM asks only the large-margin idea, with no optimization calculations.
- The overfitting item contrasts high training performance with poor new-data performance; its explanation also distinguishes underfitting. Class imbalance can make overall accuracy misleading. Validation/tuning is separate from final held-out testing; future outcomes available only after a loan decision are leakage.
- Fraud is explicitly the positive class before identifying a false positive. Recall concerns actual positives; precision concerns predicted positives. No confusion-matrix arithmetic is required.
- CNNs are associated with local image patterns without claiming exclusivity. Generated content can be false; regulatory statements require authoritative verification. Appropriate governance includes privacy, fairness, explanations, oversight and monitoring rather than an unsupported blanket prohibition or guarantee.

## Research and relevance

[The reference catalog](../content/curated/cloud-ai-ml-references.json) includes NIST SP 800-145 and AI RMF, RBI's 2023 IT outsourcing directions, official Docker/Kubernetes/AWS documentation, Red Hat's virtualization guide, Google's ML materials, scikit-learn's algorithm documentation, IBM's AI/NLP/generative-AI explanations and Britannica's expert-system entry. Relevant source sections were retrieved and inspected, including extracted NIST PDFs. [Retrieval evidence](cloud-ai-ml-research-evidence.json) records used URLs, final URLs and content hashes. An IBM expert-system URL that redirected to a topic index was excluded; a scikit-learn stable-page retrieval failure was replaced with its versioned 1.7 nearest-neighbour documentation.

[RESEARCH.md](RESEARCH.md) retains the preparation outline and recalled-paper analysis. This selection follows the user's foundation-first Bank SO IT scope. The available evidence does not establish exact cloud/AI topic frequencies or authenticate these questions as previous-year questions. Technical/model-assisted review is not independent human expert certification.

## Compatibility and validation

[cloud-ai-ml-r2.txt](../content/curated/cloud-ai-ml-r2.txt) is the canonical source. IDs `cloud-ai-ml-r2-001` through `cloud-ai-ml-r2-050` avoid attaching historical attempts to replacement questions. All 65 legacy `cloud_ai_ml-001` through `cloud_ai_ml-065` IDs are retired, including earlier exclusions. Other subjects' IDs, option order and records are unchanged. Personal edits and earlier session snapshots remain available.

The topic checker enforces scope, conceptual-only kinds, source agreement and retirements. Browser coverage includes topic filtering, scoring and the false-positive revision card with answer, explanation and references at 320px. The existing production download fix and its Chromium/WebKit online/offline checks remain in place. The same bank ships in the web app and signed Android 2.7 APK. Removing the old precision calculation reduces whole-bank independent computed-result checks from 125 to 124; that does not count conceptual source review as an executed proof. See [VALIDATION.md](VALIDATION.md).
