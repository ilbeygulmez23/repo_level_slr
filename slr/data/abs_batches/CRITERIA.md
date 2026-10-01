# Title/abstract screening instructions (reviewer 1)

SCOPE: systematic review of LLM-based repository-level code generation.

**CORE tier:** an LLM or agent produces a multi-file repository, library or application:
- NL, specification, README or requirements → repository or app (including web apps, microservices, CLI tools, and games built from scratch)
- skeleton/stubs → library
- executable or API reference → behaviourally equivalent repository (reconstruction, reproduction, paper → code repository)
- whole repository → repository translation or modernisation (re-implementation in another language or stack)
- methods, agents, multi-agent frameworks, and training environments or data for these tasks
- empirical studies of such systems

**CONTEXTUAL tier:** an LLM generates a function, class or file whose correctness depends on the surrounding repository (cross-file dependencies, project APIs) AND is evaluated by execution (tests). Examples: CoderEval, DevEval, RepoExec, EvoCodeBench. Also covers retrieval/context methods evaluated on such benchmarks.

**INCLUDE** only if all hold:
- English
- 2022 or later
- uses LLMs or LLM agents
- falls in the core or contextual tier
- primary contribution is a benchmark/dataset, a method/agent/training approach, or an empirical study

**EXCLUDE** codes (pick the most specific one):
- EC1: issue resolution, bug repair, patching, refactoring, performance optimisation, or feature addition / edits / in-place migration of an EXISTING repository (SWE-bench style)
- EC2: pure code completion (next line, span, infilling) evaluated only by similarity (EM/ES/BLEU). If a completion benchmark uses executable tests on repository-dependent code, treat it as contextual or unsure.
- EC3: isolated code generation without repository dependency (HumanEval-style, single-file snippets, class-level without repo context, text-to-SQL, domain snippets)
- EC4: output is not source code (documentation, tests only, code review, QA, summarisation, vulnerability/bug detection, repository understanding)
- EC5: not LLM-based
- EC6: secondary study (survey, SLR, review, position/vision paper, tutorial, thesis, editorial, opinion, blog)
- EC8: insufficient information (no abstract and an ambiguous title; 1–2 page abstract only)
- EC0: off-topic
- EC10: not a research article (dataset/software deposit, replication package, whitepaper, podcast)

**UNSURE:** use "unsure" when relevance cannot be decided from the title and abstract; these records go to full-text review. Be recall-oriented: for anything plausibly core, prefer unsure over a wrong exclusion. Decide only from the given title, venue and abstract; do not use external tools.

**OUTPUT:** `batchN_decisions.csv` with header `rid,decision,reason,tier,note`, exactly one row per input row. Write it with Python's csv module.
- decision: include | exclude | unsure
- reason: the EC code for exclude; empty otherwise
- tier: core | contextual for include/unsure; empty for exclude
- note: justification of at most 15 words, always filled (quote the key phrase)
