# Style guide for the revision

The supervisor's feedback on the draft:
- It is verbose and reads as AI-generated. They want short, on-point papers with minimal buzzwords and no repetition.
- Every claim must rest on cited evidence.
- Cross-study claims must respect differences in model generation and in measurement validity.

Two frameworks govern the revision:
- **Structure:** Kitchenham & Charters' SLR report structure and the PRISMA 2020 checklist.
- **Sentences:** Gopen & Swan, "The Science of Scientific Writing" (1990), and Williams, *Style*. Put old information first and new information in the stress position at the end of the sentence. Make the actors the subjects and the actions the verbs. Each paragraph opens with a topic sentence that states its claim.

## Hard rules
1. **No run-in labels or slogans.** Do not use `\paragraph{Gap.}`, `\paragraph{Why two tiers.}`, `\textbf{Relevant beats more.}`, "The lesson is ...", "The pattern is ...", "Two caveats apply." or "Three weaknesses recur:". A paragraph starts with a full topic sentence. Use `\subsection` only for real subsections.
2. **Bullets only for genuinely parallel enumerations of three or more short items** that a reader would scan. Never use bullets to list examples that support a claim. Write one sentence citing them, or use a table if numbers are compared.
3. **One claim, one place.** State each fact once. Elsewhere, point to it with a reference (Section~\ref{...}, Table~\ref{...}). Do not restate findings in section openers or closers. No closing summary sentences such as "Taken together, ...".
4. **Every factual statement about a study carries its \cite.** Every number matches the ledger in `ledger/<section>.md`. Use the "Correct statement" whenever the verdict is not VERIFIED. Drop claims marked NOT FOUND. Rewrite claims marked MISLEADING.
5. **Qualify cross-study claims by their evidence base.** State how many studies support the claim, and whether that evidence is controlled or uncontrolled. Where it matters, add the model generation (e.g., "with GPT-4-era models") and whether the source is a preprint. Do not generalise from 2023–24 models to current agents without saying so. If a counter-result rests on a weak measurement, say that in one clause instead of presenting it as established.
6. **Confident, not defensive.** Say what was done and what the evidence shows. Do not stack hedges or over-state threats. One accurate qualifier is better than three vague ones.
7. **No buzzwords or mannerisms.** Avoid: "central", "first-order", "crucially", "notably", "landscape", "paradigm", "holistic", "robust" (unless technical), "we caution", "instructive", "at first sight", "it is worth noting", em-dash asides, "not X but Y" framing, colon-then-reveal, and scare quotes around invented labels.
8. **Short sentences, concrete subjects.** Aim for at most about 25 words per sentence and at most about 5 sentences per paragraph.
9. **Tool names.** Do not name the LLM vendor or model used for the review itself. Say "LLM agents".
10. **Keep the LaTeX.** Keep `\cite` keys, `\label`s, `\ref`s, the macros from generated/numbers.tex, and the table environments compiling. Tables may be trimmed. Do not invent new bib keys.

## Length targets (words, excluding tables)
| Section | Target |
|---|---|
| abstract | ≤ 200 |
| introduction | ≈ 450 |
| background | ≈ 350 |
| methodology | ≈ 1400 |
| overview | ≈ 250 |
| rq1 | ≈ 650 |
| rq2 | ≈ 750 |
| rq3 | ≈ 950 |
| rq4 | ≈ 950 |
| synthesis | ≈ 650 |
| threats | ≈ 300 |
| conclusion | ≈ 150 |

## Fact ownership (where each topic lives; elsewhere refer to it)
- Corpus counts by year, tier, task, language, and venue: overview.
- Task taxonomy and specification specificity: rq1. Benchmark scale table: rq2.
- Oracle taxonomy, partial credit, evasion, LLM judges: rq3. Leakage and contamination: rq2.
- Design interventions and evidence map: rq4. Hand-off hypothesis and agenda: synthesis only.
- Abstract and introduction give at most one headline result each, without repeating rq numbers in full.
