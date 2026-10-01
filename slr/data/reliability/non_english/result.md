# Re-screening of two records excluded only for language

Date: 2026-10-01. Criteria: `slr/data/ft_batches/FT_CRITERIA.md`, with the English-only criterion dropped.

| key | ft_decision | ft_reason | full text |
|---|---|---|---|
| doi:10.14801/jkiit.2026.24.5.75 | exclude | EC8 (would be EC7 once the English version is added) | not obtained (paywalled DBpia) |
| doi:10.18690/um.feri.7.2026.16 | exclude | EC1 | obtained (UM Press OA PDF, 17 pp., read in Slovenian) |

Neither record is included, so no extraction rows or notes are needed.

---

## 1. doi:10.14801/jkiit.2026.24.5.75: Atomic Logic Sheet (JKIIT 24(5):75–92, 2026)

Authors: Mansu Kim, Museong Choi, Eunyoung Wang, Sungtaek Chung (Tech University of Korea).

**Full-text attempts**
- OpenAlex: `is_oa=false`, `oa_status=closed`. There is no `oa_url` and no repository copy. The only location is the DOI landing page.
- doi.org resolves to DBpia NODE12870587. The page has `FREE_YN: "N"` and `PDF_YN: "N"`, and the article is available only through an institutional login or purchase. It has 18 pages. The page shows only the Korean and English abstracts and the keywords: LLM, atomic logic sheet, prompt engineering, AI sycophancy, schema hallucination.

**What the abstract establishes (read in Korean, consistent with the English abstract)**
- The study proposes ALS, a markdown-structured representation of business logic. It runs a three-group comparison in a Warehouse Management System (WMS) domain with a Claude Code CLI agent: A = requirements only, B = natural-language design document, C = ALS.
- Logic compliance rate (LCR): A 90.7%, B 94.7%, C 96.1%. Conflict detection rate (CDR): A 0.0%, B 17.5%, C 100%. Schema deviation (SDC): A 44.1, B 1.0, C 3.5.
- The abstract does not say whether the agent produces a multi-file application or a repository. It also does not say how LCR, CDR and SDC are scored.

**Related English version (found while searching; not in the pool)**

Kim, Choi, Shim and Chung, "Structured Business Logic Injection for LLM-Based Code Generation: What a Design Document Must Carry", *Electronics* 15(17):3884, published 2026-08-28, doi:10.3390/electronics15173884. It is gold OA and I read the full text. It is clearly an extended version of the JKIIT study: same ALS, same WMS domain, same Claude Code setup, same LCR/CDR/SDC metrics. It adds a fourth condition (B+, prose with the same content as ALS) and two replications, and its numbers differ from JKIIT (LCR A 93.1 / B 96.8 / B+ 97.7 / C 96.8; CDR 10.0 / 43.1 / 100 / 100). Setup in the English version:
- Claude Sonnet 4.5 in non-interactive Claude Code builds a Java 17 / Spring Boot 3 / PostgreSQL WMS backend with 19 tables. It works through four sequential feature tasks (T1–T4) and then eight conflicting change requests (T5). There are 20 runs per condition.
- Evaluation is entirely static. LCR is a rule-based checklist script over 98 items. SDC compares the generated schema against a reference DDL. CDR is adjudicated by two human raters (κ = 0.993 and 1.000) and cross-checked with a byte-level diff. The authors state that compilation and test pass rates are not measured.

**Decision: exclude, EC8**
- No full text could be obtained, and the abstract alone does not show that the output is a multi-file repository or application. It also does not say how the evaluation works.
- If the Electronics paper is added to the pool, JKIIT becomes **EC7**, as the earlier and shorter version of doi:10.3390/electronics15173884.
- **Recommendation:** add doi:10.3390/electronics15173884 as a snowball candidate. It is a borderline core candidate: task nl-to-repo (agent-built multi-file Spring Boot backend), contribution method;empirical, language Java, evaluation other;human (static checklist plus schema comparison against a reference DDL), venue Electronics (MDPI) 2026.
- The case against including it:
  - Nothing is executed.
  - The focus is the format of the design document, not repository generation itself.
  - T5 is change requests to the code the agent built earlier in the same run.

---

## 2. doi:10.18690/um.feri.7.2026.16: CODORQ (OTS 2026, 29th conference proceedings, pp. 184–200, University of Maribor Press)

Author: Tomaž Kolmanič (WagaLabs d.o.o.).

**Full text**

OpenAlex reports gold OA. doi.org resolves to press.um.si chapter 1467, and the PDF is at `catalog/view/1156/1806/6808`. I extracted it with pypdf and read it in full in Slovenian.

**Content**
- CODORQ is a local-first coordination layer, built as an MCP server in Node/TypeScript, over existing agent CLIs: Codex CLI, Claude Code and Antigravity CLI.
- It provides:
  - persistent memory
  - a task model with 12 statuses
  - roles and separation of duties (developer / reviewer / QA)
  - one Git worktree per task
  - tmux session binding and liveness checks (watchdog and reaper)
  - compact MCP views
  - an operator web UI
- The only demonstration is one case study in which CODORQ develops CODORQ itself. It adds a missing "Complexity" filter to the existing task UI:
  - Codex implements it: commit fdf0a68, 6 files, +74/−4 lines, 17/17 focused tests passing, typecheck and web build passing.
  - A Claude instance reviews it.
  - An Antigravity instance runs QA.
- The author states that the paper does not show any gain in productivity or quality. There is no baseline, no benchmark and no comparative evaluation. Descriptive figures: 523 commits, 162 TypeScript files, 75,559 LOC, 62 MCP tools, all written by agents under human supervision.

**Decision: exclude, EC1**
- The only evaluated activity is a feature addition to an existing repository.
- The paper is otherwise a system description and experience report with no evaluation (EC6 also applies).
- It does not generate a repository from a specification.
