# Full-text adjudication log (reviewer 1 = main session over agent decisions)

Borderline cases raised by the full-text agents and the final reviewer-1 decision. Candidates for reviewer-2 checking.

| Key | Paper | Agent decision | Final | Rationale |
|---|---|---|---|---|
| arxiv:2609.21293 | GameASG-Bench | include core | **exclude EC3** | Output is a single self-contained index.html. Core requires a multi-file repository/application (protocol §1). Rule added to the deviations log. |
| arxiv:2607.13921 | Generative Compilation | include contextual | include contextual | Generated files are placed into a reference repository and run against its unit tests. |
| arxiv:2603.20299 | HCAG | include core | include core, low QA | Task only just extractable; tables inconsistent (flagged in note). |
| arxiv:2502.17139 | FastCoder | include contextual | include contextual | Efficiency method for repository-level generation; Pass@1 unchanged by design. Discuss under RQ4 efficiency. |
| arxiv:2505.21577 | RepoMaster | exclude EC4 | exclude EC4 | Reuses existing repositories to solve tasks; no generated repository is evaluated. |
| arxiv:2508.07966 | CBA user study | include core | include core | Create tasks reported separately from edit tasks. |
| doi:10.1109/ase63991.2025.00057 | RustRepoTrans | include contextual | include contextual | The preprint 2411.13990 is already EC7. |
| arxiv:2312.05772 | A3-CodGen | exclude EC2 | exclude EC2 (redefined) | Repository-dependent generation, but no execution-based evaluation (human-labelled reuse and LOC). Falls under the broadened EC2. |
| arxiv:2402.03630 | IDECoder | exclude EC2 | exclude EC2 | Exact match / CodeBLEU only; short vision paper. |
| arxiv:2304.07590 | Self-Collaboration | exclude EC3 | exclude EC3 | Evaluated on isolated benchmarks; multi-file examples are qualitative only. |
| arxiv:2311.09835 | ML-Bench | include contextual | **exclude EC3** | Outputs are mostly one-line bash commands that invoke repository scripts, not repository-dependent code units. |
| arxiv:2406.14497 | CodeRAG-Bench | include contextual | include contextual (peripheral) | Only the RepoEval function split (373 samples, test-based) is in scope; it is reported separately. |
| arxiv:2409.16299 | HyperAgent | include contextual | include contextual (peripheral) | Generalist agent with a separately reported RepoExec evaluation. |
| arxiv:2406.10263 | CARD | include contextual | include contextual (peripheral) | Retrieval efficiency method; RepoEval function split with tests. |
| arxiv:2404.00599 | EvoCodeBench v1 | exclude EC7 | exclude EC7 | Earlier version of 2410.22821 (NeurIPS 2024 D&B). |
| doi:10.47392/irjaem.2026.0294 | Deepsite | exclude EC8 | exclude EC8 | Platform description; accuracy figures without task, dataset or protocol. |
| doi:10.54254/2755-2721/2026.31609 | WFC-Gen | exclude EC8 | exclude EC8 | Output size, repository dependence and tests not described; implausible claims. |
| arxiv:2608.09273 | ECAT | include core | include core, low QA | Generates a new ArkTS repository (not an in-place edit); 3 repositories; LLM-judge evaluation, no tests. |
| arxiv:2508.04295 | EvoC2Rust | include core | include core | Project-level translation; project-level evaluation is only compile rate and line acceptance, with tests at module level. Relevant to RQ3. |
| arxiv:2608.26557 | DeepRepro | include core | include core, low QA | 5-page demo paper; LLM-judge-only evaluation; baselines copied from other papers. |
| arxiv:2603.03194 | BeyondSWE | include core | include core (peripheral) | Mixed benchmark; Doc2Repo subset (50 of 500 tasks) has its own construction pipeline and metrics. |
| arxiv:2607.26777 | CodeSpec | exclude EC1 | **include core (peripheral)** | Consistency with HyperAgent/CodeRAG-Bench: primarily feature development, but reports a separate NL2Repo-Bench evaluation (104 tasks). |
| arxiv:2601.01271 | CatchAll | exclude EC1 | exclude EC1 | Catch-block generation inside existing code; mostly CodeBLEU. |
| arxiv:2605.19901 | OOD design study | include core | include core | Small multi-class Java project; measures design quality. |
| arxiv:2605.06136 | BUILD-AND-FIND | include core | include core, low QA | 2 tasks; LLM agents do all the measuring. |
| arxiv:2604.06373 | Cursor large-project study | include core | include core | Human-in-the-loop generation; design issues in the generated projects. |
| arxiv:2511.07584 | SemanticForge | include contextual (abstract) | exclude EC1 | RepoKG-50 is built from commit-diff edit tasks. |
| arxiv:2507.09866 | LiveRepoReflection | exclude EC3 | exclude EC3 | Synthetic Exercism-style mini-repos without real project dependencies. |
| arxiv:2601.11077 | ABC-Bench | include contextual | include contextual | Masked backend endpoints in real repositories, like CoderEval/DevEval; GPT-5-generated API tests. |
| arxiv:2512.12216 | SWE-Playground | include core | include core (peripheral) | Training pipeline; Commit0-Lite results reported separately (~3%). |
| arxiv:2511.03404 | ProjectGen | include core | include core | PRD + UML + architecture doc with the reference directory tree (strong reference coupling). |
| arxiv:2410.19245 | MaCTG | include core | include core, low QA | ChatDev-style module/project decomposition; tasks are script-sized and multi-file output is not verified. |
| arxiv:2403.10059 | Repoformer | include contextual | include contextual (peripheral) | Completion method; executable evidence only from the RepoEval function split. |
| arxiv:2401.06391 | ToolGen | include contextual | include contextual (peripheral) | Main benchmark is similarity-based; CoderEval Pass@1 subset (176 tasks). |
| arxiv:2409.00921 | Typed Holes | include contextual | include contextual | Repository-dependent update function; 5 small synthetic apps. |
| arxiv:2406.11612 | Long Code Arena | exclude EC2 | exclude EC2 | ChrF / API recall / exact match; no executed tests. |
| doi:10.24963/ijcai.2025/848 | TransGraph | include core | include core (peripheral) | Mostly function-level; 2 projects reported separately. |
| arxiv:2503.22688 | CodeIF-Bench | include contextual | include contextual (peripheral) | Only 40 intra-file DevEval tasks evaluated with tests; the cross-file tier was dropped. |
| arxiv:2503.23231 | CCCI | include contextual | include contextual (peripheral) | Closed industrial data; Build Pass compiles and runs the code on test cases. |
| arxiv:2508.20263 | Athena | include core | include core | HCI prototype; user study plus error counts; no automated functional tests. |
| arxiv:2511.18274 | Rehab software | exclude EC3 | exclude EC3 | Single Scenic DSL program. |
| arxiv:2503.06689 | DependEval | exclude EC4 | exclude EC4 | Outputs dependency chains, not code. |
| doi:10.55041/ijsrem36242 | ProgAI | exclude EC7 | exclude EC7 | Abstract is a near-verbatim copy of CodeAgent (ACL 2024). |
| doi:10.5281/zenodo.21157035 | REPOFORGE | include contextual | include contextual, low QA | Doubtful provenance (Zenodo DOI vs. stated journal); implausibly high Pass@1; mixed task families. |
| doi:10.24433/co.6120886.v1 | Spec2Code | include core | include core, low QA | Code Ocean capsule; no functional check of the generated code. |
| doi:10.1109/access.2026.3686308 | VeriGen | exclude EC4 | exclude EC4 | Outputs requirements, UML and skeletal stubs; no working implementation. |
| arxiv:2509.20136 | V-GameGym | exclude EC3 | exclude EC3 | Single-file Pygame programs (multi-file rule). |
| arxiv:2601.00376 | InlineCoder | exclude EC2 | exclude EC2 | EM/ES/BLEU only; the authors state that Pass@k was not used. |
| doi:10.5281/zenodo.20709565 | State Not Tokens | include core | **exclude EC1** | Main task is in-place JS→TS migration of an existing repository; single-author Zenodo deposit with an implausible NL2Repo-Bench claim. |
| arxiv:2608.23564 | SWE Refactor Bench | include core | include core (peripheral) | 7 of 20 tasks are whole-repository language rewrites, reported separately; the rest are EC1-type migrations. |
| arxiv:2606.08135 | TICoder | include contextual | include contextual, low QA | Source of the test cases used in planning is unstated (possible leakage). |
| arxiv:2604.03632 | LiveCoder | include core | include core | Test pass rate is both the selection signal and the metric; discuss under RQ3. |
| arxiv:2609.02272 | PaperCompiler | include core | include core, low QA | LLM-judge-only evaluation (o3-mini generator, o3-mini-high judge). |
| arxiv:2601.13240 | KoCo-Bench | include contextual | include contextual | The scored task is function generation inside projects; project level is only qualitative. |
| arxiv:2601.02430 | WebCoderBench | exclude EC3 | exclude EC3 | Plain LLMs output a single page; the multi-file rule applies. |
| arxiv:2605.26017 | SPDDWL | include core | include core, low QA | n=1 project, single run. |
| arxiv:2605.02455 | Spec-driven vision paper | exclude EC6 | exclude EC6 | Self-described vision paper; the pilot study is illustrative only. |
| doi:10.6084/m9.figshare.32854478.v1 | PULSE | include core (peripheral) | **exclude EC8** | No full text; the project-level evaluation is not described (no numbers, languages or metric), so IC5 is not met. |
| arxiv:2604.16314 | SelfEvolve | include contextual | include contextual, low QA | 11 tasks, of which 4 are repository-dependent; executed pytest oracles. |
| arxiv:2608.27906 | RCCA | exclude EC3 | exclude EC3 | Single-file HTML output. |
| arxiv:2606.03907 | Agentic tools build-vs-buy | exclude EC1 | exclude EC1 | Registered-report protocol without results; scaffolded starting project. |
| arxiv:2506.02049 | EvoGit | include core | include core, low QA | Full text defines the task; evaluation is two qualitative case studies with no metrics or baselines. |
| doi:10.1109/forge66646.2025.00026 | AgileCoder | include core (abstract) | include core, low QA | Re-reviewed with the arXiv full text; ProjectDev has 14 manually scored tasks. |
| doi:10.1109/llm4code66737.2025.00016 | YABLoCo | exclude EC8 (abstract) | include contextual | Re-reviewed with the arXiv full text (2505.04406). |
| arxiv:2606.16244 | BRACE | unsure | exclude EC3 | Repository-level part is one model and one table on mostly single-file BaxBench backends. |
| arxiv:2606.31159 | Security calibration | unsure | exclude EC1 | Its repository-level task is fixing CVEs in existing code. |
| arxiv:2609.06383 | PROOF | include core (peripheral) | include core (peripheral) | Main target is spec-driven maintenance; the only reported evaluation rebuilds 3 SWE-bench repositories from spec (high contamination risk). |
| arxiv:2604.17187 | React Native app study | include core | include core, low QA | One prompt, one seed, manual checklist. |
| arxiv:2604.19742 | PlayCoder | include contextual | include contextual, low QA | LLM-generated unit tests; inconsistent scale figures. |
| arxiv:2603.23633 | Security repair of generated projects | exclude EC1 | exclude EC1 | Repair of existing generated projects; 2603.00897 is its earlier version (also EC1). |
| doi:10.1016/j.future.2026.108599 | Delphi→C# industrial pipeline | include core (abstract) | **exclude EC6** | Self-described early observations; experience report. |
| doi:10.1145/3803437.3805266 | Repo-level C→Rust (truncated abstract) | include core (abstract) | **exclude EC8** | Evaluation not described; IC5 not met (consistent with PULSE). |
| doi:10.1145/3786583.3786915 | IBM COBOL→Java | include core (abstract) | **exclude EC8** | Evaluation not described; IC5 not met. |
| doi:10.1145/3808169 | PtrTrans | include core (abstract) | **exclude EC8** | Benchmark size and oracle unknown from abstract; IC5 not met. |
| doi:10.1109/icassp55912.2026.11463415 | SimulatorCoder | include core | **exclude EC3** | Reliability-check adjudication: 138 tasks at function/class/module level; multi-file output never stated, no existing repository (was include core, low QA). |
| doi:10.1109/csecs69124.2026.11541607 | GPT-5 fullstack generator | include core (abstract) | include core, low QA | Evaluation described (static quality tools and 2 students) but no functional tests. |
| doi:10.1109/ase63991.2025.00287 | ASML case study | include contextual | include contextual, low QA | pass@k = 0 everywhere; build@k is the effective metric; language unstated. |
| doi:10.1109/ase63991.2025.00235 | SolContractEval | include contextual (abstract) | include contextual, low QA | Execution-based replay of transactions described in the abstract; full text not read. |
| doi:10.18653/v1/2025.naacl-long.7 | CodexGraph | include contextual (peripheral) | include contextual (peripheral) | Separate EvoCodeBench Pass@1 evaluation. |
| doi:10.1145/3729287 | Skel | exclude EC3 | exclude EC3 | Programs merged into single files. |
| doi:10.5753/wtf.2026.23233 | Software aging (Python) | exclude EC3 | exclude EC3 | BaxBench single-file backend scenarios. |
| doi:10.1109/apsec65559.2024.00052 | APSEC enterprise app | include core (abstract) | **exclude EC8** | Evaluation not described in the abstract; IC5 not met (consistent rule). |
| arxiv:2401.06401 | DevEval (first version) | exclude EC7 | exclude EC7 | Same first four authors and benchmark lineage as 2405.19856 (verified via arXiv). |
| doi:10.1007/s10664-024-10573-2 | Tymcrat | include core | include core, low QA | No translated program compiles; correctness is a manual sample of 41 functions. |
| doi:10.1145/3650212.3652115 | CoderUJB | include contextual (peripheral) | include contextual (peripheral) | Mixed benchmark; 238 function-generation tasks against project tests are reported separately; context is class-level. |
| doi:10.18653/v1/2024.acl-long.810 | ChatDev | include core | include core | Found only via snowballing; SRDD evaluation. |
| arxiv:2308.00352 | MetaGPT | include core | include core, low QA | Found only in snowballing round 2; repository-level evaluation is 7 SoftwareDev tasks with human executability ratings and no tests. |
| doi:10.1109/ase63991.2025.00051 | RustAssure | include core (abstract) | include core, low QA | Whole C codebases (5 projects), but only per-function metrics (compile, symbolic equivalence). |
| doi:10.1145/3795154.3795362 | CloudMAS | include core (abstract) | include core, low QA | Abstract describes evaluation (compilation, test suites, deployment). |
| doi:10.1145/3786167.3788408 | BAEs | include core (abstract) | include core, low QA | Runnable-project check and cost measures versus ChatDev/GHSpec; the sprint evolution part is close to EC1. |
| doi:10.1109/iceca66444.2025.11383462 | Semantic Kernel for SE | include (abstract) | exclude EC8 | Reports 65% success but not how success is judged (IC5). |
| doi:10.1145/3728941 | ArkAdapter | include core (abstract) | exclude EC1 | Ports libraries by fixing syntax mismatches in the existing code (in-place). |
| doi:10.1145/3702987 | AgileGen | exclude EC8 (abstract) | include core, low QA | Re-reviewed with the arXiv full text (2407.15568): multi-file web apps, 40 projects + SRDD, human executability ratings; Gherkin hand-off. |
| (see batch30) | Experiential Co-Learning | include (R1, main session) | include core, low QA | Snowballing round 4; ChatDev metrics on SRDD, no functional tests (full text checked). |
