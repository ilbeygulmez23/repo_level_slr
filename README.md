# Replication package: LLM-based repository-level code generation, a systematic literature review

This repository contains the search, screening, reliability, and extraction data for the systematic literature review *Repository-Level Code Generation with LLMs: A Systematic Literature Review*. It also contains the scripts that produce every number reported in the paper.

The review follows Kitchenham and Charters (2007), Wohlin's snowballing guidelines (2014), and PRISMA 2020. It covers studies published between 1 January 2022 and 30 September 2026. The final corpus holds 175 studies: 103 core-tier studies, in which a model builds a multi-file repository, and 72 contextual-tier studies, in which a model generates repository-dependent code that is judged by executing tests.

## Layout

| Path | Content |
|---|---|
| `slr/protocol.md` | Review protocol: scope, research questions, sources, criteria, and the deviations log. |
| `slr/queries.json` | Database-agnostic query definition (three families of OR-ed term blocks). |
| `slr/queries_rendered.md` | The exact query strings issued to arXiv, OpenAlex, IEEE Xplore, and the ACM Digital Library. |
| `slr/data/raw/` | Raw API results from arXiv, OpenAlex, and the five snowballing rounds (JSONL). |
| `slr/data/manual/` | IEEE Xplore and ACM DL results (title, DOI, year) and the manual search log. |
| `slr/data/records.csv` | All 2,420 deduplicated records, with stable record keys. |
| `slr/data/screening.csv` | The decision and reason code for every record at the title, abstract, and full-text stages. |
| `slr/data/gold_set.csv` | The 31-study quasi-gold standard used to measure search recall. |
| `slr/data/*_batches/` | Screening batches: inputs and per-record decisions with justifications. |
| `slr/data/ft_batches/FT_CRITERIA.md` | The screening instrument (criteria, borderline rules, output schema). |
| `slr/data/ft_batches/adjudication.md` | Adjudication log for borderline full-text decisions, with a rationale for each. |
| `slr/data/reliability/` | Blind second screening of a stratified sample, Cohen's κ script, disagreements and their resolution, and the re-screening of non-English records. |
| `slr/data/corpus.csv` | Final corpus with tier, task type, contribution, languages, evaluation codes, venue, and quality flags. |
| `slr/corpus_notes.md` | Structured extraction notes for each included study. |
| `slr/notes/claim_ledgers/` | Verification of every claim in the paper against the cited full texts. |
| `survey/generated/` | Numbers, corpus table, and BibTeX generated for the paper. |

## Reproducing the pipeline

The scripts need Python 3.10+ with `requests` and `pypdf`. Run them from `slr/`. OpenAlex asks API users to identify themselves, so set `OPENALEX_MAILTO` to your e-mail address first.

```
export OPENALEX_MAILTO=you@example.org
python3 render_queries.py     # queries.json -> database-specific strings
python3 search.py             # arXiv and OpenAlex search -> data/raw/
python3 merge.py              # merge all sources and deduplicate -> data/records.csv
python3 sync_screening.py     # keep existing decisions, list new records
python3 fetch_fulltext.py     # download open full texts (not redistributed here)
python3 find_arxiv.py         # look up arXiv preprints for closed-access records
python3 snowball.py <round>   # backward and forward snowballing via OpenAlex
python3 collect_ft.py         # full-text decisions + adjudication -> corpus.csv, corpus_notes.md
python3 prisma.py             # PRISMA 2020 counts
python3 make_tex_data.py      # survey/generated/
```

`prisma.py` and `make_tex_data.py` reproduce every count in the paper from the files in this repository. A search re-run today will return more records than the frozen search did, because the indexes grow; the frozen results are in `slr/data/raw/` and `slr/data/manual/`.

## What is not included

- **Full texts of the screened papers.** They are under their publishers' copyright. `fetch_fulltext.py` downloads the openly accessible ones again.
- **Abstracts from IEEE Xplore and ACM DL exports.** The publishers' terms do not allow redistribution. The exports are reduced to title, DOI, and year, and the CSV files carry no abstract column. Abstracts from OpenAlex and arXiv remain in `slr/data/raw/` under CC0.
- **The ACM DL result pages.** These were saved as HTML because exporting is paywalled; only the DOIs resolved from them are included.

## LLM assistance

Screening and extraction were carried out by LLM agents working from the written instrument in `slr/data/ft_batches/FT_CRITERIA.md`. Every decision carries a reason code and a justification. The paper's methodology section describes the adjudication and reliability procedure, and `slr/data/reliability/` contains its data.

## License

Code is released under MIT. Data and documentation are released under CC BY 4.0. See `LICENSE`.
