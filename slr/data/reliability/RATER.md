# Independent second screening (blind)

You are an independent second screener for a systematic literature review on LLM-based repository-level code generation. You must NOT look at any earlier screening decisions. Do not open these files: `slr/data/screening.csv`, `slr/data/corpus.csv`, `slr/corpus_notes.md`, anything in `slr/data/ft_batches/` except `FT_CRITERIA.md`, `slr/data/abs_batches*/`, `slr/data/snow*_batches/`, or anything under `survey/`. Do not search the web.

Criteria: read the "Scope" and "INCLUDE / EXCLUDE / Borderline rules" sections of `slr/data/ft_batches/FT_CRITERIA.md`. Ignore its "Output" section; use the output format below. Two additional codes:
- EC9: outside 2022-01-01 to 2026-09-30, or not in English.
- EC10: not a research article (dataset or software deposit, podcast, whitepaper).

Additional rules, both part of the protocol:
- The core tier requires a multi-file artefact. A single-file application, such as one self-contained index.html, is EC3.
- The contextual tier requires executed tests. Repository-dependent generation evaluated only by similarity, human rating or other non-executable measures is EC2.

## Abstract stage (files abs_b*.csv)
Decide from the title and abstract only:
- `include`: clearly meets all criteria.
- `unsure`: plausibly in scope, but the abstract does not settle it. Unsure records go on to full text.
- `exclude`: clearly fails a criterion. Give the most specific EC code.

## Full-text stage (files ft_b*.csv)
Read the text file at `fulltext_path`: abstract, introduction, task or benchmark definition, and evaluation. Decide:
- `include`, with tier `core` or `contextual`; or
- `exclude`, with an EC code.

## Output
Write the output CSV with Python's csv module, one row per input row, with columns `key,decision,reason,tier,justification`. The justification is 20 words at most. Save it next to the input file as `<input name>_r2.csv`.
