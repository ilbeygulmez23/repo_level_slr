# Example surveys (advisor's models): study-selection methodology

Extracted 2026-09-30 from full texts (arXiv versions).

## Hu et al., TOSEM, DOI 10.1145/3786771 (arXiv 2505.08903v4)
- SLR per Kitchenham; Wohlin snowballing. RQs: what benchmarks exist / how created / challenges. Final: 291 benchmarks.
- Base = papers from 3 prior LLM4SE SLRs (Fan, Hou, Zhang) + supplementary search reusing Hou et al.'s strings (not reproduced).
- Libraries: IEEE Xplore, ACM DL, ScienceDirect, Springer, Wiley, Elsevier, Google Scholar, DBLP, arXiv. Window: before June 2025; no start date; no search date.
- **No counts at any stage**; no dedup reported. IC1–IC7 / EC1–EC4 (English; peer-reviewed or arXiv; new SE benchmark; used for LLMs; fully described).
- Title/abstract/keywords then full text; "two authors independently assessed"; no kappa.
- Snowballing backward+forward to saturation by two authors, third adjudicates.
- QA: 10 questions (clarity, SE relevance, rigor, reproducibility, impact); no scale.
- Extraction: author/year/source, focus, benchmark description, methodology, limitations, adoption, availability.
- No PRISMA diagram. Threats: construct/internal/conclusion/external. No LLM use stated.

## Wang et al., arXiv 2505.05283v3 (SDLC benchmark survey)
- RQs: SDLC coverage / distribution & imbalances / future directions. Result: 178 benchmarks from 461 papers.
- Databases: IEEE Xplore, ACM DL, ScienceDirect, Springer (+ Google Scholar in threats). From 2022; no end/search date.
- 20 keyword combinations (no Boolean strings, fields unstated).
- Counts: 1,347 retrieved → 321 after manual filtering → +140 snowballing → 461.
- Selection prioritises top venues and, for arXiv, citations/GitHub stars (coverage bias).
- QA: two co-authors independently, third resolves; criteria unstated; no kappa.
- Tiered analysis framework (general + stage-specific dimensions) instead of an extraction form.
- Process figure, not PRISMA. Threats: construct/internal/external. No LLM use stated.

## Common denominator (what reviewers expect)
Explicit RQs; Kitchenham; named databases; time window; explicit criteria; backward/forward snowballing; two reviewers + adjudication; quality assessment; extraction scheme + public artifact; process figure; threats to validity.

## Where we can be stricter than both
Verbatim Boolean strings per database; search execution date; per-stage PRISMA counts with reason codes; explicit dedup; inter-rater agreement; recall check against a quasi-gold set; disclosed LLM assistance.
