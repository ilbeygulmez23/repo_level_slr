# Fact-check ledger: survey/sections/rq4_design.tex (RQ4: System Design)

Every claim was checked against the full text in slr/data/fulltext/ (corpus notes not trusted). No .tex file was edited.
Claims checked: 110. Verdicts: VERIFIED 62, CORRECTED 13, MISLEADING 31, NOT FOUND 1, NO FULL TEXT 3.
Where a verdict says "VERIFIED (caveat)" the number is right but the Measurement line matters for how the survey may use it.
Two claims flagged by the supervisor get dedicated analyses: (a) "Structure is not uniformly beneficial" (C42–C44) and (b) "Context is not the main bottleneck" (C18–C19).

# Claims

## Lines 6–25 + table rows 153–154 (Context acquisition)


### C1 — AllianceCoder2025
- Draft: "retrieving similar code \emph{lowers} performance by up to 15\%"
- Verdict: CORRECTED
- Evidence: "retrieved similar code often introduces noise, degrading results by up to 15%" (Abstract). The figure appears only in the abstract. In Table 3 the drops are in Pass@1 points, e.g. CoderEval GPT ConAPI 36.52 vs ConSimAPI 19.57 (-17.0 pp) and Context 30.43 vs ConSim 14.35 (-16.1 pp). Similar code on its own is not always worse: RepoExec SimilarGPT 16.90 vs PureGPT 16.62.
- Correct statement: Adding retrieved similar code to other context lowers Pass@1, by up to ~17 points in Table 3 (the abstract says "up to 15%"). On its own, similar code gives roughly zero gain and sometimes a small loss.
- Models: GPT-4o-mini (2024), Gemini 1.5 Flash (2024)
- Measurement: CoderEval (230 Python tasks) + RepoExec. Pass@1/3/5 at temp 0.7. Oracle setting: the similar-code retrieval uses knowledge of the target code (RepoCoder-style, top-5), and the API setting assumes all invoked APIs are known. It is controlled (same model, only context type varies), but the oracle setting makes it an upper bound rather than a realistic retriever. No variance is reported.
- Status: preprint

### C2 — AllianceCoder2025
- Draft: "whereas the invoked APIs help most"
- Verdict: CORRECTED
- Evidence: "contextual informaion provides the most significant performance improvement ... incorporating invoked API also substantially enhances performance ... the combination of both contextual information and invoked API information yields the best overall performance" (§5.1). Table 3: ContextGPT 29.01/30.43 vs APIGPT 25.63/25.65 Pass@1 (RepoExec/CoderEval).
- Correct statement: In-file context helps most, invoked APIs (oracle) come second, and the two together are best.
- Models: GPT-4o-mini, Gemini 1.5 Flash (2024)
- Measurement: as C1. The APIs are oracle (assumed known).
- Status: preprint

### C3 — Repoformer2024
- Draft: "up to 80\% of retrievals bring no benefit"
- Verdict: VERIFIED (scope needs qualifying)
- Evidence: "up to 80% of the retrievals performed by a standard RAG method do not enhance the performance of common code LMs such as CodeGen ... and StarCoder ..., and many degrade the performance" (§1). Table 1: RepoEval function completion, StarCoder-16B ↓16 / =386 / ↑53. Fig. 3: "only improve the performance in about 20% of instances".
- Correct statement: add "in code completion with 2022-23 code LMs".
- Models: CodeGen-Mono 2B/16B (2022), StarCoder/StarCoderBase 1B-16B (2023)
- Measurement: per-instance change in ES / unit-test pass on RepoEval (455 function tasks in Table 1), with versus without RepoCoder-style sparse cross-file retrieval. Controlled (same model). Task is completion (infilling), not NL-to-function generation.
- Status: ICML 2024

### C4 — MRGBench2025
- Draft: "in-file context beats both BM25 and embedding retrieval"
- Verdict: VERIFIED
- Evidence: Table 7 (DeepSeek-Coder-33B) avg Pass@1: bm25-rag 10.1%, bge3-rag 12.9%, mix 12.3%, RepoCoder 18.1%. Table 5 in-file 22.2%. "RAG-related methods ... effectiveness is significantly inferior to that of providing in-file context alone" (Takeaway-6).
- Correct statement: n/a. The draft could add that RepoCoder also loses (18.1 vs 22.2). Note also that callee bodies (oracle structural context, 12.8%) score no better than embedding RAG (12.9%) (Table 5). That result cuts against "structure beats similarity".
- Models: DeepSeek-Coder-33B (2023) for all RAG runs; embeddings BGE-M3
- Measurement: 383 tasks (Python/Java/Go), Pass@1/3. A single generator was used for the RAG comparison. Chunks are 500 tokens, top-5, via LangChain. Controlled (same model). RAG chunks may contain the in-file content anyway, and token budgets are not matched.
- Status: preprint

### C5 — REPOCOD2024
- Draft: "providing callees is worse than dense retrieval"
- Verdict: MISLEADING
- Evidence: Table 5 overall Pass@1: GPT-4o Callees 22.8 vs RAG_Dense 27.0, but GPT-4o-mini Callees 16.5 vs RAG_Dense 15.0. "The Callees setting is comparable to RAG_BM25 and RAG_Dense but does not consistently outperform them. Across all complexity levels, it lags behind the Current-File setting." (Finding 3)
- Correct statement: Oracle callees (plus 1,024 prefix tokens) are comparable to BM25 and dense retrieval. They are worse with GPT-4o, slightly better with GPT-4o-mini, and below current-file context. The paper also finds that retrieval with high dependency recall gives the best results (§4.3).
- Models: GPT-4o, GPT-4o-mini (2024) for Table 5. Main table: CodeLlama, DeepSeekCoder, DeepSeek-V2.5, Claude 3.5 Sonnet (2023-24)
- Measurement: 980 tasks, Pass@1 against developer tests (~314 per instance), greedy, 1 run. The Callees setting is an oracle. Controlled (same model).
- Status: ACL 2025

### C6 — GRACG2025
- Draft: "better graph retrieval does not significantly improve pass@$k$, even with oracle functions"
- Verdict: NO FULL TEXT (consistent with abstract)
- Evidence: abstract (slr/data/records.csv R1076): "graph-based retrieval outperforms classical methods ... However, in terms of end-to-end code generation, we observe non-significant improvements in the metrics, even when oracle functions are used."
- Correct statement: Keep as is, but mark it as abstract-only. The abstract gives no benchmark, models or baseline. This is graph (structural) retrieval, so it is evidence that better structural retrieval does not carry over to generation. It is not evidence about similar-code retrieval (see C17).
- Models: unknown
- Measurement: unknown. pass@k against tests; the baseline for the "non-significant" comparison is not stated.
- Status: ASE Workshops 2025

### C7 — RealBench2025
- Draft: "in the core tier, RAG over previously generated files is the worst of three strategies"
- Verdict: MISLEADING
- Evidence: §3.1.1: RAG retrieves "files that have the 'import' relation with the target file" from a DAG built from the system design. Table 5 avg test pass rate L1-L4: Holistic 25.48/7.30/16.38/5.81, Incremental 21.79/6.33/23.88/13.36, RAG 21.76/5.66/15.85/11.40. "RAG achieves 2.67% average decline compared to incremental" (§RQ2); "Incremental generation performs better than RAG strategy" (Finding 4).
- Correct statement: RAG has the lowest mean test pass rate (13.67 vs 13.74 holistic vs 16.34 incremental). It is effectively tied with holistic overall and beats holistic on L4. The paper attributes the result to long inputs (with truncation) and to merging of modules. The retrieval here is structural (import-graph) retrieval of the model's own earlier output, not similarity retrieval.
- Models: GPT-4o (2024-05), Claude Sonnet 4 (2025-05), Gemini 2.5 Flash (2025), DeepSeek-V3 (2024-12), Qwen3-235B-A22B (2025), Qwen2.5-Coder-7B (2024)
- Measurement: 61 repos, ~50 tests each, greedy, 1 run. Controlled across strategies (same model). Retrieved files are truncated when they exceed the context window.
- Status: FSE 2026

### C8 — RepoScope2025, DevEval2024
- Draft: "call chains: RepoScope, with +36\% relative on DevEval"
- Verdict: MISLEADING
- Evidence: "most prominent gain is observed on DevEval with the Claude-3.5-Haiku backbone model, where RepoScope outperforms the best baseline DRACO by 36.35%" (§5.1). Table 2: the other DevEval gains are +3.64% (GPT-4o mini), +2.14% (Qwen3-235B) and +11.62% (DeepSeek-V3). RepoScope "integrat[es] both structural and similarity-based contexts" (Abstract). Ablation (Table 3, CoderEval): w/o CC -7.03%/-7.32%; w/o similar functions -5.27%/-11.38% (the largest drop).
- Correct statement: RepoScope combines call-chain and similarity context. Its best case is +36.35% relative Pass@1 over DRACO (itself a dataflow/structural method) on DevEval with Claude-3.5-Haiku; across the four backbones the DevEval gain is 2-36%. In the ablation, removing call chains costs ~7% and removing similar functions costs up to 11%. So the +36% is not a call-chain-versus-similarity effect.
- Models: GPT-4o-mini (2024), Claude-3.5-Haiku (2024), Qwen3-235B-A22B (2025), DeepSeek-V3 (2024-12)
- Measurement: DevEval 1,742 of 1,825 samples (filtered), CoderEval-Python 207. Pass@1, temp 0, 1 run. Baseline prompt lengths roughly matched to ~3.7k tokens. The ablation was run on CoderEval only, with 2 models. Two-tailed test p=2.1e-9 against DRACO.
- Status: ICSE 2026 (DevEval: preprint per corpus.csv)

### C9 — Hydra2026
- Draft: "structural units instead of text chunks: Hydra"
- Verdict: VERIFIED
- Evidence: Table 2 (same BM25 and generator): DevEval 7B Pass@1 chunk 8.46 vs structure-aware 16.67; RepoExec 7B 14.03 vs 20.79; DevEval 1.5B 4.81 vs 10.32.
- Correct statement: n/a. This is a controlled comparison of indexing units (both sides use BM25), not structure versus similarity. On retrieval method (Table 4), dependency-aware vs BM25 is a "modest" gap (DevEval 7B 16.84 vs 16.67), and the hybrid is best: "similarity-based context still provides complementary value".
- Models: Qwen2.5-Coder-1.5B/7B-Instruct (2024); GPT-4.1 mini (2025) in Table 5 only
- Measurement: DevEval + RepoExec, Pass@1/3/5. Controlled (same retriever and generator).
- Status: FSE 2026

### C10 — Hydra2026
- Draft: "which reduces NameError, TypeError, and AttributeError"
- Verdict: VERIFIED (uncontrolled)
- Evidence: "Compared to baselines (No Context, RepoCoder, RepoFormer, and RLCoder), Hydra significantly reduces critical errors such as NameError, TypeError, and AttributeError ... we observe a relative increase in AssertionError" (§RQ3, Fig. 6).
- Correct statement: Add that the error reduction is measured against different systems (uncontrolled), and that AssertionError rises.
- Models: as C9
- Measurement: error-type distribution from test logs, Fig. 6. Not a single-factor ablation.
- Status: FSE 2026

### C11 — CatCoder2024
- Draft: "types from a language server: CatCoder" (listed as structure outperforming similarity)
- Verdict: MISLEADING
- Evidence: uses "Eclipse JDT.LS ... through the Language Server Protocol" and rust-analyzer (§4.4.1). Ablation (Table 7, CodeLlama-13B): Java pass@1 FULL 44.7, -TC (similarity retrieval only) 39.5, -CR (type context only) 27.5. Averaged over models: "pass@1 score decreases by 46.89% without Relevant Code Retrieval, and decreases by 17.17% without Type Context" (§5.3).
- Correct statement: CatCoder adds language-server type context on top of similarity retrieval. Types help (−17% pass@1 when removed), but similarity retrieval matters more (−47% when removed). Type context complements similarity; it does not outperform it.
- Models: CodeLlama-13B-Instruct (2023) main; CodeLlama-7B, DeepSeek-Coder-6.7B, CodeGemma-7B, CodeQwen1.5-7B, Llama-3-8B (2023-24)
- Measurement: 199 Java + 90 Rust tasks, compile@k / pass@k. Controlled ablation.
- Status: preprint

### C12 — TypedHolesChatLSP2024
- Draft: "types from a language server: ... Typed Holes"
- Verdict: VERIFIED (weak evidence on the comparison with similarity retrieval)
- Evidence: "contextualization with type definitions is particularly impactful" (Abstract). Versus vector retrieval: "The combination of types and headers performed well against the Vector Retrieval baseline, though ... this was disproportionately due to a single confounding chunk" (§2.9). Exhaustive retrieval performed "somewhat better" than types+headers (§2.9).
- Correct statement: In 5 small MVU programs (Hazel and TypeScript), language-server types are the most useful static context. The win over vector retrieval comes from a synthetic 1,000-line codebase built to contain confounders, and is driven by one confounding chunk. Dumping all code does slightly better.
- Models: GPT-4-0613 (2023), StarCoder2-15B (2024)
- Measurement: MVUBench, 5 programs, 20 trials per configuration, temp 0.6, % of tests passed. The baseline gives the model only the function header. The authors themselves say "The appropriateness of our baselines is arguable" and "Our RAG baseline is relatively simplistic" (§4).
- Status: OOPSLA 2024

### C13 — DyRetriever2026
- Draft: "partial dependency graphs: DyRetriever"
- Verdict: MISLEADING (as evidence that structure *outperforms* similarity)
- Evidence: "removing either the DyRetriever or the similarity-based retrieval leads to a comparable average performance drop of 14.80% and 15.85% ... This demonstrates the complementarity" (§1). Table 3: graph-only beats similarity-only in 3 of 4 cells (DevEval Qwen3 35.71 vs 22.94; GPT-4o-mini 26.56 vs 15.55; CoderEval Qwen3 42.87 vs 41.57), but GPT-4o-mini CoderEval is 33.83 vs 34.00. The graph-only variant uses more tokens (e.g. DevEval 100k vs 45.5k).
- Correct statement: DyCoder combines LLM-driven partial dependency-graph retrieval with similarity retrieval. Each component contributes comparably, and graph-only beats similarity-only in most cells but at roughly twice the tokens.
- Models: Qwen3-Coder-30B (2025), DeepSeek-V3.2 (2025), GPT-4o-mini (2024)
- Measurement: CoderEval-Python + DevEval, Pass@1. The ablation covers 2 models. Not token-matched. Agentic (LLM) traversal.
- Status: ASE 2026

### C14 — CoCoGen2024
- Draft: "compiler-driven retrieval of missing context: CoCoGen, which cuts undefined-name errors from 5,133 to 1,042 in one iteration"
- Verdict: VERIFIED (number); caveat on effect
- Evidence: "UNDEF errors are notably reduced from 5,133 to 1,042 after one iteration" (§5.4, Fig. 6).
- Correct statement: The number is correct. Add that the counts are aggregated over all sampled solutions. Also, the pass-rate gain over similarity-based RepoCoder appears only at pass@5/10: in the ablation Pass@1 is 28.01 for CoCoGen vs 28.72 for RepoCoder (Table 3), and Code Llama's project-level Pass@1 is 13.04 vs 16.09 (Table 2).
- Models: GPT-3.5-Turbo (2023), Code Llama 13B (2023)
- Measurement: CoderEval-Python splits, Pass@1/5/10. Error counts come from static analysis of sampled outputs. Fig. 6 compares against RepoCoder and no-feedback.
- Status: preprint

### C15 — RepoClassBench2024
- Draft: "Symbol-lookup tools used by an agent reach 77.6\% Pass@1 on RepoClassBench Java, compared with 54.7\% for RepoCoder"
- Verdict: MISLEADING
- Evidence: Table 3 (Java DETAILED, GPT-4): RRR 77.56 (sd 2.06), RepoCoder 54.74 (1.03). RRR uses an oracle loop: "This iterative cycle persists until either all test cases pass or the maximum allowed number of oracle calls is reached" (Fig. 2). RepoCoder "does not utilize oracle feedback" (§5.3.1). Table 10: RRR iteration 1 = 13.85%. Python: 29.38 vs 23.54.
- Correct statement: RRR (repository tools plus compiler/test feedback for up to 5 iterations) reaches 77.6% vs 54.7% for RepoCoder, which gets no feedback, on Java-DETAILED with GPT-4. The comparison mixes tools with execution feedback. With compiler-only feedback RRR scores 65.1% (Table 6). The Python gap is small (29.4 vs 23.5).
- Models: GPT-4 (2023); appendix: GPT-3.5-turbo-instruct, Llama3-70B, Phi3
- Measurement: 130 Java / 97 Python / 60 C# classes. Pass@1 at temp 0.2, sd over 6 generations. Uncontrolled: RRR has a test oracle the baseline lacks.
- Status: preprint

### C16 — Table row 153 (RepoScope, Hydra, CatCoder, Typed Holes, CoCoGen)
- Draft: "Structural context (call chain, types, dependencies) & C & +"
- Verdict: VERIFIED for "C, + as an addition"; MISLEADING if read as "beats similarity"
- Evidence: controlled ablations exist. RepoScope w/o CC -7%; Hydra Table 2 indexing; CatCoder -TC -17%; Typed Holes feature ablation. CoCoGen Table 3 is mixed at Pass@1 (28.01 vs 28.72).
- Correct statement: C, +: structural context improves results when added to similarity context. Note that CoCoGen is ± at Pass@1.
- Models/Measurement/Status: see C8-C14

### C17 — Table row 154 (AllianceCoder, Repoformer, MRG-Bench, RealBench, GRACG)
- Draft: "More/similar-code retrieval & C & $\pm$/--"
- Verdict: MISLEADING
- Evidence: RealBench's RAG is import-graph retrieval (C7). GRACG is GNN graph retrieval (C6). Neither is similar-code retrieval. Removing similarity retrieval hurts in CatCoder (-47%), DyRetriever (-15.85% avg), RepoScope (w/o SF up to -11.38%) and Hydra (hybrid > DAR). REPOCOD dense ≥ oracle callees for GPT-4o.
- Correct statement: Move RealBench and GRACG to a separate row, "Structural retrieval with no end-to-end gain" (±). For similar-code retrieval the direction is ±. It hurts or gives nothing on its own in AllianceCoder (oracle), Repoformer (completion) and MRG-Bench (vs in-file context), and helps as a complement in CatCoder, DyRetriever, RepoScope and Hydra.
- Status: AllianceCoder and MRG-Bench are preprints; Repoformer ICML 2024; RealBench FSE 2026; GRACG ASEW 2025 (no full text)


## Lines 27–28 (Context is not the main bottleneck) — see dedicated analysis (b)


### C18 — MRGBench2025 (arxiv:2508.02998)  [dedicated analysis (b)]
- Draft: "MRG-Bench attributes more than 68% of failures to misunderstanding *what* to build rather than *how*."
- Verdict: MISLEADING. The number matches. However, the paper's "What" category is defined to include repository context, and the paper's own conclusion is to retrieve better *what*-context. Using it as evidence that "context is not the main bottleneck" inverts the paper's framing.
- Evidence (§5.3): "over 68% of failures stem from missing 'What information' - models cannot understand what code functionality the user requirements correspond to within the current repository context." "What information" is defined as information that guides models to the functional logic, "potentially including function definitions, comments, classes, sibling functions, or functions with similar names". The paper then says: "we should further enhance retrieval techniques for this type of information, such as repository README documents, feature descriptions". The annotation prompt (Fig. 4) asks which information type "is missing from the model-generated incorrect code snippets, based on the provided standard answer code segments".
- Correct statement: "For Claude-3.5-Sonnet's failed function completions, an LLM-vote annotation attributes >68% of failures to missing 'what' information (what the function should do in this repository) rather than 'how' information (callable APIs and frameworks). The authors read this as a need for better requirement-level context, not as evidence against context."
- Models analysed: failures of **Claude-3.5-Sonnet only** (2024). Annotators: GPT-4o, Claude-3.5-Sonnet, Gemini-2.5-Pro, DeepSeek-V3 and Qwen2.5-72B, all 2024-25. The RAG comparisons use DeepSeek-Coder-33B (2023).
- Measurement:
  - **LLM coding, not human.** A 5-model vote at T=0 assigns a binary What/How label. Only 5:0 and 4:1 votes are kept; 3:2 cases are discarded, for an 86.3% retention rate. There is no human validation or agreement statistic. The label is assigned by comparison with the *reference* implementation, so any functional divergence from the reference tends toward "What".
  - Scope: 383 function-completion samples from 22 projects (Python, Java, Go), with signature and docstring as input. It is not repository generation and uses no agents ("Lack of agent based method" is listed as a threat to validity). The number of failed cases annotated is not reported.
- Status: preprint (2025).

### C19 — LLMHallucinationsinPract2024 (arxiv:2409.20550)  [dedicated analysis (b)]
- Draft: "A hallucination taxonomy finds task-requirement conflicts (43.5%) more frequent than project-context conflicts (24.6%)."
- Verdict: MISLEADING. The numbers are VERIFIED (43.53% and 24.56%), but they are misleading as support for "context is not the bottleneck". The models were given *no repository context*. The percentages are shares of hallucination *instances*, not of failures. The third category, factual-knowledge conflicts, is 31.91%. The paper's own RAG mitigation (adding repository context) improved Pass@1 for all six models.
- Evidence: "In the Raw method, we only provide LLMs basic docstrings and function signatures." The taxonomy reports "1) Task Requirement Conflicts (43.53%)", "2) Factual Knowledge Conflicts (31.91%)" and "3) Project Context Conflicts (24.56%)". Table I shows RAG raising Pass@1 for every model, e.g. ChatGPT 10.40% -> 12.61%.
- Correct statement: "On CoderEval (230 Python functions), a manual taxonomy of hallucinations produced by six 2021-24 models, prompted with only a docstring and signature, finds task-requirement conflicts (43.5%) more common than factual-knowledge (31.9%) or project-context (24.6%) conflicts."
- Models: CodeGen-350M-Mono (2022), PanGu-α-2.6B (2021), GPT-3.5-Turbo (2022-23), DeepSeekCoder-6.7B-base (2023), CodeLlama-7B-Python (2023) and StarCoder2-7B (2024). Raw Pass@1 was 0.04-10.4%.
- Measurement:
  - **Manual open coding.** Two authors built the taxonomy from 23 tasks × 6 models × 10 samples (1,380 snippets). Three volunteers then annotated the remaining snippets "independently". No inter-rater agreement is reported, and the paper does not say how disagreements were resolved. Multiple hallucinations may be coded per snippet, and the coders compared outputs against the ground truth.
- Status: corpus.csv `venue`=preprint, but `venue_record`="Proceedings of the ACM on software engineering" (2024). Reconcile; it is probably published in PACMSE.


## Lines 30–56 + table row 155 (Planning representation)


### C20 — (corpus-level; no citation)
- Draft: "Core-tier methods almost always insert an intermediate artefact between the requirement and the code."
- Verdict: MISLEADING
- Evidence: slr/data/corpus.csv: 104 core-tier records; only ~66 have "method" in `contribution` (35 pure method), the rest are benchmark/empirical only. Method papers without a requirement-to-code planning artefact include training/RL work (WebGen-R1 arxiv:2604.20398, DeNovoSWE arxiv:2606.10728, MindForge arxiv:2607.27146, SWE-Playground arxiv:2512.12216), validation/testing methods (RustAssure, ReCodeAgent), and state/memory methods (Persistent Cross-Attempt State arxiv:2604.03632). Translation methods use skeletons that are derived from source code, not from a requirement. The corpus has no column coding "uses intermediate artefact", so no count backs "almost always".
- Correct statement: "Most NL-to-repo/NL-to-app agent frameworks in the core tier (e.g., the 12 listed below) insert an intermediate artefact..." Alternatively, code the corpus and report k/N.
- Models: n/a
- Measurement: no tally exists; this is the drafter's impression
- Status: n/a

### C21 — CodeS2024
- Draft: "hierarchical sketches: CodeS"
- Verdict: VERIFIED
- Evidence: "RepoSketcher, FileSketcher, and SketchFiller" ... "a multi-layer sketch" (abstract)
- Models: n/a (characterisation)
- Measurement: n/a
- Status: preprint

### C22 — RPGZeroRepo2025
- Draft: "a persistent Repository Planning Graph of capabilities, files, data flows, and interfaces"
- Verdict: VERIFIED
- Evidence: "encodes capabilities, file structures, data flows, and functions in a unified graph"; "Repository Planning Graph (RPG), a persistent ..." (abstract, Sec. 1)
- Models: n/a
- Measurement: n/a
- Status: ICLR 2026

### C23 — Repo02026
- Draft: "a dual requirement/component DAG that evolves under cohesion and coupling metrics"
- Verdict: VERIFIED
- Evidence: "Dual-DAG, consisting of a requirement-level DAG, a component-level DAG, and their alignment relation"; "Split—low cohesion Merge—high coupling" (abstract, Fig. 2, Sec. II-C)
- Models: n/a
- Measurement: n/a
- Status: preprint

### C24 — CodeTeam2026
- Draft: "a machine-checkable contract normalised from competing designs"
- Verdict: VERIFIED
- Evidence: "multiple Architect agents draft competing software design sketches ... a CTO agent then evaluates, selects, and normalizes the most promising SDS into a machine-checkable contract" (abstract)
- Models: n/a
- Measurement: n/a
- Status: preprint

### C25 — ProjectGen2025
- Draft: "a semantic architecture tree"
- Verdict: VERIFIED
- Evidence: "Semantic Software Architecture Tree (SSAT)" (abstract)
- Models: n/a
- Measurement: n/a
- Status: preprint

### C26 — TraceDev2026
- Draft: "a requirement--design--code traceability graph"
- Verdict: VERIFIED
- Evidence: "a heterogeneous traceability graph linking requirements, design models, and code artifacts" (Sec. 1)
- Models: n/a
- Measurement: n/a
- Status: ISSTA 2026

### C27 — CodeSpec2026
- Draft: "executable architecture and behaviour specifications"
- Verdict: VERIFIED
- Evidence: "compiles them into complementary architecture and behavior specifications" (abstract). Note: the task is feature development in *existing* repositories (FeatureBench), not generation from scratch.
- Models: n/a
- Measurement: n/a
- Status: preprint

### C28 — SpecFirst2026
- Draft: "a structured behavioural specification elicited by probing the binary"
- Verdict: VERIFIED
- Evidence: "A dedicated spec agent first probes the binary and combines observations with documentation into a structured specification" (abstract). The spec is a Markdown document ("Markdown under named headings", Sec. VII); it is not machine-checked.
- Models: n/a
- Measurement: n/a
- Status: preprint

### C29 — WebDesignIter2026
- Draft: "an architectural knowledge graph"
- Verdict: VERIFIED
- Evidence: "a persistent repository-level knowledge graph (WebAppArchKG) that integrates code structure and design ..." (Sec. 1). The KG is built from the existing code repository ("The initial code repository is first transformed into a knowledge graph").
- Models: n/a
- Measurement: n/a
- Status: preprint

### C30 — EvoDev2025
- Draft: "a feature DAG"
- Verdict: VERIFIED
- Evidence: "constructs a Feature Map, a directed acyclic graph that explicitly models dependencies between features" (abstract)
- Models: n/a
- Measurement: n/a
- Status: preprint

### C31 — PaperCompiler2026
- Draft: "provenance-linked file specifications"
- Verdict: VERIFIED
- Evidence: "preserving source provenance ... The resulting specifications encode non-degradation requirements, ownership assignments, cross-file dependencies, and file-level constraints" (abstract)
- Models: n/a
- Measurement: n/a
- Status: preprint

### C32 — AgileCoder2025
- Draft: "a code dependency graph: AgileCoder" (listed as an intermediate artefact between requirement and code)
- Verdict: MISLEADING
- Evidence: "Dynamic Code Graph Generator, which creates a Code Dependency Graph (CDG) that updates ... whenever the code is updated"; "ignoring G means that all source code is always included in the instructions" (Sec. 4.3, 5)
- Correct statement: AgileCoder's CDG is derived from the generated code. It serves as a retrieval and context-selection structure, not as a plan sitting between the requirement and the code. Its planning artefacts are the sprint backlog and acceptance criteria.
- Models: n/a
- Measurement: n/a
- Status: FORGE 2025

### C33 — AgileCoder2025
- Draft: "Removing the code dependency graph in AgileCoder: executability 57.5 → 23.4." (under "keeping everything else fixed ... large drops")
- Verdict: MISLEADING
- Evidence: Table 4 "Executability 57.50 23.38"; the text says "increasing from 23.28% to 57.50%". Table 4 caption: "In the case of the lack of G, we only consider tasks that do not encounter the Exceeding Context Length issue". "#ExceedingCL 0 11". Table 2 gives the full system as 57.79.
- Correct statement: In the ablation table, executability is 57.50 with G and 23.38 without it (the text says 23.28). The variant without G hit context-length overflow 11 times, and those tasks were excluded, so the two arms are scored on different task subsets. Removing G also puts all source code in the prompt. The ablation therefore tests context retrieval and overflow, not planning representation. Cost was roughly matched ($0.44 vs $0.48).
- Models: GPT-3.5-Turbo-0613 (2023) and Claude 3 Haiku (2024) per App. A.1; the paper does not say which backbone was used for Table 4.
- Measurement: ProjectDev, 14 author-collected tasks, 3 runs each. Executability is scored by **human evaluation** against the expected requirements (e.g., 4/10 requirements met = 40%). No reference tests, no inter-rater agreement, and no significance test.
- Status: FORGE 2025

### C34 — WebDesignIter2026
- Draft: "Removing design knowledge in WebDesignIter: −11.4 points Pass@1."
- Verdict: VERIFIED
- Evidence: Table II "w/o Design ... 23.50 (-11.40) 42.10 (-6.00)"; "All variants are evaluated under identical protocols." (Sec. C, RQ2)
- Correct statement: (Add for context.) On Pass@2 the drop is only −6.0, smaller than for removing the Code Graph (−7.0). The same table shows that removing the sandbox, i.e. the test-feedback loop, costs only −3.3.
- Models: Claude 4 Sonnet (2025) only
- Measurement: Web-Bench, 50 projects × 20 sequential tasks; the oracle is the benchmark's reference e2e test scripts (Playwright). The paper reports one run, with no repeats, variance, or significance test. Each ablated variant disables one module, and per-variant call/token budgets are not reported.
- Status: preprint

### C35 — Repo02026
- Draft: "Removing structural evolution in Repo0: −13 points on django."
- Verdict: CORRECTED
- Evidence: Table III django "w/o Structural Evolution 81.58 (-5.92) 10.94 (-2.65) 61.03 (-13.33) / 91.66 (-8.34)"
- Correct statement: On django, removing structural evolution lowers **Pass Rate** by 13.33 points (74.36→61.03). Coverage drops 5.92 and Voting Rate 8.34. The ablation removes the *evolution loop*; the Dual-DAG artefact stays in place. Removing the Dual-DAG itself costs −10.0 Pass Rate on django, −2.26 on requests and 0.0 on statsmodels. The django Repo0 row in Table III (Cov 87.50, Vote 100.00) does not match Table II (80.50/97.12 for GPT-5 mini).
- Models: GPT-5 mini and DeepSeek V3.2 (2025); the paper does not say which backbone the ablation used (requests/statsmodels rows match GPT-5 mini)
- Measurement: RepoCraft subset (django: 165 tasks). Pass Rate uses ground-truth tests that an LLM rewrote to fit the generated repository's interface (cross-model: DeepSeek V3.2 rewrites for GPT-5 mini). Voting Rate is an LLM majority vote. There are 3 runs at temperature 0, and no significance test. Ablation budgets are not reported.
- Status: preprint

### C36 — CodeSpec2026
- Draft: "Removing the specification in CodeSpec: 70.7 → 62.6."
- Verdict: MISLEADING
- Evidence: Table 3 "w/o All Specification 62.6±6.07 0.09"; Table 1 "Mini-SWE-Agent 62.6±6.07 0.09"
- Correct statement: The numbers are right (resolved tasks 9→7 of 30). However, the "w/o All Specification" row is identical to the Mini-SWE-Agent baseline, including the ±6.07 std and the $0.09 cost, so it is probably the bare scaffold rather than a specification-only ablation. Cost doubles with specifications ($0.09→$0.18). The two bootstrap std bands overlap (70.7±5.19 vs 62.6±6.07), and no significance test is given.
- Models: DeepSeek-V4-Pro, max thinking (2026)
- Measurement: FeatureBench Lite, 30 tasks; %Passed is the share of fail-to-pass reference tests passed. Std comes from bootstrapping the 10,000 task-level results; there is a single run. The paper says methods "share the same ... interaction budgets", but cost differs 2×.
- Status: preprint

### C37 — CodeSpec2026
- Draft: "The executable-vs-textual gap grows to 71.8 vs 43.8 on long instructions."
- Verdict: MISLEADING
- Evidence: "CodeSpec achieves 71.8% on instructions of 3,000–5,000 words, compared with 43.8% for CodeSpec (Text)"; Fig. 3a values: >5,000 words, CodeSpec 38.3 vs CodeSpec(Text) 36.3 vs RTADev 17.2; 3,000–5,000 words, RTADev 68.9.
- Correct statement: The 71.8 vs 43.8 gap is in the 3,000–5,000-word bin only. In the longest bin (>5,000 words) the gap shrinks to 2 points (38.3 vs 36.3). Another textual-plan agent, RTADev, reaches 68.9 in the 3,000–5,000 bin. All bins come from 30 Lite tasks split three ways (~10 tasks each), and no test is given.
- Models: DeepSeek-V4-Pro (2026)
- Measurement: FeatureBench Lite, 30 tasks binned by length; single run
- Status: preprint

### C38 — SpecFirst2026
- Draft: "Adding the specification phase in SpecFirst: +6.9–21.3% relative across four models, all p<0.01."
- Verdict: VERIFIED
- Evidence: Table II, Qwen3.5-397B 33.66→40.84 (+21.3%), Qwen3.6-35B 27.51→31.40 (+14.1%), GPT-5.5-high 59.02→65.14 (+10.4%), GPT-5.4-mini 39.09→41.78 (+6.9%); "All improvements are statistically significant (p <0.01)" (paired two-sided Wilcoxon, Sec. V-A)
- Correct statement: (Add.) The absolute gains are +2.7 to +7.2 points. The draft should state that the task is ProgramBench, i.e. behavioural reconstruction against an execute-only binary.
- Models: Qwen3.5-397B-A17B, Qwen3.6-35B-A3B, GPT-5.5-high, GPT-5.4-mini (all 2026)
- Measurement: ProgramBench, all 200 instances. The oracle is ProgramBench's hidden behavioural tests derived from the reference binary. The paper reports one run per configuration. The control is reasonable: same mini-swe-agent scaffold and same model ("the only difference ... is that we introduce spec agent"). But the spec agent is an extra phase with its own turn budget (step cap 1,000), so compute is not matched (see C39).
- Status: preprint

### C39 — SpecFirst2026
- Draft: "SpecFirst's gain is not cost-matched: the specification phase adds 48–130% cost."
- Verdict: VERIFIED
- Evidence: "The total cost of SPECFIRST is higher by 48%–130% across models" (Sec. VII-C, Table VII: Qwen3.5 +48%, Qwen3.6 +56%, GPT-5.4-mini +51%, GPT-5.5-high +130%)
- Correct statement: (Minor.) The 48–130% is the total-pipeline increase. The spec phase alone costs $0.25–$3.16 per instance, and the synthesis cost also changes (−17% to +32%).
- Models: as C38
- Measurement: mean API cost per instance
- Status: preprint

### C40 — DbCConstraints2025
- Draft: "Adding design-by-contract pre- and postconditions to class specifications: significantly higher pass@k"
- Verdict: NO FULL TEXT
- Evidence: Abstract (records.csv R1263): "incorporating explicit design constraints during prompting significantly boosts initial generation accuracy (measured via the pass@k metric), particularly in Python but also in C++."
- Correct statement: The claim is consistent with the abstract. The ablation is prompt-level (NL-only vs NL+pre/postconditions) on **one** medium-complexity system. The models, n, and test details cannot be verified.
- Models: "six state-of-the-art LLMs" (unnamed in abstract)
- Measurement: pass@k against reference unit tests (corpus.csv `evaluation`=reference-unit-tests); otherwise unknown
- Status: IEEE Access 2025

### C41 — AgileCoder, WebDesignIter, Repo0, CodeSpec, SpecFirst, DbC (table row, line 155)
- Draft: "Structured, checked plan representation & C & + & AgileCoder, WebDesignIter, Repo0, CodeSpec, SpecFirst, DbC"
- Verdict: MISLEADING
- Evidence: see C32–C40
- Correct statement: The row header "checked plan" does not fit several of the cited studies.
  - AgileCoder's CDG is a code-derived retrieval graph, and its ablation compares different task subsets.
  - SpecFirst's spec is an unchecked Markdown document.
  - WebDesignIter's Design module is prose architectural knowledge.
  - Repo0's ablation removes the evolution loop, not the artefact.
  - Only CodeSpec's (executable) and DbC's (pre/postconditions) artefacts are "checked", and CodeSpec's ablation row equals its baseline.

  Suggested change: "Structured plan/spec representation | C (5 preprints + 1 FORGE; single runs except Repo0, SpecFirst) | + | ...". Alternatively, move AgileCoder to a context/retrieval row.
- Models: GPT-3.5/Claude-3-Haiku (2023–24) for AgileCoder; Claude 4 Sonnet (2025) for WebDesignIter; GPT-5 mini/DeepSeek V3.2 (2025) for Repo0; DeepSeek-V4-Pro (2026) for CodeSpec; Qwen3.5/3.6, GPT-5.4-mini/5.5 (2026) for SpecFirst
- Measurement: mixed oracles: human judgement (AgileCoder), reference e2e tests (WebDesignIter), LLM-rewritten tests plus LLM vote (Repo0), reference F2P tests (CodeSpec), behavioural tests from a binary (SpecFirst)
- Status: 1 FORGE 2025, 1 IEEE Access (no full text), 4 preprints


## Lines 58–64 (Counter-evidence) — see dedicated analysis (a)


### C42 — E2EDevBench2025 (arxiv:2511.04064)  [dedicated analysis (a)]
- Draft: "adding a Designer agent (Designer+Developer+Tester) gives the *worst* result (22.6--32.8%): the Developer treats the design as authoritative and drifts from the requirement."
- Verdict: MISLEADING. The numbers are VERIFIED; the causal clause is not: the mechanism is the authors' untested hypothesis, presented in the draft as a finding.
- Evidence (Table 3): SDAgent-DDT Impl-Rate is "Flash 12.82 31.88 22.63%" and "Pro 19.18 27.56 32.79%", with a mean of 27.71%. The comparable means are DT 49.48% and Single 45.72%. On the mechanism, §4.2 says: "we hypothesize that the performance bottleneck originates in its Design Agent ... Once the Dev Agent receives what it perceives as an authoritative implementation plan, it tends to prioritize this plan over direct engagement with the original requirement document". No trajectory analysis, design-quality measurement or ablation supports this. The paper's own failure coding (Table 5) puts "Architectural Design Flaw" at only 5.6% of failures, pooled over all three agents.
- Correct statement: "With the same model and the same SWE-agent base, a sequential Designer->Developer->Tester pipeline fulfilled the fewest requirements (22.6% Flash, 32.8% Pro, against 45.5-53.5% for Developer->Tester). The authors *hypothesise* that the Developer over-trusts the design document."
- Models: Gemini-2.5-Pro and Gemini-2.5-Flash (2025). One model family serves as agent, test-migration agent and judge.
- Measurement:
  - Same model and harness? Yes. All three configurations are built on SWE-agent with the same toolset, temperature 0.2, and "a maximum of 200 agent steps was allocated for each task". The paper also says the Dev/Test agents are "configured identically" to those in SDAgent-Single. The step cap is not binding: DDT averages 86-108 steps. DDT is also not starved of budget, since it uses the least cost of the three (Pro $4.85 vs DT $7.05). Budget is held constant as a cap, not matched in spend.
  - Primary oracle: the Impl-Rate is **LLM-judged**. Gemini-2.5-Pro receives the code, the migrated-test results and the requirements list, and marks each requirement implemented or not, three times. A requirement counts as implemented only on 3/3 agreement, and inconclusive items stay in the denominator. On 10 projects and 546 requirements, the judge agreed with 3 graduate students 76.7-84.4% of the time (Pearson 0.62-0.67).
  - Secondary oracle: the test pass rate uses **reference tests adapted by an LLM**. A "Test Migration Agent" (Gemini-2.5-Pro, single-agent setup) rewrites the original PyPI project's tests to fit each generated project. The tests are therefore coupled to the reference behaviour, and their success depends on how easily the migrator can map the reference API onto the generated architecture. DDT-Pro produces many more files than the other configurations (13.74 vs 6.58 for DT-Pro and 3.50 for Single-Pro), with similar LOC. Its pass rate is also lowest (63-67% vs 75-80%).
  - Tasks and runs: 50 PyPI projects (2024Q1-2025Q1). Table 3 does not say whether the numbers come from one run or are averaged. A separate N=3 run analysis (Pro only, Fig. 5) gives requirements fulfilled by all 3 runs as DDT 446, Single 700 and DT 796, so the ranking is stable across runs. No significance tests or CIs are reported.
  - Could the measurement explain it? Only partly. The LLM-mediated oracles (migration plus judge) could penalise a more fragmented, design-doc-driven layout, since there are more files to locate and the reference-API mapping is harder. The judge is also the same model family as the agent. However, the gap is about 20 pp on the requirement metric, which does not need the reference architecture: the judge reads requirements against code. It appears for both models and in all 3 runs. A measurement artefact is therefore unlikely to explain all of it. The most likely confound is the *specific* design: one sequential prose hand-off with no feedback from Developer to Designer. That is not "structure" in general.
- Status: preprint (arXiv Nov 2025, ACM template placeholder "Conference'17").

### C43 — Athena2025 (arxiv:2508.20263)  [dedicated analysis (a)]
- Draft: "Athena's structured intermediate representations increase coverage, but they also increase the number of bugs (10.4 vs 1.25 per app) when no validation layer checks them."
- Verdict: MISLEADING. The numbers are correct. "Coverage" is not what was measured, and "when no validation layer checks them" is the survey's own gloss. The paper attributes the bugs to code volume and to SwiftUI being a low-resource language, not to an unchecked IR.
- Evidence: §5.2.3 reports "prototypes created with Athena contained 6.0 (SD = 2.2) views and 353.9 (SD = 92.8) lines of code, compared to 3.1 (SD = 1.1) and 117.8 (SD = 36.8) of the baseline". §5.2.4 says: "As a result of Athena allowing for more complex app structures and generating multiple code files, the prototypes created with Athena contained more bugs (mean = 10.4, SD = 13.4) compared to that of the baseline (mean = 1.25, SD = 3.1). However, most bugs ... were easy to fix ... All but one participant (P2) were able to fix all bugs". §6 says: "higher number of compilation errors ... (due to the larger volume of code in the more complex apps it produced)".
- Correct statement: "In a 12-participant user study (GPT-4o), apps prototyped with Athena's IRs were about 3x larger (353.9 vs 117.8 LOC; 6.0 vs 3.1 views) and contained more bugs (mean 10.4, SD 13.4, vs 1.25, SD 3.1). The bugs were mostly easy-to-fix compile errors, and the authors attribute them to code volume and to SwiftUI being low-resource."
- Models: GPT-4o (2024) in both conditions. The model is the same, but the baseline is the ChatGPT UI rather than a matched harness.
- Measurement:
  - **Human user study.** n=12 Apple-internal iOS developers, within-subject design, one 25-minute task per condition (Music and Parking tasks, counterbalanced). Participants decided when they were "satisfied" and then exported the code. Neither the time budget nor the amount of generated code is matched.
  - The bug count is raw, not normalised for size. Per KLOC the ratio drops from 8.3x to about 2.8x (29 vs 11 bugs/KLOC). With SD 13.4 on n=12, no significance test is reported. The paper does not say who counted the bugs or how.
  - The separate technical evaluation (10 author-made apps, Athena only, with no baseline) found 7.3 compile and 4.0 navigation errors per app. Most navigation errors were "placeholder comments", which appeared after the authors suppressed TODOs in the prompt.
  - Could the measurement explain it? Largely, yes. The comparison confounds structure with output size and task ambition. The tasks are open-ended, so Athena users built bigger apps. "Bugs" also lumps trivially fixable compile errors together with logic errors. Athena does not cleanly show that IRs make code buggier.
- Status: preprint (Apple; HCI prototype paper).

### C44 — Repo02026 (arxiv:2608.19854)  [dedicated analysis (a)]
- Draft: "Letting an LLM freely restructure the plan in Repo0 over-decomposes it and lowers accuracy."
- Verdict: CORRECTED. It is a single-repository, single-model analysis. One round of free restructuring *helps* relative to no evolution. Accuracy falls below the no-evolution baseline only at 3-5 rounds. "Over-decomposes" is the authors' explanation and is not quantified.
- Evidence: §V-C (Fig. 4, statsmodels, GPT-5 mini) compares w/o evolution (Cov 75.90, Pass 79.90 in the figure but 81.90 in the text, Vote 93.00), fixed 1 round (78.74 / 81.10 / 94.10), fixed 3 rounds (70.45 / 75.73 / 86.55), fixed 5 rounds (69.32 / 74.52 / 85.16) and Repo0 (80.68 / 85.51 / 98.65). The authors write: "Repeated structural actions can continue beyond the point of structural convergence, leading to unnecessary fragmentation ... it degrades coverage, pass rate, and voting rate after one round". No component counts or fragmentation metric are reported for these variants.
- Correct statement: "In Repo0's own analysis (one repository, GPT-5 mini), letting the LLM restructure the architecture without the cohesion/coupling metrics helped after one round but fell below the no-evolution baseline after 3-5 rounds (Pass Rate 74.5-75.7 vs about 80-82). The authors attribute this to over-fragmentation."
- Models: GPT-5 mini (2025) for this analysis. The main results also use DeepSeek V3.2 (2025).
- Measurement:
  - Same model? Yes, and decoding is deterministic (T=0). Budget is *not* matched: the fixed-round variants spend more structural-action calls than "w/o evolution".
  - Oracle: the RepoCraft/RPG pipeline, which is **reference-coupled and LLM-mediated**. Pass Rate is "the fraction of benchmark tasks whose adapted ground-truth tests pass on the generated repository", and the reference tests are rewritten by the *other* model (cross-model). Voting Rate is an LLM majority vote. Coverage is LLM matching against reference functional categories.
  - Tasks and runs: statsmodels/StatModeler, 234 evaluation tasks. Repo0 results are averaged over 3 runs. The paper does not state whether the budgeted variants are also averaged. There is no significance test.
  - Could the measurement explain it? Plausibly in part. A more fragmented repository makes it harder for the test-rewriting LLM and the voting LLM to locate the interface that corresponds to the reference, so over-decomposition is penalised by the oracle as well as by any real loss of correctness. Note also that the text and the figure disagree on the w/o-evolution Pass Rate (81.90 vs 79.90).
- Status: preprint (2026).


## Lines 66–94 + table rows 157, 158, 162 (Agent decomposition; Harness)


### C45 — (none)
- Draft: "Multi-agent role frameworks in the style of ChatDev and MetaGPT are the most common baselines"
- Verdict: NOT FOUND
- Evidence: No citation and no corpus count given. ChatDev/MetaGPT do appear as baselines in E2EDev, RepoGenesis (MetaGPT only), TraceDev and ChatDev/MetaGPT themselves, but "most common" needs a count over the corpus.
- Correct statement: "ChatDev- and MetaGPT-style role frameworks appear as baselines in several corpus studies (E2EDev, RepoGenesis, TraceDev)". Alternatively, give a count from corpus.csv.
- Models: n/a
- Measurement: n/a
- Status: n/a

### C46 — E2EDev2025
- Draft: "six frameworks across six model backbones"
- Verdict: VERIFIED
- Evidence: "Six frameworks (Vanilla LLM, GPT-Engineer, Self-Collaboration, MapCoder, ChatDev, and MetaGPT) are evaluated across all six LLM backbones." (App. B.1)
- Correct statement: Note that the six include the Vanilla LLM itself, so five frameworks are compared against vanilla. OpenHands and SWE-Agent were run on two backbones only.
- Models: Claude-Haiku 4.5 (2025), GPT-4o (2024), GPT-4o-mini (2024), Qwen2.5-7B/72B-Instruct (2024), Qwen2.5-Max (2025)
- Measurement: 46 projects, 244 requirements, 703 BDD tests (Behave, human-verified). Req. Acc / Test Acc averaged over 3 runs. Same budget per backbone.
- Status: preprint

### C47 — E2EDev2025
- Draft: "give no consistent gain over a vanilla LLM"
- Verdict: MISLEADING
- Evidence: "Agentic frameworks do not consistently improve the effectiveness of base LLMs." (§4.2). In Table 3 (Req. Acc.), GPT-Engineer beats Vanilla on 5/6 backbones (e.g., 53.75 vs 48.69 on Haiku 4.5), MapCoder on 4/6, and ChatDev on 2/6 (Qwen-Max 43.93 vs 43.33; Qwen-70B 43.15 vs 35.75).
- Correct statement: The paper's own phrasing holds. However, the single-agent GPT-Engineer gains on 5/6 backbones. Among the multi-agent frameworks, ChatDev beats vanilla on only 2/6 and MetaGPT on none.
- Models: as C46
- Measurement: as C46. The gains of 1–7 points sit against run-to-run SDs of up to about 2.7.
- Status: preprint

### C48 — E2EDev2025
- Draft: "MetaGPT scores near zero in almost all configurations"
- Verdict: VERIFIED
- Evidence: Table 3, MetaGPT Req. Acc. 5.39 (Haiku 4.5), 0.00 (GPT-4o), 0.00 (4o-mini), 1.65 (Qwen-Max), 0.00 (Qwen-70B), 0.00 (Qwen-7B). "causing MetaGPT to fail on nearly all test cases and requirements, even with strong LLMs"
- Models: as C46
- Measurement: as C46. Official MetaGPT run without adaptation. 44% of its failures are code inconsistency from communication breakdown (§4.3), so the score may partly reflect integration of the framework rather than the idea.
- Status: preprint

### C49 — E2EDev2025
- Draft: "ChatDev costs about ten times more"
- Verdict: CORRECTED
- Evidence: Table 3 cost ($/project), ChatDev vs Vanilla: 0.174/0.015 (Haiku), 0.1947/0.016 (4o), 0.0118/0.0010 (4o-mini), 0.0249/0.0025 (Qwen-Max), 0.0387/0.0029 (70B), 0.0075/0.0003 (7B).
- Correct statement: "ChatDev costs 10–25× more than a single-prompt LLM (10–13× on five of six backbones)". The ratio is derived by us; the paper does not state "10×".
- Models: as C46
- Measurement: Cost comes from a single run, estimated from token usage × API price.
- Status: preprint

### C50 — RepoGenesis2026
- Draft: "MetaGPT reaches Pass@1 below 3%"
- Verdict: VERIFIED
- Evidence: Table 4, MetaGPT Pass@1 Python/Java: GPT-5.1 1.46/1.14, Claude 2.85/2.10, Qwen3-30B 0.15/0.00.
- Correct statement: Add context. All open-source agents are low (best Qwen-Agent+Claude 12.65%; DeepCode ≤1.95%). MetaGPT+Claude has the highest API coverage (73.04% Py / 74.14% Java). There is no vanilla-LLM baseline.
- Models: GPT-5.1, GPT-5.1 mini (2025), Claude Sonnet 4.5 (2025), Qwen3-30B-A3B (2025)
- Measurement: RepoGenesis (Verified), 30 repos. A repo passes only if all tests pass. Averaged over 5 runs. MetaGPT is configured with n_round=5 and custom prompts.
- Status: preprint

### C51 — RoleBasedMAEval2026
- Draft: "Role-based evaluation on 12 Java repositories: at most 40% of generated classes compile."
- Verdict: MISLEADING
- Evidence: "We evaluate this approach on 12 Java repositories". Table 2 Overall Compile: LLM-Only 31%, Agentic-seq 22%, Agentic-refl 40%. Per group, Agentic-refl reaches 43% (Simple, Complex). "Agentic code generation performed better than standalone LLMs"
- Correct statement: The overall compile rate is at most 40% (43% in some groups). However, the paper's finding is that role-based agents (ChatDev 2.0, reflexive) beat a standalone GPT-5 on similarity and compile rate. It does not belong in a list of studies where role frameworks "perform poorly" relative to alternatives.
- Models: GPT-5 (2025) for generation. Judges: Claude Code/Sonnet 4.6 and ChatGPT 5.4 (2026).
- Measurement: There are no functional tests ("tests impossible to execute"). The study uses compile %, JPlag/CrystalBLEU similarity, and LLM-judged scenario intent. Runs per project are not stated.
- Status: IEEE Software 2026

### C52 — ChatDev2024
- Draft: "ChatDev reports a quality score 2.6 times that of MetaGPT, but on its own metrics of executability, placeholder-freeness, and embedding consistency"
- Verdict: VERIFIED
- Evidence: "in comparison to MetaGPT, ChatDev significantly raises the Quality from 0.1523 to 0.3953" (ratio 2.60). Completeness = "percentage of software without any 'placeholder' code snippets". Executability = "percentage of software that compiles successfully and can run directly". Consistency = "cosine distance between the semantic embeddings". Quality = their product (§4).
- Models: ChatGPT-3.5 (gpt-3.5-turbo, 2023), with GPT-4 as pairwise judge
- Measurement: SRDD has 1,200 LLM-generated task prompts. There are no functional tests. The paper also reports pairwise GPT-4/human preference.
- Status: ACL 2024

### C53 — MetaGPT2023
- Draft: "MetaGPT evaluates repository-level output on only seven tasks, using human executability ratings and no tests."
- Verdict: VERIFIED
- Evidence: "In the comparisons, we randomly select seven representative tasks for evaluation." (out of 70 SoftwareDev tasks). "(A) Executability: this metric rates code from 1 (failure/non-functional) to 4 (flawless)" via human evaluation (§4.1)
- Correct statement: Optionally add that MetaGPT reports 3.75 vs ChatDev 2.25 executability. Each framework thus claims to beat the other on its own metric.
- Models: GPT-4-era (2023). The SoftwareDev model is not stated explicitly; the appendix uses gpt-4-0613 and gpt-3.5-turbo-0613.
- Measurement: n=7 tasks, human 1–4 rating, plus human revision count. No test oracle at repo level. HumanEval/MBPP are tested but are function level.
- Status: ICLR 2024

### C54 — E2EDev2025, ChatDev2024, MetaGPT2023
- Draft: "Under the test-based oracle of E2EDev, these frameworks show no consistent advantage."
- Verdict: VERIFIED
- Evidence: Table 3. ChatDev ≤ Vanilla on 4/6 backbones and MetaGPT ≈0 on all.
- Correct statement: Qualify the model shift. The self-reports used GPT-3.5/GPT-4 (2023), while E2EDev uses GPT-4o / Qwen2.5 / Haiku 4.5 (2024–25) and current framework versions.
- Models: see C46, C52, C53
- Measurement: see C46
- Status: preprint (E2EDev)

### C55 — ECAT2026
- Draft: "removing the independent discriminator collapses the score on the largest repository from 71.2 to 12.0"
- Verdict: VERIFIED
- Evidence: Table 2 (App. A.1), Meshtastic: ECAT Agent 71.2 vs w/o Discriminator 12.0 (Align 62.0 vs 10.7). "a single agent both updates and evaluates the repository within a shared context"
- Correct statement: State that the score is an Agent-as-Judge checklist score. The ablation removes both the separate agent and the separate context.
- Models: DeepSeek-V4-Pro (2026); Qwen3.7-Plus (2026) for GUI entropy
- Measurement: 3 repos (Gallery 50K, AntennaPod 120K, Meshtastic 300K LOC). The metric is an LLM agent-as-judge feature checklist (Full/Partial/Missing) plus a node-alignment graph metric; there are no tests. Main results use 3 runs; runs for the ablation are not stated.
- Status: preprint

### C56 — ReCodeAgent2026
- Draft: "removing the validator costs 30 points of test pass rate"
- Verdict: VERIFIED
- Evidence: "removing the validator agent (NoV) leads to the highest decrease in test validation (↓30.3%)" (§4.4.1). The value is absolute points; base agents are reported as 25.3% "(↓61.2%)" against 86.5%.
- Correct statement: Note that NoV removes "dedicated test execution and diagnostic feedback". The ablation therefore removes execution feedback as well as independence.
- Models: Claude Sonnet 4.5 (2025) via Claude Code 2.1.19
- Measurement: 118 projects, 4,583 translation units, 4 PL pairs. The oracle is test pass rate on translated tests, co-translated by the system (assertion equivalence 99.3% reported). Runs are not stated.
- Status: ASE 2026

### C57 — TraceDev2026
- Draft: "TraceDev: removing the tester drops success to 13.9%."
- Verdict: VERIFIED
- Evidence: "Removing the Tester Agent results in a dramatic drop in success rate to just 13.9%" (§5.2). The full system scores 47.19% (Fig. 8).
- Correct statement: Add the baseline: 47.2% → 13.9% (ETOUR, DeepSeek-V3.2). Add the missing \cite.
- Models: DeepSeek-V3.2 (2025)
- Measurement: ETOUR (use cases, 962 test tasks). Tests are LLM-generated, and success is computed only on tests that pass an LLM (DeepSeek-V3.2) semantic check with 3-vote majority. The judge is the same model as the generator. Single configuration.
- Status: ISSTA 2026

### C58 — E2EDevBench2025
- Draft: "E2EDevBench: Developer+Tester is the best architecture."
- Verdict: CORRECTED
- Evidence: Table 3 Impl-Rate: Pro DT 53.50% > Single 42.97% > DDT 32.79%. Flash: Single 48.46% > DT 45.47% > DDT 22.63%. Mean DT 49.48% > Single 45.72%.
- Correct statement: "Developer+Tester is best on average and with Gemini-2.5-Pro, but the single agent is best with Gemini-2.5-Flash." The single agent also writes and runs its own tests, so this is the cleanest test of an independent tester. Add \cite.
- Models: Gemini-2.5-Pro, Gemini-2.5-Flash (2025)
- Measurement: 50 PyPI projects. The primary metric is LLM-judged requirement implementation (Gemini-2.5-Pro, 3 votes, unanimity), so the judge is the same model as the Pro generator. Test pass rate is supplementary. Max 200 steps, temp 0.2. Main table appears to be a single run.
- Status: preprint

### C59 — NanoHarness2026
- Draft: "task-specific subagents give the largest single gain, while general-purpose subagents hurt"
- Verdict: VERIFIED
- Evidence: "task-specific subagents bring the largest single-component gain of 5.91 percentage points" (Qwen3.7-Max). DeepSeek-V4-Pro: +4.46 (also largest). General subagents: −0.70 and −2.31 (Figs. 11–12).
- Correct statement: Optionally note that the task-specific subagents are "behavior analysis, differential testing, and submission review". They are thus verification roles, while the general subagents are SDLC roles.
- Models: Qwen3.7-Max, DeepSeek-V4-Pro (2026)
- Measurement: ProgramBench, 200 tasks, temp 0, step limit cut from 1,000 to 300. Single run per configuration, with no variance reported. The general-subagent effect (−0.7) is within plausible noise for one model.
- Status: preprint

### C60 — NL2RepoBench2025
- Draft: "finds under 1 point of difference across harnesses"
- Verdict: CORRECTED
- Evidence: "Claude-Sonnet-4.5 exhibits less than a 1% performance variation across the three agent frameworks". Table 3: Claude Code 40.23, OpenHands 39.9, Cursor 39.2.
- Correct statement: "about 1 point (39.2–40.2) across OpenHands, Claude Code and Cursor with Claude Sonnet 4.5". The max−min gap is 1.03.
- Models: Claude Sonnet 4.5 (2025), one model only
- Measurement: 104 tasks. The oracle is the upstream pytest suite (avg pass rate). No iteration limit. Single run; no variance reported.
- Status: preprint

### C61 — RepoModBench2026
- Draft: "finds 12.6 points between two harnesses with the same model"
- Verdict: VERIFIED
- Evidence: Table 3, GPT-5.2: OpenCode 43.0 vs Codex CLI 30.4 (= 12.6). Opus 4.5: Claude Code 48.2 vs OpenCode 42.0 (= 6.2).
- Correct statement: Add that the vendor harness (Codex CLI) is the worse one here, and the Opus pair differs by 6.2.
- Models: Claude Opus 4.5 (2025), GPT-5.2 (2025)
- Measurement: 21 repos, 8 languages, hidden implementation-agnostic tests (11K+). 4h timeout. Apparently a single run per agent.
- Status: preprint

### C62 — SaaSBench2026
- Draft: "finds Claude Code and Codex CLI ahead of OpenHands with the same model"
- Verdict: CORRECTED
- Evidence: Table 2 shows Claude Code > OpenHands for all 8 models (e.g., Opus 4.7 20.68 vs 18.12; avg 11.64 vs 9.26). Codex CLI appears only in Fig. 4a (two models). The text says only "Commercial IDE-based frameworks often outperform open-source agent frameworks."
- Correct statement: "Claude Code is ahead of OpenHands for all eight models (by 1.3–4.1 points). Codex CLI is reported only in a figure, and the text says vendor frameworks 'often' outperform."
- Models: GPT-5.4, Claude Opus 4.7, Gemini 3.1 Pro, Kimi K2.6, Qwen 3.6 Plus, DeepSeek V4 Pro, GLM 5.1, MiniMax M2.7 (all 2026)
- Measurement: 30 tasks, 5,370 validation nodes, partly judged by an LLM (Claude Sonnet 4.5 rubric judge). Single rollout per configuration. Same budget (500 steps, 10,800 s). Gaps of 1–4 points from a single rollout on 30 tasks may be within noise.
- Status: preprint

### C63 — CLIToolBench2026
- Draft: "CLI-Tool-Bench … find[s] the minimal mini-SWE-agent ahead of OpenHands"
- Verdict: VERIFIED
- Evidence: "models generally achieve higher scores using Mini-SWE-Agent compared to OpenHands". Table II average SM 32.50 vs 26.78. Mini-SWE is higher for 6/7 models; DeepSeek-V3.2 is tied (27.41 vs 27.44).
- Models: GPT-5.4 (2026), Claude Sonnet 4.6 (2026), DeepSeek-V3.2, Qwen-3.5-plus, GLM-5, MiniMax-M2.5, Kimi-k2.5 (2025–26)
- Measurement: 94 CLI repos. Black-box differential testing against the original tool with LLM-fuzzed tests. Single trajectory per configuration, with McNemar/bootstrap applied to model ranking. Claude Sonnet 4.6 scores anomalously low (7.2 SM on OpenHands), which suggests harness or model incompatibility.
- Status: preprint

### C64 — RepoZero2026
- Draft: "RepoZero … find[s] the minimal mini-SWE-agent ahead of OpenHands"
- Verdict: MISLEADING
- Evidence: "Mini-SWE-Agent generally outperforms OpenHands-bash … whereas OpenHands-bash represents a baseline agent configuration restricted to a rudimentary bash interface" (§6.1). Tables 2–3: e.g., Claude-4.6-Sonnet Py2JS 54.70 vs 51.46. Exception: Minimax-M2.5 C2Rust 25.39 (mini) < 28.48 (OH).
- Correct statement: "RepoZero finds mini-SWE-agent generally ahead of OpenHands-bash, a bash-only OpenHands configuration". It is not full OpenHands, and the paper attributes the gap to context engineering.
- Models: Claude-4.6-Sonnet (2026), DeepSeek V3.1–V4, GLM-5/5.1, Kimi-K2.5/2.6, Ernie-5.0, MiniMax-M2.5/2.7 (2025–26). Mini-SWE was run with only 7 of 12 models.
- Measurement: 600 samples (400 Py2JS, 200 C2Rust). The pass criterion is strict string-equal outputs on hidden black-box tests. No iteration cap. Mean ± bootstrap SD.
- Status: NeurIPS 2026 D&B

### C65 — PaperBench2025
- Draft: "its IterativeAgent helps o1 (13.2 → 24.4) but hurts Claude"
- Verdict: VERIFIED
- Evidence: Table 4 shows o1-high 13.2 ± 0.3 with BasicAgent. Table 5 shows o1-high 24.4 ± 0.7 and Claude-3.5-Sonnet 16.1 ± 0.1 (vs 21.0 ± 0.8). "the prompt tuning used for IterativeAgent is differentially suited for OpenAI o-series models"
- Correct statement: Optionally give "Claude 3.5 Sonnet 21.0 → 16.1". Note that IterativeAgent also removes the submit tool and changes prompts.
- Models: o1-high (2024), o3-mini-high (2025), Claude 3.5 Sonnet New (Oct 2024). These are older than every other harness study in this list.
- Measurement: 20 ICML papers, 8,316 rubric leaves. The grader is an LLM judge (o3-mini-high; F1 0.83 vs human on JudgeEval). 3 runs per paper, 12 h budget.
- Status: preprint

### C66 — NanoHarness2026 (cited as ProgramBench2026)
- Draft: "On ProgramBench, harness components add 6–7 points"
- Verdict: VERIFIED
- Evidence: "NanoHarness improves over mini-SWE-agent by 7.37 and 6.21 percentage points on Qwen3.7-Max and DeepSeek-V4-Pro"
- Correct statement: The numbers come from NanoHarness, so cite NanoHarness2026. ProgramBench2026 is only the benchmark. Also note that product harnesses still score higher (OpenCode 51.68 / Claude Code 52.33 vs 50.25 on Qwen3.7-Max).
- Models: Qwen3.7-Max, DeepSeek-V4-Pro (2026)
- Measurement: as C59
- Status: preprint

### C67 — NanoHarness2026
- Draft: "context compression cuts tokens by 54–77% but costs 4–5 points"
- Verdict: CORRECTED
- Evidence: "It cuts prompt tokens by 54.29% and 77.02% for the two models, yet RQ2 shows corresponding score drops of 4.86 and 3.85 percentage points"
- Correct statement: "cuts prompt tokens by 54–77% but costs 3.9–4.9 points". Compression is triggered at a 350K-token budget.
- Models: Qwen3.7-Max, DeepSeek-V4-Pro (2026)
- Measurement: as C59
- Status: preprint

### C68 — NanoHarness2026
- Draft: "only strong models benefit from complex harnesses"
- Verdict: MISLEADING
- Evidence: "on newer and more open-ended repository-level tasks such as ProgramBench and GitTaskBench, complex harnesses behave more like capability amplifiers: only sufficiently capable models can reliably exploit the additional workflow complexity". However, "On SWE-style issue repair … complex harnesses mainly compensate for weaker models".
- Correct statement: "On ProgramBench and GitTaskBench, only the strongest models gained from OpenCode over mini-SWE-agent. On SWE-bench Pro the pattern reversed."
- Models: 10 open-weight models, Qwen3-Max…Qwen3.7-Max and DeepSeek-R1…V4-Pro (2025–26)
- Measurement: RQ1 uses N=70 ProgramBench, 54 GitTaskBench and 300 SWE-bench Pro instances. Single run, temp 0.
- Status: preprint

### C69 — E2EDev2025, RepoGenesis2026, RoleBasedMAEval2026 (table line 157)
- Draft: "Role-based multi-agent (ChatDev/MetaGPT style) & U & ± & E2EDev, RepoGenesis, Role-based MA eval"
- Verdict: MISLEADING
- Evidence: E2EDev and RoleBasedMAEval both run the same model with and without the framework (same tasks, same budget), which is a controlled comparison although not a component ablation. E2EDev's direction is mostly −. RoleBasedMAEval's is + (similarity, compile 40 vs 31%). RepoGenesis has no vanilla baseline.
- Correct statement: Keep "±", but mark the evidence "C (same-model comparison)" or define U to include this case. Optionally add TraceDev (ChatDev/MetaGPT baselines 16–20%).
- Models: see C46, C50, C51
- Measurement: see C46, C50, C51
- Status: preprint / preprint / IEEE Software

### C70 — ECAT2026, ReCodeAgent2026, TraceDev2026 (table line 158)
- Draft: "Independent verifier/discriminator agent & C & + & ECAT, ReCodeAgent, TraceDev"
- Verdict: MISLEADING
- Evidence: All three have ablations (C55–C57). In ReCodeAgent and TraceDev, removing the agent also removes test execution ("without dedicated test execution and diagnostic feedback"; "Without the generate-test-refine loop"). ECAT's ablation merges contexts. E2EDevBench (C58) is the only design that keeps self-testing in the baseline, and its result is mixed.
- Correct statement: "Verifier agent with execution or judge feedback: C, +", plus a note that the ablations do not separate independence from feedback. Add E2EDevBench (±).
- Models: DeepSeek-V4-Pro; Claude Sonnet 4.5; DeepSeek-V3.2 (2025–26)
- Measurement: see C55–C57
- Status: preprint / ASE 2026 / ISSTA 2026

### C71 — NanoHarness2026 (table line 162)
- Draft: "Context compression in harness & C & -- & NanoHarness"
- Verdict: VERIFIED
- Evidence: "Context compression reduces the score by 4.86 percentage points for Qwen3.7-Max and 3.85 percentage points for DeepSeek-V4-Pro"
- Correct statement: The row rests on one preprint with two models, one benchmark (ProgramBench) and a single run. Consider adding "(1 study)".
- Models: Qwen3.7-Max, DeepSeek-V4-Pro (2026)
- Measurement: as C59
- Status: preprint


## Lines 96–115 + table rows 159–161 (Execution feedback)


### C72 — Oxidizer2025
- Draft: "In Oxidizer, rule-based feature mappings plus per-fragment differential validation reach 73% function-level I/O equivalence on 7 Go projects."
- Verdict: VERIFIED
- Evidence: "we successfully validate the I/O equivalence for an average of 73% of the translated functions (ranging from 63% to 86%)" (§1; Table 2 "Average 99 73"); "seven open-source Go projects" (§1, Table 1)
- Models: Claude 3 Sonnet (2024) only; temp 0.2
- Measurement: function counted equivalent if I/O matches on snapshots collected by running the source project's own unit tests; uncovered functions count as non-equivalent. 7 projects (314-6,642 LoC, max 369 functions), Go stdlib only; single run.
- Status: OOPSLA 2025 (PACMPL)

### C73 — Oxidizer2025
- Draft: "Without the feature mappings, translation aborts on every benchmark."
- Verdict: MISLEADING
- Evidence: "with both type-compatibility checks and feature mapping disabled ... Without them, Algorithm 2 aborts for all of our benchmarks" (§7.2; Table 2 "No Feature Map": 0% equivalent on all 7, 3-96% compiled before abort)
- Correct statement: In the ablation that disables both feature mapping and type-compatibility checks, the type-driven phase aborts on all 7 projects (0% validated equivalence; 3-96% of code translated before the abort). This ablation tests the rule-based mappings and type checks. It does not test execution feedback, so it does not support the "executable feedback" claim the bullet sits under.
- Models: Claude 3 Sonnet (2024)
- Measurement: as C72; single run per configuration.
- Status: OOPSLA 2025

### C74 — RepoTransBench2024
- Draft: "Translation-only baselines achieve near-zero success, while agents with execution loops achieve up to 33%"
- Verdict: VERIFIED
- Evidence: "with Claude, RepoTransAgent achieves 32.8% SR compared to 0.0% for TranslationOnly and 11.3% for ErrorFeedback" (§VI-A, Table IV; TranslationOnly 0.0-0.2% across 8 models)
- Models: Claude-Sonnet-4, GPT-4.1, o3-mini, Gemini-2.5-Flash-Lite, Qwen3-235B(+think), DeepSeek-Chat/Reasoner (all 2025; the arXiv v2 text was revised after the 2024 v1)
- Measurement: SR = all tests in a task pass, using LLM-multi-agent-generated test suites (61% line coverage); 1,897 repos, 13 language pairs; runs and agent step budget not stated. A non-agent ErrorFeedback condition also scores 0.9-15.6%. Agent vs translation-only uses the same backbone, but compute is not matched. The best-model SR is 32.8% for both Claude-Sonnet-4 and GPT-4.1. For DeepSeek-R the agent reaches only 1.2%.
- Status: corpus.csv venue = preprint, but venue_record/DOI = IEEE TSE (10.1109/tse.2025.3645056). Check this and update the venue.

### C75 — AutoP2C2026
- Draft: "Without its feedback loop, AutoP2C produces no runnable repository at all."
- Verdict: VERIFIED (scope caveat)
- Evidence: "Without the iterative feedback-driven implementation, AutoP2C relies entirely on single-pass generation, resulting in completely non-executable implementations across all test cases" (§4.5, Table 3)
- Models: GPT-4o (decomposition), o1-mini (generation), o1 (validation), o3-mini (refinement) (2024-25); temp 0
- Measurement: the ablation covers 4 of the 8 Paper2Repo papers (Table 3). "Runnable" means the code executes and reproduces the paper metric. Single run. The benchmark is self-built. The removed stage is a multi-model refinement stage that adds extra LLM calls, so compute is not matched.
- Status: ICASSP 2026. The available full text is the arXiv version ("Preprint, Under Review"), so its numbers may differ from the ICASSP camera-ready.

### C76 — CRUSTBench2025
- Draft: "Test repair more than doubles CRUST-Bench success (o3: 19 → 48%)."
- Verdict: VERIFIED (with nuance)
- Evidence: Table 4 "OpenAI o3 35 19 68 31 63 48" (pass@1 test 19, +compiler repair 31, +test repair 48)
- Models: o3, Claude Opus 4, o1, Claude 3.7/3.5, GPT-4o, o1-mini, Gemini 1.5 Pro, open models (2024-25)
- Measurement: 100 C repos with hand-written Rust interfaces and tests; greedy decoding, single run; 3 repair rounds. The 19→48 gain mixes compiler and test feedback: 19→31 comes from compiler repair, 31→48 from adding failing tests. Test repair lowers build success (68→63). The paper's text contradicts its own table. The text says "best-performing model, o1 ... only 15%" while Table 4 gives o3 19%. The text also says test repair adds "between 0% and 9%" over compiler repair, while the table gives o3 +17. The repair feedback comes from the benchmark tests, which are also the scoring oracle, and no held-out split is reported.
- Status: COLM 2025

### C77 — RepoZero2026
- Draft: "RepoZero's code--test co-evolution raises OpenHands from 26 to 43%."
- Verdict: VERIFIED (underspecified)
- Evidence: Table 4 "Retry-0 ... 26.08±2.26 ... Retry-2 ... 42.88±2.93" (OpenHands-bash)
- Correct statement (optional): "with DeepSeek V3.1 on Py2JS, two code-test-refine retries raise OpenHands-bash from 26 to 43% (Mini-SWE-Agent: 44 to 52%)."
- Models: DeepSeek V3.1 only (2025)
- Measurement: Py2JS subset only. Hidden black-box I/O tests generated by an LLM and filtered for determinism. The agent generates its own tests from 4 visible white-box cases. Retries add compute, so compute is not matched. The ± values suggest resampling, but the number of runs is not stated.
- Status: NeurIPS 2026 D&B

### C78 — TDDev2026
- Draft: "Agentic TDD in TDDev raises accuracy from 67.8 to 91.5%."
- Verdict: VERIFIED (underspecified)
- Evidence: Table 6 "Sonnet Vanilla — 67.8 [58.3, 77.0] ... +TDD-Agent Sonnet 91.5 [86.1, 96.5] 23.7 ***"
- Models: Claude Sonnet 4.6 backbone (2026); MiniMax M3 and Qwen3.5-397B in other cells
- Measurement: 20 WebGen-Bench apps; one oracle evaluation per app. The oracle is an LLM browser tester (Claude Sonnet 4.6), the same model as the developer in this cell. In the tester fixture validation, its accuracy is 75% on correct apps. The human-authored WebGen-Bench tests were "converted ... into the acceptance-test format ... supplied to the TDD loop", so the loop sees the oracle's tests. Wilcoxon test with bootstrap CI.
- Status: ASE 2026

### C79 — EnvGraph2026
- Draft: "EnvGraph, which attributes failures to their environment or reference source, gains 10--13 points on NL2Repo-Bench."
- Verdict: CORRECTED
- Evidence: Table 3 (NL2Repo) Overall vs Direct: GPT-5 "33.2(+11.5)", DeepSeek-V3.2 "28.9(+3.9)", Gemini-3-Pro "44.02(+5.72)"; the +13.11 figure is RAL-Bench GPT-5 (Table 2)
- Correct statement: On NL2Repo-Bench, EnvGraph gains 3.9-11.5 points over direct generation across three backbones, and only 0.3-3.2 points over the strongest baseline (e.g. 28.9 vs Repo2Run 28.6; 44.0 vs 43.0). It attributes failures to external dependencies, internal references, or residual logic.
- Models: GPT-5 (2025), DeepSeek-V3.2 (2025), Gemini-3-Pro-Preview (2025)
- Measurement: NL2Repo-Bench 104 tasks, upstream pytest; greedy, single run; max 4 iterations for EnvGraph and the iterative baselines, but the Direct baseline gets no iterations, so compute is not matched.
- Status: preprint

### C80 — GenerativeCompilation2026
- Draft: "Compiler feedback during decoding reduces compile errors from 66% to 13%."
- Verdict: MISLEADING
- Evidence: "Post-generation compiler feedback (PC) reduces the average compiler error rate from 65.9% to 20.7% ... adding on-the-fly feedback with GC reduces the error rate further to 13.1%" (§7.2, Table 1)
- Correct statement: Post-generation compiler feedback cuts the average compile-error rate from 65.9% to 20.7%. In-decoding feedback lowers it further to 13.1% (better in 13 of 14 configurations, significant in 9). Most of the 66→13 drop comes from ordinary post-hoc feedback.
- Models: Claude Opus 4.8, GPT 5.3 Codex, Gemini 3.5 Flash, Kimi K2.7, GLM 5.2, Qwen3.5 397B/9B (2026)
- Measurement: 20 CRUST-Bench instances (Translation) plus a self-built UpdatedAPI set; 2 samples per task at temp 0.6; budget n=15/20 total with k=10 restarts, the same total budget for PC and GC. Error rate = fraction of outputs with ≥1 rustc error.
- Status: preprint

### C81 — Commit02024
- Draft: "Lint feedback hurts open models in Commit0."
- Verdict: VERIFIED
- Evidence: "progressing from Stage 1 to Stage 2 results in a decline in performance with the open-weights models" (§5; Table 1: DeepSeek-V2.5 16.55→11.61, Llama-3.1-70B 7.10→1.83, 405B 8.08→1.76; Codestral flat 6.34→6.34; Claude 3.5 Sonnet 17.80→18.79)
- Models: Claude 3.5 Sonnet, o1-preview, GPT-4o-mini, DeepSeek-V2.5, Llama-3.1 8B/70B/405B, Codestral (2024)
- Measurement: Commit0 lite (16 libraries); unit-test pass rate; single run (none reported). Stage 2 is ruff lint/type-check revision applied on top of stage 1. Evidence for "untrusted feedback" is the authors' qualitative reading of one case.
- Status: preprint (corpus.csv)

### C82 — TDDev2026 (uncited in sentence)
- Draft: "Qwen's self-written tests produce no benefit from TDD until the tester is replaced."
- Verdict: VERIFIED (citation missing)
- Evidence: "TDD therefore does not consistently improve Qwen3.5 when the same backbone must both implement the application and interpret test failures"; Table 6: Qwen3.5 fb +4.8 (n.s.), −4.4, −0.8; Sonnet fb +9.4†, +6.8†, +9.4*
- Correct statement: Add \cite{TDDev2026}. Say "self-judged test feedback" rather than "self-written tests": the oracle tests are supplied, and Qwen acts as the tester that interprets them. Also note that after the tester is replaced, two of the three gains are only suggestive (p=.056, .092).
- Models: Qwen3.5-397B-A17B, Claude Sonnet 4.6 (2026)
- Measurement: as C78 (20 apps, single evaluation, LLM oracle).
- Status: ASE 2026

### C83 — DynamicEval2026
- Draft: "In Dynamic Eval, three quarters of the gain arrives in the first three rounds, and the net gain turns negative by round five."
- Verdict: NO FULL TEXT
- Evidence: Abstract (IEEE export, slr/data/manual/ieee_F1.csv): "roughly three-quarters of the gains emerged within the first three rounds, and net feedback gain turned negative by Round 5"
- Correct statement: The wording matches the abstract. The abstract does not say whether the "net feedback gain" turns negative per round (marginal) or cumulatively, and the draft's "the net gain turns negative" reads as cumulative. Write "the per-round net gain" only after checking the full text, or hedge.
- Models: not stated in abstract (unknown)
- Measurement: DevEval Python tasks; multi-round repair with unit-test feedback. Whether the feedback tests are the evaluation tests is unknown; n and runs unknown.
- Status: IEEE AITest 2026

### C84 — (attributed in draft to DynamicEval2026; actually TDDev2025, arXiv:2509.25297)
- Draft: "One to two TDD rounds lower accuracy before three rounds raise it."
- Verdict: CORRECTED (misattribution)
- Evidence: TDDev2025 Table 9: "Test Acc. 58.3 25.3 25.2 70.2" (no feedback / 1 / 2 / 3 rounds); "introducing 1-2 rounds of feedback does not immediately improve ... accuracy drops to 25.3%" (§5.2)
- Correct statement: In an earlier TDDev preprint~\cite{TDDev2025} (Claude-4-Sonnet), 1-2 feedback rounds drop WebGen-Bench test accuracy from 58.3% to about 25%, and three rounds raise it to 70.2%. This is a single run on a small task set. The 2026 TDDev (ASE) does not report this dip.
- Models: Claude-4-Sonnet (2025)
- Measurement: Req-to-App-MM (WebGen-Bench augmented, 101 tasks; RQ3 subset size not stated); LLM browser testing agent (Claude-4-Sonnet) as the oracle; single run. A 33-point drop followed by a 45-point rise suggests high variance.
- Status: preprint

### C85 — NL2RepoBench2025 (uncited here), CLIToolBench2026
- Draft: "Several models stop early without building or testing; this happens in NL2Repo-Bench and CLI-Tool-Bench."
- Verdict: MISLEADING
- Evidence: NL2Repo: "Qwen3-Thinking terminates early in 49.0% of tasks"; GPT-5 "frequently halts prematurely and awaits user confirmation, with 13.4% of tasks"; "We hypothesize ... 'hallucination of verification' ... bypassing the need for actual execution and testing" (§4.3.3). CLI-Tool-Bench: "Claude-Sonnet-4.6 ... frequently concludes the generation trajectory immediately after writing the initial code ... without invoking standard compilation checks like go build" (§IV)
- Correct statement: In NL2Repo-Bench, some models end early: Qwen3-Thinking in 49% of tasks, and GPT-5 waits for user input. "Early" means fewer than 100 turns, and the authors only hypothesise that the model skipped testing. In CLI-Tool-Bench, the log analysis shows that one model, Claude Sonnet 4.6, often submits without compiling. Add \cite{NL2RepoBench2025}.
- Models: NL2Repo: Qwen3-Thinking/Instruct, GPT-5, Claude Sonnet 4/4.5, DeepSeek V3.1/3.2, GLM-4.6, Kimi-K2 (2025). CLI: GPT-5.4, Claude Sonnet 4.6, DeepSeek-V3.2, Qwen-3.5-plus, GLM-5, MiniMax-M2.5, Kimi-k2.5 (2026)
- Measurement: NL2Repo 104 tasks, upstream pytest, behaviour counted from tool and turn logs. CLI-Tool-Bench 94 tasks, single generation run, behaviour from qualitative log analysis.
- Status: both preprint

### C86 — VibeCodeBench2026
- Draft: "Vibe Code Bench finds that self-testing correlates with accuracy (r=0.72) far more than edit volume does (r=0.09)."
- Verdict: VERIFIED
- Evidence: "Across the 16 evaluated models, browser tool calls per application show a positive correlation with accuracy (Pearson r=0.72)"; "Edit calls correlate weakly with accuracy (r=0.09)" (§5.1)
- Models: 16 models incl. GPT-5.3-Codex, Claude Opus 4.6, GPT-5.2(-Codex), GLM-5, Grok 4.1, DeepSeek V3.2 (2025-26)
- Measurement: model-level correlation (n=16 points), observational, not an intervention. "Self-testing" = browser tool calls. The oracle is an autonomous browser agent with LLM-as-judge substeps over 100 apps / 964 workflows.
- Status: preprint

### C87 — ChessEnginesPL2026 (uncited here)
- Draft: "The chess study's self-Elo scripts illustrate this"
- Verdict: VERIFIED (citation missing)
- Evidence: "The other eleven of the 15 overestimate by 200 Elo to 1100 Elo" (§6.1); "∆ ... runs to −1078 for chess-assembly-codex" (Table 6)
- Correct statement: Add \cite{ChessEnginesPL2026}. Four of 15 self-claims fall within 150 Elo; two of those triangulated across UCI_Elo levels with at least 100 games each. Better self-evaluation protocols therefore fix part of the gap.
- Models: Claude Code (Opus 4.6/4.7), Codex (gpt-5-codex, gpt-5.3-codex, gpt-5.4) (2025-26)
- Measurement: external Elo from a gauntlet against rated engines plus a Bradley-Terry fit; 15 engines with self-claims, out of 34.
- Status: preprint

### C88 — E2EDevBench2025
- Draft: "E2EDevBench's finding that insufficient self-verification is a leading failure cause."
- Verdict: MISLEADING
- Evidence: Abstract: "the primary reason for failure is not incorrect code implementation, but rather the omission of requirements and inadequate self-verification"; but Table 5: "3. Task Verification (5.7%) ... Inadequate Verification (5.7%)" vs "Requirement Omission (27.9%)", "Dependent Feature Failure (21.0%)"
- Correct statement: E2EDevBench's abstract names inadequate self-verification as a primary failure reason. Its own root-cause taxonomy, however, attributes only 5.7% of failures to inadequate verification, against 55.8% to task planning (27.9% requirement omission).
- Models: Gemini-2.5-Pro, Gemini-2.5-Flash (2025)
- Measurement: 50 PyPI projects; 1,000 sampled unimplemented requirements from Pro runs, labelled by LLM pre-annotation followed by human refinement; temp 0.2, 200-step cap.
- Status: preprint

### C89 — table row "Execution/test feedback loops | C | + | CRUST-Bench, RepoZero, AutoP2C, TDDev, EnvGraph"
- Draft: Evidence C, direction +
- Verdict: VERIFIED (with qualification)
- Evidence: same-backbone ablations exist in all five (C75-C79).
- Correct statement: Keep "C, +". Add a footnote: no study matches compute between the feedback and no-feedback arms. In CRUST-Bench, TDDev2026 and (likely) Commit0, the feedback uses the oracle's own tests. AutoP2C's ablation covers 4 papers, and EnvGraph's margin over the execution-based baseline Repo2Run is ≤3 points.
- Models/Status: see C75-C79

### C90 — table row "Lint-only / untrusted feedback | C | -- | Commit0, TDDev (weak tester)"
- Draft: Evidence C, direction --
- Verdict: MISLEADING
- Evidence: Commit0 Table 1 (stage 2 drops for open models; Claude 3.5 +1.0, Codestral flat). TDDev2026 Table 6 (Qwen fb: +4.8 n.s., −4.4, −0.8; none significant)
- Correct statement: Use direction "±/--". The lint harm is confined to weaker 2024 open models. In TDDev2026, the weak tester removes the gain without significantly harming the result.
- Status: Commit0 preprint; TDDev ASE 2026

### C91 — table row "Many feedback rounds | C | ± | Dynamic Eval, TDDev"
- Draft: Evidence C, direction ±
- Verdict: MISLEADING (attribution)
- Evidence: DynamicEval NO FULL TEXT (abstract only). The non-monotone round curve comes from TDDev2025 Table 9, not TDDev2026. TDDev2026 Table 8 reports loop-internal tester accuracy across k, not oracle accuracy, and the MiniMax curve peaks at k=3.
- Correct statement: Cite TDDev2025 and TDDev2026 explicitly. Mark DynamicEval as abstract-only. "C" is acceptable because rounds were varied with the model held fixed.
- Status: AITest 2026 (no FT); TDDev2025 preprint; TDDev2026 ASE 2026


## Lines 117–144 + table rows 163–164 (State, environment, training)


### C92 — RepoZero2026 (no \cite in draft)
- Draft: "Long-horizon runs lose their early constraints. RepoZero calls this ``contextual drift''."
- Verdict: VERIFIED
- Evidence: "agents frequently exhibit \"contextual drift\" during extended reasoning sequences, losing track of critical requirements as the trajectory length increases." (Sec. failure analysis, insight "Long-term Memory and Context Retention")
- Models: open-source models in OpenHands-bash (Kimi-K2.5/2.6, GLM-5/5.1, DeepSeek-V3.1/V3.2/V4, Ernie-5.0; 2025-26)
- Measurement: qualitative observation from failure breakdown (Fig. 4 right); not quantified; task is repository translation (Py2JS, C2Rust), not NL-to-repo.
- Status: NeurIPS 2026 D&B

### C93 — LiveCoder2026
- Draft: "cross-attempt success and failure memory: LiveCoder"
- Verdict: VERIFIED
- Evidence: "This state includes success knowledge ... failure knowledge ... and a historical-best repository" (Abstract)
- Models: GPT-5 (2025), DeepSeek-V3-0324 (2025), Claude-Sonnet-4.5 (2025), Gemini-3-Pro-Preview (2025)
- Measurement: RAL-Bench (38 tasks) + NL2Repo-Bench (104 tasks); functional test pass rate; max 4 attempts; no repeated runs/variance reported. Validity concern: the per-attempt functional score that drives the memory and historical-best selection is the benchmark's functional test pass rate ("This metric also determines the preservation of the historical-best repository", Metrics) -> evaluation oracle used as feedback.
- Status: preprint

### C94 — CodeMEM2026
- Draft: "AST-guided session memory in place of transcripts: CodeMEM"
- Verdict: VERIFIED
- Evidence: "Code Context Memory ... through AST-guided LLM operations, along with the Code Session Memory that constructs a code-centric representation of interaction history" (Abstract); baseline "Full-Context (FC), which uses all conversation history" (Sec. 4.2)
- Models: DeepSeek-V3.2 (2025), greedy decoding
- Measurement: CodeIF-Bench L-2 (40 dialogues, 360 instructions) and CoderEval (230 Python tasks, multi-round); test-based IA/CA/IFR/Pass@1; single greedy run. Scope: iterative function-level generation in repository context, not repository construction. Also has a context memory, not only session memory.
- Status: preprint

### C95 — DeepRepro2026
- Draft: "repository memory with re-planning from the current state: DeepRepro"
- Verdict: VERIFIED
- Evidence: "a memory module compresses completed artifacts into structured repository memory"; "a subplanning module dynamically selects ... conditioned on the current implementation state" (Sec. 1/2)
- Models: GPT-5.4 (2026), DeepSeek-V4-Flash (2026) for execution ablation
- Measurement: PaperBench Code-Dev (5-paper subset + 20-paper full set); LLM judge GPT-4.1-mini (o3-mini for human comparison).
- Status: CIKM 2026

### C96 — EvoGit2025
- Draft: "Git lineage as the coordination medium: EvoGit"
- Verdict: VERIFIED
- Evidence: "all coordination emerges through a Git-based phylogenetic graph that tracks the full version lineage" (Abstract)
- Models: not named in main text
- Measurement: 2 case-study tasks (website, bin-packing meta-solver), 16 agents x 120 iterations, sparse human feedback; no baseline, no quantitative oracle. Note EvoGit explicitly has no "shared memory".
- Status: preprint

### C97 — LiveCoder2026, CodeMEM2026, DeepRepro2026, EvoGit2025
- Draft: "None of these has been compared against the others under a fixed budget."
- Verdict: VERIFIED
- Evidence: grep of each full text for the other three names returns zero hits. LiveCoder compares to Direct/Self-Reflection/SE-Agent/AlphaEvolve/CSE/Live-SWE-Agent; CodeMEM to FC/MemGPT/Mem0/A-Mem; DeepRepro to PaperBench baselines; EvoGit has no baseline.
- Models: n/a
- Measurement: absence-of-evidence; the four also use disjoint benchmarks (RAL/NL2Repo; CodeIF/CoderEval; PaperBench; case studies).
- Status: mixed (CIKM 2026 + 3 preprints)

### C98 — EnvGraph (arxiv 2604.03622; no \cite in draft)
- Draft: "31--69\% of failed direct generations on NL2Repo-Bench are environment-related (EnvGraph)."
- Verdict: VERIFIED (with caveat)
- Evidence: "environment-related failures account for 34.7%, 68.9%, and 30.9% of failed direct generations for GPT-5, DeepSeek-V3, and Gemini-3-Pro-Preview" (Sec. motivating study, Fig. 2)
- Correct statement: 31-69% (three models) ... note EnvGraph's "environment-related" includes repository-internal reference resolution failures, which it says are the more frequent component ("but also, and more often, from repository-internal reference resolution failures").
- Models: GPT-5 (2025), DeepSeek-V3 (2024/25), Gemini-3-Pro-Preview (2025)
- Measurement: manual annotation of all failed direct generations on NL2Repo-Bench (104 tasks); annotator count/agreement not reported; single run.
- Status: preprint

### C99 — SaaSBench (arxiv 2605.17526; no \cite in draft)
- Draft: "In 63.5\% of SaaSBench capability units, the stack never runs stably."
- Verdict: VERIFIED
- Evidence: "Overall, in 63.5% of the capability units, the generated stack never runs stably." (Sec. 5.4); T5 type "accounts for 63.5% of all capability units" (App. B.7)
- Models: 480 capability units "from two agents" (frameworks OpenHands/Claude Code; backbones incl. GPT-5.4, Gemini 3.1 Pro, Claude Opus 4.7, Kimi K2.6, Qwen 3.6 Plus, DeepSeek V4 Pro, GLM 5.1; 2026)
- Measurement: trajectory taxonomy (T1-T5) from execution traces + node-level failure profiles; classification procedure (manual vs automatic) not specified; T5 also includes "premature claims of success".
- Status: preprint

### C100 — ParEvalRepo2025
- Draft: "ParEval-Repo: build-system generation is the main bottleneck."
- Verdict: CORRECTED
- Evidence: "generating working build systems is a major obstacle to successful full-repository translation" (Conclusion); "difficulty with generating functional build systems and cross-file dependencies pose challenges" (Abstract); "Overall score is consistently significantly lower than Code-only score" (Sec. 8)
- Correct statement: ParEval-Repo: generating working build systems is a major obstacle (alongside cross-file dependencies) in LLM translation of HPC repositories.
- Models: GPT-4o mini (2024), o4-mini (2025), Gemini 1.5 Flash (2024), Llama 3.3 70B (2024), QwQ-32B (2025)
- Measurement: build + pass@1 on small HPC mini-apps; repository translation (CUDA->OpenMP/Kokkos etc.), not NL-to-repo; several configurations incomplete due to budget.
- Status: ICPP 2025

### C101 — HiRAS2026
- Draft: "HiRAS: most paper-to-repository failures occur at execution rather than generation."
- Verdict: VERIFIED
- Evidence: "failures predominantly arise during execution rather than code generation"; "only 3 out of 110 runs fail at the structured code generation stage" (Sec. 6.2)
- Models: Qwen3-Coder-480B (2025), DeepSeek-v3.1-Terminus (2025)
- Measurement: manual analysis of representative cases + score drop ~45% (CodeDev) -> ~20% (full PaperBench), LLM judge (o3-mini-high / GPT-4o-mini). Caveat: the dominant execution errors are "incorrect inter-file dependencies ... import failures", i.e., code defects surfacing at execution, not only environment issues.
- Status: preprint

### C102 — ABCBench2026
- Draft: "Environment setup ... should be measured separately, as ABC-Bench already does."
- Verdict: VERIFIED
- Evidence: "decomposing the workflow into two distinct stages: Environment Build (S1) ... and Functional Execution (S2)" (Sec. 4, "Environment Configuration as the Primary Bottleneck")
- Models: Qwen3 family, Nex-N1, DeepSeek-V3.2, GPT-5, Claude Sonnet 4.5 (2025)
- Measurement: 224 backend tasks (92 with env config), external E2E API tests; S1/S2 split on the 92 env tasks; pass@1 with +-std reported. Tasks are masked existing repos, not from-scratch.
- Status: preprint

### C103 — DeNovoSWE2026, BeyondSWE2026
- Draft: "DeNovoSWE's 4,818 documentation-to-repository instances lift Qwen3-30B-A3B from 5.8 to 47.2\% on Doc2Repo."
- Verdict: VERIFIED
- Evidence: "DeNovoSWE comprises 4,818 high-quality instances"; "raising its score on the challenging BeyondSWE-Doc2Repo benchmark from 5.8% to 47.2%" (Abstract). Doc2Repo is a BeyondSWE task ("Document-to-repository generation (Doc2Repo)", BeyondSWE Sec. 3).
- Models: Qwen3-30B-A3B-Instruct (2025) student; SFT on ~11k trajectories distilled from DeepSeek-V4-Pro (2026) teacher; also Qwen3.5-35B-A3B 43.8->50.0.
- Measurement: Doc2Repo = 50 tasks, Pass Rate = average % of adapted original-repo tests passed (reference-coupled; tests "validated ... against the reference implementation"); mean of 3 trials. NL2Repo gain 4.3->23.0. Caveats: base is a non-agentic Instruct model (issue-SWE SFT alone gives 29.2); same author group as BeyondSWE (Chen, Zhao, Meng, Jia; Renmin/AweAI); no explicit train/test repo-overlap analysis found.
- Status: preprint (both)

### C104 — MindForge2026
- Draft: "MindForge's source-free environments raise ProgramBench pass rate from 38 to 50\%, and transfer to SWE-bench and NL2Repo-Bench."
- Verdict: VERIFIED
- Evidence: "increasing the average test pass rate from 37.98% to 49.51%" (Sec. 4.1); "10.70/4.56 on NL2Repo-Bench (with-/without tests), 5.04 on SWE-bench Verified, 5.93 on SWE-bench Pro, 5.22 on SWE-bench Multilingual" (Abstract)
- Models: Qwen3.6-27B (2026) student; GLM-5.2 (2026) teacher; 1,001 trajectories
- Measurement: ProgramBench 200 tasks, hidden tests vs. reference executable (reference-coupled behavioural oracle); single run on ProgramBench/NL2Repo/DeepSWE/RepoZero, 3 runs elsewhere; repo-overlap check reported (none with NL2Repo).
- Status: preprint

### C105 — RepoGenesis2026, WebGenBench2025, JamBenchJamSet2026
- Draft: "RepoGenesis, WebGen-Bench, JAMER ... fine-tune on their own data."
- Verdict: VERIFIED
- Evidence: RepoGenesis "fine-tuned Qwen3-8B on this distilled dataset" (Sec. 5.2); WebGen-Bench "fine-tune Qwen2.5-Coder-Instruct models of sizes 7B, 14B, and 32B" on WebGen-Instruct (Sec. 1); JAMER "Qwen3.5-27B-SFT ... LoRA-fine-tuned" on JamSet.
- Models: Qwen3-8B (2025); Qwen2.5-Coder-7/14/32B (2024) with DeepSeek-V3 trajectories; Qwen3.5-27B (2026)
- Measurement: RepoGenesis test Pass@1 on Verified split (GenesisAgent-8B ~ GPT-5 mini); WebGen-Bench accuracy via WebVoyager UI agent (LLM-agent oracle), 38.2% for 32B; JAMER deterministic Godot compile/SCS/BAS pipeline.
- Status: preprint (all)

### C106 — RepoST2025
- Draft: "... and RepoST fine-tune on their own data." (under "Recent work turns construction tasks into training data")
- Verdict: MISLEADING
- Evidence: "Unlike existing works that aim to build entire repositories for execution ... we provide execution feedback with sandbox testing, which isolates a given target function" (Abstract)
- Correct statement: RepoST trains on function-level generation within existing repositories (7,415 functions), not repository construction; gains are +5.5 Pass@1 HumanEval, +3.5 RepoEval.
- Models: Qwen2.5-Coder family (2024)
- Measurement: function-level tests in sandbox scripts.
- Status: preprint

### C107 — WebGenR12026
- Draft: "WebGen-R1 applies reinforcement learning with execution-grounded rewards."
- Verdict: CORRECTED
- Evidence: "cascaded multimodal reward that ... couples structural guarantees with execution-grounded functional feedback and vision-based aesthetic supervision" (Abstract); "sfunc = 1 if Nerr = 0" (Sec. 3.3); "We employ a VLM as a proxy for human preference judgment" (Sec. 3.3)
- Correct statement: WebGen-R1 applies GRPO with a cascaded reward: build/static gates, a binary no-runtime/console-error score, and a VLM-judge aesthetic score.
- Models: Qwen2.5-Coder-7B-Instruct (2024) base
- Measurement: WebGen-Bench (101 tasks) FSR via predefined interactive checks + VLM-scored AAS + render ratio.
- Status: preprint

### C108 — DeNovoSWE2026, MindForge2026, WebGenBench2025, WebGenR12026 (line 144)
- Draft: "a reward derived from reference-coupled tests or from an LLM judge teaches whatever that oracle rewards."
- Verdict: VERIFIED (as applicable to the cited training studies)
- Evidence: Doc2Repo tests validated "against the reference implementation" (BeyondSWE Sec. 3.3); ProgramBench "execute-only binary serving as the behavioral oracle" (MindForge Sec. 3.3); WebGen-Bench "WebVoyager UI agent" + GPT-4o aesthetics; WebGen-R1 reward includes VLM judge.
- Models: see C103-C107
- Measurement: all headline training gains (DeNovoSWE, MindForge) are measured with reference-coupled test oracles; WebGen-Bench/WebGen-R1 with LLM/VLM-agent oracles. None reports an independent oracle check. Note: the sentence is a conjecture, not a finding of any cited study.
- Status: preprints

### C109 — LiveCoder2026, CodeMEM2026 (table row 163)
- Draft: "Persistent cross-attempt/session state & C & + & LiveCoder, CodeMEM"
- Verdict: VERIFIED (with caveat)
- Evidence: LiveCoder Table 4: removing any component lowers Func. for all 4 models ("removing any one consistently reduces functional performance", RQ3); CodeMEM ablation "w/o CtxMem ↓3.6, w/o CtxAST ↓4.4, w/o SessAST ↓1.9" (Table 1)
- Models: see C93, C94
- Measurement: LiveCoder ablation on RAL-Bench at attempt 2 only, single run, non-functional score sometimes rises (+1.65,+2.55,+6.23); oracle leakage concern (C93); on NL2Repo LiveCoder is -3.1% vs best baseline for one model (Table 2 "Imp."). CodeMEM is not repository construction (C94).
- Status: preprints

### C110 — DeNovoSWE2026, MindForge2026, SWEPlayground2025 (table row 164)
- Draft: "Training on construction trajectories & C & + & DeNovoSWE, MindForge, SWE-Playground"
- Verdict: MISLEADING (for SWE-Playground)
- Evidence: SWE-Playground Table 1 Commit-0 resolved rate "1.82 -> 2.95" (7B), "2.31 -> 3.64" (32B); main gains on SWE-bench Verified (1.8->17.0; 7.0->31.2) and SWT-Bench.
- Correct statement: DeNovoSWE and MindForge show large base-vs-SFT gains on repository construction (reference-coupled tests, distilled from 2026 frontier teachers); SWE-Playground's gain on its only construction-like benchmark (Commit-0 Lite) is ~+1 pp.
- Models: Qwen2.5-Coder-7B/32B (2024) for SWE-Playground
- Measurement: base vs fine-tuned same backbone (controlled for data, not for teacher distillation); no comparison vs. equal-size non-construction SFT except Scale-SWE-Agent in DeNovoSWE.
- Status: preprints

# Dedicated analysis (a): "Structure is not uniformly beneficial" (lines 58–64, table row 156)

Per-study measurement details are in C42 (E2EDevBench), C43 (Athena), C44 (Repo0).

## Conclusion on (a)
- None of the three cases shows that "structure" hurts in general.
  - E2EDevBench is the only controlled comparison: same model and base agent, two models, 3 runs, about 20 pp. It shows that one particular *sequential prose design hand-off* hurt Gemini-2.5 agents, under an LLM-judged oracle with moderate human agreement. The mechanism is the authors' hypothesis.
  - Athena is a 12-person HCI study whose bug gap is confounded with 3x larger output. It says nothing about validated vs unvalidated IRs.
  - Repo0's case is one repository and one model, with a reference-coupled LLM-mediated oracle. Even there, one round of unconstrained restructuring helped.
- The draft's reading ("a plan helps when it is checked ... and can hurt when it is merely handed over as prose") is a plausible *hypothesis* that fits E2EDevBench and Repo0. No study tests it directly: none compares checked and unchecked versions of the same artefact. Athena does not bear on it.
- Counter-counter-evidence in the corpus: E2EDev (arxiv:2510.14509, human-coded, GPT-4o/Qwen) finds that "multi-agent frameworks significantly reduce requirement misalignment" via component analysis. Structured hand-offs are therefore not uniformly harmful either.
- Table row line 156 ("Plan handed over as prose | C | --") overstates the evidence. Only E2EDevBench is controlled, and Athena's IRs are structured (storyboard, data model and GUI skeletons), not prose. Suggest "U/C(1) | -- | E2EDevBench (DDT)" and drop Athena, or move Athena to a "±, confounded" row.
- Defensible rewording: "Structure is not automatically beneficial. In one controlled preprint (E2EDevBench; Gemini-2.5, 50 projects, LLM-judged requirement fulfilment), inserting a Designer agent whose prose design document was passed sequentially to the Developer gave the lowest requirement-fulfilment rate (22.6-32.8% vs 45.5-53.5% without it). The authors hypothesise that the Developer over-trusts the design. In Repo0 (one repository, GPT-5 mini), unconstrained LLM restructuring degraded results after more than one round, while metric-guided restructuring improved them. Athena's IR-scaffolded apps had more bugs, but they were also about three times larger, so the comparison does not isolate the IR. Whether verification of the plan is what separates the helpful from the harmful cases has not been tested directly."



# Dedicated analysis (b): "Context is not the main bottleneck / the dominant problem is specification understanding" (lines 27–28)

Per-study details are in C18 (MRG-Bench) and C19 (hallucination taxonomy).

## Newer evidence in the corpus (2025-26 models)
For "requirement/specification understanding dominates":
- E2EDevBench (arxiv:2511.04064; Gemini-2.5-Pro, 2025; preprint) codes 1,000 unimplemented requirements. Its root-cause taxonomy (Table 5) is Task Planning 55.8% (Requirement Omission 27.9%, Requirement Misinterpretation 22.2%, Architectural Design Flaw 5.6%), Task Execution 38.6% (Dependent Feature Failure 21.0%, Superficial Implementation 12.5%, Context & Task Forgetting 1.9%) and Task Verification 5.7%. The method is "LLM pre-annotation, then human refine". The authors conclude: "The core bottleneck is comprehension". Caveat: omission is partly attention/planning rather than "understanding", and the requirement verdicts come from the LLM judge.
- ProjDevBench (arxiv:2602.01655; GPT-5, Claude Sonnet 4.5, Gemini 3 Pro; preprint) gives "Specification misalignment" as its first failure mode. This is a qualitative grouping of online-judge statuses (Wrong Answer 41.86%), with no coded distribution.
- E2EDev (arxiv:2510.14509; GPT-4o/Qwen, 2024; preprint) uses human coding by four experts on 360 projects. Requirement Missing and Requirement Misaligned are major categories, but the paper also blames code inconsistency in multi-agent settings on "exposure to excessive or irrelevant context".

Against, or for a different dominant problem (core tier, 2025-26 agents):
- SaaSBench (arxiv:2605.17526; 2026 models incl. GPT-5.4 and Gemini 3.1 Pro; preprint) analyses 480 capability units from two agents: "in 63.5% of the capability units, the generated stack never runs stably. Another 32.1% are only superficially accessible but structurally incomplete. Only 3.8% progress to a stage where incomplete business logic becomes the main bottleneck." The dominant problem there is environment and setup, not specification. The classification is trajectory-based, and the coder is not reported.
- NL2Repo-Bench (arxiv:2512.12730; Claude-Sonnet-4.5, GPT-5 and others, 2025; preprint) gives a qualitative failure taxonomy: "A significant portion of failures stem from ImportError or ModuleNotFound" (package structure) plus "Test Suite Alignment" (a reference-coupled oracle). It also finds that early termination ("overconfidence") and context window size matter ("Context Size Is Necessary But Not Sufficient").
- EnvGraph (arxiv:2604.03622; preprint) manually annotated all failed direct generations on NL2Repo-Bench (104 tasks; GPT-5, DeepSeek-V3, Gemini-3-Pro-Preview, 2025). It found "environment-related failures account for 34.7%, 68.9%, and 30.9%". The paper adds that these arise "more often, from repository-internal reference resolution failures". That is a cross-file consistency (context) problem in 2025 frontier models, which is direct evidence *against* "context is not the main bottleneck" in the core tier. The number of annotators and their agreement are not reported.
- HiRAS (arxiv:2604.17745; Qwen3-Coder-480B and DeepSeek-v3.1, 2025): its dominant execution failures are "incorrect inter-file dependencies ... import failures", which is the same direction.
- BeyondSWE (arxiv:2603.03194; 2026; preprint) finds that agents with search "still struggle to convert retrieved information into precise, version-compatible, and locally actionable code". On that benchmark, acquiring and grounding context remains a bottleneck.

## Conclusion on (b)
- Both cited analyses are function-level, not repository-generation studies.
  - MRG-Bench analyses failures of one 2024 model (Claude-3.5-Sonnet) using a 5-LLM vote with no human check. Its "What" category is defined to include repository context, and the paper itself calls for better what-context retrieval.
  - The hallucination taxonomy analyses six 2021-24 models (≤7B plus GPT-3.5), which were given no repository context at all. It counts hallucination instances, not failures, and does not report inter-rater agreement.
- Neither supports "context is not the main bottleneck". At most, both are consistent with "code-similarity/API retrieval addresses a minority of function-level failures in pre-2025 models".
- Transfer to 2025-26 frontier agents is not established by these studies. Agents now gather their own context, and newer corpus evidence points different ways. E2EDevBench (Gemini-2.5, LLM+human coding) supports requirement omission/misinterpretation as the largest category for end-to-end agents. SaaSBench, NL2Repo-Bench, EnvGraph and HiRAS (GPT-5, Gemini-3, Claude-4.5, 2025-26 models) locate the dominant core-tier failures in environment and stack setup and in repository-internal reference resolution, i.e. cross-file consistency, which is itself a context problem.
- Defensible rewording: "Two function-level analyses of pre-2025 models suggest that retrieval addresses only part of the failure mass. In MRG-Bench, an LLM-vote annotation of Claude-3.5-Sonnet failures attributes >68% to missing 'what' information (what the function should do in this repository) rather than 'how' information. A manual hallucination taxonomy of six 2021-24 models, prompted without repository context, finds requirement conflicts (43.5%) more frequent than project-context conflicts (24.6%). For 2025-26 agents, E2EDevBench likewise finds requirement omission and misinterpretation to be the largest failure class (50.1%). Core-tier benchmarks such as SaaSBench and NL2Repo-Bench, however, locate most failures in environment setup and packaging. Which bottleneck dominates therefore depends on the tier and the setting, and the claim that context is *not* a bottleneck is not supported."
- Delete "Better retrieval therefore addresses a minority of failures". Neither study measured what fraction of failures retrieval fixes. The only intervention data, hallucination-paper Table I, shows RAG helping all six models.


## Cross-study claims

### X-a — "Structure is not uniformly beneficial ... a plan helps when it is checked ... and can hurt when it is merely handed over as prose" (lines 58, 64)
- Supported? Only weakly. The single controlled case is E2EDevBench (preprint; Gemini-2.5; LLM-judged). Athena is confounded by output size and is not a prose hand-off. Repo0 is one repository and one model, with a reference-coupled, LLM-mediated oracle, and even there one round of free restructuring helped. No study compares a checked and an unchecked version of the same artefact.
- Rewording: see "Conclusion on (a)" above.

### X-b — "Context is not the main bottleneck ... Better retrieval therefore addresses a minority of failures. The dominant problem is specification understanding" (lines 27–28)
- Supported? No. Both sources are function-level studies of pre-2025 models: Claude-3.5-Sonnet coded by a 5-LLM vote, and six 2021–24 models with no repository context in the prompt. MRG-Bench's "What" category includes repository context. Newer core-tier evidence from 2025–26 models (EnvGraph, HiRAS, SaaSBench, NL2Repo) points to setup and cross-file reference failures. E2EDevBench (Gemini-2.5) supports requirement omission and misinterpretation as the largest category, but only for end-to-end agents.
- Rewording: see "Conclusion on (b)" above.

### From Lines 6–25 + table rows 153–154 (Context acquisition)
1. "Retrieval is the most studied intervention in the contextual tier, and its findings are consistent: the right context helps, while more context often does not."
   - Partly supported. Consistent finding: naive similarity retrieval often adds nothing beyond in-file context. Evidence: AllianceCoder (oracle; GPT-4o-mini/Gemini-1.5-Flash; preprint), Repoformer (completion; 2022-23 code LMs; ICML), MRG-Bench (one model, DeepSeek-Coder-33B; preprint). Not consistent:
     - REPOCOD: every added context beats the baseline, and oracle callees do not beat dense retrieval.
     - CatCoder, DyRetriever, RepoScope, Hydra: similarity retrieval contributes substantially as a complement.
     - RealBench and GRACG test structural, not similarity, retrieval.
     - Typed Holes: exhaustive context slightly beats selective types+headers.
   - No study holds the token budget fixed while varying "more".
   - Rewording: "In three studies of 2023-24 models (two preprints, one on completion), adding similarity-retrieved code to in-file context gave little or negative gain; in-file context and (oracle) dependencies were more useful. Methods that combine similarity with structural retrieval find the two complementary."

2. "Structural signals consistently outperform lexical or embedding similarity."
   - Not supported as stated. Only Hydra (DAR vs BM25/dense; gap "modest") and DyRetriever (graph-only > similarity-only in 3/4 cells, ~2x tokens) run a head-to-head controlled comparison. Typed Holes has a weak, confounded comparison. RepoScope, CatCoder and DyRetriever all combine structure with similarity, and their ablations show similarity is needed. In CatCoder, similarity matters more than types. RepoScope's +36% is against a structural baseline (DRACO). Counter-evidence: REPOCOD (callees ≤ dense for GPT-4o), MRG-Bench (callee bodies 12.8% ≈ embedding RAG 12.9%), GRACG (graph retrieval gives no significant end-to-end gain). The RepoClassBench 77.6 vs 54.7 gap is confounded by test feedback.
   - Rewording: "Structural signals (call chains, types, dependency graphs, structure-aware indexing) consistently add value on top of similarity retrieval in controlled ablations (RepoScope, CatCoder, DyRetriever, Hydra; mostly peer-reviewed, 2023-25 models). Where structure and similarity were compared head-to-head, structure wins modestly (Hydra, DyRetriever), and the best systems combine both. Oracle callees alone do not beat dense retrieval (REPOCOD, MRG-Bench)."

3. Section heading "Structure beats similarity" — retitle "Structure complements similarity".

### From Lines 30–56 + table row 155 (Planning representation)
- **"Ablations that remove the structured artefact while keeping everything else fixed consistently report large drops"**: not supported as worded.
  - (a) Only SpecFirst states a single-variable control (same scaffold and model), and even it is not compute-matched (+48–130% cost).
  - (b) AgileCoder's ablation changes the task subset (11 context-overflow failures excluded) and removes context retrieval, not a plan.
  - (c) CodeSpec's "w/o All Specification" row is identical to the Mini-SWE-Agent baseline, and it halves cost.
  - (d) Repo0 removes the evolution loop, not the artefact. Removing the Dual-DAG itself gives 0 to −10 Pass Rate.
  - (e) The drops are not uniformly "large": SpecFirst +2.7–7.2 absolute; WebDesignIter Pass@2 −6.0; CodeSpec −8.1 with overlapping bootstrap std on n=30.
  - (f) Model generations differ (2023 GPT-3.5 to 2026 GPT-5.5/DeepSeek-V4).
  - (g) Oracles differ: human rating, LLM-rewritten tests plus LLM vote, reference tests.
  - (h) 4 of the 5 inspectable studies are preprints, and the DbC study has no full text.

  Suggested rewording: "In five within-study ablations (four preprints and one workshop paper, models from GPT-3.5 to GPT-5.5), removing or omitting a structured plan or specification lowered the primary metric (by 2.7–34 points). Only SpecFirst isolates the artefact under a fixed scaffold and model with a significance test, and its gain costs 48–130% more. The others either change more than the artefact or rely on a single run on ≤50 tasks."
- **"Most other comparisons against ChatDev and MetaGPT are uncontrolled"**: partly supported, but too strong as a blanket term. Several method papers (e.g., CodeTeam: "all agents ... share the same backbone model"; CodeSpec: "same ... interaction budgets") control the backbone model. What they generally do not control is token or call budget. Example: AgileCoder vs ChatDev on ProjectDev uses 36,818 vs 7,440 tokens ($0.44 vs $0.12). AgileCoder's HumanEval table also mixes rows across backbones (GPT-3.5, Claude 3 Haiku, GPT-4). Suggested rewording: "Most head-to-head comparisons against ChatDev and MetaGPT fix the backbone model but not the token or call budget. Gains therefore confound the representation with extra computation (e.g., AgileCoder uses ~5× ChatDev's tokens)."

### From Lines 66–94 + table rows 157, 158, 162 (Agent decomposition; Harness)
**X1. "[Role frameworks] perform poorly under neutral evaluation" (l.67)**
- Support: partial.
  - E2EDev (preprint; GPT-4o/Qwen2.5 2024, Haiku 4.5 2025) supports it for MetaGPT (≈0) and weakly for ChatDev (≤ vanilla on 4/6).
  - RepoGenesis (preprint; GPT-5.1/Sonnet 4.5) shows MetaGPT <3%, but every open-source agent is <13% and MetaGPT has the best API coverage. It gives an absolute number, not a relative one.
  - RoleBasedMAEval (peer-reviewed; GPT-5) finds the role-based pipeline better than a standalone LLM, with no test oracle. This is evidence against "poorly" in a relative sense.
- "Neutral" is fair only in that the evaluators are not the framework authors. Two of the three are preprints.
- Rewording: "In third-party evaluations, MetaGPT fails almost completely (E2EDev, RepoGenesis; both preprints, 2024–26 models). ChatDev does not beat a single-prompt baseline on most E2EDev backbones. A peer-reviewed GPT-5 study finds a ChatDev-2.0 pipeline more similar to developer code than a standalone LLM, but only 40% of its classes compile."

**X2. "The contrast with the frameworks' own reports is instructive" (l.73–75)**
- Model-generation mixing: the self-reports use GPT-3.5 (ChatDev) and GPT-4 (MetaGPT), both 2023. E2EDev re-runs them with 2024–25 models and current code.
- The self-reports also contradict each other. ChatDev claims quality 2.6× MetaGPT, and MetaGPT claims executability 3.75 vs ChatDev 2.25. This is a stronger point about self-evaluation than the model contrast.
- Rewording: add "(with 2023-era GPT-3.5/GPT-4 backbones)" and mention the mutual contradiction.

**X3. "Where decomposition does help, it adds a separate verifier with an independent signal" / "multi-agent designs pay off when they introduce an independent check, and add cost and failure points when they only relay prose" (l.76, 84)**
- Support: partial. All four ablations use 2025–26 models (DeepSeek-V3.2/V4-Pro, Sonnet 4.5, Gemini 2.5), so there is no generation mixing.
- In ReCodeAgent and TraceDev the ablation removes test execution, not just independence. ECAT's oracle is an LLM agent-as-judge on 3 repos (preprint). E2EDevBench, which isolates independence, is mixed by model (Pro +10.5, Flash −3.0) and is judged by the same Gemini-2.5-Pro.
- NanoHarness supports the claim, since its task-specific subagents are differential-testing and review roles.
- "relay prose" rests on E2EDevBench DDT and E2EDev cost. Both are preprints.
- Rewording: "In ablations from 2025–26 (two peer-reviewed, ReCodeAgent and TraceDev; three preprints), removing a verifier agent that runs tests or a judge costs 30–60 points. Most of these ablations remove execution feedback along with the separate agent, so the evidence supports an execution-grounded check more than independence per se."

**X4. "Harness effects are therefore small between comparable general-purpose scaffolds. They are large when a scaffold restricts exploration, compresses long specifications, or fails to match the model." (l.93–94)**
- Support: weak, contradicted in part.
  - Same-model gaps between general-purpose scaffolds are not small in several studies: RepoMod (OpenCode vs Codex CLI) 12.6 and 6.2; CLI-Tool-Bench (mini-SWE vs OpenHands) avg 5.7; NanoHarness RQ1 (OpenCode vs mini-SWE on ProgramBench N=70) about 4.5–6.5 for top models; SaaSBench 1.3–4.1. Only NL2Repo (1 model) shows about 1.
  - The direction is also inconsistent: the vendor harness is better in SaaSBench (Claude Code) and worse in RepoMod (Codex CLI).
  - "restricts exploration" rests on RepoZero's OpenHands-bash. "compresses long specs" rests on one preprint with 2 models. "fails to match the model" rests on PaperBench, the only study with 2024-era models (o1, Claude 3.5 Sonnet), where the manipulation was a prompt and submit-tool change.
  - All seven studies are single-run or near-single-run on ≤200 tasks, and all but RepoZero are preprints.
- "NanoHarness offers a controlled reconciliation" overstates one preprint using open-weight models only.
- Rewording: "Same-model harness gaps range from about 1 point (NL2Repo) to 12.6 points (RepoMod-Bench), and the sign is inconsistent: vendor CLIs lead in SaaSBench but trail in RepoMod-Bench. In one controlled preprint (NanoHarness, two 2026 open-weight models), adding verification subagents helps and context compression hurts on ProgramBench. Because most comparisons are single-run preprints, benchmarks should fix the harness or report it as a factor."

### From Lines 96–115 + table rows 159–161 (Execution feedback)
**"Executable feedback is the most consistently supported intervention in the corpus"**
- Partly supported. The eight bullets mix different interventions. Two of them do not isolate execution feedback against no feedback: C73 is a rule and type-check ablation, and C79 is environment attribution with an execution-based baseline that comes within 1 point. One bullet (C80) attributes the post-hoc feedback gain to in-decoding feedback.
- Model generations run from Claude 3 Sonnet (2024; Oxidizer) through o1/o3/GPT-4o (2024-25; CRUST, AutoP2C) to Sonnet 4.6, GPT-5 and Opus 4.8 (2026; TDDev, EnvGraph, GenComp). The direction is consistent across generations, but the effect sizes are not comparable.
- Peer review: of the five table-row studies, CRUST (COLM), AutoP2C (ICASSP; FT is the preprint version), RepoZero (NeurIPS D&B) and TDDev2026 (ASE) are peer-reviewed; EnvGraph is a preprint.
- Validity:
  - No study holds compute fixed. Feedback arms always get more calls.
  - Several loops feed back the same tests that score the result (CRUST test repair, TDDev2026 acceptance tests derived from the oracle tests, Commit0 stage 3). This inflates the gains.
  - Task counts are small: AutoP2C ablation n=4, TDDev2026 n=20, Oxidizer n=7.
  - "Most consistently" is a comparison the section does not make against the other interventions.
- Suggested rewording: "Execution feedback is the intervention with the most same-model ablations in the corpus. Four peer-reviewed studies and several preprints, spanning GPT-4o-era to 2026 models, report gains from compiler or test feedback over single-pass generation (e.g. CRUST-Bench o3 19→48%; TDDev Sonnet 4.6 67.8→91.5% on 20 apps). None holds compute fixed, and several feed back the same tests used for scoring."

**"The qualifications are equally consistent"**
- Not supported as worded. The evidence for each qualification is thinner and weaker than the gains:
  - Untrusted feedback: one 2024 preprint (Commit0, open models only) and one controlled, peer-reviewed result (TDDev2026 Qwen, n=20, effects not significant).
  - Saturation: one abstract-only paper (DynamicEval) and one misattributed single-run preprint result (TDDev2025).
  - Agents not using feedback: observational behaviour logs (NL2Repo, CLI-Tool-Bench) and a 16-point correlation (VibeCode), all preprints.
  - Unreliable self-assessment: chess (preprint, non-functional Elo) and E2EDevBench, whose own data puts verification failures at 5.7%.
- Suggested rewording: "Several studies, mostly preprints, qualify these gains. Feedback from a weak tester or a linter can erase or reverse them (TDDev2026, Commit0). Returns can diminish after a few rounds (DynamicEval, abstract only; TDDev2025). Behavioural logs and correlations suggest some agents skip self-testing (NL2Repo-Bench, CLI-Tool-Bench, Vibe Code Bench). And agents' self-assessments can be far off without an independent oracle (chess study)."

### From Lines 117–144 + table rows 163–164 (State, environment, training)
- "Long-horizon runs lose their early constraints" (line 118): rests on one qualitative remark in RepoZero (translation task, open models 2025-26). Reword: "RepoZero (NeurIPS 2026 D&B) qualitatively observes 'contextual drift': agents lose track of requirements stated in the initial prompt as trajectories lengthen."
- "Several methods attack the problem with explicit state" (C93-C96): only LiveCoder and CodeMEM have ablations; DeepRepro is evaluated with an LLM judge; EvoGit has no baseline and states it uses no shared memory. Reword: "... of these, only LiveCoder and CodeMEM (preprints) report ablations, on disjoint benchmarks."
- "The environment as a failure source" + "Environment setup is a distinct capability from writing code" (lines 129-136): EnvGraph's "environment-related" category is mostly repository-internal reference resolution, and HiRAS's execution failures are mostly inter-file import errors; both are code defects that surface at execution. SaaSBench (T5) and ABC-Bench (S1) do isolate deployment/environment. ParEval-Repo is translation with 2024-era small models. Reword: "Failures surface at build/run time more often than in code logic: ... (EnvGraph counts both missing dependencies and broken internal imports). Measuring environment build separately from functional tests, as ABC-Bench does, would separate these."
- "Recent work turns construction tasks into training data" (line 139): holds for DeNovoSWE, MindForge, RepoGenesis, WebGen-Bench, JAMER, WebGen-R1; not for RepoST (function-level). All are preprints; DeNovoSWE/MindForge gains are SFT distillation from 2026 frontier teachers (DeepSeek-V4-Pro, GLM-5.2) into 27-30B students, evaluated with reference-coupled tests; DeNovoSWE evaluated on a benchmark from the same group. Reword: "In preprints, SFT on distilled construction trajectories lifts 27-30B open models substantially (DeNovoSWE: 5.8->47.2% on BeyondSWE-Doc2Repo, from the same group; MindForge: 38->49.5% on ProgramBench), measured by reference-coupled tests."
- Line 144 oracle carry-over: plausible and consistent with C108, but no cited study demonstrates reward hacking; flag as the authors' inference.
- Table row "Training ... C +": supported for DeNovoSWE and MindForge; drop or qualify SWE-Playground (+~1 pp on Commit-0 Lite).

## Unsupported

### From the dedicated analyses
- Line 28, "Better retrieval therefore addresses a minority of failures": no study measured the fraction of failures that retrieval fixes. The hallucination paper's RAG pilot improved all six models. Fix: delete.
- Line 28, "The dominant problem is specification understanding": not established beyond function-level pre-2025 analyses. Fix: weaken and scope it (see the (b) rewording).
- Line 60, "the Developer treats the design as authoritative and drifts from the requirement": this is the authors' hypothesis ("we hypothesize"), not a measured finding. Fix: write "the authors hypothesise that ...".
- Line 61, "increase coverage" and "when no validation layer checks them": Athena measured size (views and LOC), not coverage, and does not attribute the bugs to missing validation. Fix: reword per C43.
- Line 62, "over-decomposes it": not quantified in Repo0. Also, one round of free restructuring improved on no evolution. Fix: reword per C44.
- Line 64, "The pattern is that a plan helps when it is checked ...": no direct test exists. Fix: present it as a hypothesis.
- Table row 156, "C" for the prose hand-off and Athena listed under it: Athena's IRs are structured, and its comparison is an uncontrolled user study. Fix: drop Athena or mark the row U with a ± direction.

### From Lines 6–25 + table rows 153–154 (Context acquisition)
- C2 "invoked APIs help most": the paper says in-file context helps most. Fix: correct it.
- C5 "callees worse than dense retrieval": holds for GPT-4o only. Fix: "comparable; worse for GPT-4o".
- C7 RealBench used as evidence against similarity retrieval: its RAG is import-graph based. Fix: re-characterise or move it.
- C8 "+36% relative" attributed to call chains: this is the best of 8 cells, against DRACO, for a system that also uses similarity. Fix: "up to +36% (one of four backbones)", and say RepoScope is hybrid.
- C11/C13 CatCoder and DyRetriever cited as "structure outperforms similarity": their ablations show complementarity, and in CatCoder similarity matters more. Fix: reword.
- C15 RepoClassBench gap attributed to symbol-lookup tools: confounded with test-oracle feedback. Fix: add "with compiler/test feedback".
- C17 table row 154: RealBench and GRACG are not similar-code retrieval. Fix: split the row.
- C6 GRACG: abstract only. Fix: mark "(abstract only)" or drop it.

### From Lines 30–56 + table row 155 (Planning representation)
- C20 "Core-tier methods almost always insert an intermediate artefact": there is no tally in the corpus, and counter-examples exist (training/RL, validation, memory methods). Fix: restrict to NL-to-repo/app agent frameworks and give k/N after coding, or weaken to "most".
- "keeping everything else fixed" (line 50): no cited study except SpecFirst states this, and SpecFirst is not cost-matched. Fix: delete the phrase or qualify per study.
- AgileCoder as a planning representation (list entry, ablation bullet, table row): the evidence shows a code-derived context-retrieval graph. Fix: reclassify, or say "context structure".
- CodeSpec "on long instructions": holds for the 3,000–5,000-word bin only. Fix: name the bin, or drop the claim.
- DbC "significantly higher pass@k": the claim rests on the abstract only (no full text). Fix: mark as abstract-level and single-system, or drop it from the "controlled evidence" list.
- Table row "checked plan" (line 155): most of the cited artefacts are not checked. Fix: rename the row to "Structured plan/specification", or prune the citations.

### From Lines 66–94 + table rows 157, 158, 162 (Agent decomposition; Harness)
- C45 "most common baselines": no citation or count. Cite a corpus count or weaken to "frequent".
- l.81 TraceDev bullet and l.82 E2EDevBench bullet lack \cite. Add \cite{TraceDev2026} and \cite{E2EDevBench2025}.
- l.91 "On ProgramBench~\cite{ProgramBench2026}, harness components add 6–7 points…": the numbers are NanoHarness's. Cite NanoHarness2026 (ProgramBench as the benchmark only).
- l.89 SaaSBench "Codex CLI ahead of OpenHands": figure only, no number in the text. Weaken to "Claude Code ahead of OpenHands for all eight models" or read the value from Fig. 4a.
- l.90 RepoZero "ahead of OpenHands": the comparison is with OpenHands-bash, a restricted configuration. Correct the wording.
- l.92 "only strong models benefit from complex harnesses": this is task-dependent and reversed on SWE-bench Pro. Scope it to ProgramBench/GitTaskBench.
- l.93 "small between comparable general-purpose scaffolds": contradicted by RepoMod-Bench, CLI-Tool-Bench and NanoHarness RQ1. Rewrite as in X4.

### From Lines 96–115 + table rows 159–161 (Execution feedback)
- C82 "Qwen's self-written tests ..." has no citation. Fix: cite TDDev2026 and reword to "self-judged test feedback".
- C84 "One to two TDD rounds lower accuracy ..." is placed under the DynamicEval citation but comes from TDDev2025 (arXiv:2509.25297). Fix: cite TDDev2025, give the model (Claude-4-Sonnet) and note the small sample, or delete.
- C85 has no NL2Repo-Bench citation, and NL2Repo's claim that models skip building or testing is a hypothesis. Fix: cite NL2RepoBench2025 and weaken to "end early (Qwen3-Thinking 49%); CLI-Tool-Bench logs show Claude Sonnet 4.6 submitting without compiling".
- C87 "The chess study" has no citation. Fix: cite ChessEnginesPL2026.
- C88 E2EDevBench "leading failure cause" contradicts the paper's own Table 5 (5.7%). Fix: reword per C88 or delete.
- C79 "10-13 points on NL2Repo-Bench" is wrong. Fix: 3.9-11.5 over Direct, ≤3.2 over the best baseline. NL2Repo-Bench is also uncited here.
- C80 "66% to 13%" credits post-hoc feedback to in-decoding feedback. Fix: split the two figures as in C80.
- C73 Oxidizer's ablation is not evidence for execution feedback. Fix: move it to the structure/rules discussion, or reword.
- C83 DynamicEval rests on the abstract only. Fix: mark it as abstract-level evidence, or obtain the full text.
- RepoZero bullet (C77) lacks \cite and the backbone. Fix: add \cite{RepoZero2026} and "DeepSeek V3.1, Py2JS".
- RepoTransBench venue: corpus.csv says preprint, but the record DOI is IEEE TSE. Fix: verify and update corpus.csv/bib.

### From Lines 117–144 + table rows 163–164 (State, environment, training)
- Line 118 RepoZero: no \cite. Fix: add \cite{RepoZero2026}.
- Line 131 EnvGraph and line 132 SaaSBench: no \cite. Fix: add \cite{EnvGraph2026}, \cite{SaaSBench2026}.
- Line 141 RepoGenesis: no \cite. Fix: add \cite{RepoGenesis2026}.
- Line 133 ParEval-Repo "the main bottleneck": paper says "a major obstacle". Fix: weaken (C100).
- Line 141 RepoST as construction training data: misclassified. Fix: move to a footnote/"function-level within repositories" or delete (C106).
- Line 142 WebGen-R1 "execution-grounded rewards": omits VLM-judge component, which matters for line 144. Fix: reword (C107).
- Line 136 "should be measured separately": normative; EnvGraph/HiRAS evidence conflates environment with internal-import defects. Fix: qualify (see cross-study).
- Table row 164 SWE-Playground: negligible construction gain. Fix: remove or annotate (C110).
