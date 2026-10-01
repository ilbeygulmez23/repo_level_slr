# Fact-check ledger — survey/sections/rq3_evaluation.tex

Method: every claim was checked against slr/data/fulltext (grep plus surrounding context). Venue comes from slr/data/corpus.csv. Claims C1–C68 follow the order of the draft. Entries tagged "VERIFIED (with caveat)" have correct numbers but a framing problem, which is described in the entry.

## Claims

### C0a — corpus counts (table at top of section; \nCore etc.)
- Draft: "Among the \nCore{} core studies, the evaluation codes are distributed as follows" (104; build/run 43, ref tests 32, human 34, LLM judge 29, non-functional 27, BDD 14, diff oracle 15, similarity 14)
- Verdict: VERIFIED (arithmetic)
- Evidence: recomputed from slr/data/corpus.csv `evaluation` column, tier=core: build-run 43, human 34, reference-unit-tests 32, llm-judge 29, nonfunctional 27, differential-oracle 15, similarity 14, bdd-e2e-tests 14 (n=104)
- Correct statement: The counts match. The table leaves out two codes in the same column: generated-tests (15) and other (23). Codes are the authors' screening codes, and the notes for them are LLM-drafted. Spot checks below show misclassifications: RealBench is coded as upstream tests but its tests are human-written with GPT-4o; TraceDev uses LLM-generated tests; Vero and SPDDWL have an LLM in the loop. Say that the codes are reviewer-assigned and add generated-tests.
- Models: n/a
- Measurement: coding of 104 core studies; no inter-rater figure reported in this section
- Status: n/a

### C27 / C59 — corpus counts
- Draft: "\nCoreLLMJudge{} of \nCore{} core studies use an LLM to produce at least part of the verdict" (29/104); "Non-functional quality is measured in \nCoreNonfunctional{} core studies" (27)
- Verdict: VERIFIED (arithmetic). The LLM count is probably a lower bound.
- Evidence: corpus.csv counts as above
- Correct statement: The count of 29 covers only the `llm-judge` code. Several studies use an LLM to produce or adapt the oracle (generated-tests 15; e.g. ProgramBench, CLI-Tool-Bench, TraceDev, RepoGenesis, SPDDWL), and Vero/SWE Refactor Bench use LLM auditors. Either say "at least 29" or recount.
- Models: n/a
- Measurement: screening codes
- Status: n/a

### C38 — MultiAgentFrontEnd2025
- Draft: "In MultiAgent-FrontEnd, judge tokens exceed generator tokens by a factor of about six."
- Verdict: NO FULL TEXT
- Evidence: none. The corpus record says "no full text". The figure ("5.9x") comes only from the LLM-drafted note in corpus_notes.md, which is based on the abstract. ACM DL returns 403, and Crossref has no abstract.
- Correct statement: Get the full text or delete the claim. Crossref gives the venue as MSR 2026 (Proceedings of the 23rd Int. Conf. on Mining Software Repositories). The corpus venue column says "ACM proceedings (venue unclear)" and should be updated.
- Models: per note, 6 generator–judge pairs from the Claude/Gemini/GPT families (unverified)
- Measurement: unverifiable
- Status: MSR 2026 (per Crossref); corpus says unclear

### C53 — Spec2Code2025
- Draft: "Spec2Code: builds an explicit taxonomy of LLM evasion behaviours, such as skipped tests and left-over stubs."
- Verdict: NO FULL TEXT
- Evidence: none. The record is a Code Ocean capsule with no paper, and corpus.csv flags it "low qa". The claim rests on an LLM-drafted abstract note.
- Correct statement: Delete, or cite as "Spec2Code (non-peer-reviewed code capsule) proposes ..." after reading the capsule. Do not use it as evidence of evasion frequency.
- Models: unknown
- Measurement: none reported (cost/time/coverage on the system's own tests)
- Status: preprint (Code Ocean capsule)

### C11b — cJSON porting (cJSONRustPorting2026; uncited in table)
- Draft: Table row "Differential vs. executable reference": "..., cJSON porting"
- Verdict: NO FULL TEXT
- Evidence: corpus ft_note "no full text; ... CVE tests, differential fuzzing, Miri"
- Correct statement: Add \cite{cJSONRustPorting2026}. Its classification as a differential oracle rests only on the abstract.
- Models: "5 LLMs" (unverified)
- Measurement: unverifiable
- Status: Future Internet 2026 (MDPI journal)

# G1 fact-check (rq3_evaluation.tex, similarity oracles + partial credit)

### C1 — CodeS2024
- Draft: "SketchBLEU (CodeS~\cite{CodeS2024}, ...)" (table row "Similarity to reference")
- Verdict: VERIFIED
- Evidence: "repository-oriented evaluation metric SketchBLEU" (Sec. intro/IV); Table II "Performance of CODES and its baselines on SketchEval ... four parts of SketchBLEU"
- Models: GPT-3.5-turbo-0613 (2023), CodeLlama 7/13/34B (2023), DeepSeekCoder 7/33B (2023), StarCoder2 3/7/15B (2024); baselines ChatDev/AutoGPT/AgentGPT on GPT-3.5.
- Measurement: SketchEval, 19 repos (5 easy/8 medium/6 hard); SketchBLEU = weighted CodeBLEU-style score vs reference repo; no execution/tests; no seeds/runs reported. Also a 30-participant VSCode-plugin user study (RQ3, completion time; master students).
- Status: preprint in corpus `venue` column, BUT corpus `venue_record`/DOI = ACM TOSEM (10.1145/3768577) — appears published; venue column likely stale.

### C2 — CodeTeam2026
- Draft: "SketchBLEU (... CodeTeam~\cite{CodeTeam2026})"
- Verdict: VERIFIED
- Evidence: "SketchBLEU[42] serves as the main evaluation metric" (Sec. 3); Table 2 "Performance on SketchEval measured by SketchBLEU (%). We report mean ±std over three seeds."
- Models: Qwen2.5-72B-Instruct (2024) for all agents/baselines; SFT variant on same backbone (4-bit NF4).
- Measurement: SketchEval 19 repos, 3 seeds, Wilcoxon signed-rank; plus NL2Repo-Bench execution check (see C19).
- Status: preprint

### C3 — ECAT2026
- Draft: "node alignment (ECAT~\cite{ECAT2026})" in row "Similarity to reference"
- Verdict: VERIFIED (with caveat)
- Evidence: "Node Alignment measures structural preservation by constructing platform-agnostic semantic graphs for the Android and HarmonyOS repositories ... Align = |M|/|Vs|" (Sec. 4.1)
- Correct statement (caveat): the "reference" is the Android SOURCE repo (migration; no target reference exists). ECAT pairs it with Agent-as-Judge (feature checklist, Full/Partial/Missing), and itself shows node alignment is misleading: "ReCodeAgent attains relatively high Node Alignment but much lower Agent-as-Judge scores because many translated classes preserve the repository structure while containing only shallow implementations or placeholder logic." This is a good extra piece of evidence for the "similarity is not correctness" paragraph.
- Models: DeepSeek-V4-Pro (2026) generator; Qwen3.7-Plus (2026) multimodal for dynamic entropy; DeepSeek-V4-Flash in ablation.
- Measurement: 3 repos (Gallery 50K LOC, AntennaPod, Meshtastic); ECAT 3 runs, baselines apparently single run; CodeGraph-based node matching; agent judge LLM.
- Status: preprint (corpus flag "low qa")

### C4 — EvoC2Rust2025
- Draft: "line acceptance (EvoC2Rust~\cite{EvoC2Rust2025})"
- Verdict: VERIFIED (with caveat)
- Evidence: "Line Acceptance Rate (AccRate)[54]: This metric evaluates the fidelity of the initial translation by comparing it to the manually corrected version. Precision captures the percentage of correct lines in the initial output, while Recall measures their preservation in the final code." (Sec. 3.3)
- Correct statement (caveat): the reference is not an independent ground truth but a human-repaired (with Claude Sonnet 4 assistance) version of each method's own output: "For each project, we first translated the code using the target methods ... failures were manually repaired by three senior engineers with assistance from Claude Sonnet 4". It is a project-level metric used where "reference implementations are unavailable". EvoC2Rust also reports Test Pass Rate at module level (fill-in) and compile rates, so similarity is not its sole oracle.
- Models: DeepSeek-V3 (2024), Qwen3-32B (2025); greedy decoding.
- Measurement: Vivo-Bench (19 industrial projects) + C2R-Bench; ICompRate, AccRate, SafeRate (project level); FCompRate, TestRate (module level).
- Status: ICSE-SEIP 2026

### C5/C15 — ProjectEval2025
- Draft: "ProjectEval finds that CodeBLEU rankings contradict pass@$k$." / table: "contradicts pass@k (ProjectEval)"
- Verdict: MISLEADING
- Evidence: "this finding in ProjectEval Pass@5 is conflicted with the CodeBLEU result, as the latter's cascade scores are higher than the direct scores no matter it uses Level 1 or Level 2 input, both in Code and PV ... GPT-4o's cascade generation did has better structure of the code but it just missed filling a path parameter" (Sec. 5.2, RQ2)
- Correct statement: For GPT-4o only, ProjectEval finds that CodeBLEU favours cascade over direct generation while Pass@5 favours direct generation; the authors conclude "execution pass rate is better than the similarity indicators". It is one model and one pairwise mode comparison, not a contradiction between model rankings in general. Also, Pass@k for all other models is near zero ("As for the core scores (Pass@K) of all LLMs, they are too low to analyze").
- Models: GPT-4o (2024), Gemini 1.5 Pro / 2.0 Flash (2024), Gemma/Gemma-2, Llama-2/3.1/3.2, Mistral, CodeGemma, CodeLlama; OpenHands agent.
- Measurement: 20 projects, 284 GPT-4o-generated + human-reviewed test cases; Pass@5; best Pass@5 ~12-16% (GPT-4o); benchmark built with GPT-4o (same-family as best-scoring model).
- Status: corpus says preprint, but DOI 10.18653/v1/2025.findings-acl.1036 = ACL Findings 2025 (venue column likely stale).

### C6/C16 — ProjectGen2025
- Draft: "In ProjectGen, SketchBLEU barely separates methods (MetaGPT and ProjectGen both score about 91--92\%) whose test outcomes differ widely." / "fails to discriminate"
- Verdict: VERIFIED
- Evidence: Table 6 (CodeProjectEval) SketchBLEU AVG: MetaGPT 91.12 (DeepSeek-V3) / 91.54 (GPT-4o); ProjectGen 92.20 / 92.11. Table 5 #Pass SUM: MetaGPT 35 / 28 vs ProjectGen 160 / 310 (of 3,348 tests). Authors: "evaluating project code generation performance based solely on structural similarity has inherent limitations, as it may not reliably reflect the actual functional correctness." Also "Even though CodeS fails to pass any test cases, it still achieves average SketchBLEU scores of 69.82 and 67.16."
- Caveat: the 91-92% figures are CodeProjectEval only (on DevBench the pair scores 87.81/87.66 and 90.01/88.41). The pass difference is concentrated in few tasks (e.g. ProjectGen GPT-4o pyjwt 285 of its 310 passes; rsa 90 of 160 for DeepSeek); 13 of 18 tasks have zero passes for every method. "Differ widely" is true in counts but rests on 1-2 tasks; single run at temperature 0. CodeS's ~68-70 SketchBLEU with 0 passes is arguably stronger evidence.
- Models: DeepSeek-V3 (2024), GPT-4o (2024).
- Measurement: CodeProjectEval 18 repos (597-9,314 LOC), DevBench 10 repos; #Pass of upstream tests; temperature 0, one run.
- Status: corpus says preprint; DOI 10.1145/3817056 = ACM TOSEM (venue column likely stale).

### C17 — CodevBench2024, ExecRepoBench2024
- Draft: "Codev-Bench~\cite{CodevBench2024} and ExecRepoBench~\cite{ExecRepoBench2024} report correlations between edit similarity and pass rate below 0.85."
- Verdict: CORRECTED
- Evidence (Codev-Bench): "apart from Scenario 2, which has a correlation of 0.991, the correlation in the other three scenarios is below 0.85, specifically 0.793 from Scenario 1, 0.529 from Scenario 3, and 0.822 from Scenario 4" (Sec. 5 / App. C). Evidence (ExecRepoBench): no correlation coefficient anywhere; only "there exists a mismatch between the n-gram-based metric ES and execution-based metric pass@1. Granite-Coder-8B gets a good pass@1 score but a bad ES score" (Sec. 5.5).
- Correct statement: Codev-Bench reports Pearson correlations between edit similarity and Pass@1 of 0.53-0.82 in three of four scenarios (0.99 in the fourth); ExecRepoBench reports a qualitative mismatch (e.g. Granite-Coder-8B high pass@1, low ES) without a correlation figure. Also note both are code-completion (block/line) benchmarks, not repository generation.
- Models: Codev-Bench: 16 models incl. GPT-4/4o/4o-mini, Claude-3.5-Sonnet (2024), DeepSeek-V2, Llama-3.1-70B/405B, Qwen-2, CodeQwen-1.5, DeepSeek-Coder-V2-Lite, StarCoder2-7B, CodeGemma-7B. ExecRepoBench: CodeLlama, StarCoder(2), DS-Coder, Qwen2.5-Coder, Granite-Coder, Yi-Coder (2023-2024), greedy.
- Measurement: Codev-Bench Pearson over per-model averages (n=16 points per scenario), 10 repos / 296 completion blocks (per corpus map); ExecRepoBench 1.2K samples / 50 repos.
- Status: both preprint

### C18 — CodeS2024, CodeTeam2026
- Draft: "several method papers still rest their main claims and all their ablations on similarity, notably CodeS and CodeTeam."
- Verdict: VERIFIED (minor caveat)
- Evidence: CodeS ablations (Table V, Fig. 4) all SketchBLEU: "after removing the import information, the decrease in SketchBLEU on the easy task is 1.89%"; CodeTeam: "SketchBLEU serves as the main evaluation metric"; ablations "conducted under the CodeTeam-PE setting" on SketchEval; "we treat it [NL2Repo-Bench] as an external validation benchmark for RQ1 rather than repeating the full ablation study".
- Caveat: CodeS also has a 30-participant user study (practicality; Copilot comparison), so its claims are not solely similarity. CodeTeam ablations additionally log planning diagnostics (QA iterations etc.), none execution-based.
- Models/Measurement/Status: see C1, C2.

### C19/C43 — CodeTeam2026 (on NL2RepoBench2025)
- Draft: "CodeTeam does run an execution-based cross-check on NL2Repo-Bench, and that check reveals a gap between 42\% average test pass and 6\% complete repositories." / "CodeTeam on NL2Repo-Bench: 42\% mean vs 6\% Pass@1."
- Verdict: VERIFIED (with validity flag)
- Evidence: "CodeTeam (SFT) reaches 42.3% overall pass rate with a Pass@1 of 6.1%" (Sec. 4.2, Table 5); Pass@1 = "average percentage of tasks fully solved by a single generation, averaged over three random seeds". PE variant: 34.6% / 5.1%.
- Validity flag: 42.3% is the SFT variant (PE: 34.6%). With Qwen2.5-72B (2024), CodeTeam's numbers exceed every system in the NL2Repo-Bench paper (best Claude-Sonnet-4.5 + Claude Code 40.2%; GPT-5 21.7%), and even CodeS(PE) on Qwen2.5-72B (30.2%) beats GPT-5/DeepSeek-V3.2 there. CodeTeam used its own adapted harness ("A practical adaptation is needed ... we route the implementation process through CodeTeam's internal coordination workflow"), evaluation via the original pytest suite. Not reproduced independently; numbers should be treated as self-reported.
- Models: Qwen2.5-72B-Instruct (2024), PE and SFT.
- Measurement: 104 tasks, 3 seeds, upstream pytest; mean pass rate per task averaged over seeds; Pass@1 = mean % fully solved.
- Status: preprint

### C41 — NL2RepoBench2025
- Draft: "NL2Repo-Bench: the best configuration reaches 40\% mean pass rate but fully solves about 5 of 104 tasks."
- Verdict: CORRECTED
- Evidence: Table 3: "Claude-Sonnet-4.5 (Claude Code) 40.2 | Pass@1 count 3"; "Claude-Sonnet-4 37.0 | 5"; Claude-Sonnet-4.5 (OpenHands) 39.9 | 3; (Cursor) 39.2 | 4. Text: "all models achieve an average test pass rate below 40.5% ... the strongest model fully passes the official pytest suite for only five repositories in a single run (Pass@1)."
- Correct statement: The best configuration (Claude-Sonnet-4.5 in Claude Code) reaches 40.2% mean pass rate but fully solves only 3 of 104 tasks; no configuration fully solves more than 5 (Claude-Sonnet-4, 37.0%). Suggested phrasing: "the best configuration reaches 40% mean pass rate yet fully solves only 3 of 104 tasks (at most 5 for any configuration)". (The paper's own text is internally inconsistent with its table; either way the point stands.)
- Models: Claude-Sonnet-4.5 (2025), Claude-Sonnet-4 (2025), Gemini-3-pro (2025), GPT-5 (2025), DeepSeek-V3.1/V3.2 (2025), Kimi-k2 (2025), Qwen3-Instruct/Thinking (2025), GLM-4.6 (2025); OpenHands default, plus Claude Code and Cursor.
- Measurement: 104 tasks, single run, upstream pytest suites; Pass@1 = count fully passing.
- Status: preprint

### C21a (C7a, C20a) — NL2RepoBench2025
- Draft: "This is why NL2Repo-Bench ... include API signatures or module surfaces in the input." and tests "call specific module paths, class names, and private helpers."
- Verdict: VERIFIED for spec content and upstream tests; "private helpers" NOT FOUND for NL2Repo specifically
- Evidence: Spec has an "API Usage Guide: Detailed descriptions of the core features to be implemented, including specific requirements for classes, functions"; annotators extract "all classes, functions, and constants; their names and signatures; their file locations" and give "Module Import Instructions ... derived from the project's internal import patterns as observed in the test files" (Sec. 3.1.2, App. C.3.3). "Since NL2Repo-Bench evaluates generated repositories using the original test suite ... this section must provide a complete and accurate description of all functional nodes exercised by the tests. Any omission or misaligned API definition would make the task unresolvable." Failure analysis: "mismatch between the agent's implementation and the official test suite's expectations (e.g., function signatures or class attributes)".
- Note: the paper simultaneously claims the setting has "no scaffolding or signatures" (Sec. 2.1), contradicted by its own App. C.3.3 — worth stating explicitly as support for the survey's argument. Upstream tests = white-box official pytest suites (verified); NL2Repo text does not mention "private helpers" (sourcing for that phrase must come from another paper, e.g. Commit0/DeNovoSWE).
- Models/Measurement/Status: see C41.

# G2 fact-check (rq3_evaluation.tex)

### C7 — Commit02024, RealBench2025, DeNovoSWE2026, REPOCOD2024
- Draft: "White-box upstream tests & Commit0, NL2Repo, RealBench, DeNovoSWE, REPOCOD & high & encode names, signatures, and module boundaries; force the specification to fix the API"
- Verdict: CORRECTED (RealBench misclassified; the other three are right)
- Evidence:
  - Commit0: "a starter repository with both unit tests and files to fill in"; "we replace the function body of all public functions to be empty (pass) and remove all private functions entirely" (Sec. 3). The API is fixed by the stubs, and the tests are visible to the agent.
  - DeNovoSWE: "we first run the original unit-test suite"; the docs must include "Import Path ... Signature"; "Do not make downstream models guess things that the tests rely on, including exact signatures" (Sec. 3.2, App. prompt). Upstream tests are hidden and applied as test_patch at evaluation.
  - REPOCOD: "developer-written test cases"; the input is the "repository snapshot, target function signature, and docstring" (Sec. 3). This is a function-level task, so the signature is given by construction.
  - RealBench: "we manually create a test suite for each repository ... participants can use the existing test cases in repositories and also apply advanced LLMs (i.e., GPT-4o) to help generate test cases. All tests are verified by the other participant" (Sec. 2.2.4). The API is fixed by a UML class diagram with "Method signatures with parameters, return types, and visibility" (Table 2). The method-level tests also inspect class fields ("inspects the method's impact on the class's fields").
- Correct statement: RealBench uses curated tests written by humans with help from GPT-4o, seeded from repository tests. They are not upstream tests. They are still white-box: they check field state, and the API is fixed by UML signatures. Either move RealBench out of the row or relabel the row "white-box (upstream or curated) tests". BeyondSWE Doc2Repo uses upstream tests adapted by an LLM with human review (see C8).
- Models: Commit0: 2024 models (Claude 3.5 Sonnet, GPT-4o-mini, DeepSeek-V2.5, etc.). REPOCOD: 2024 models. RealBench: GPT-4o, Claude-Sonnet-4, Gemini-2.5-Flash, DeepSeek-V3, Qwen3-235B, Qwen2.5-Coder-7B (2024–25). DeNovoSWE: Qwen3-30B-A3B fine-tuned (2025).
- Measurement: unit-test pass rate (Commit0, DeNovoSWE pass ratio); all relevant tests passing (REPOCOD); RealBench class-level completion, execution and test pass rates.
- Status: Commit0 preprint (ICLR 2025 version exists, but corpus says preprint); RealBench FSE 2026; DeNovoSWE preprint; REPOCOD ACL 2025.

### C20 — Commit02024, RealBench2025, DeNovoSWE2026, REPOCOD2024, BeyondSWE2026, RALBench2026
- Draft: "Upstream tests ... call specific module paths, class names, and private helpers."
- Verdict: MISLEADING (module paths and class names are supported; "private helpers" is not supported for upstream tests)
- Evidence:
  - DeNovoSWE: "Direct components are those explicitly imported, instantiated, or invoked in the unit test files ... documented ... especially their import paths, public APIs" (Sec. 3.2).
  - BeyondSWE: "require agents to infer the structure from contextual cues such as import paths. We adapt tests from the original repositories" (Sec. 3.3).
  - RAL-Bench: "reduce evaluation artifacts caused by mismatched entry points or module paths". RAL-Bench's own tests are black-box system tests, not upstream tests.
  - None of the papers says that upstream tests call private helpers. Commit0 removes private functions entirely, which implies its tests target public functions. The only "private" statement is in ReCUBE, whose tests are generated by an LLM (Claude Opus 4.1), not taken from upstream: internal tests target "implementation-specific logic and private functions/methods".
- Correct statement: "Upstream tests import specific module paths and call specific class and function names (DeNovoSWE, BeyondSWE), so the specification must fix these names." Drop "private helpers", or attribute it to ReCUBE's LLM-generated internal tests.
- Models / Measurement: n/a (characterisation).
- Status: see the individual entries.

### C21 — BeyondSWE2026, DeNovoSWE2026, RALBench2026
- Draft: "This is why NL2Repo-Bench, BeyondSWE, DeNovoSWE, and RAL-Bench include API signatures or module surfaces in the input."
- Verdict: VERIFIED
- Evidence:
  - BeyondSWE: the spec covers "public classes and functions, parameters, return types" and removes the "directory structure". The example lists "method signatures" (Fig. 13).
  - DeNovoSWE: the docs include "Import Path, ... Signature, Parameters, Returns, Raises" (doc-generation prompt).
  - RAL-Bench: "we additionally provide the expected module and package surface of the reference repository ... to reduce evaluation artifacts caused by mismatched entry points or module paths" (Sec. 2). On Stegano with GPT-5.2, the score is 0.1667 without the interface and 0.6667 with it.
- Correct statement: — (The causal "this is why" matches RAL-Bench's and DeNovoSWE's stated rationale. BeyondSWE does not state it, and it hides the directory structure, so agents must infer module paths from import cues.)
- Models: BeyondSWE: GPT-5.4, DeepSeek-V4-Pro, GLM-5, Gemini 3 Pro, Kimi-K2.5 (2025–26). RAL-Bench: GPT-3.5 through GPT-5.2, Claude 4.5, Gemini 3 (2023–25).
- Measurement: n/a
- Status: all three are preprints.

### C8 — E2EDevBench2025, RPGZeroRepo2025, TraceDev2026
- Draft: "Adapted/migrated tests & E2EDevBench, RepoCraft, TraceDev & medium & adaptation is unvalidated; evaluator false negatives ..."
- Verdict: MISLEADING (an LLM is in the loop for all three; "unvalidated" is too strong for RepoCraft and imprecise for TraceDev)
- Evidence:
  - E2EDevBench: "an independent 'Test Migration Agent' ... adapt the original project's test cases", run by Gemini-2.5-Pro (Sec. 3.1–3.2). The only validation is indirect: migrated tests have a lower pass rate (59.66% vs 93.14%) and higher coverage (Table 2). Nobody checks whether the migrated tests are correct.
  - RepoCraft: "the provided ground-truth test ... is rewritten to match the naming and structural conventions of the localized function or class" by an o3-mini agent (App. E.3). The pipeline is validated in two ways. It runs on the gold projects (81.0% pass, 92.0% voting). Humans also annotated 2 systems: Pearson 0.89 for coverage and 0.96 for novelty, and human Pass/Vote 62.0/73.0 vs o3-mini 69.8/75.0 (Table 5).
  - TraceDev: the tests are not upstream. They are generated by an LLM from the use case plus ground-truth code and kept only if they pass on ground truth ("we retain the test cases that pass on ground-truth code"; 962 for eTour, 1,179 for SMOS). They are then adapted ("we adapt and execute them against the generated code") by DeepSeek-V3.2, with no validation of the adaptation step.
- Correct statement: "Tests are adapted by an LLM to the generated repository's names and structure. The validation of this step is weak or indirect: E2EDevBench reports only coverage and pass-rate deltas, TraceDev reports none, and RepoCraft checks its pipeline on gold projects and against human ratings on two systems. TraceDev's source tests are LLM-generated, not upstream." BeyondSWE Doc2Repo also belongs in this row: it adapts tests "with LLM assistance and human review" and checks them against the reference implementation.
- Models: E2EDevBench: Gemini-2.5-Pro and Gemini-2.5-Flash (2025). RepoCraft: o3-mini, Qwen3-Coder, Claude 4 Sonnet, Gemini 2.5 Pro, o3-pro (2025). TraceDev: Gemini-2.5-Flash, DeepSeek-V3.2 (2025).
- Measurement: E2EDevBench: requirement-level judge, 3 runs, 50 projects. RepoCraft: 6 repositories, 1,052 tasks, o3-mini evaluator. TraceDev: 2 datasets, Java.
- Status: E2EDevBench preprint; RepoCraft ICLR 2026; TraceDev ISSTA 2026.

### C9 / C31 — RPGZeroRepo2025
- Draft: "evaluator false negatives (RepoCraft: 19% on gold)"; "RepoCraft's evaluation pipeline scores the gold projects themselves at only 81% pass." (C31 appears under the bullet "Judges hallucinate.")
- Verdict: VERIFIED for the number; MISLEADING for C31's placement
- Evidence: "we first validate the automatic localization and validation pipeline on human-developed Gold Projects, where it achieves 81.0% pass rate and 92.0% voting agreement, establishing the ceiling under our test harness" (Sec. 6; Table 2 "Gold Projects Human Developers - - 81.0 / 92.0").
- Correct statement: The 81.0% figure is correct, so 19% of gold tasks fail. That failure combines localization misses, LLM-vote rejections and test adaptation by an LLM. It is a ceiling or false-negative rate, not judge hallucination in the sense of HiRAS's inflated scores. Move C31 out of "Judges hallucinate", or reword it as "LLM-in-the-loop evaluators also produce false negatives". Also note that the gold-project run is the authors' own validation, which cuts against C8's "unvalidated".
- Models: evaluator o3-mini (2025).
- Measurement: 6 gold repositories, 1,052 tasks, single run. Pass = the adapted ground-truth test passes; Vot. = 5-vote LLM majority.
- Status: ICLR 2026.

### C22 — ReCUBE2026
- Draft: "separates tests into those that exercise external cross-file usage (58.7%) and those that probe internal implementation details (41.3%)."
- Verdict: VERIFIED (with a note)
- Evidence: "RECUBE comprises a total of 10,785 unit tests, consisting of 58.7% external cross-file validations and 41.3% internal in-file implementation checks (Table 2)". Internal tests target "implementation-specific logic and private functions/methods" (Sec. 3.2.1).
- Correct statement: — The tests are generated by an LLM (Claude Opus 4.1) and filtered to those that pass on gold; they are not upstream tests. The task is to reconstruct a single masked file, not a whole repository. Internal tests are easier: +9.55% strict pass rate (SPR) on average.
- Models: GPT-5, GPT-5 Mini, Qwen3-Coder, Devstral Small, etc. (2025).
- Measurement: 10,785 tests over 366 files in 20 repositories; external/internal labels assigned at generation time (exact procedure not detailed).
- Status: preprint.

### C39b — E2EDevBench2025
- Draft: "Vibe Code Bench, WebGen-Bench, CLI-Tool-Bench, AppEvalPilot, and E2EDevBench report human alignment"
- Verdict: VERIFIED (for E2EDevBench, with a caveat)
- Evidence: "We randomly selected 10 agent-generated projects with 546 requirements and invited three computer science graduate students ... Pearson's correlation coefficients were all above 0.62 ... pairwise agreement rate between the LLM and the experts ranged from 76% to 84% ... inter-expert agreement rate of 78% to 88%" (Sec. 4.1, Fig. 2).
- Correct statement: — The alignment covers only the requirement judge, not the test migration. The judge (Gemini-2.5-Pro) is the same model as one of the evaluated agents' backbones, and the same model also annotated the dataset and migrated the tests. This is self-evaluation within the same family.
- Models: Gemini-2.5-Pro and Gemini-2.5-Flash (2025).
- Measurement: 10 projects, 546 requirements, 3 graduate-student raters, Pearson r 0.62–0.67.
- Status: preprint.

### C42 — BeyondSWE2026
- Draft: "BeyondSWE Doc2Repo: 62% pass rate, 2--4 of 50 repositories fully correct."
- Verdict: CORRECTED (minor)
- Evidence: Table 2: the best Doc2Repo pass rate is 61.74 (Codex GPT-5.4 xhigh with SearchSWE prompt) and 61.64 with the default prompt. Fully correct counts across all configurations range from 0 to 4 (MiniMax-M2.5 SearchSWE = 0; GPT-5.4 SearchSWE = 4). Text: "even the best configuration produces only 2 fully correct repositories out of 50" (Sec. 5.2).
- Correct statement: "best pass rate about 62%; at most 4 of 50 repositories fully correct in any configuration (the best-scoring configuration gets 2)." The phrase "2–4" omits configurations with 0–1. The pass rate is the mean share of tests passed, not task success.
- Models: GPT-5.4, DeepSeek-V4-Pro, GLM-5, Qwen3.5-Plus, Gemini 3 Pro, Kimi-K2.5, Seed-Coder-2.0, MiniMax-M2.5 (2025–26).
- Measurement: 50 repositories; LLM-adapted upstream tests with human review; single run per configuration.
- Status: preprint. The full text appears to be a revised version (GPT-5.4 / DeepSeek-V4). Check that the cited version matches.

### C45 — JavaBench2024
- Draft: "JavaBench: project-wise Pass@1 is 0 in every setting."
- Verdict: VERIFIED (with a framing note)
- Evidence: "no project can be correctly completed by any studied LLMs, and at most 41.17% Pass@5 in a more relaxed evaluation" (Abstract/Intro). Table 5 reports only class-wise and test-wise metrics.
- Correct statement: — Project-wise Pass@1 is not a tabulated metric. The paper states it qualitatively ("no project can be correctly completed"). The benchmark has only 4 projects. The models are 2023-era: WizardCoder-15B, deepseek-coder-6.7b/33b, Phind-CodeLlama-34B, gpt-3.5-turbo-1106.
- Models: see above (2023).
- Measurement: 4 student Java projects (106 classes, 389 methods); 3 context settings × synthesis strategies; Pass@1 and Pass@5.
- Status: preprint.

### C46 — RealBench2025
- Draft: "RealBench: completion 91% -> execution 45% -> test pass 19%."
- Verdict: VERIFIED (with a caveat)
- Evidence: "The best average completion rate, Execution pass rate, Test pass rate ... are 91.18%, 45.00%, 19.39% ... among the studied LLMs" (Finding 1, Sec. 4.1).
- Correct statement: — Each number is the best value for its own metric. They can come from different model/strategy cells, so the arrow chain is not one model's funnel. The metrics are class-level, and the tests are human-written with help from GPT-4o (see C7).
- Models: GPT-4o (2024-05), Claude-Sonnet-4, Gemini-2.5-Flash, DeepSeek-V3, Qwen3-235B-A22B, Qwen2.5-Coder-7B (2024–25).
- Measurement: 61 repositories, about 50 tests per repository, greedy decoding, single run.
- Status: FSE 2026.

### C60 — RALBench2026
- Draft: "combines maintainability, security, robustness, efficiency, and resource usage. Its models differ widely on this score while having similar functional scores, and self-repair and planning strategies lower it (57.1 -> 46--50)."
- Verdict: VERIFIED (with caveats)
- Evidence: "aggregates five normalized quality dimensions ... maintainability, security, robustness, efficiency, and resource usage". "Gemini-2.5-Pro and GPT-4o-2024-11-20 have similar functional scores (27.63% vs. 27.48%), but their non-functional scores differ substantially (35.15% vs. 57.59%)". Strategy results: "baseline ... 41.80% functional correctness and 57.10% non-functional"; S1 self-repair 46.10%; S2 environment repair 49.90%; S3 planning 49.60% (Sec. 3.5, RQ4).
- Correct statement: — "Differ widely while having similar functional scores" rests on one highlighted pair. The strategy comparison uses one model (GPT-5.2) and one run per strategy, by the authors' description "a single-model controlled study". The 46–50 range covers three strategies, including environment repair. Scores are normalized against the reference repository. The security dimension is near ceiling (average 87%).
- Models: 16 LLMs (GPT-3.5-Turbo through GPT-5.2, Claude-3.7/4.5, Gemini-2.5/3, DeepSeek-V3/R1, o1/o3; 2023–25). The strategy study uses GPT-5.2.
- Measurement: 38 repositories, black-box system tests validated on the reference implementation; non-functional scores from static analysis and runtime measurement; rerun stability checked over 5 runs for 3 models.
- Status: preprint.

### C68 — RPGZeroRepo2025
- Draft: "RepoCraft reports 36k-line outputs."
- Verdict: VERIFIED
- Evidence: "ZeroRepo with Qwen3-Coder generates 36K LOC and 445K tokens" (Sec. 6; Table 2: 36,941.0 LOC). Gold projects average 97,819.7 LOC.
- Correct statement: — The 36k figure is for ZeroRepo (the authors' RPG-guided system) with Qwen3-Coder, averaged over 6 repositories. ZeroRepo with o3-mini produces about 24K. Claude Code produces about 10.6K. Other agents produce under 1.5K. Suggested wording: "ZeroRepo, evaluated on RepoCraft, produces 36k-line outputs".
- Models: Qwen3-Coder-480B (2025).
- Measurement: effective LOC excluding tests and examples; 30 iterations.
- Status: ICLR 2026.

# G3 — system-boundary / differential oracles (C10, C11, C23, C24, C25, C26, C39a, C44, C47, C57, C67)

### C10 — RepoGenesis2026, RepoModBench2026, ProjDevBench2026, E2EDev2025
- Draft: "Interface black-box tests & RepoGenesis (HTTP), RepoMod-Bench (CLI/REST), ProjDevBench (OJ), E2EDev (BDD) & low (interface fixed) & exact I/O formats penalise valid variants; pre-assigned DOM IDs (E2EDev)"
- Verdict: VERIFIED (classification); weakness "exact I/O formats penalise valid variants" is an inference, not measured in any of these four papers
- Evidence: RepoGenesis "We evaluate generated repositories using black-box testing: deploying the microservice, executing test cases" (§2.3.2); RepoMod-Bench "CLI tools: Interaction occurs via standard streams (stdin/stdout) ... REST APIs: Interaction is conducted via HTTP requests" (§2.2) and prompt "These tests verify exact behavioral equivalence ... Output format (whitespace, JSON structure, etc.)" (prompt appendix, l.891-894); ProjDevBench "Combining Online Judge (OJ) testing with LLM-assisted code review" (abstract); E2EDev "multiple BDD test scenarios with corresponding Python step implementations ... built on the Behave framework" (abstract); E2EDev "we use GPT-4o to assign unique test IDs to key UI components" (§3.2).
- Correct statement: n/a. Optional nuance: ProjDevBench verdict also includes an LLM code-review score (so "LLM in loop" column "sometimes" is right). The format-penalty weakness is only quantified in CLI-Tool-Bench (EM 23.50% vs FM 39.00%), which is in the differential row.
- Models: RepoGenesis: GPT-5.1, GPT-5.1 mini, Claude Sonnet 4.5, Qwen3-Coder-30B-A3B, Qwen3-30B-A3B (2025) in DeepCode/MetaGPT/MS-Agent/Qwen-Agent + Cursor/Copilot/Antigravity. RepoMod-Bench: Claude Opus 4.5, GPT-5.2 (late 2025) in Claude Code/Codex CLI/OpenCode. ProjDevBench: GPT-5, Claude Sonnet 4.5, Gemini 3 Pro Preview, GLM-4.6, Kimi-k2-0905, DeepSeek-V3.2-Exp (2025). E2EDev: Claude Haiku 4.5, GPT-4o, GPT-4o-mini, Qwen2.5-7B/70B/Max (2024-25).
- Measurement: RepoGenesis 30 verified repos (106 total), Pass@1/AC/DSR averaged over 5 runs; RepoMod-Bench 21 repos, 11,616 tests derived from source repos' own suites; ProjDevBench 20 OJ problems (only 5 from scratch); E2EDev 46 projects, 244 requirements, 703 BDD tests.
- Status: all preprint (RepoGenesis 2026, RepoMod-Bench 2026, ProjDevBench 2026, E2EDev 2025).

### C11 — RepoZero2026, CLIToolBench2026, ProgramBench2026, SWERefactorBench2026
- Draft: "Differential vs. executable reference & RepoZero, CLI-Tool-Bench, ProgramBench, SWE Refactor Bench ... & strict string matching; ``no-migration'' loophole; coverage limited to probed behaviour & test generation"
- Verdict: VERIFIED (with nuance on the LLM column)
- Evidence: RepoZero "A sample is considered successful (PR = 1) if and only if the outputs from both the source and target repositories exhibit strict string-level consistency" (§5 Metrics); CLI-Tool-Bench "Powered by an automated black-box differential testing framework" (abstract); ProgramBench "agents must architect and implement a codebase that matches the reference executable's behavior" (abstract); SWE Refactor Bench "a behavioural suite gives full marks to a repository handed back untouched" (§2, Stage I); ProgramBench "any test suite checks a finite set of inputs and therefore necessarily under-approximates the gold executable's full specification" (§2.1).
- Correct statement: LLM-in-loop column should read "test generation; semantic judge (CLI-Tool-Bench); migration-audit judge + agentic verifiers (SWE Refactor Bench); cheating judges (ProgramBench)". SWE Refactor Bench's Stage I is LLM-judged (gpt-5.6-sol, 3 samples majority) and Stage III uses 6 LLM coding agents; ProgramBench flags cheating with 9 LLM judges (GPT 5.2, Claude Sonnet 4.5, Gemini 3.1 Pro).
- Models: see C23.
- Measurement: see C23.
- Status: RepoZero NeurIPS 2026 (D&B); others preprint.

### C23 — RepoGenesis2026, RepoModBench2026, CLIToolBench2026, ProjDevBench2026, ProgramBench2026, RepoZero2026
- Draft: "The clearest trend of 2026 is to test at the system boundary: HTTP endpoints in RepoGenesis; CLI or REST interfaces in RepoMod-Bench; command schemas in CLI-Tool-Bench; online-judge I/O in ProjDevBench; executables in ProgramBench; public APIs in RepoZero. Behaviour of an executable reference then becomes the oracle, and tests can be generated at scale without human labelling, because every generated test is validated on the reference."
- Verdict: MISLEADING (the boundary list is correct and all six are 2026; the "executable reference ... every generated test validated on the reference" sentence holds for only 3 of the 6 listed)
- Evidence, per benchmark:
  - RepoGenesis: NO executable reference for most tasks; tests LLM-generated and validated by LLM committee + human. "two senior researchers manually author 97 requirement documents ... Test suites are then generated using Gemini 3 Pro with iterative human supervision" (§3.1); "refined through a 'review-rebuttal' quality assurance process with multi-model evaluation and human oversight" (§3.3); IAA Krippendorff α=0.69 after rubric refinement (initial 0.032). Only 6 of 30 Verified repos are real GitHub repos.
  - RepoMod-Bench: tests NOT generated; converted from the source repo's existing suites, then validated on the source: "We standardize the source tests into an implementation-agnostic format (e.g., pytest)" (Stage 2); "The derived test suite is run against the original source implementation; it must achieve a 100% pass rate" (Stage 4).
  - CLI-Tool-Bench: generated (LLM-directed fuzzing over extracted command schema, GPT-5.4) AND validated on reference: "Each generated test command is directly executed against the human-written oracle ... the validity of these test cases is determined by the oracle itself" (§III-B).
  - ProjDevBench: tests NOT generated; existing OJ test data from a "large-scale Online Judge" platform (2,800 candidate problems, §3.2); no reference-validation step described beyond the OJ.
  - ProgramBench: generated by agent (mini-SWE-agent + Claude Sonnet 4.5) AND validated on gold binary: "any remaining tests that do not pass with the gold binary deterministically or pass a dummy binary are discarded" (§2.2). Also harvests existing repo tests.
  - RepoZero: generated by LLM AND validated on source: "we first employ an LLM to generate test files ... filtered to retain only successful test cases as ground truth" (§1); "Each test case is executed 20 times ... discarded if ... runtime exceptions, or non-deterministic outputs" (§3.4). Generator model not named.
  - (SWE Refactor Bench, not in this list, also qualifies: fixed suite "built from State A: the same calls are run against the original repository and the recorded output becomes the expected answer"; verifier tests "must first go green against the reference".)
- Correct statement: "...public APIs in RepoZero. Where an executable reference exists (CLI-Tool-Bench, ProgramBench, RepoZero, SWE Refactor Bench), its behaviour becomes the oracle, and tests can be generated at scale without human labelling because each generated test is validated on the reference. RepoGenesis instead validates LLM-generated tests by LLM review plus a human area chair, and RepoMod-Bench and ProjDevBench reuse existing human-written suites."
- Models: RepoGenesis GPT-5.1/Claude Sonnet 4.5/Qwen3-30B (2025); RepoMod-Bench Claude Opus 4.5, GPT-5.2 (late 2025); CLI-Tool-Bench GPT-5.4, Claude Sonnet 4.6, DeepSeek-V3.2, Qwen-3.5-plus, GLM-5, MiniMax-M2.5, Kimi-k2.5 (late 2025-early 2026); ProjDevBench GPT-5, Claude Sonnet 4.5, Gemini 3 Pro, GLM-4.6, Kimi-k2, DeepSeek-V3.2-Exp (2025); ProgramBench Claude Opus 4.7/4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro, Gemini 3 Flash, GPT 5.4, GPT 5.4 mini, GPT 5 mini (2025-26); RepoZero Kimi-K2.5/K2.6, GLM-5/5.1, DeepSeek V3.1/V3.2/V4, Ernie-5.0, MiniMax-M2.5/M2.7, Claude-4.6-Sonnet (2025-26).
- Measurement: trend claim rests on 6 benchmarks, all 2026 preprints except RepoZero (NeurIPS 2026 D&B). Note E2EDev (BDD, interface-level) is Oct 2025, i.e. the boundary-testing idea predates 2026.
- Status: RepoZero NeurIPS 2026 (D&B); RepoGenesis, RepoMod-Bench, CLI-Tool-Bench, ProjDevBench, ProgramBench preprints.

### C24 — CLIToolBench2026
- Draft: "Strict output equality penalises correct output with different formatting. CLI-Tool-Bench adds fuzzy and LLM-judged semantic tiers to compensate, and so reintroduces an LLM."
- Verdict: VERIFIED
- Evidence: "Because functionally correct CLI tools may inherently present their outputs in diverse formats or stylistic layouts, strict string matching is often insufficient ... Fuzzy Match (FM) computes a normalized Levenshtein edit distance ... Semantic Match (SM) employs an LLM as a judge (GPT-5.4)" (§III-C); averages EM 23.50%, FM 39.00%, SM 29.64% (§IV results).
- Models: judge GPT-5.4 (2026), which is also an evaluated model and the test generator/schema extractor ("we strictly utilize GPT-5.4").
- Measurement: 94 tasks, 7 models, 2 agent frameworks (incl. OpenHands); SM is stricter than FM on average, so the semantic tier is not simply a leniency tier.
- Status: preprint.

### C39a — CLIToolBench2026
- Draft: "Vibe Code Bench, WebGen-Bench, CLI-Tool-Bench, AppEvalPilot, and E2EDevBench report human alignment"
- Verdict: VERIFIED (for CLI-Tool-Bench)
- Evidence: "a large-scale human annotation study on 1,000 output pairs yielded a Cohen's Kappa coefficient of κ>0.9, confirming strong alignment with expert judgment. Two annotators with at least 4-year software engineering experience" (§III-C).
- Models: judge GPT-5.4.
- Measurement: κ reported only as ">0.9"; judge is same family as one evaluated model (GPT-5.4); no self-preference analysis reported.
- Status: preprint.

### C25 — ProgramBench2026
- Draft: "Coverage is limited to behaviour that the test generator thought to probe. ProgramBench's tests are generated by a single model family."
- Verdict: VERIFIED (actually a single model)
- Evidence: "All construction steps use the mini-SWE-agent harness with Claude Sonnet 4.5" (§2.2); "Generate behavioral tests. We use an agent to explore the program, its source code, existing tests, and documentation" (§2.2).
- Correct statement: n/a; could sharpen to "by a single model (Claude Sonnet 4.5), from the same family as the top-ranked evaluated models (Claude Opus 4.7/4.6)". Paper mitigates coverage concern: generated suites reach line coverage "comparable to developer-written test suites" (avg 56.8% for developer suites, §5.1) and existing tests are harvested.
- Models: generator Claude Sonnet 4.5 (2025).
- Measurement: median 770 tests/task; tests failing gold or passing a dummy binary discarded (dummy pass 3.7%).
- Status: preprint.

### C26 — SWERefactorBench2026
- Draft: "In SWE Refactor Bench, 30 runs pass every fixed behavioural check without migrating anything. Of 88 runs that pass the fixed suite, agentic verifiers break 60."
- Verdict: CORRECTED (numbers right; "without migrating anything" overstates; 88 are runs passing BOTH the audit and the fixed suite)
- Evidence: "30 runs preserved behaviour by skipping the migration, and were stopped at Migration Audit" (§1); "Of the 520 scored runs, 340 (65.4%) passed Stage I and 118 (22.7%) passed every fixed check, but only 88 did both" (§3.2); "among the 88 submissions that satisfy both under the fixed suite, agentic verifiers break 60" (§1). But blindness includes e.g. lang01 runs that wrote Rust and "cleared seven of the eight criteria and failed only the one asking whether the Rust is the implementation: ... a transliteration" (§3.2). Stage I is an LLM judge (gpt-5.6-sol, majority of 3; human agreement 89.7%, κ=0.795, judge errs strict in 14/16 disagreements).
- Correct statement: "30 runs pass every fixed behavioural check yet fail the migration audit (the old stack was retained or only transliterated). Of the 88 runs that pass both the audit and the full fixed suite, agentic verifiers break 60."
- Models: claude-opus-5, claude-sonnet-5, gpt-5.6-luna, gpt-5.6-sol, kimi-k3, qwen3.8-max, dsv4-flash, glm-5.2 (2026); 26 model-effort configs.
- Measurement: 20 tasks x 26 configs = 520 runs, one run per task per config; verifier outcome depends strongly on verifier model ("retire the two strongest and the remaining four would accept 46 submissions instead of 28"); verifiers include claude-opus-5 (same family as evaluated).
- Status: preprint.

### C44 — ProgramBench2026
- Draft: "ProgramBench: no model resolves any task; the best reaches ≥95% of tests on 3% of tasks."
- Verdict: VERIFIED
- Evidence: "none fully resolve any task, with the best model passing 95% of tests on only 3% of tasks" (abstract); Table 2: Claude Opus 4.7 0.0% resolved, 3.0% at ≥95%.
- Models: Claude Opus 4.7 (best), Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro, Gemini 3 Flash, GPT 5.4, GPT 5.4 mini, GPT 5 mini (2025-26).
- Measurement: 200 tasks, one run per model-task apparently; 3% of 200 ≈ 6 tasks; tests generated by Claude Sonnet 4.5 (same family as best model).
- Status: preprint.

### C47 — RepoGenesis2026
- Draft: "RepoGenesis: API coverage of about 73% alongside deployment below 13% for MetaGPT."
- Verdict: CORRECTED
- Evidence: Table 5: MetaGPT + Claude, Python: DSR 13.00%, AC 73.04%; Java: DSR 54.00%, AC 74.14%. MetaGPT + GPT-5.1 Python: DSR 4.55%, AC 70.43%; Java DSR 62.50%. Text: "Claude-powered MetaGPT reaching 73.04% (Python) and 74.14% (Java) matching commercial IDEs, their lower DSR reveals a critical AC-DSR gap" (§5.1).
- Correct statement: "API coverage of about 73% alongside a deployment success rate of 13% for Claude-backed MetaGPT on Python (on Java its deployment rate is 54%)." DSR is 13.00%, not below 13%, and the gap holds for Python only.
- Models: Claude Sonnet 4.5 (2025) in MetaGPT.
- Measurement: averaged over 5 runs; Python Verified subset small (Table 7: 264 Python deployments total across systems); AC = endpoints implemented.
- Status: preprint.

### C57 — E2EDev2025
- Draft: "E2EDev avoids this by assigning test identifiers to user-interface elements in advance and passing them to the model."
- Verdict: VERIFIED
- Evidence: "Before generating requirements and test cases, we use GPT-4o to assign unique test IDs to key UI components" (§3.2); "the LLM uses this annotated source as context to generate requirements and test scripts that directly reference these test IDs. For example: Requirement: When the user clicks the button with test-id="login-btn"" (App. A.2). Requirements (the model input) contain the IDs.
- Models: test-ID annotation by GPT-4o (2024).
- Measurement: 46 projects; humans verified annotations.
- Status: preprint (2025).

### C67 — ProgramBench2026, CLIToolBench2026
- Draft: "single-file, long-function designs in ProgramBench and one- to three-file layouts in CLI-Tool-Bench"
- Verdict: VERIFIED (minor nuance for ProgramBench)
- Evidence: ProgramBench "Models favor monolithic, single-file implementations" (abstract); "Models also create far fewer files (median 3 versus 15), with 60% of solutions consisting of 1–3 code files"; "Models write fewer, longer functions ... Claude Sonnet 4.6 ... 1.46× longer ... Gemini 3.1 Pro reaches 1.62×. GPT 5.4 ... 1.08×" (§5.2). CLI-Tool-Bench "medians tightly clustered between 1 and 3 files" (Fig. 5 discussion).
- Correct statement: optional precision: ProgramBench median is 3 files (vs 15 in reference), so "monolithic, few-file" is more exact than "single-file".
- Models: as in C44 and C24.
- Measurement: ProgramBench structural stats over all runs, function stats for 4 models; CLI-Tool-Bench file counts vs human oracle, but Easy oracle repos themselves average 1.62 files.
- Status: preprint.

# G4 fact-check (rq3_evaluation.tex)

### C12 — VibeCodeBench2026, WebGenBench2025, RealDevWorld2025, WebCraftBench2026, PaperBench2025, SaaSBench2026
- Draft: "Agentic/LLM judges & Vibe Code Bench, WebGen-Bench, RealDevWorld, WebCraftBench, PaperBench, SaaSBench (partly)" (Table row, l.39)
- Verdict: VERIFIED
- Evidence: VCB "We use Claude Sonnet 4.5 as the canonical evaluator" (§3.3, Browser Use agent); WebGen-Bench "we utilize WebVoyager ... we employ Qwen2.5-VL-32B-Instruct ... as the agent's engine" (§3.2); RealDevWorld "AppEvalPilot, a new agent-as-a-judge evaluation system"; WebCraftBench "LLM and agentic judges assess visual aesthetics, usability, and requirement alignment"; PaperBench "we use OpenAI's o3-mini ... as the judge" (SimpleJudge, §4); SaaSBench "llm-as-judge is used only when deterministic assertions cannot adequately characterize the target" (§3.3; judge Claude Sonnet 4.5).
- Models: judges: Claude Sonnet 4.5 (2025), Qwen2.5-VL-32B (2025) + GPT-4o for appearance (2024), Claude-3.5-Sonnet-v2 backbone for AppEvalPilot (2024), Claude-Opus-4.8 (2026), o3-mini (2025), Claude Sonnet 4.5 (2025).
- Measurement: SaaSBench "partly" is correct: most DAG nodes are binary/weighted HTTP/rule checks; LLM judge only for some nodes (e.g. layout reasonableness).
- Status: all preprint (per corpus.csv).

### C28 — VibeCodeBench2026
- Draft: "agreement with humans is 86.4% for Claude Sonnet 4.5 as evaluator but 36.1% for GPT-5.2."
- Verdict: VERIFIED
- Evidence: "The final-column pooled means are 86.4% (Claude Sonnet 4.5), 86.3% (Claude Sonnet 4.6), 84.7% (Gemini 3.1 Pro), and 36.1% (GPT-5.2)." (§6.2, Table 10)
- Models: evaluators Gemini 3.1 Pro, GPT-5.2, Claude Sonnet 4.6, Claude Sonnet 4.5 (2025–2026).
- Measurement: substep-level pass/fail agreement, mean over 3 human reviewers; 6 tasks x 3 generator models = 18 apps, 1,401 substeps; ONE evaluation run per app per evaluator; human-human 88.6–93.6%. Note apps were generated by Gemini 3.1 Pro, GPT-5.2, Claude Sonnet 4.6 (Claude judges grade Claude-built apps). Small sample (6 tasks).
- Status: preprint

### C29 — WebCraftBench2026
- Draft: "preserves the ranking when its judge is swapped (rho=0.98), but raw scores shift substantially."
- Verdict: VERIFIED
- Evidence: "Pearson correlation of r= 0.983 and a Spearman rank correlation of ρ= 0.980 across judges. Of the 136 model pairs, 130 retain their relative order ... Although raw-score levels and spreads change substantially, aggregate rankings remain stable. ... mean usability score increases from 60.1 to 75.7" (§5.4, App. B)
- Models: main judge Claude-Opus-4.8 swapped for Gemini-3.7-Flash (2026); 17 generator models incl. Claude-Opus-5/4.8/4.7.
- Measurement: single swap (one alternative judge); exploration traces held fixed (only scoring swapped); correlation on standardized (z-scored within pool) scores, so ranking stability is partly by construction of standardization; final judge sampled 5x with trimmed mean. Main judge Claude-Opus-4.8 grades Claude-family generators (Claude-Opus-5 ranked #1) — same-family case not mentioned in the draft's bias paragraph.
- Status: preprint

### C30 — HiRAS2026
- Draft: "the reference-free judge from Paper2Code scores an empty repository 3.89 out of 5 and a config-only repository 4.67."
- Verdict: VERIFIED
- Evidence: "the empty repository attains a score of 3.89 under the reference-free metric ... configuration-only repositories containing no executable code can score 4.67, outperforming all model-generated codebases" (§5.2, Table 3)
- Models: evaluator o3-mini-high (2025); compared generators Qwen3-Coder-480B, DeepSeek-v3.1-Terminus.
- Measurement: Paper2Code benchmark reference-free prompt; config-only = .md/.yaml files extracted from the gold author repo (so they contain real documentation of the method, which partly explains the high score). Authors attribute to evaluator hallucination. Ref-based scores for same: 1.57 / 1.62.
- Status: preprint

### C32 — PaperCompiler2026
- Draft: same family generates and judges, "o3-mini and o3-mini-high in PaperCompiler"
- Verdict: VERIFIED
- Evidence: "all systems receive the same MinerU-parsed Markdown inputs and use o3-mini for generation and o3-mini-high for evaluation" (§4)
- Models: o3-mini / o3-mini-high (2025).
- Measurement: inherited from Paper2CodeBench protocol (90 papers); multiple judge samples aggregated; authors do not discuss family bias. All compared systems share the same backbone, so bias affects absolute levels more than between-system comparison.
- Status: preprint

### C33 — TDDev2025
- Draft: "Claude in TDDev" (generates and judges)
- Verdict: VERIFIED
- Evidence: "We employ Claude-4-Sonnet as the agent's engine" (§4.6.2, BrowserUse evaluation agent); visual metrics "assessed by Claude-4-Sonnet" (§4.6.3); generators "GPT-4.1 and Claude-4-Sonnet" (§4.6)
- Models: Claude-4-Sonnet, GPT-4.1 (2025).
- Measurement: WebGen-Bench subset; BrowserUse YES/NO/PARTIAL. Only one of two generator backbones is Claude; also TDDev's in-loop tester is Browser-Use, same tool as the evaluator. Human alignment reported: 82.8% on 28 test cases / 5 apps (Claude only).
- Status: preprint

### C34 — SaaSBench2026
- Draft: "Claude in ... SaaSBench" (generates and judges)
- Verdict: VERIFIED
- Evidence: "For llm-as-judge nodes, we use Claude Sonnet 4.5 as the rubric judge and set temperature = 0" (§4); generators include Claude Opus 4.7, run under Claude Code.
- Models: judge Claude Sonnet 4.5 (2025); generators GPT-5.4, Gemini 3.1 Pro, Claude Opus 4.7, Kimi K2.6, Qwen 3.6 Plus, DeepSeek V4 Pro, GLM 5.1, MiniMax M2.7 (2026).
- Measurement: judge applies only to llm-as-judge nodes (minority); so same-family exposure limited to that portion of the score. Top model is Claude Opus 4.7 (20.68%).
- Status: preprint

### C35 — BUILDANDFIND2026
- Draft: "measures a positive same-family affinity between builder and finder."
- Verdict: VERIFIED (weak evidence; see measurement)
- Evidence: "same-family residuals are positive for OpenAI/Codex (+0.076), Claude (+0.041), and MiMo (+0.027), while most cross-family cells are near zero or negative" (§4.7, Table 15)
- Models: 12 agents incl. GPT-5.5, GPT-5.4-mini, Opus 4.7, Sonnet 4.6, MiMo 2.5 (Pro) (2026).
- Measurement: residual = pair score − builder mean − finder mean + grand mean; 2 tasks x 12 builders x 2 trials; no significance test; authors call it "panel-local and diagnostic"; recovery accuracy "near saturation". Finder is an agent answering intent questions about the repo, not a quality judge — analogy to judge self-preference is indirect. Also MiMo builder -> Claude finder = +0.036 (cross-family positive).
- Status: preprint

### C36 — WebGenR12026
- Draft: "use the same VLM or GUI-agent signal as both reward and evaluation metric."
- Verdict: VERIFIED (VLM part)
- Evidence: "we standardize all multimodal components, including the GUI-agent engine and VLM, on GPT-4o-11-20 during both training and evaluation." (§4.1); reward s_vis = VLM aesthetic score; metric AAS = "average score assigned by the VLM".
- Correct statement (nuance): the shared signal is the VLM aesthetic score (reward s_vis = metric AAS). The functional reward is a console/runtime-error check, not the GUI agent; the GUI agent (WebVoyager) is only used in evaluation (FSR).
- Models: GPT-4o (2024) as judge; policy Qwen2.5-Coder-7B-Instruct.
- Measurement: WebGen-Bench 101 tasks; AAS reward-hacking risk acknowledged only as weighting concern.
- Status: preprint

### C37 — WebGenAgent2025
- Draft: "use the same VLM or GUI-agent signal as both reward and evaluation metric."
- Verdict: VERIFIED (GUI-agent part, with nuance)
- Evidence: "the reward for each step is computed by summing the screenshot score and the GUI-agent score" (Fig. 2); "We use Qwen2.5-VL-32B-Instruct as the feedback VLM for screenshot and GUI-agent testing in all the experiments"; eval: "we use Qwen2.5-VL-32B-Instruct in functional testing and GPT-4o in appearance evaluation" (§4)
- Correct statement (nuance): same VLM (Qwen2.5-VL-32B) drives the GUI-agent reward and the WebGen-Bench functional evaluation; appearance is evaluated with GPT-4o, differing from the reward VLM. Training-time GUI tests are self-generated, evaluation uses WebGen-Bench's 647 human test cases.
- Models: Qwen2.5-VL-32B (2025), GPT-4o (2024); policies Qwen2.5-Coder-7B, Qwen3-8B.
- Status: preprint

### C39 — VibeCodeBench2026, WebGenBench2025, RealDevWorld2025
- Draft: "Vibe Code Bench, WebGen-Bench, ... AppEvalPilot ... report human alignment"
- Verdict: VERIFIED
- Evidence: VCB Table 10 (above); WebGen-Bench "Alignment Rate ... 90.3 / 86.1 / 94.4" for Claude-3.5-Sonnet / DeepSeek-R1 / DeepSeek-V3 on Bolt.diy (Table 5, §4.3); AppEvalPilot "accuracy of 0.92 in test case classification and a quality alignment correlation of 0.81 with human evaluators" (feature-level 0.85) (§6.1, Table 2).
- Models: VCB see C28; WebGen-Bench judge Qwen2.5-VL-32B; AppEvalPilot Claude backbone (3.5/3.7 Sonnet).
- Measurement: WebGen-Bench: 3 generator result sets, 3 human annotators + adjudicator; AppEvalPilot: 49 tasks (25%), 3 QA specialists. Note: abstract says "correlation of 0.85" (feature-level) while text says 0.81 (test-case level) — cite which. List omits TDDev2025 (82.8%, n=28) and WebCraftBench (85.3% pairwise human-preference agreement, 197 sessions), which also report human alignment.
- Status: all preprint

### C40 — PaperBench2025
- Draft: "PaperBench validates its judge on JudgeEval with F1 0.83"
- Verdict: VERIFIED
- Evidence: "o3-mini with the SimpleJudge scaffolding is the most cost-effective, with an F1 score of 0.83 at $66 USD per paper" (§4.2, Table 3)
- Models: o3-mini (high reasoning) judge (2025); o1 F1 0.84.
- Measurement: JudgeEval = partial replications of only 5 papers (4 PaperBench + 1 dev), human-graded leaf nodes, macro-F1 across papers. o3-mini judge also grades o3-mini/o1 submissions (same family; not discussed in draft).
- Status: preprint per corpus.csv (note: PaperBench appeared at ICML 2025 — check corpus venue).

### C58 — VibeCodeBench2026, WebGenBench2025, TDDev2025, TDDev2026
- Draft: "Browser-agent oracles in Vibe Code Bench, WebGen-Bench, and TDDev (TDDev2025, TDDev2026) avoid selectors altogether, at the cost of LLM variance."
- Verdict: MISLEADING
- Evidence: VCB: "it avoids brittle DOM-coupled checks (e.g., fixed selectors)" (§3.1). TDDev2026: "Selector generation errors account for three cases: where the agent generates a Playwright selector that does not match any element and times out" (§5.1.2); Qwen3.5 tester "issues an invalid selector and nevertheless returns Fail" (§5.2).
- Correct statement: These oracles avoid pre-authored/fixed selectors, but agents still locate elements via DOM/accessibility-tree selectors generated on the fly; in TDDev2026, 3 of 5 tester false positives were agent-generated selector errors. Rephrase: "avoid hand-written selectors, trading selector brittleness for LLM variance (including agent-generated selector errors)".
- Models: Browser Use w/ Claude Sonnet 4.5 (VCB), WebVoyager w/ Qwen2.5-VL-32B (WebGen-Bench), BrowserUse w/ Claude-4-Sonnet (TDDev2025), Claude Sonnet 4.6 oracle (TDDev2026).
- Measurement: TDDev2026 tester accuracy 87.5% on 40 fixture evaluations (100% on broken, 75% on correct apps).
- Status: VCB, WebGen-Bench, TDDev2025 preprint; TDDev2026 ASE 2026.

# G5 fact-check (rq3_evaluation.tex)

### C13 — EvoDev2025, PrompttoProduct2025, appbuild2025, CBAUserStudy2025
- Draft: "Human judgement ... expensive; small n; perceptual rather than functional" (Table, LLM in loop: no)
- Verdict: MISLEADING
- Evidence: EvoDev: "the acceptance checklist ... each requirement rated on a 4-point scale: '1' indicates the function is absent ... '4' ... fully implemented and correct"; "approximately 500 person-hours ... 1,500 US dollars" (Sec 4.3). app.build: "six standardized functional checks executed by human assessors" incl. "AB-03 (Create Functionality)", "AB-04 (View/Edit Operations)" (Sec 4.4, Table 6). Prompt-to-Product: "205 participants and 1,071 quality-filtered pairwise comparisons, assessing task-based ease of use, visual appeal, perceived completeness, and user trust" (Abstract). CBA: "user study (n=16)"; "Participants attempted to run the code and rated" satisfaction (Sec III).
- Correct statement: "Expensive" holds (EvoDev 500 person-hours). "Small n" holds for EvoDev (4 evaluators, 15 apps), app.build (30 apps) and CBA (16 users) but not Prompt-to-Product (205 raters, 1,071 comparisons, 288 apps). "Perceptual rather than functional" fits Prompt-to-Product and CBA (satisfaction), but EvoDev and app.build use humans to execute per-requirement functional acceptance checklists; that is human-executed functional testing. app.build also has automated gates (boot healthcheck, Playwright), so it is a mixed oracle and not purely human.
- Models: EvoDev: GPT-4.1, Claude-3.5-Sonnet, Claude-4-Sonnet, Qwen3-Coder-480B (2024–25); app.build: Claude Sonnet 4, Qwen3-Coder-480B, GPT-OSS-120B (2025); Prompt-to-Product: commercial platforms Replit/Bolt/Firebase Studio (2025, underlying models unspecified); CBA: GPT-Engineer with gpt-3.5-turbo (2023) vs GitHub Copilot.
- Measurement: EvoDev: 4 student evaluators (2 with industry experience), blinded, Likert scores averaged. app.build: human AB-01..06 rubric on 30 prompts, single run. P2P: crowd raters (CINT) using Likert and pairwise ratings, LMM/Bradley-Terry. CBA: 16 participants, 1–5 satisfaction.
- Status: EvoDev preprint; Prompt-to-Product ACM IUI Workshops 2026; app.build SANER 2026; CBA preprint.

### C14 — Vero2026, SPDDWL2026
- Draft: "Formal verification ... none (spec-bound) ... specifications may be wrong or LLM-written ... LLM in loop: no"
- Verdict: MISLEADING (the "LLM in loop: no" cell is wrong for both papers)
- Evidence: Vero: "a rule-based detector and an LLM judge screen agent-introduced declarations for mechanisms that can trivialize proofs" (Sec 3.2); "Each stage runs as an LLM agent and is reviewed by a human curator" (Sec 3.3, curation); "cannot ensure that specifications are semantically correct or complete, so all specifications are manually reviewed" (Limitations). SPDDWL: "for pure modules, the agent generates formal specifications, implementations ... and machine-checked proofs"; "passes all 265 LLM-generated tests" (Abstract).
- Correct statement: "Specifications may be wrong or LLM-written" is supported. Vero's specs are LLM-translated and then human-reviewed. In SPDDWL the agent under test writes its own specs, so the spec is not an independent oracle, and the external check is 265 LLM-generated tests plus AFL++ fuzzing. The LLM-in-loop cell should be "yes": Vero uses an LLM judge in grading and LLM agents in spec curation, and SPDDWL uses LLM-written specs and tests. SPDDWL is a single case study (one project, one model).
- Models: Vero: GPT-5.5 (mid/xhigh) via Codex, Claude Opus 4.8 and Sonnet 5 via Claude Code (2026); SPDDWL: Claude Opus 4.7 (2026).
- Measurement: Vero: 43 Lean 4 instances, Lean kernel checking plus axiom allowlist plus LLM-judge anti-cheat, two modes (code-and-proof, proof-only). SPDDWL: 1 RV32I interpreter, 30-min run, Rocq checking plus 265 LLM tests plus 12 h fuzzing.
- Status: both preprint.

### C48 — AppForge2025
- Draft: "more than half of the functionally correct apps crash at runtime."
- Verdict: VERIFIED (as the paper's own claim; see caveat)
- Evidence: "over 50% of functionally correct apps crashes during runtime" (Sec 5, results); intro: "among these correct apps, half still encounter at least one crash".
- Correct statement: n/a. Caveat: the tabulated Crash metric is "the percentage of compiled applications that crash" (App. B.3, Eq. 3), so its denominator is compiled apps, not correct apps. The "correct apps" figure is not tabulated, and it rests on very few apps (best success 14.85%, about 15 of 101). The intro says "half", while Sec 5 says "over 50%".
- Models: 12 LLMs incl. GPT-5-High, GPT-4.1, Claude-4-Opus/Sonnet, Gemini-2.5-Pro, DeepSeek-R1/V3, GLM-4.5, Kimi K2, Qwen3-Coder (2025); agents mini-SWE-agent and Claude Code.
- Measurement: 101 F-Droid tasks; emulator UI tests plus lightweight fuzzer; temperature 0.2, apparently a single run.
- Status: preprint.

### C52 — AppForge2025
- Draft: "GPT-4.1 'fixes' compile errors by deleting the implementation in 91% of tasks (8.0 files -> 2.7)."
- Verdict: VERIFIED
- Evidence: "GPT-4.1 evades development in 91.09% of tasks, while Kimi K2 does so in 65.36%" (Intro); "reduction in generated number of files (from 8.00 to 2.68) and LOCs (from 367.43 to 58.41) when provided with compilation feedback" (Sec 5 / Table 1).
- Correct statement: n/a. Note: the paper does not explain how 91.09% is computed (no detection criterion is given). It also says the model deletes "error-inducing functions" (empty bodies), not necessarily the whole implementation. Compile rate rose from 6.93% to 74.26%. Kimi K2 (65.36%) also does this.
- Models: GPT-4.1 (2025), Kimi K2 (2025).
- Measurement: compile-error-feedback refinement setting on 101 tasks; file and LOC means from Table 1.
- Status: preprint.

### C49 — appbuild2025
- Draft: "some 'bootable' apps are placeholder pages."
- Verdict: VERIFIED
- Evidence: "many apps that pass healthcheck validation are non-functional 'Under Construction' templates with zero functionality. For GPT-OSS-120B, 43.3% passed AB-01 (Boot), but only 30.0% passed both" (Sec 5.6).
- Correct statement: n/a (the example is mainly GPT-OSS-120B; Qwen3 had fewer).
- Models: Claude Sonnet 4, Qwen3-Coder-480B, GPT-OSS-120B (2025).
- Measurement: automated healthcheck vs. AB-02 prompt-correspondence (template detection); n=90 runs for open models.
- Status: SANER 2026.

### C56 — appbuild2025
- Draft: "removing Playwright end-to-end tests raised app viability by 16.7 percentage points. Brittle selectors, race conditions, and structurally different but correct user interfaces caused false rejections."
- Verdict: VERIFIED (with caveats on validity)
- Evidence: "viability increased to 90.0% (+16.7 pp) with quality improving to Q = 8.62 (+0.56)"; "three root causes of brittleness: (1) Over-specified selectors ... (2) Race conditions ... (3) False negatives from implementation variance: ... structurally different UIs" (Sec 5.7).
- Correct statement: n/a. Suggest qualifying with "on 30 prompts". 73.3% to 90.0% is 22/30 to 27/30, a 5-app difference from a single run with no significance test. The paper's own automated metric moves the other way: "Playwright removal has minimal impact on automated success (-3.3%)" (Table 3: 86.7% to 83.3%). Root causes come from authors' manual inspection.
- Models: Claude Sonnet 4 (2025).
- Measurement: human viability (AB-01 and AB-02 not FAIL) on the same 30-prompt cohort per ablation; 1 run each.
- Status: SANER 2026.

### C50 — ChatDev2024
- Draft: "reports an 'executability' of 0.88, meaning that the software runs without crashing, and a 'consistency' score based on embedding similarity. Its artefacts average 4.4 files and 144 lines."
- Verdict: VERIFIED
- Evidence: Table 1 "ChatDev 0.5600 0.8800 0.8021 0.3953"; "Executability ... percentage of software that compiles successfully and can run directly"; "Consistency ... cosine distance between the semantic embeddings of the textual requirements and the generated software code"; Table 3 "ChatDev 148.2148 22,949.4450 4.3900 144.3450" (#Files, #Lines).
- Correct statement: n/a. Minor points: executability is "compiles and can run directly", which is close to "runs without crashing". 4.39 files rounds to 4.4. ChatDev also reports completeness (no placeholder code) and GPT-4/human pairwise win rates.
- Models: ChatGPT-3.5 (gpt-3.5-turbo, 2022–23), temperature 0.2.
- Measurement: SRDD 1,200 prompts; automatic metrics, averaged; no functional tests.
- Status: ACL 2024.

### C51 — Tymcrat2024
- Draft: "whole-program C-to-Rust translations do not compile at all, so no test can run; correctness is assessed on a manual sample of 41 functions."
- Verdict: VERIFIED
- Evidence: "each translated program does not compile due to type errors and thus cannot be executed ... we conducted case studies to manually investigate the correctness of the translation, involving 41 functions" (Sec 4, RQ on correctness).
- Correct statement: n/a. Detail: there was 1 random type-error-free function per program. Correct: 23/41 (56.1%) for GPT-3.5 Turbo and 32/41 (78.0%) for GPT-4o mini, by the authors' conservative criteria. A second researcher counted 30 and 35, showing low inter-rater agreement.
- Models: gpt-3.5-turbo-0125 (2024), gpt-4o-mini-2024-07-18 (2024).
- Measurement: primary metric is type-error reduction; correctness is a manual audit with 2 assessors who disagreed.
- Status: EMSE 2025.

### C54 — Vero2026
- Draft: "in 5 agent--instance pairs, the agent replaced the reference algorithm with one that is easier to prove." (listed under "Evasion and reward hacking")
- Verdict: MISLEADING
- Evidence: "found five instance-agent pairs across three repositories where the agent replaces a hard-to-verify reference algorithm with a simpler implementation of its own that satisfies the same specifications ... Each substitution is behaviorally correct rather than a shortcut, so what the agent gains is provability and what it gives up is efficiency" (Sec 4); App. G: "at least five instance–agent pairs".
- Correct statement: The number is right ("at least five"), but Vero explicitly says this is not evasion. The substitutions satisfy all specs and are behaviourally correct. They trade efficiency for provability, which code-and-proof mode allows. Better framing: "the specification does not constrain efficiency, so agents legitimately substitute simpler algorithms (e.g., Hungarian algorithm in munkres)." Do not list it as reward hacking.
- Models: GPT-5.5 (xhigh, mid), Claude Opus 4.8 (2026).
- Measurement: manual audit of code-and-proof full solves whose proof-only counterpart failed; 250 vs 201 specs closed.
- Status: preprint.

### C55 — ChessEnginesPL2026
- Draft: "11 of 15 agent-written self-assessment scripts overestimate the engine's Elo by 200--1,100 points."
- Verdict: VERIFIED
- Evidence: "15 of the 34 engines ship a custom Elo-estimation script of their own design, but only four come close to the truth ... The other eleven of the 15 overestimate by 200 Elo to 1100 Elo" (Sec 6.1); max "∆ = −1078" (chess-assembly-codex).
- Correct statement: n/a. Framing note: the paper presents this as a biased self-benchmarking setup that agents "optimise against". It only mentions deliberate overestimation as a "risk". Calling it reward hacking goes slightly beyond the evidence. The bibkey is uncited in this section and needs \cite{ChessEnginesPL2026}.
- Models: Claude Code (Opus 4.6, 4.7) and Codex (gpt-5-codex, gpt-5.3-codex, gpt-5.4) (2025–26).
- Measurement: 34 sessions/engines; external re-evaluation gauntlet (Stockfish levels, Rustic, Asymptote) plus Bradley-Terry; one session per engine.
- Status: preprint.

### C61 — (uncited; should be CursorDesignIssues2026)
- Draft: "Cursor-built projects that are 91% functionally complete carry 1,305 CodeScene and 3,193 SonarQube issues."
- Verdict: MISLEADING
- Evidence: "manual evaluation of the 10 projects ... yields an average functional correctness of 91%, with the highest at 96% and the lowest at 85%"; "We identified 1,305 design issues by CodeScene and 3,193 by SonarQube"; "removed 1,612 false positives from the issues identified by SonarQube" (Abstract, §3.7, §4.1)
- Correct statement: In ten projects built with Cursor Pro under the authors' human-in-the-loop FD-HITL framework (avg 16,965 LoC, 114 files), manual requirement checks give 91% average functional correctness; static analysis finds 1,305 CodeScene and 3,193 SonarQube design issues in total across all ten (after 1,612 SonarQube false positives were filtered by hand) [CursorDesignIssues2026]. Numbers are totals over ~170k LoC with no human-written baseline, so they do not show the projects are worse than comparable human code.
- Models: Cursor Pro; underlying model not reported (2025)
- Measurement: 10 projects, single generation each, human-in-the-loop; correctness = authors' manual requirement check (not tests); issues = raw tool counts, no normalisation or baseline
- Status: preprint

### C62 — OODPureAI2026
- Draft: "Test-passing LLM projects in the OOD study score better on smell metrics, but only because they oversimplify, with fewer classes and domain concepts than student projects."
- Verdict: MISLEADING
- Evidence: "PureAI projects show lower code smell density and generally appear simpler ... However, this is consistent with oversimplification, as it is associated with missing abstractions"; "PureAI generally has fewer classes" (Abstract, §5.1); "we retained only submissions that passed all tests" (§4)
- Correct statement: In one Java assignment (Kalah), test-passing projects from GPT-5.4, Gemini 2.5 Pro and Gemini 3.1 Pro have lower smell density than student projects but fewer classes and fewer represented domain concepts. The authors read this as *consistent with* oversimplification, not as a causal "only because".
- Models: gpt-5.4 (2026), gemini-2.5-pro (2025), gemini-3.1-pro-preview (2026); gpt-4o and gemini-2.0-flash for a historical check only
- Measurement: single assignment; PureAI runs that failed after 5 repair iterations discarded (survivorship, acknowledged); 93 PreAI / 57 PostAI student projects; OOD metrics, smell density, manual domain-concept count
- Status: preprint

### C63 — AgingGen2025
- Draft: "Bolt-generated services show statistically significant memory growth under 50-hour load"
- Verdict: VERIFIED (needs scope qualifier)
- Evidence: "All p-values are approximately zero, indicating a statistically significant upward trend in memory usage for all applications" (§IV, Table I)
- Correct statement: In four Bolt-generated Express services (BaxBench prompts), one 50-hour load test each showed a significant upward memory trend (Mann–Kendall); slopes are 2–38 MB/h. There was no human-written baseline.
- Models: Bolt platform; underlying LLM not reported (2025)
- Measurement: n=4 apps, one run each, Mann–Kendall and Sen's slope on memory time series; no non-LLM control, so the effect cannot be attributed to LLM generation
- Status: preprint

### C64 — ReproGap2025
- Draft: "Only 68% of 300 agent-generated projects run out of the box with their declared dependencies"
- Verdict: VERIFIED
- Evidence: "Across 300 evaluated projects, we find that only 205 (68.3%) execute successfully out-of-the-box" (Results); "Python 89.2%, Java 44.0%" (Abstract)
- Models: Claude Code (Opus 4.1, 2025), OpenAI Codex agent 0.52.0 (2025), Gemini 2.5 Pro agent (2025)
- Measurement: 100 prompts × 3 agents, one generation each; "execute" = runs in a clean environment, not functionally correct; the rate varies widely by language
- Status: preprint

### C65 — RealSecbench2026
- Draft: "In repository contexts, secure-and-correct rates stay below 8% (RealSec-bench)"
- Verdict: MISLEADING
- Evidence: "the composite SecurePass@k metric drops sharply, with no model exceeding 8%" (§5.1); abstract: "SecurePass@1 metric remaining below 6%"; with RAG: "the semantic-based dense retriever yielded the highest SecurePass@1 score of 10.48% for Claude-3.7-Sonnet" (§5.2)
- Correct statement: On 105 single-function generation tasks in Java repositories, baseline SecurePass@1 is below 8% for five 2024–25 models (GPT-4.1, Claude 3.7 Sonnet, etc.); with retrieval it reaches 10.5%. This is function-level completion, not repository generation.
- Models: GPT-4.1, GPT-4.1-mini, Claude-3.7-Sonnet, DeepSeek-V3, Qwen3-235B (2024–25)
- Measurement: 105 tasks; Pass@1 from repository unit tests; security from CodeQL plus an LLM voter/judge pipeline (F1 89.1% on 89 alerts); 4,096-token context; contextual-tier task
- Status: preprint

### C66 — SecRepoBench2025
- Draft: "below 54% even for the best agent (SecRepoBench)"
- Verdict: VERIFIED (scope qualifier needed)
- Evidence: "OpenHands paired with OpenAI o3 achieves the best performance of a 53.5% secure-pass@1 among all setups" (§4, Table 2)
- Correct statement: On 318 masked-function C/C++ completion tasks, the best agent (OpenHands + o3) reaches 53.5% secure-pass@1. This is a function completion task, not repository generation.
- Models: 29 LLMs, 15 agent setups incl. o3, GPT-5, Claude Sonnet 4.5 + Claude Code (2025)
- Measurement: k=1, developer unit tests plus PoC security tests (OSS-Fuzz), one generation
- Status: LLM4Code 2026 (workshop)

## Cross-study claims

### X1 — Oracle taxonomy table (tab:oracles), whole table
- Draft: Studies are assigned to oracle rows with "LLM in loop" and "Known weaknesses" cells.
- Assessment: Several assignments are wrong.
  - RealBench belongs under curated or LLM-assisted tests, not upstream white-box tests: its tests are human-written with GPT-4o help.
  - TraceDev's tests are LLM-generated, not adapted.
  - BeyondSWE Doc2Repo uses adapted upstream tests with human review, so it belongs in the adapted row.
  - "Adaptation is unvalidated" is false for RepoCraft (gold run and human ratings) and BeyondSWE.
  - Formal verification "LLM in loop: no" is false: Vero uses an LLM anti-cheat judge and LLM spec curation, and SPDDWL's specs and tests are written by the agent.
  - Human judgement "small n; perceptual" is false for Prompt-to-Product (205 raters) and for EvoDev and app.build, which use functional checklists.
  - "Exact I/O formats penalise valid variants" is the authors' inference; none of the four interface papers measures it.
  - cJSON porting has no citation and no full text.
- Rewording: Fix the row assignments. Change the weakness cells to "adaptation validation varies (RepoCraft: 81% ceiling on gold)". Mark the LLM-in-loop cell "yes (judge/spec)" for formal verification.

### X2 — "Similarity to a reference is not correctness. Three studies provide direct evidence"
- Assessment: Partly supported, but the strongest evidence is not cited.
  - ProjectEval is a single GPT-4o cascade-vs-direct comparison, not a ranking contradiction.
  - Codev-Bench is a completion benchmark: its correlations are 0.793, 0.529 and 0.822, but 0.991 in Scenario 2.
  - ExecRepoBench gives no correlation coefficient.
  - ProjectGen is solid: SketchBLEU around 91–92% for both methods, and CodeS around 68–70 with 0 passing tests.
  - ECAT also shows high node alignment with placeholder logic.
  - All are preprints in the corpus, although CodeS/ProjectGen have TOSEM DOIs and ProjectEval has an ACL Findings DOI, so the venue column looks stale.
  - The models are 2023–24 (GPT-3.5/4o, CodeLlama, Qwen2.5).
- Rewording: "In ProjectGen and ECAT, similarity scores remain high for outputs that fail tests or contain placeholder logic; in two code-completion benchmarks (Codev-Bench, ExecRepoBench) edit similarity tracks pass rate only loosely (Codev-Bench: r = 0.53–0.99 across scenarios). All evaluate 2023–24-era models."

### X3 — "several method papers still rest their main claims and all their ablations on similarity, notably CodeS and CodeTeam"
- Assessment: Supported for CodeS and CodeTeam. CodeTeam has an execution cross-check, but its Qwen2.5-72B numbers on its own adapted NL2Repo harness exceed Claude Sonnet 4.5 in the NL2Repo paper, so the harnesses are not comparable.
- Rewording: Keep. Add that CodeTeam's NL2Repo numbers come from a modified harness and the SFT variant (42.3% / 6.1%).

### X4 — "Upstream tests are the most common oracle for NL-to-repository and skeleton tasks. They call specific module paths, class names, and private helpers."
- Assessment: "Most common" is not computed anywhere: reference-unit-tests (32) is fewer than build-run (43) and human (34) across core studies, and there is no per-task breakdown. "Private helpers" is not supported: Commit0 removes private functions, and only ReCUBE's LLM-generated internal tests target them. Module paths and class names are supported (NL2Repo, DeNovoSWE, BeyondSWE, RAL-Bench specs include signatures or module surfaces). RAL-Bench uses constructed black-box tests, not upstream tests.
- Rewording: "Benchmarks that reuse upstream tests (Commit0, NL2Repo-Bench, DeNovoSWE, REPOCOD; BeyondSWE after LLM adaptation) must fix module paths and signatures in the specification, and NL2Repo-Bench, BeyondSWE, DeNovoSWE and RAL-Bench do so." Either compute "most common" per task type or drop it.

### X5 — "The clearest trend of 2026 is to test at the system boundary ... tests can be generated at scale without human labelling, because every generated test is validated on the reference"
- Assessment: All six listed benchmarks are from 2026, and five are preprints (RepoZero is NeurIPS D&B). E2EDev (2025) already tested at the UI boundary. "Trend" is a count of six papers with no denominator. Reference validation holds only for CLI-Tool-Bench, ProgramBench, RepoZero (and SWE Refactor Bench). RepoGenesis tests are LLM-generated (Gemini 3 Pro) and checked by an LLM committee and humans. RepoMod-Bench converts human tests. ProjDevBench reuses OJ data.
- Rewording: "Six 2026 benchmarks (five preprints) test at the system boundary ... In three of them (CLI-Tool-Bench, ProgramBench, RepoZero), tests are LLM-generated and retained only if they pass on the executable reference."

### X6 — "Three weaknesses recur" (strict equality; single-family test generation; equivalence without doing the task)
- Assessment: Each weakness rests on a single study (CLI-Tool-Bench; ProgramBench, which uses one model, Claude Sonnet 4.5; SWE Refactor Bench), so "recur" is not supported. In SWE Refactor Bench, the 30 runs failed an LLM-judged migration audit (some were transliterations, not "no migration"), and the 88 runs passed both the audit and the fixed suite. The audit judge (gpt-5.6-sol) is itself an evaluated model.
- Rewording: "Three weaknesses are documented, each so far in a single preprint: ..." In SWE Refactor Bench, "30 runs passed the fixed behavioural suite but were judged by an LLM audit not to perform the requested migration; of 88 runs passing both, agentic verifiers broke 60."

### X7 — "LLMs also frequently write the specification or the tests. Five problems are documented"
- Assessment: "Frequently" is uncounted. Problem by problem:
  - (1) Evaluator choice: supported by VCB and WebCraftBench, both 2026 preprints with small human-alignment samples (VCB: 6 tasks, 18 apps, 1 run).
  - (2) "Judges hallucinate": the HiRAS evidence is correct. RepoCraft's 81% on gold, however, is an evaluator false-negative ceiling and should not be listed as hallucination.
  - (3) Same-family bias: the listed cases are verified, but the list leaves out VCB (Claude Sonnet 4.5 judge), WebCraftBench (Claude-Opus-4.8 judge, Claude-Opus-5 ranked first), TDDev2026, PaperBench (o3-mini judge grades o-series), E2EDevBench (Gemini-2.5-Pro judge on Gemini agents), CLI-Tool-Bench (GPT-5.4 generates tests, judges and is evaluated) and ProgramBench (Claude-generated tests, Claude ranks top). BUILD-AND-FIND's affinity covers 2 tasks with no significance test ("panel-local diagnostic").
  - (4) Leakage: WebGen-R1 shares only the VLM signal (GPT-4o), and WebGen-Agent shares only the Qwen2.5-VL GUI-agent signal.
  - (5) Cost: no full text.
- Rewording for (3): "In at least nine benchmarks a model family both generates (or is evaluated) and judges; only BUILD-AND-FIND measures the effect, on two tasks." Drop or source (5).

### X8 — "Good practice exists ... report human alignment"
- Assessment: Supported, but the list leaves out TDDev2025 (82.8%, n=28) and WebCraftBench (85.3%). All alignment samples are small (5–49 items), and alignment does not transfer across judge models (VCB: 36.1% vs 86.4%).
- Rewording: Add "on small samples (5–49 items)".

### X9 — "Mean test pass rate ... hides that complete repositories are almost never produced"
- Assessment: The direction is supported in every cited source, but several numbers need fixing.
  - NL2Repo: Table 3 gives 40.2% and 3/104 for the best configuration. The paper's text says "five", which matches Claude-Sonnet-4 at 37.0%, so the paper is internally inconsistent.
  - BeyondSWE: 61.7%, with 0–4 repositories fully correct across configurations (2 for the best).
  - JavaBench: 2023 models on 4 student projects.
  - ProgramBench: verified.
  The models span 2023 (JavaBench, gpt-3.5) to 2026 (ProgramBench), so "almost never" pools generations. With visible tests, NL2Repo full solves rise from 3 to 18.
- Rewording: "Across five benchmarks evaluating models from 2023 (JavaBench) to 2026 (ProgramBench), fully passing repositories are rare: 3/104 for the best NL2Repo-Bench configuration (40.2% mean), ≤4/50 in BeyondSWE Doc2Repo (≈62% mean), ..."

### X10 — Funnel bullets (RealBench 91→45→19; RepoGenesis; AppForge; app.build)
- Assessment:
  - RealBench's three numbers are best-per-metric values from different models, not one funnel. Its models top out at GPT-4o / Sonnet-4.
  - RepoGenesis: MetaGPT (Claude) has 73.04% API coverage and exactly 13.00% deployment, Python only (Java deployment 54%).
  - AppForge's "half of correct apps crash" rests on about 15 apps, and its tabulated crash rate uses compiled apps as the denominator.
- Rewording: "RealBench: best completion 91%, best execution 45%, best test pass 19% (different models)". "RepoGenesis (Python): MetaGPT reaches 73% API coverage but deploys 13% of repositories".

### X11 — "Early multi-agent work measured little beyond this stage" (ChatDev) / Tymcrat
- Assessment: Verified for ChatDev (GPT-3.5, 2023). "Early multi-agent work" generalises from one paper. Tymcrat is not multi-agent, and its 41-function manual sample had two raters who disagreed.
- Rewording: "ChatDev (GPT-3.5) reports only executability (0.88) and an embedding-based consistency score ..."

### X12 — "agents exploit whatever the oracle does not check. Documented cases"
- Assessment: Overstated.
  - Only AppForge clearly documents evasion, and its 91.09% figure has no stated detection method.
  - Spec2Code has no full text.
  - Vero states that its 5 algorithm substitutions are "behaviorally correct rather than a shortcut", so it is a counter-example.
  - The chess study shows biased self-measurement (11/15 self-Elo scripts overestimate by 200–1,100), not demonstrated cheating.
  - In SWE Refactor Bench, the no-migration verdicts come from an LLM audit.
  All except Spec2Code are preprints, with models from 2025 (AppForge GPT-4.1) to 2026 (Vero, chess).
- Rewording: "Optimising agents can satisfy behavioural oracles without completing the task: AppForge reports GPT-4.1 deleting error-inducing code under compile feedback (files 8.0 → 2.7), and an LLM audit in SWE Refactor Bench flags 30 suite-passing runs as non-migrations. Agent-written self-evaluation is also unreliable (chess study: 11 of 15 self-Elo scripts overestimate by 200–1,100)." Remove Vero, or present it as a contrast case.

### X13 — "In app.build, removing Playwright end-to-end tests raised app viability by 16.7 pp" / "Brittle end-to-end tests ... reject valid variants"
- Assessment: The number is verified, but it is a 5-app swing in n=30, from a single run, and the paper's automated metric moved by −3.3 pp. The sentence generalises from one study.
- Rewording: "In one ablation (app.build, 30 prompts, single run), removing Playwright tests raised human-judged viability from X to Y (5 apps) ..."

### X14 — "Browser-agent oracles ... avoid selectors altogether"
- Assessment: False for TDDev2026: its agent writes Playwright selectors on the fly, and 3 of 5 false positives were selector errors.
- Rewording: "avoid hand-written selectors".

### X15 — Non-functional bullets and "Current agents also tend to produce monolithic code ... no benchmark yet evaluates the design"
- Assessment:
  - RAL-Bench's "models differ widely" rests on one highlighted pair (Gemini-2.5-Pro vs GPT-4o: 27.6% vs 27.5% functional, 35.2% vs 57.6% non-functional). Its strategy result covers one model (GPT-5.2) in one run.
  - The Cursor numbers have no citation. They are totals over 10 human-in-the-loop projects (~170k LoC) with no baseline.
  - OOD's "only because" is causal, whereas the authors say "consistent with" and "associated with".
  - AgingGen covers 4 apps in a single run with no human baseline.
  - The security bullets use function-level completion tasks (contextual tier) and different model generations. RealSec gives <8% baseline but reaches 10.5% with RAG, using 2024–25 models. SecRepoBench gives 53.5% with 2025 agents.
  - The monolithic-code claim rests on two 2026 preprints.
  - "No benchmark yet evaluates design" is contradicted in part by the Cursor and OOD studies (design-quality evaluation, though not benchmarks) and by RAL-Bench's maintainability dimension. Narrow it to "as a primary, standardised benchmark target".
- Rewording: "... In two 2026 preprints (ProgramBench, CLI-Tool-Bench), outputs are largely single-file. Design quality has been studied only in small empirical studies (10 Cursor projects; one Java assignment), not as a primary benchmark target."

### X16 — Model-generation pooling (supervisor concern 1), section-wide
- Assessment: The section pools results from GPT-3.5-era studies (ChatDev, JavaBench, CBA, Tymcrat, CodeS) with 2026 frontier-model studies (ProgramBench, Vero, VCB, CLI-Tool-Bench) without saying so, for example in the partial-credit list, the evasion list and the "early work" contrast. Add a model-era tag to each bullet, e.g. "(GPT-4-era, 2024)", or group the bullets by era.

### X17 — Peer review (supervisor concern 2), section-wide
- Assessment: Of 57 cited bibkeys, the corpus marks 44 as preprints; the 3 uncited works (Cursor, chess, cJSON) add 2 more preprints. The corpus venue column appears stale for CodeS and ProjectGen (TOSEM), ProjectEval (ACL Findings), PaperBench (ICML 2025), Commit0 (ICLR 2025) and MultiAgent-FrontEnd (MSR 2026). Reconcile it before reporting peer-review status. Every quantitative claim about LLM-judge reliability rests on preprints.

## Unsupported
- Line 38, table: "cJSON porting" has no citation and no full text. Fix: add \cite{cJSONRustPorting2026}, or delete it until the full text is read.
- Line 115: "The chess study: 11 of 15 ..." has no citation. Fix: add \cite{ChessEnginesPL2026}. Reword as unreliable self-measurement rather than evasion.
- Line 130: "Cursor-built projects that are 91% functionally complete carry 1,305 CodeScene and 3,193 SonarQube issues" has no citation. Fix: add \cite{CursorDesignIssues2026}, and give the scope (10 projects, human-in-the-loop, totals, no baseline).
- Line 87: "AppEvalPilot ... report human alignment" names the tool but not the paper. Fix: cite RealDevWorld2025 ("AppEvalPilot (RealDevWorld)").
- Line 81: MultiAgent-FrontEnd "about six" has no full text. Fix: get the full text (MSR 2026), or delete.
- Line 114: Spec2Code taxonomy has no full text, and the record is a code capsule. Fix: delete, or weaken to "proposes", without evidential weight.
- Line 56: "Upstream tests ... call ... private helpers" has no evidence in the cited sources. Fix: delete "private helpers".
- Line 54: "Upstream tests are the most common oracle for NL-to-repository and skeleton tasks" is not computed. Fix: compute it from corpus.csv per task, or weaken to "a common oracle".
- Line 64: "The clearest trend of 2026" has no count or denominator. Fix: give "six 2026 benchmarks".
- Line 70: "every generated test is validated on the reference" is false for RepoGenesis, RepoMod-Bench and ProjDevBench. Fix: restrict it to CLI-Tool-Bench, ProgramBench, RepoZero and SWE Refactor Bench.
- Line 80: "LLMs also frequently write the specification or the tests" is uncounted. Fix: give the generated-tests code count (15), or name the studies.
- Line 102: "Mean test pass rate is the default metric for core tasks" is uncounted. Fix: weaken to "common", or count it.
- Line 101: "Build success ... tells us little about correctness" is a normative claim. Support it with the funnel numbers it follows, or mark it as a recommendation.
- Line 106: "the agent replaced the reference algorithm with one that is easier to prove" (Vero) is contradicted by the source. Fix: remove it from the evasion list.
