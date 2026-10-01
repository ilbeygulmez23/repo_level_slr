# Full-text eligibility + light extraction (reviewer 1)

You get a batch CSV with columns `key, title, abs_decision, tier, note, text_file`. `text_file` is a plain-text extraction of the paper's PDF; it is empty if no open full text was found. Read the abstract, introduction, task/benchmark definition, and evaluation sections of each paper. Skim the rest. Skip references.

## Scope (same as screening; now decide definitively)

**CORE tier:** an LLM or agent produces a multi-file repository, library or application. This covers:
- NL / spec / README / requirements / paper → repository or app (web apps, microservices, CLI tools, games, SaaS)
- skeleton/stubs → library
- executable or API reference → behaviourally equivalent repository (reconstruction/reproduction)
- whole repository → repository translation or modernisation
- methods, agents and training environments or data for these
- empirical studies of such systems

**CONTEXTUAL tier:** an LLM generates a function, class or file whose correctness depends on the surrounding repository (cross-file dependencies, project APIs) AND is evaluated by executing tests.

**INCLUDE** only if all of these hold:
- English, first public 2022 or later
- uses LLMs or LLM agents
- falls in the core or contextual tier
- the primary contribution is a benchmark/dataset, a method/agent/training approach, or an empirical study
- the task and evaluation are described well enough to extract

**EXCLUDE** codes (most specific):
- **EC1:** edits, feature addition, issue resolution, repair, refactoring, optimisation, or in-place migration of an EXISTING repository
- **EC2:** pure code completion evaluated only by similarity
- **EC3:** isolated generation, no repository dependency
- **EC4:** output is not source code
- **EC5:** not LLM-based
- **EC6:** secondary study, position/vision paper, tutorial, thesis, experience report
- **EC7:** duplicate or version of another study (name the other one in the note)
- **EC8:** insufficient information to determine task/evaluation, or no full text AND the abstract is insufficient
- **EC0:** off-topic

**Borderline rules:**
- **Mixed benchmarks** (e.g., issue fixing plus a doc→repo subset): include only if the repository-generation part is a substantive, separately reported component. Otherwise exclude with EC1.
- **Multi-agent "software development" frameworks** (ChatDev/MetaGPT-style): include as core if they generate complete, multi-file software and evaluate it.
- **Completion benchmarks:** contextual include only if they use executable tests.
- **No full text:** decide from the abstract. If undecidable, use EC8 and state "no full text" in the note.

## Output

Write `batchN_ft.csv` using Python's csv module, with exactly one row per input row. Columns:

| Column | Values |
|---|---|
| `key` | as given |
| `ft_decision` | include / exclude |
| `ft_reason` | EC code if excluded, else empty |
| `tier` | core / contextual (include only) |
| `task` | one of: `repo-context-gen`, `skeleton-to-library`, `nl-to-repo`, `nl-to-app` (web/mobile/game/UI-driven), `paper-to-repo`, `behavioral-reconstruction`, `repo-translation`, `other` |
| `contribution` | semicolon list from: `benchmark`, `method`, `empirical`, `training-data` |
| `languages` | e.g. `Python;Java`, or `multi` if more than 4 |
| `evaluation` | semicolon list from: `reference-unit-tests`, `generated-tests`, `bdd-e2e-tests`, `differential-oracle`, `llm-judge`, `human`, `similarity`, `build-run`, `nonfunctional`, `other` |
| `venue` | peer-reviewed venue if stated in the paper (e.g. "ICSE 2026"), else `preprint` |
| `note` | 25 words max: justification plus anything notable (e.g. "mixed benchmark; doc2repo subset 120 tasks") |

Reply with counts and any rows you found hard, one line each.

## Paper notes (for every INCLUDED paper)

Also write `batchN_notes.md` with one entry per included paper, in the style of the first author's own reading notes. Write in Turkish and keep technical terms in English, as the author does. Be concrete: give numbers, dataset sizes, metrics and model names. Be critical, but only about what the paper actually shows. Do not invent results; if something is not reported, say so.

Format (keep the headings exactly):

```
### <ShortName> — <full title> (<venue or preprint>, <year>) [<key>]
<1–2 cümle: ne tür bir çalışma (benchmark / method / empirical), ne yapıyor>
<Nasıl çalışıyor: input → output, veri kaynağı ve ölçeği, dil(ler), agent/harness, değerlendirme yöntemi ve metrikler>
Findings:
- <en önemli 2–5 bulgu, sayılarla>
Relevant Limitations:
- <1–4 madde>
Key Takeaway:
- <1–2 madde: survey ve sonraki çalışma için ne öğretiyor>
```

For Relevant Limitations, look through the author's research lenses:
- Is the evaluation coupled to a reference implementation (white-box tests, similarity to a reference, reverse-engineered specs)? Would it penalise valid alternative designs?
- Is an LLM used inside the measurement (LLM-judge, LLM-generated tests or specs)? Does the same model family write the spec, the tests and the verdict?
- Are hand-offs free-form natural language, or structured/executable artefacts (contracts, graphs, UML, BDD, tests)?
- Contamination and freshness; benchmark scale (number of independent repositories); language coverage.
- Model/harness confounds, unfair baselines, cost.

Length: roughly 120–250 words for core papers and 70–150 words for contextual papers.

Example of the target style (the author's note on RepoZero, abridged):

```
### RepoZero — RepoZero: Can LLMs Generate a Code Repository from Scratch? (preprint, 2026) [arxiv:2605.07122]
Agent'a kaynak reponun API spec'i + 4 white-box test örneği veriliyor, repoyu başka bir dilde sıfırdan yeniden implemente etmesi isteniyor. Doğrulama, kaynak repo ile üretilen reponun çıktılarının string-level eşleşmesi.
Test üretimi tamamen otomatik ve oracle-doğrulamalı: LLM test case üretiyor, her case kaynak repoda 20 kez çalıştırılıyor; non-deterministik olanlar atılıyor.
Findings:
- Çoğu model %20-40 bandında; Mini-SWE-Agent, OpenHands'i tutarlı şekilde geçiyor.
- Üretilen çalıştırılabilir kodun ~%40'ı kaynak reponun deterministik çıktısını tutturamıyor.
Relevant Limitations:
- Harici paket yasağı yapay; strict string-level eşleşme formatı farklı ama doğru çözümleri cezalandırıyor.
Key Takeaway:
- Referans repoyu oracle olarak kullanmak, insan emeği olmadan doğrulanmış test üretmenin yolu.
```
