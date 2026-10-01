# Review Protocol — LLM-Based Repository-Level Code Generation

Status: DRAFT v0.1 (2026-09-30). Frozen before the final search run; any later change is logged in §11.

Guidelines followed: Kitchenham & Charters (2007) for SLRs in SE; Wohlin (2014) for snowballing; PRISMA 2020 for selection reporting.

## 1. Scope

**Definition.** *Repository-level code generation* is the generation of source code by an LLM or LLM-based agent where either (a) the output is a multi-file repository, library or application (*core tier*), or (b) the output is a smaller unit (function, class, file) whose correctness depends on dependencies, interfaces or behaviour defined elsewhere in a repository and is judged by execution (*contextual tier*).

**Core tier** covers: natural-language/specification → repository; skeleton/stub → library; executable/API reference → behaviourally equivalent repository (reconstruction, reproduction); repository → repository translation/modernisation; methods, agents and training environments for these tasks.

**Contextual tier** covers: repository-dependent function/class/file generation benchmarks and methods evaluated with executable tests.

**Out of scope:** pure code completion (next-line/span, evaluated by similarity); issue resolution, bug repair, PR-based feature addition in an existing repository (SWE-bench family); tasks whose output is not code (documentation, tests only, review, repository QA).

## 2. Research questions

- **RQ1 Task formulation.** How is repository-level generation formulated (input specification, initial workspace, output boundary, autonomy)?
- **RQ2 Benchmarks.** How are benchmarks constructed (source repositories, specifications, oracles, languages, contamination defences)?
- **RQ3 Evaluation.** How is correctness and quality measured, and how strongly are metrics coupled to a reference implementation?
- **RQ4 System design.** Which design choices (context/retrieval, planning representation, multi-agent workflow, execution feedback, memory) are used, and which are supported by controlled evidence?
- **RQ5 Gaps.** What limitations and open problems recur?

## 3. Sources

| Source | Access | Fields searched |
|---|---|---|
| arXiv | API, automated (`search.py`) | title, abstract |
| OpenAlex | API, automated (`search.py`) | title, abstract |
| ACM Digital Library | manual, institutional | title, abstract |
| IEEE Xplore | manual, institutional | all metadata |
| Scopus | manual, institutional | title, abstract, keywords |

OpenAlex indexes most ACM/IEEE/Springer/Elsevier venues and arXiv; it is used as a broad-coverage index in addition to the publisher databases. arXiv is required because a large share of the field appears first (or only) as preprints.

## 4. Search strings

Defined once, database-agnostically, in `queries.json` as three query families (union). Each family is a conjunction of term blocks; terms inside a block are OR-ed. `render_queries.py` translates them into each database's syntax (`queries_rendered.md`), so the same logic is applied everywhere.

- **F1 repository-level code generation:** REPO_SCOPE ∧ CODEGEN ∧ LLM
- **F2 whole-repository construction:** WHOLE_REPO ∧ LLM
- **F3 from-scratch software:** FROM_SCRATCH ∧ SW_ARTIFACT ∧ CODE ∧ LLM

No negative terms are used (e.g., NOT SWE-bench): in-scope papers routinely mention issue-resolution benchmarks, so exclusions are applied during screening, not retrieval. "Code completion" is kept in the search for the same reason; completion-only studies are excluded at screening with a reason code.

**Window:** 2022-01-01 to the search execution date (search date = cutoff). Start motivated by the LLM era (ChatGPT/Codex); the earliest known in-scope studies are from 2023.

**Search validation (quasi-gold standard).** Before freezing, recall of the automated search is measured against a quasi-gold set of known in-scope studies (from the preliminary review, §9). Strings are revised until recall is acceptable; each revision and its recall are logged.

## 5. Selection criteria

Inclusion (all must hold):
- **IC1** Publicly available between 2022-01-01 and the cutoff; full text accessible.
- **IC2** Written in English.
- **IC3** Uses LLMs or LLM-based agents to generate code.
- **IC4** Falls in the core or contextual tier (§1).
- **IC5** Primary contribution: benchmark/dataset, generation method/agent/training approach, or empirical study.

Exclusion (any; recorded as reason code):
- **EC1** Issue resolution, bug repair, or edit/feature addition to an existing repository.
- **EC2** Repository-dependent completion or generation evaluated only by similarity or other non-executable measures (e.g., exact match, CodeBLEU, human-labelled reuse).
- **EC3** Isolated code generation (no repository dependency).
- **EC4** Output is not source code (docs, tests only, review, QA, repository understanding).
- **EC5** Not LLM-based.
- **EC6** Secondary study (survey, SLR, position), editorial, thesis, tutorial. Secondary studies are logged separately as related work.
- **EC7** Duplicate or earlier version of an included study.
- **EC8** Insufficient information to determine task and evaluation (e.g., 2-page abstract).
- **EC9** Out of time window / not English / no full text.
- **EC0** Off-topic (term collision, e.g., "repository" in a non-SE sense).
- **EC10** Not a research article (dataset/software deposit, replication package, podcast episode, whitepaper).

Preprints are included and flagged; peer-review status is recorded and re-checked before submission.

## 6. Procedure

1. **Identification:** run all families on all sources; store raw exports and the log (source, family, date, hits).
2. **Deduplication:** DOI → arXiv ID → normalised title. Preprint and published version = one study; the peer-reviewed version is canonical.
3. **Title/abstract screening:** include / exclude (reason) / unsure. Unsure goes to full text.
4. **Full-text eligibility:** final decision with reason code.
5. **Snowballing (Wohlin):** backward (references) and forward (citations via OpenAlex) on all included studies; new candidates pass steps 3–4; iterate until no new inclusions.
6. **Quality assessment and data extraction** on the final set (§8).

**Reviewers.** Reviewer 1 (first author, LLM-assisted, see §10) screens all records; reviewer 2 (co-author) independently checks all inclusions and a random sample of exclusions. Agreement is reported (Cohen's κ); disagreements are resolved by discussion.

## 7. Outputs

`data/search_log.csv` (identification), `data/records.csv` (deduplicated), `data/screening.csv` (decisions, reason codes, reviewer columns), `data/snowball.csv`, `data/corpus.csv` (final set), and PRISMA counts from `prisma.py`.

## 8. Quality assessment and extraction

QA is used to weight evidence, not to exclude studies (a new preprint has no citations yet by definition). Dimensions (0/1/2): task definition clarity; dataset provenance; evaluation validity (executable, validated); experimental detail; artefact availability; threats/contamination analysis; comparative evidence (baselines, ablations, controlled comparisons).

Extraction fields: metadata, publication status, tier, task type, input specification, initial workspace, output boundary, languages, benchmark source/size, oracle type, metrics, structural coupling to reference, system design dimensions (retrieval, planning representation, agents, feedback loop, memory), contamination defences, reported limitations.

## 9. Quasi-gold set

The known in-scope studies from the preliminary review (the author's 15-paper draft plus studies identified during preliminary reading), each verified against its primary source. It is used only to measure search recall. Studies are not added to the corpus by virtue of being in the gold set; they must be retrieved by the search or snowballing and pass screening like any other record. List: `data/gold_set.csv`.

## 10. Use of LLMs

LLM assistance (Claude) is used for (i) implementing the search/deduplication scripts, (ii) a first-pass title/abstract and full-text screening against the criteria above, with a reason code per decision, and (iii) drafting extraction entries. All inclusions and a random sample of exclusions are verified by human reviewers, and agreement is reported. This is disclosed in the paper.

## 11. Deviations log

| Date | Change | Reason |
|---|---|---|
| 2026-09-30 | Removed "0-to-1" and "zero-to-one" from WHOLE_REPO (pilot) | Tokenised as "0 to 1": 2,230 OpenAlex hits, mostly probability/score ranges. In-scope 0-to-1 papers are still matched by other terms (e.g., "software generation"). |
| 2026-09-30 | Added "non-standalone", "project-specific", "real-world repositories", "real-world code repositories", "real-world projects" to REPO_SCOPE | Quasi-gold check: CoderEval was missed because it describes repository dependence without the term "repository-level". About 125 extra OpenAlex hits. |
| 2026-09-30 | arXiv: first block of each family executed as one sub-query per term, results unioned | The arXiv API returns HTTP 503 for the full-length query. Logically equivalent; no change to search semantics. |
| 2026-09-30 | Added reason code EC10 | OpenAlex returns non-article records (Zenodo deposits, podcasts) that are not covered by EC0–EC9. |
| 2026-09-30 | EC2 broadened from "pure completion evaluated by similarity" to any repository-dependent completion/generation without execution-based evaluation | Full text showed repository-dependent generation papers without executed tests (e.g., A3-CodGen); the contextual tier requires execution-based evaluation, so these share the EC2 rationale. |
| 2026-09-30 | Core tier requires a multi-file artefact; single-file applications (e.g., one self-contained index.html) are EC3 | Keeps the core/isolated boundary operational; raised by GameASG-Bench. |
| 2026-09-30 | Title-stage audit: 191 records excluded as EC0 whose titles contain software/code terms were returned to abstract screening | Gold-set tracing showed 3 in-scope studies (NL2Repo-Bench, ReCUBE, FeatLens) lost at the title stage through manual list errors. Title-stage EC0 is now applied only to titles without any software/code term. |
| 2026-10-01 | Language restriction (IC2/EC9 "not English") dropped | LLM-assisted screening reads non-English papers. The two records excluded only for language were re-screened in the original language: the Korean JKIIT paper (EC8, closed access, insufficient abstract) and the Slovenian CODORQ paper (EC1). |
| 2026-10-01 | Reliability check replaces the planned human reviewer 2 | No second human reviewer is available. A blind second LLM rater using a different model re-screened a stratified random sample: abstract stage n=300, κ=0.85; full text n=100, κ=0.78. A third pass resolved the 16 disagreements; 15 upheld the first decision. SimulatorCoder was excluded (EC3), and two abstract-stage reason codes were corrected (EC8→EC0, EC8→EC3). Data: data/reliability/. |
| 2026-10-01 | Venue status corrected for 6 studies | Crossref showed publication venues for CodeS, ProjectGen (TOSEM), ProjectEval (Findings ACL 2025), MultiAgent-FrontEnd (MSR 2026), PaperBench (ICML 2025) and Commit0 (ICLR 2025). |
| 2026-10-01 | Claim verification | Every statement in the draft was checked against the cited full text. 122 of 354 were flagged and then corrected or removed. Ledgers: notes/claim_ledgers/. |
