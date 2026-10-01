# Fact-check ledger: abstract, introduction, background, overview, synthesis, conclusion

Corpus numbers were recomputed from `slr/data/corpus.csv` (176 rows), cross-checked against `survey/generated/numbers.tex`, and **not** taken from the prose. Model years are approximate release years.

## Corpus-level recomputation (corpus.csv)
| Quantity | corpus.csv | numbers.tex | Text |
|---|---|---|---|
| Included / core / contextual | 176 / 104 / 72 | 176/104/72 | same |
| Year 2023 / 24 / 25 / 26 | **5** / 31 / 65 / 75 | 5/31/65/75 | abstract says "four studies in 2023" (wrong) |
| Core by year 23/24/25/26 | 2/10/40/52 (92/104 = 88% are 2025+) | – | "large majority" OK |
| Contextual by year | 3/21/25/23 (pre-2025: 24 ctx vs 12 core) | – | "contextual dominates before 2025" OK |
| Peer-reviewed / preprint (venue column) | 64 / 112 | 64/112 | same |
| Peer-reviewed core | 36/104; core *benchmark* papers: 31/44 preprint | – | – |
| Core tasks | nl-to-app 40, nl-to-repo 30, translation 16, behav.-recon. 7, skeleton 5, paper 5, **other 1** | same | overview list omits the 1 "other" (sums to 103) |
| Python / Python-only | 96 / 70 (13 "multi" + 8 unspecified/blank not resolved → 96 is a lower bound) | 96/70 | same |
| Core LLM-judge | 29/104 | 29 | same |
| Core with any execution oracle (ref tests, differential, generated, BDD, build-run) | 88 | – | – |
| Core with a test-based oracle | 65; of these, reference unit tests: **32 (49%)**; ref-tests ∪ differential: 44 (68%) | 32 | "most execution-based oracles coupled to a reference" (see A4) |
| Contribution codes | method 110, benchmark 85, empirical 70, training-data 16; benchmark∧training-data: **9/85** | – | "many benchmark papers also train" (see O16) |
| QGS | 31 entries in gold_set.csv, 31/31 present in DB `records.csv` | – | recall 31/31 OK |

---

## Abstract

### C1 — (corpus)
- Draft: "This literature grew from four studies in 2023 to \nYearTwentySix{} in the first nine months of 2026."
- Verdict: CORRECTED
- Evidence: corpus.csv year=2023 → 5 rows (BioCoder, CoderEval, RepoCoder, IEEE C3 mobile study, MetaGPT); numbers.tex `\nYearTwentyThree{5}`
- Correct statement: "from five studies in 2023 to 75 in the first nine months of 2026" (use `\nYearTwentyThree{}` instead of a hard-coded word).
- Models: n/a
- Measurement: year = first public version (per overview)
- Status: n/a

### C2 — (methodology data)
- Draft: "validated the search against a 31-study quasi-gold standard (recall 31/31)"
- Verdict: VERIFIED
- Evidence: gold_set.csv has 31 rows; all 31 arXiv IDs are in records.csv with database sources (none snowball-only). Note: 3 gold studies (2404.00599, 2502.18793, 2312.05772) are not in the final corpus; that is fine for search recall but should not be read as "31 included".
- Models: n/a
- Measurement: retrieval recall, not inclusion recall
- Status: n/a

### C3 — (corpus)
- Draft: "Of 3306 records identified, 176 primary studies are included: 104 ... core and 72 ... contextual"
- Verdict: VERIFIED
- Evidence: numbers.tex nRawTotal 3306; corpus.csv 176 rows, tier core 104 / contextual 72
- Status: n/a

### C4 — (corpus; also Conclusion "Most execution-based oracles presuppose a reference design")
- Draft: "Most execution-based oracles are coupled to a reference implementation."
- Verdict: MISLEADING
- Evidence: Of 65 core studies that use a test-based oracle, 32 (49%) use reference unit tests. The draft's own Table `tab:oracles` rates differential and interface black-box oracles as "low" coupling. The claim reaches "most" (44/65) only if differential testing against a reference *executable* counts as "coupled to a reference implementation". If build-run checks are included (88 studies), the share is 36%.
- Correct statement: "About half of the core studies with test-based oracles (32 of 65) use upstream white-box tests that presuppose the reference's internal API. Most of the rest test behaviour against a reference executable or a fixed interface."
- Measurement: evaluation codes are LLM-assisted extraction (corpus.csv `evaluation`); a study may have several codes.

### C5 — (corpus)
- Draft: "LLMs sit inside the measurement of 29 of the 104 core studies."
- Verdict: VERIFIED (lower bound)
- Evidence: 29 core rows with `llm-judge`.
- Measurement: this counts only LLM *judges*. LLM-generated/adapted tests and LLM-written specifications (e.g., E2EDevBench test migration with Gemini-2.5-Pro, BeyondSWE specs by Gemini 3 Pro) are not counted, so "inside the measurement" is underestimated. Say "LLM judges appear in 29 of 104".

### C6 — NL2RepoBench2025, BeyondSWE2026, ProgramBench2026
- Draft: "Partial-credit pass rates hide that almost no complete repository is ever produced."
- Verdict: VERIFIED
- Evidence: NL2Repo: "the strongest model fully passes the official pytest suite for only five repositories in a single run" (§4); BeyondSWE: "even the best configuration produces only 2 fully correct repositories out of 50" (§5.2); ProgramBench: "none fully resolve any task" (abstract)
- Models: Claude Sonnet 4/4.5, GPT-5, Gemini 3 Pro (2025); GPT-5.4, Gemini 3 Pro (2025–26); Opus 4.7, GPT-5.4 (2026)
- Measurement: single runs; reference tests (NL2Repo, BeyondSWE), fuzz-generated behavioural tests (ProgramBench)
- Status: all preprints

---

## Introduction

### C7 — chen2021humaneval
- Draft: "Frontier models now saturate these benchmarks"
- Verdict: NOT FOUND (no source cited for saturation; Chen et al. 2021 cannot support it)
- Correct statement: cite a recent leaderboard or report, or write "reach above 90% on HumanEval [cite]".

### C8 — CoderEval2023, DevEval2024, RepoExec2024
- Draft: these are examples of the contextual line (function/class tested inside the project)
- Verdict: VERIFIED
- Evidence: corpus tier = contextual, task repo-context-gen for all three
- Status: CoderEval ICSE 2024; DevEval, RepoExec preprint

### C9 — NL2RepoBench2025
- Draft: "writing a library from a requirements document and an empty workspace"
- Verdict: VERIFIED
- Evidence: "Given only a single natural-language requirements document and an empty workspace" (abstract)
- Status: preprint

### C10 — Commit02024
- Draft: "filling a stubbed library"
- Verdict: VERIFIED
- Evidence: corpus task skeleton-to-library; NL2Repo's description of Commit0: "provides project structure and function signatures as strong priors"
- Status: preprint

### C11 — ProgramBench2026
- Draft: "rebuilding a program from its executable alone"
- Verdict: CORRECTED
- Evidence: "given only a program and its documentation, agents must architect and implement a codebase" (abstract)
- Correct statement: "rebuilding a program from its executable and documentation"
- Models: Claude Opus 4.7/4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro, GPT-5.4 (2025–26)
- Status: preprint

### C12 — RepoZero2026
- Draft: "re-implementing a repository in another language against a behavioural oracle"
- Verdict: VERIFIED
- Evidence: "RepoZero-Py2JS ... reimplement them in JavaScript, and RepoZero-C2Rust" (§3); black-box tests
- Status: NeurIPS 2026 (D&B)

### C13 — VibeCodeBench2026, SaaSBench2026
- Draft: "building a deployable application from a prompt"
- Verdict: VERIFIED
- Evidence: Vibe Code Bench: "can produce a complete, deployable web application from a natural language" (§1)
- Status: preprints

### C14 — NL2RepoBench2025
- Draft: "no model exceeds 41% mean test pass rate, and the best completes about 5 of 104 repositories"
- Verdict: VERIFIED (with a nuance)
- Evidence: "all models achieve an average test pass rate below 40.5% ... the strongest model fully passes ... only five repositories" (§4, Table 3). Table 3: best mean is Claude-Sonnet-4.5 (Claude Code) at 40.2%, with Pass@1 count 3; the count of 5 belongs to Claude-Sonnet-4 (37.0%).
- Correct statement (optional): "the best mean is 40%, and no configuration fully completes more than 5 of 104"
- Models: Claude Sonnet 4/4.5, GPT-5, Gemini 3 Pro, DeepSeek-V3.1/3.2, Kimi-K2, Qwen3, GLM-4.6 (2025)
- Measurement: upstream pytest suites (white-box); single run; OpenHands unless noted
- Status: preprint

### C15 — ProgramBench2026
- Draft: "no model fully solves a single task"
- Verdict: VERIFIED
- Evidence: "none fully resolve any task, with the best model passing 95% of tests on only 3% of tasks" (abstract)
- Models: as C11 (2025–26)
- Measurement: agent-fuzzed behavioural tests vs reference executable; 200 tasks; mini-SWE-agent
- Status: preprint

### C16 — SaaSBench2026
- Draft: "the best configuration reaches about 21%"
- Verdict: VERIFIED
- Evidence: "The best result is only 20.68%, achieved by Claude Opus 4.7 under Claude Code" (§4)
- Models: Opus 4.7 and others (2026)
- Measurement: hybrid score over 5,370 validation nodes, partly LLM-judged; 30 tasks
- Status: preprint

### C17 — (sample size of intro figures)
- Draft: "Results on these tasks are consistently low." (C14–C16)
- Verdict: VERIFIED (see the Cross-study note X5 on model generations)
- Evidence: as above

### C18 — tao2025ragsurvey, liu2024agents4se, dong2025agentsurvey, guo2025agenticse, wang2025sdlcbench, hu2025benchmarks, jiang2025issuesurvey
- Draft: "Existing secondary studies cover parts of this space ... none of them systematically reviews the generation of whole repositories"
- Verdict: VERIFIED for the 4 surveys checked (Tao, Liu, Dong, Wang, Hu abstracts: none targets whole-repository generation). NO FULL TEXT for Guo, Jiang and Ge (bib titles only).
- Evidence: see C21–C25.

### C19 — (corpus)
- Draft: "A reproducible systematic review of 176 primary studies (January 2022 – September 2026)"
- Verdict: VERIFIED (numbers.tex; methodology l.11)

---

## Background

### Related surveys cited
| Key | Title (bib) | arXiv | Checked against |
|---|---|---|---|
| tao2025ragsurvey | Retrieval-Augmented Code Generation: A Survey with Focus on Repository-Level Approaches | 2510.04905 | arXiv abstract (WebFetch) |
| dong2025agentsurvey | A Survey on Code Generation with LLM-based Agents | 2508.00083 | arXiv abstract (WebFetch) |
| liu2024agents4se | LLM-Based Agents for Software Engineering: A Survey | 2409.02977 | arXiv abstract (WebFetch) |
| guo2025agenticse | A Comprehensive Survey on Benchmarks and Solutions in SE of LLM-Empowered Agentic System | 2510.09721 | bib only |
| wang2025sdlcbench | SDLC Perspective: A Survey of Benchmarks for Code LLMs and Agents | 2505.05283 | full text (scratchpad) |
| hu2025benchmarks | Assessing and Advancing Benchmarks for Evaluating LLMs in SE Tasks (TOSEM) | 2505.08903 | full text (scratchpad) |
| ge2025vibe | A Survey of Vibe Coding with LLMs | 2510.12399 | bib only |
| jiang2025issuesurvey | Agentic Software Issue Resolution with LLMs: A Survey | 2512.22256 | bib only |
| hou2024llm4se | LLMs for SE: A Systematic Literature Review (TOSEM) | 2308.10620 | not available |

### C20 — (definitions / scope)
- Draft: "A core task ... runs for hundreds of agent turns"
- Verdict: MISLEADING
- Evidence: NL2Repo averages about 180 turns and ProjDevBench 138 turns (rq1). However, many core studies are non-agentic or few-shot, e.g., ParEval-Repo's non-agentic file-by-file method, RealBench's holistic/incremental prompting, and the 2023 mobile study.
- Correct statement: "in agentic benchmarks, typically runs for over a hundred turns"

### C21 — tao2025ragsurvey
- Draft: "survey retrieval-augmented code generation with a repository-level focus. Their object is context retrieval for completion and function generation, which corresponds to part of our contextual tier." Table: whole-repo "--", eval validity "partial".
- Verdict: VERIFIED (slightly narrow)
- Evidence: abstract: "models must retrieve, organize, and utilize repository-scale context to generate coherent and executable code changes ... examines retrieval strategies, graph-based and non-graph-based retrieval paradigms, training-driven optimizations, and autonomous agent architectures"
- Correct statement (optional): "...context retrieval for repository-level completion, generation and code changes, including agentic retrieval"
- Status: preprint (Oct 2025)

### C22 — liu2024agents4se, dong2025agentsurvey, guo2025agenticse
- Draft: "discuss end-to-end development as one application among many, and their corpora largely predate the 2025–2026 wave"
- Verdict: VERIFIED for Liu and Dong; NO FULL TEXT for Guo
- Evidence: Liu: v1 4 Sep 2024, "We collect 124 papers" (v2 Dec 2025, abstract still 124, so the "to mid-2024" corpus in Table 1 is consistent). Dong: v1 31 Jul 2025 / v2 30 Sep 2025, scope "full software development lifecycles". Dong's corpus can reach mid-2025, so "largely predate" holds only for the 2026 part of the wave.
- Correct statement (optional): "...predate most of the late-2025 and 2026 repository-generation benchmarks"

### C23 — wang2025sdlcbench, hu2025benchmarks
- Draft: "catalogue benchmarks across the software life cycle. They do not analyse how repository-generation oracles depend on reference implementations or on LLM judges."
- Verdict: VERIFIED
- Evidence: Wang: "systematically review 178 benchmarks from 461 papers ... from the perspective of the SDLC"; LLM-Judge appears only as a table metric label. Hu: "thorough review of 291 benchmarks". Neither has an oracle-coupling analysis (grep for judge/oracle/reference implementation).
- Status: Wang preprint (v3 Mar 2026); Hu TOSEM 2025

### C24 — wang2025sdlcbench, hu2025benchmarks, hou2024llm4se
- Draft: "the two benchmark surveys, like most LLM4SE reviews [hou2024llm4se], report neither database-specific Boolean strings nor per-stage selection counts"
- Verdict: CORRECTED
- Evidence: Wang §III reports per-stage counts: "In total, we retrieved 1,347 relevant papers ... resulting in 321 articles ... added 140 additional papers ... collected 461 papers", plus a keyword list (but no per-database Boolean strings). Hu: "following the search strategy and search strings defined by Hou et al. [114]". It reports the final count of 291 but no per-stage counts. Hou et al. (TOSEM) is not available locally. To my knowledge it publishes its keyword sets and stage counts, so it is likely a counter-example to "most LLM4SE reviews". Check before keeping the cite.
- Correct statement: "Wang et al. report per-stage counts but only a keyword list. Hu et al. reuse Hou et al.'s strings without per-stage counts. Neither gives database-specific Boolean strings." Drop "like most LLM4SE reviews [hou2024llm4se]", or replace it with a sourced claim.

### C25 — ge2025vibe, guo2025agenticse, jiang2025issuesurvey (Table rows)
- Draft: Table `tab:related` focus and coverage cells
- Verdict: NO FULL TEXT
- Evidence: bib titles are consistent with the "Focus" column. The coverage cells ("partial") are unverified.

### C26 — (scope claim)
- Draft: "the contextual literature supplies most of the controlled evidence on context acquisition"
- Verdict: VERIFIED
- Evidence: RQ4 context-acquisition list: AllianceCoder, Repoformer, MRG-Bench, REPOCOD, GRACG, RepoScope, CatCoder and others are all contextual. The only core entry is RealBench.

---

## Overview

### C27 — (corpus) year distribution
- Draft: "5 in 2023, 31 in 2024, 65 in 2025, and 75 in the first nine months of 2026"
- Verdict: VERIFIED (corpus.csv)

### C28 — CoderEval2023, RepoCoder2023, DevEval2024, EvoCodeBench2024, RepoExec2024 + corpus
- Draft: "The contextual tier dominates before 2025: [five benchmarks] established repository-dependent function generation with execution-based evaluation."
- Verdict: VERIFIED
- Evidence: pre-2025: 24 contextual vs 12 core. All five are tier=contextual with reference-unit-tests or generated-tests. RepoCoder's main metric is similarity (EM/ES); only its function-level subset is executed.
- Status: CoderEval ICSE 2024, EvoCodeBench NeurIPS 2024 D&B; others preprint

### C29 — (no citation)
- Draft: "The core tier took off in 2025–2026, once agent harnesses such as OpenHands, mini-SWE-agent, Claude Code, and Codex CLI could sustain the hundreds of turns..."
- Verdict: NOT FOUND (causal claim, uncited; the timing is correlational only)
- Correct statement: "The core tier grew in 2025–2026, at the same time as general-purpose agent harnesses (OpenHands, ...) became the default evaluation scaffold (used by N of 92 2025+ core studies)."

### C30 — (corpus)
- Draft: "Of the 104 core studies, the large majority appeared in 2025 or later."
- Verdict: VERIFIED (92/104 = 88%). Give the number.

### C31 — (corpus)
- Draft: "Only 64 studies (as stated in their full text) are peer-reviewed; the remaining 112 are preprints or venue-unstated."
- Verdict: VERIFIED (corpus.csv `venue`: 112 "preprint")
- Measurement: the venue string is LLM-extracted. Spot-checks match (RealBench "Proc. ACM Softw. Eng. ... FSE"; ParEval-Repo ICPP; RepoZero NeurIPS D&B).

### C32 — NL2RepoBench2025, ProgramBench2026, SaaSBench2026
- Draft: "A review restricted to peer-reviewed work would omit most of the benchmarks that define the core tier, including ..."
- Verdict: VERIFIED
- Evidence: 31 of 44 core benchmark papers are preprints; all three named are preprints

### C33 — (corpus) tiers and task counts
- Draft: "104 core, 72 contextual; NL→app 40, NL→repo 30, translation 16, behavioural reconstruction 7, paper→repo 5, skeleton→library 5"
- Verdict: CORRECTED (minor)
- Evidence: corpus.csv also has 1 core study coded `other`, so the six listed types sum to 103.
- Correct statement: add "and one other (\nTaskOther{})".

### C34 — (corpus) Python
- Draft: "Python ... appears in 96 studies and is the only language in 70"
- Verdict: VERIFIED (as coded). 13 "multi" and 8 unspecified/blank rows are not resolved to languages, so 96 is a lower bound. Add "at least".

### C35 — (corpus) other languages
- Draft: "the corpus covers Java, C/C++, Rust, Go, and JavaScript/TypeScript"
- Verdict: VERIFIED (Java 30, C 12 / C++ 10, Rust 13, Go 4, JS 22 / TS 16 explicit codes)

### C36 — SolEval2025, ChainBench2026, ECAT2026, JamBenchJamSet2026, Vero2026
- Draft: "Solidity, Move, and Cairo (SolEval, ChainBench), ArkTS (ECAT), GDScript (JAMER), and Lean 4 (Vero)"
- Verdict: VERIFIED except ChainBench, which has NO FULL TEXT (zenodo record; Move/Cairo come from the corpus code only)
- Evidence: corpus languages: SolEval "Solidity"; ChainBench "Solidity;Rust;Move;Cairo"; ECAT "Java;Kotlin;ArkTS"; JAMER "GDScript"; Vero "Lean"
- Status: SolEval EMNLP 2025; the others preprint

### C37 — RepoTransBench2024
- Draft: "static-to-dynamic translation succeeds far more often than the reverse"
- Verdict: VERIFIED
- Evidence: "dynamic-to-static language translation being much more challenging ... (achieving below 10% vs. static-to-dynamic at 45-63%)" (abstract)
- Models: GPT-4o-era and open models (2024)
- Measurement: generated tests + build; 100 repositories
- Status: preprint

### C38 — CLIToolBench2026
- Draft: "Go is a bottleneck for CLI generation"
- Verdict: VERIFIED
- Evidence: "Golang emerges as a severe bottleneck" (§5, radar analysis)
- Measurement: 45 Go tasks; differential + generated tests
- Status: preprint

### C39 — RepoGenesis2026
- Draft: "Java services deploy more often but pass fewer tests than Python services"
- Verdict: VERIFIED
- Evidence: "Java achieves higher overall DSR (41.67%) than Python (28.41%)" (Table 7); "Python performance generally exceeds Java" (§5.1); best Pass@1 23.67% Python vs 21.45% Java
- Models: Copilot/Cursor IDEs, MetaGPT etc. with Claude/GPT-5.1 backbones (2025)
- Measurement: DSR over 96 Java / 264 Python runs; black-box HTTP tests; the Pass@1 gap is small (2 points)
- Status: preprint

### C40 — ReproGap2025
- Draft: "Java projects run out of the box in 44% of cases versus 89% for Python"
- Verdict: VERIFIED
- Evidence: "Python achieves 89.2% reproducibility, JavaScript 61.9%, and Java just 44.0%" (§1)
- Models: Claude Code, OpenAI Codex, Gemini CLI (2025)
- Measurement: 300 projects from 100 prompts (25 Java prompts × 3 agents); build/run only
- Status: preprint

### C41 — (corpus)
- Draft: "Benchmarks and methods are the most frequent contributions."
- Verdict: VERIFIED (method 110, benchmark 85, empirical 70, training-data 16)

### C42 — RepoGenesis2026, WebGenBench2025, JamBenchJamSet2026
- Draft: "Many benchmark papers also train a model on data derived from their own benchmark"
- Verdict: MISLEADING
- Evidence: only 9 of 85 benchmark papers carry `training-data`. All three examples are correct: RepoGenesis fine-tunes Qwen3-8B (GenesisAgent); WebGen-Bench fine-tunes Qwen2.5-Coder on WebGen-Instruct trajectories; JAMER LoRA-fine-tunes Qwen3.5-27B.
- Correct statement: "Nine of the 85 benchmark papers also release training data or train a model on data derived from their benchmark (e.g., ...)."

### C43 — DeNovoSWE2026, MindForge2026, SWEPlayground2025
- Draft: "Dedicated training-environment papers ... are a 2025–2026 development."
- Verdict: VERIFIED
- Evidence: SWE-Playground "Training Versatile Coding Agents in Synthetic Environments"; MindForge "lack of scalable training environments"; DeNovoSWE "Scaling Long-Horizon Environments". The training-data-only rows are 2025–26, except Repoformer (2024), which trains retrieval, not environments.
- Status: all preprints

---

## Synthesis

### C44 — NL2RepoBench2025, BeyondSWE2026, SaaSBench2026 (via rq3)
- Draft: "The best mean pass rates on realistic from-scratch benchmarks lie between 20% and 62%."
- Verdict: VERIFIED (numbers), but see X4
- Evidence: SaaSBench 20.68% (Opus 4.7, 2026); NL2Repo 40.2% (Sonnet 4.5, 2025); BeyondSWE Doc2Repo 61.74% (GPT-5.4 xhigh + Codex, 2026)
- Measurement: the metrics differ (SaaSBench is a node-weighted hybrid score with an LLM judge; the others are reference pytest pass rates). The models span 2025–26.
- Status: all preprints

### C45 — NL2RepoBench2025, BeyondSWE2026, CodeTeam2026
- Draft: "The share of repositories that are fully correct is in the low single digits"
- Verdict: CORRECTED (minor)
- Evidence: NL2Repo 5/104 = 4.8%; BeyondSWE best 2–4/50 = 4–8% ("(7) / 4" for GPT-5.4 SearchSWE); CodeTeam 6%; ProgramBench 0%
- Correct statement: "at most 8% (0–4 repositories per benchmark)"

### C46 — RepoModBench2026, RealBench2025, NL2RepoBench2025 (via rq1)
- Draft: "Size is the strongest predictor of difficulty."
- Verdict: NOT FOUND
- Evidence: each study shows a monotone drop with size. No study compares size against other predictors such as specification length, domain or language, so "strongest" is unsupported. CodeSpec, for example, finds that instruction length separates methods.
- Correct statement: "In the three benchmarks that report it, pass rate falls steeply with target size."

### C47 — NL2Repo, BeyondSWE, DeNovoSWE, RAL-Bench (via rq3)
- Draft: "Many 'NL-to-repository' benchmarks are, in effect, the reconstruction of a known implementation from a detailed description."
- Verdict: VERIFIED
- Evidence: BeyondSWE: "generates a specification covering purpose, usage examples, public classes and functions, parameters, return types, and behavior" (§3.2); DeNovoSWE capability documents are drafted from the source repository (§3.2)

### C48 — (rq2/rq3)
- Draft: "Four issues recur ... Each can change rankings by more than the method differences reported in the literature."
- Verdict: NOT FOUND
- Evidence: ranking effects are documented only for (a) the evaluator choice (Vibe Code Bench agreement 86.4% vs 36.1%; WebCraftBench ρ=0.98, i.e., the ranking is *preserved*) and (b) similarity vs pass@k (ProjectEval). There is no ranking evidence for feedback leakage or for behaviour-only loopholes.
- Correct statement: "Two of them, the evaluator choice and similarity-based scoring, have been shown to change verdicts or rankings."

### C49 — (no citation)
- Draft: "Most method papers change the planning representation, the agent decomposition, the feedback, and the budget all at once. They compare against ChatDev and MetaGPT, often under a different harness or backbone."
- Verdict: NOT FOUND (no count in the extraction data)
- Correct statement: report the count (method papers whose main comparison is against ChatDev/MetaGPT, and whether the backbone is matched), or weaken to "Many".

### C50 — MRGBench2025
- Draft: "MRG-Bench attributes most failures to misunderstanding *what* to build"
- Verdict: VERIFIED (with validity caveats)
- Evidence: "over 68% of failures stem from missing 'What information'" (§5.3)
- Models: generation by Claude-3.5-Sonnet, GPT-4o, o3-mini, DeepSeek-R1, CodeLlama etc. (2024–early 2025). The *annotated failures are Claude-3.5-Sonnet's only*.
- Measurement: the labels come from a 5-LLM vote (GPT-4o, Claude-3.5-Sonnet, Gemini-2.5-Pro, DeepSeek-V3, Qwen2.5-72B). 3:2 cases are dropped (86.3% retained), and there is no human validation. "What information" includes sibling functions and class context, i.e., repository context, not only the NL requirement. The task is function-level (contextual tier); the "hand-off" here is a docstring.
- Status: preprint

### C51 — CBAUserStudy2025
- Draft: "98% of user prompts contain functional requirements but only 3 of 48 contain test cases"
- Verdict: VERIFIED
- Evidence: Table II: "Functional Requirements 0.98 47"; "Testable Examples 0.06 3"
- Models: GitHub Copilot / GPT-Engineer (2024–25)
- Measurement: 16 participants, 48 prompts, qualitative coding. The paper reports prompt *content*, not that missing tests caused failures; the functional-requirement correlation with satisfaction is 0.09 (n.s.). The label is "testable examples", not "test cases".
- Status: preprint

### C52 — E2EDevBench2025
- Draft: "a design handed from a Designer agent to a Developer agent" (as a free-form hand-off weak link)
- Verdict: VERIFIED (as the authors' hypothesis)
- Evidence: "we hypothesize that the performance bottleneck originates in its Design Agent ... the Dev Agent ... tends to prioritize this plan over direct engagement with the original requirement document" (§5); DDT mean 27.71% vs DT 49.48%
- Models: Gemini-2.5-Pro / Flash only (2025)
- Measurement: 50 projects; temperature 0.2; apparently a single run. The requirement implementation rate is judged by Gemini-2.5-Pro, the same family as the evaluated models; human agreement was checked on 10 projects. Flash beats Pro in Single (48.5 vs 43.0), which suggests high run-to-run variance. The design is a free-form "detailed project design document".
- Status: preprint

### C53 — RepoZero2026
- Draft: "a plan the agent writes for itself and loses over hundreds of turns (the 'contextual drift' of RepoZero)"
- Verdict: MISLEADING
- Evidence: "Despite the inclusion of all white-box constraints in the initial prompt, agents frequently exhibit 'contextual drift' ... losing track of critical requirements" (§5)
- Correct statement: "requirements given in the initial prompt and lost over long trajectories (RepoZero's qualitative 'contextual drift')". The lost content is the given requirement, not a self-written plan, and the observation is not quantified.
- Models: open models with OpenHands-bash and others (2025–26)
- Status: NeurIPS 2026 D&B

### C54 — RPGZeroRepo2025
- Draft: "RPG's motivation"
- Verdict: VERIFIED (motivation only, not evidence)
- Evidence: "Current approaches rely on natural language planning, which often [struggles] due to its inherent ambiguity and lack of structure" (abstract)
- Measurement: the headline comparison against Claude Code is uncontrolled. The only RPG ablation (Table 4) measures localization *steps* with o3-mini (6.2 vs 13.3), not correctness. RepoCraft is the authors' own benchmark and uses adapted tests plus an o3-mini judge.
- Status: ICLR 2026

### C55 — BeyondSWE2026, DeNovoSWE2026
- Draft: "an LLM-written specification reverse-engineered from code" (listed as a weak-link hand-off)
- Verdict: NOT FOUND (as evidence of a weak link)
- Evidence: the construction is VERIFIED ("Gemini 3 Pro ... explores the codebase and generates a specification", BeyondSWE §3.2; DeNovoSWE uses drafting, critic and repair agents). Neither paper attributes failures to the specification; DeNovoSWE adds a critic loop specifically to ensure the doc "provides enough information". This is a *benchmark-validity* concern (the spec may omit test-relevant behaviour), not an observed failure point of generation systems.
- Correct statement: move it to the evaluation-validity paragraph, or say "a hand-off whose fidelity is not measured".

### C56 — ParEvalRepo2025
- Draft: "a natural-language summary passed between translation agents (ParEval-Repo, where interface mismatches dominate)"
- Verdict: CORRECTED
- Evidence: the context agent does pass "LLM generated summaries of translation changes" (§3.2). But errors "relating to CMake configuration, as well as undeclared identifiers and function argument or type mismatches ... are broadly common" (§8.3), and the paper concludes "generating working build systems is a major obstacle". The non-agentic approach, which passes no summaries, "tends to achieve the highest scores". The errors are not attributed to the summaries.
- Correct statement: "ParEval-Repo, where build-configuration errors and cross-file interface errors are the most common compile failures, across both agentic and non-agentic methods"
- Models: GPT-4o mini, Gemini 1.5 Flash, Llama-3.3 and others (2024)
- Status: ICPP 2025

### C57 — CodeSpec2026
- Draft: "71.8 vs 43.8 for executable vs textual specifications on long instructions"
- Verdict: MISLEADING (the numbers are correct)
- Evidence: "CodeSpec achieves 71.8% on instructions of 3,000–5,000 words, compared with 43.8% for CodeSpec(Text)" (RQ3, Fig. 3a). The same figure shows ≤3,000 words: 77.2 vs 69.5, and >5,000 words: 38.3 vs 36.3.
- Correct statement: "On FeatureBench Lite (30 feature-addition tasks), executable specs beat a textual-spec variant by 8 points on short and 28 points on mid-length instructions, but only 2 points on the longest. The overall ablation without all specification is 70.7 → 62.6."
- Models: DeepSeek-V4-Pro (2026), single backbone
- Measurement: a subgroup of a 30-task split (bucket n unreported); fail-to-pass tests. The task is **feature development in existing repos, which this review's own scope excludes**.
- Status: preprint

### C58 — RealBench2025
- Draft: "removing class diagrams drops test pass rate from 16.3% to 3.6%"
- Verdict: VERIFIED (numbers) / validity concern
- Evidence: "a 12.74% drop (16.34% - 3.60%) of test pass rate in the incremental strategy" (§4.3)
- Models: GPT-4o, Claude-Sonnet-4, Gemini-2.5-Flash, DeepSeek-V3, Qwen3-235B, Qwen2.5-Coder-7B (2024–25), averaged
- Measurement: the oracle is upstream white-box tests. Class diagrams supply the class/method names and attributes those tests call, so the drop conflates "structured artefact helps" with "the oracle needs the reference interface" (the authors: failures "caused by the absence of implementation details such as class attributes and methods"). The comparison removes information; it does not compare structured vs prose.
- Status: FSE 2026

### C59 — SkeletonGuidedTranslatio2025
- Draft: "without the skeleton, dependencies cannot be resolved and scores fall to zero"
- Verdict: MISLEADING
- Evidence: omitting skeletons results in "the failure to find the function under test during the test. ... This failure renders our scoring mechanism ineffective because unresolved dependencies cause all build and test scores to drop to zero" (§4.2.2). The skeleton fixes the interfaces that the component-wise evaluator relies on, and the drop to zero is reported "for certain libraries".
- Correct statement: "without the skeleton, translated code no longer matches the interfaces the evaluator expects, and scores collapse". This is an oracle-coupling effect at least as much as a generation effect.
- Models: GPT-4o, GPT-4o-mini, GPT-4-turbo, Claude-3.5-Sonnet, Qwen-plus (2024)
- Status: preprint

### C60 — SpecFirst2026
- Draft: "SpecFirst's specification phase and design-by-contract constraints also improve results"
- Verdict: CORRECTED
- Evidence: SpecFirst: "improving test pass rates by 6.9%–21.3% ... all statistically significant" (abstract). The spec is "SPEC.md" with "a light scaffold of six named headings" (§III-C), i.e., *semi-structured Markdown, not machine-checkable*. "it spends more budget than the baseline" (+48–130% cost, Threats). SpecFirst contains no design-by-contract; that result is DbCConstraints2025, which is not cited here.
- Correct statement: "SpecFirst's persistent, sectioned Markdown specification improves pass rate (not cost-matched); design-by-contract pre- and postconditions raise pass@k [DbCConstraints2025]". Note that SpecFirst supports *persistence/explicitness*, not *checkability*.
- Models: GPT-5.5-high, GPT-5.4, Qwen3.5-397B, Qwen3.6-35B (2026)
- Measurement: 200 ProgramBench tasks, differential tests vs reference binary
- Status: preprint

### C61 — (rq3)
- Draft: "Oracles become more reliable when the external contract is executable (differential and interface tests) than when a judge reads prose."
- Verdict: NOT FOUND
- Evidence: no study compares the reliability of differential/interface oracles with LLM judges on the same outputs. RQ3 documents judge variance (Vibe Code Bench 86.4% vs 36.1% human agreement) *and* loopholes in behaviour-only oracles ("no-migration", strict string matching).
- Correct statement: "LLM-judge verdicts vary with the evaluator, whereas executable oracles are deterministic but have their own loopholes."

### C62 — (self-description)
- Draft: "The supporting ablations each vary a single system rather than the representation alone."
- Verdict: VERIFIED (consistent with C57–C60)

### C63 — Athena2025
- Draft: "Several studies show that structure without verification can hurt (Athena ...)"
- Verdict: MISLEADING
- Evidence: Athena produced more bugs (mean 10.4 vs 1.25), but "As a result of Athena allowing for more complex app structures and generating multiple code files" and apps with "twice as many views and three times as much code" (§5.2.4). The authors attribute the bugs to code volume, and users preferred Athena for prototyping (9/12).
- Correct statement: "In Athena, structured IRs yielded larger apps with more (mostly easily fixed) bugs; no size-normalised comparison is reported."
- Models: GPT-4o (2024), both conditions
- Measurement: 12-participant within-subject user study, 25-minute tasks; bug counts per app; not test-based
- Status: preprint

### C64 — E2EDevBench2025 (second use)
- Draft: "...structure without verification can hurt (... the Designer agent in E2EDevBench)"
- Verdict: MISLEADING
- Evidence: the Designer's output is a "detailed project design document", i.e., free-form prose (§3). The same result is used two paragraphs earlier as evidence that a *free-form* hand-off is the weak link (C52). It cannot count both as a free-form failure and as an unverified-structure failure.
- Correct statement: keep it only as a free-form hand-off example (C52), with the authors' "we hypothesize" qualifier.

### C65 — CodeSpec2026
- Draft: "no study compares free-form, structured, and executable hand-offs under a fixed model, harness, and budget"
- Verdict: VERIFIED (nuance)
- Evidence: CodeSpec(Text) vs CodeSpec is a two-level textual-vs-executable comparison under one model and harness (FeatureBench Lite). No three-level comparison exists, but say that a two-level one does.

### C66 — RealBench2025
- Draft (P1): "RealBench shows that 'creating the modules named in the design' and 'implementing them correctly' are separable abilities."
- Verdict: VERIFIED
- Evidence: "LLMs are good at finding and creating modules defined in UML diagrams, but the quality of generated modules is often poor" (abstract/§4)

### C67 — CLIToolBench2026, RepoModBench2026, ProgramBench2026, RepoZero2026
- Draft (P2): "each implement parts of this. None implements all of it together with side-effect checks and tolerance to formatting differences."
- Verdict: VERIFIED for "parts" (all use differential or interface black-box oracles); NOT FOUND for the universal negative (no per-benchmark feature table)
- Correct statement: back it with a small feature table (external contract / reference executable / completeness gate / held-out tests / side-effects / format tolerance).

### C68 — RPGZeroRepo2025, CodeTeam2026
- Draft (P3): "RPG and CodeTeam already [use a graph or an architect agent]"
- Verdict: VERIFIED for RPG (graph); CodeTeam not re-checked (rq4 describes a "machine-checkable contract normalised from competing designs")

### C69 — (corpus)
- Draft (P5): "Independent-repository counts are small, most core evaluations are single runs, and the field is Python-centric."
- Verdict: NOT FOUND for "most ... single runs" (no extraction field); Python-centric VERIFIED (96/176, 70 Python-only)
- Correct statement: report the count of core studies with repeated runs or CIs, or say "many (e.g., NL2Repo, E2EDevBench)".

### C70 — RepoZero2026, CLIToolBench2026, E2EDevBench2025, ProgramBench2026
- Draft (P5): "oracle-validated test generation (RepoZero, CLI-Tool-Bench), quarterly refresh (E2EDevBench), and source-free executables (ProgramBench)"
- Verdict: VERIFIED (nuance on E2EDevBench)
- Evidence: E2EDevBench: "From the first quarter of 2024 to the first quarter of 2025, we randomly sample 10 standard-compliant projects each quarter" (§3). This is time-sliced sampling, not a demonstrated ongoing refresh; it is described as "dynamically curated". Say "quarter-sliced sampling".

### C71 — RALBench2026, CursorDesignIssues2026, OODPureAI2026, AgingGen2025, ReproGap2025
- Draft (P6): "Maintainability, security, ... are measured only occasionally, and never together. Yet they diverge from functional scores (...)"
- Verdict: VERIFIED for "diverge" (all five evaluate non-functional quality beyond tests). NOT FOUND for "never together". The Cursor study has **no \cite**.
- Correct statement: add `\cite{CursorDesignIssues2026}`. Drop "never together" or support it (27/104 core studies have non-functional codes; check whether any of them combine ≥3 dimensions).

---

## Conclusion

### C72 — (corpus)
- Draft: "We reviewed 176 studies"
- Verdict: VERIFIED

### C73 — (corpus)
- Draft: "Most execution-based oracles presuppose a reference design."
- Verdict: MISLEADING (same as C4)

### C74 — (corpus, rq3)
- Draft: "Many verdicts involve LLMs whose independence is unreported."
- Verdict: VERIFIED (29/104 core with LLM judges; RQ3 names only 5 benchmarks that report human alignment). Give the numbers.

### C75 — (rq3)
- Draft: "Agents exploit whatever an oracle fails to check."
- Verdict: MISLEADING (overgeneralised)
- Correct statement: "Agents have been observed exploiting unchecked oracle gaps (e.g., delegation to the original, stubs) [cite RQ3 cases]."

---

## Cross-study claims

### X1 — The hand-off hypothesis (Synthesis §"The hand-off hypothesis"; Intro contribution 5; Conclusion)
Claim: "failures concentrate where information passes between stages as free-form natural language", and structured, checkable artefacts improve results "in controlled comparisons".

**Supporting "weak link" examples (C50–C56).**
- **MRG-Bench.** Function-level (contextual) task. Failures are labelled by an LLM vote and cover only Claude-3.5-Sonnet failures (2024), with no human check. The "What" category includes missing repository context, not only the NL requirement.
- **CBA study.** Measures what prompts contain (n=48), not where failures arise.
- **E2EDevBench.** Single-family (Gemini 2.5) authors' hypothesis on 50 projects, judged by the same family. This is the strongest piece of direct evidence, and it is one preprint.
- **RepoZero.** Mischaracterised: the drift is about given requirements, not self-written plans. Qualitative only.
- **RPG.** Motivation, not a finding.
- **BeyondSWE / DeNovoSWE.** No failure attribution; this is a benchmark-validity point.
- **ParEval-Repo.** Does not support the claim. Build and interface errors are common across methods, and the method without summaries does best.

**Supporting "structure helps" comparisons (C57–C60).** All four are confounded:
- **CodeSpec.** A favourable subgroup on 30 *out-of-scope* feature-addition tasks; the gap is about 2 points on the longest bucket.
- **RealBench and Skeleton-Guided.** The structured artefact supplies the interface names that the reference/component oracle needs (measurement coupling), and the comparison removes information rather than changing representation.
- **SpecFirst.** Supports a persistent semi-structured Markdown spec (not checkable), with +48–130% cost, and contains no DbC.

**Opposing evidence (C63, C64).** Athena's bug increase is confounded with 3× code volume. E2EDevBench is double-counted, as both a free-form failure and a structure failure.

**Model generations.** The weak-link evidence is 2024–25-era (Claude-3.5-Sonnet, GPT-4o, Gemini 2.5). Two of the four "structure helps" results are 2024-era models on oracle-coupled setups (RealBench, Skeleton); the other two are 2026 models (CodeSpec, SpecFirst). No result holds across generations.

**Peer review.** Of the 14 hand-off citations, only RealBench (FSE), ParEval-Repo (ICPP), RepoZero (NeurIPS D&B) and RPG (ICLR) are peer-reviewed. ParEval-Repo does not support the claim, and RepoZero and RPG are qualitative or motivational.

**Verdict.** Calling it a "hypothesis" is right, but the surrounding wording is too strong: "failures concentrate", "the weak link is often", "results improve in controlled comparisons", "The rule suggested by the evidence is nonetheless simple: at every stage boundary, replace free-form text...". The "controlled comparisons" are ablations whose effect is partly an oracle-interface artefact. The prescriptive rule is not warranted.

**Defensible rewording.** "In several preprints, mostly evaluating 2024–25 models, authors attribute failures to under-specified or drifting natural-language requirements and plans (E2EDevBench, MRG-Bench via LLM-annotated labels). Ablations that remove a structured artefact reduce pass rates (RealBench, Skeleton-Guided Translation, CodeSpec, SpecFirst). However, in two of these the artefact also supplies the interface names the reference-coupled oracle requires, and none holds information content constant. We therefore propose, as a hypothesis to be tested (P3), that checkable intermediate artefacts outperform free-form hand-offs." Delete the "rule ... is nonetheless simple" sentence, or recast it as a design suggestion conditional on P3.

### X2 — "The most consistently supported interventions are executable feedback and structured, persistent intermediate artefacts" (Abstract; Synthesis Finding 4; Conclusion)
- Executable feedback: the evidence in RQ4 is many-study and mostly within-system ablations (RepoZero, CRUST-Bench, TDDev, AutoP2C), with the documented qualifications. This half is defensible.
- Structured artefacts: see X1. Of the controlled ablations, two are oracle-coupled, one is a subgroup on an out-of-scope task, and one is not cost-matched. "Checked" is not what was ablated in SpecFirst.
- Rewording: "Executable feedback is the most frequently supported intervention in within-system ablations across 2024–26 models. Ablations removing structured planning artefacts also report drops, but these are mostly single-system preprints, and in some the artefact also fixes the interface the oracle tests."

### X3 — "Adding more agents or more retrieved context is not reliably helpful" (Abstract; Finding 4; Conclusion "much weaker support")
- Context: the evidence is almost entirely contextual-tier, function-level, and 2023–24 models (Repoformer, AllianceCoder, REPOCOD, MRG-Bench). It does not transfer automatically to 2026 agentic core tasks.
- Agents: E2EDev (six frameworks), RepoGenesis, E2EDevBench. These are neutral evaluations, but ChatDev/MetaGPT run on older backbones.
- Rewording: "In function-level studies with 2023–24 models, more retrieved context often did not help. In neutral evaluations, role-based multi-agent frameworks (ChatDev/MetaGPT style) showed no consistent gain over single agents."

### X4 — "Repository construction is unsolved, and headline numbers overstate progress ... 20%–62%" (Finding 1)
- The range pools different metrics (node-weighted hybrid with LLM judge vs pytest pass rate) and model generations (Sonnet 4.5 in 2025 vs GPT-5.4/Opus 4.7 in 2026). All sources are preprints.
- "Overstate progress" is supported in the narrow sense that mean pass rate ≫ fully-correct rate (NL2Repo, BeyondSWE, CodeTeam, ProgramBench).
- Rewording: "On four from-scratch benchmarks (all preprints, models released 2025–26), the best mean test pass rates range from about 21% to 62%, while at most 8% of repositories pass every test."

### X5 — "Results on these tasks are consistently low" (Intro)
- Supported for the three named benchmarks, which are 2025–26 frontier models, so this is not a generation artefact.
- Add the model qualifier: "even for 2025–26 frontier models (Claude Opus 4.7, GPT-5.4)".

### X6 — "Few studies isolate design choices under a fixed model, harness, and budget" (Abstract; Finding 5)
- Plausible and consistent with RQ4, but uncounted (C49).
- Rewording: give the count of studies with controlled ablations (Table `tab:evidence` "C" rows), e.g., "N of M method papers report an ablation under a fixed backbone".

### X7 — "Evaluation validity is the central methodological problem" (Abstract; Finding 3)
- A judgement call. It is supported as "frequently documented", but the "each can change rankings by more than method differences" part is unsupported (C48).
- Rewording: drop the ranking sentence, or limit it to the evaluator-choice and similarity-metric evidence.

---

## Unsupported
| # | Location | Claim | Problem | Fix |
|---|---|---|---|---|
| U1 | Intro ¶1 | "Frontier models now saturate these benchmarks" | no citation | cite (e.g., a model report or leaderboard), or weaken |
| U2 | Overview Growth | core tier took off "once agent harnesses ... could sustain the hundreds of turns" | causal, uncited | weaken to co-occurrence, or count harness use |
| U3 | Synthesis F1 | "Size is the strongest predictor of difficulty" | no comparison of predictors | "pass rate falls steeply with size in three benchmarks" |
| U4 | Synthesis F3 | "Each can change rankings by more than the method differences" | evidence only for 2 of 4 issues | weaken/limit |
| U5 | Synthesis F5 | "Most method papers change ... all at once ... compare against ChatDev and MetaGPT" | no count | count from extraction, or "many" |
| U6 | Synthesis hand-off ¶ | "Oracles become more reliable when the external contract is executable than when a judge reads prose" | no comparative study | rephrase as a trade-off (C61) |
| U7 | Synthesis hand-off list | "SpecFirst's ... design-by-contract constraints" | DbC is not in SpecFirst | cite DbCConstraints2025 separately |
| U8 | Synthesis hand-off list | BeyondSWE/DeNovoSWE as weak-link hand-offs | no failure attribution in either | move to evaluation validity |
| U9 | Synthesis P2 | "None implements all of it" | universal negative without a feature table | add a table or weaken |
| U10 | Synthesis P5 | "most core evaluations are single runs" | not extracted | count, or "many" |
| U11 | Synthesis P6 | "the Cursor design-issues study" | missing \cite | `\cite{CursorDesignIssues2026}` |
| U12 | Synthesis P6 | non-functional qualities "never together" | not checked | verify across the 27 nonfunctional-coded core studies, or delete |
| U13 | Synthesis hand-off ¶ | "The rule suggested by the evidence is nonetheless simple: ... replace free-form text with an artefact that can be checked" | evidence does not isolate checkability (X1) | delete, or frame as P3's hypothesis |
| U14 | Background Related | "like most LLM4SE reviews [hou2024llm4se]" | "most" is uncounted; Hou likely reports search strings and stage counts | drop, or verify Hou and cite counter-examples |
| U15 | Conclusion | "Agents exploit whatever an oracle fails to check" | overgeneralised | "have been observed to exploit ... [cite RQ3]" |

## Verdict tally (C1–C75)
VERIFIED 47 · CORRECTED 7 · MISLEADING 10 · NOT FOUND 10 · NO FULL TEXT 1 (C25). Partial no-full-text cases (ChainBench in C36, Guo in C22) are noted inside VERIFIED entries. Mixed entries are counted under their worse verdict (C67, C69 and C71 as NOT FOUND). C52 and C58 are VERIFIED for the numbers but carry validity flags that feed X1.
