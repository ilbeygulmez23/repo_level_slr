# Claim verification for the survey draft

The survey is in `survey/sections/*.tex`. The supervisor's main feedback is that every claim must rest on evidence. They also raised two specific concerns:
1. The studies evaluate different model generations, such as GPT-4-era models in 2023–24 versus GPT-5- or Claude-4.x-era models in 2025–26. The draft pools their findings as if they had tested the same models.
2. Many studies are not peer-reviewed. Before the draft builds an argument on a result, someone has to check how that result was measured. A "counter-example" may simply reflect a flawed measurement.

## Resources
- `survey/generated/keys.csv` maps each bib key to a record key (`short,bibkey,tier,task,key`).
- Full texts are in `slr/data/fulltext/<key with ':' and '/' replaced by '_'>.txt`. Example: `arxiv:2302.00288` becomes `arxiv_2302.00288.txt`.
- `slr/data/corpus.csv` holds venue and peer-review status (column `venue`; `preprint` if not peer-reviewed).
- `slr/corpus_notes.md` holds per-study notes. They are LLM-drafted, so do not trust them; always confirm against the full text.
- For cited works not in the corpus, look in `survey/extra.bib` and `survey/generated/corpus.bib`.

## Task
Go through every sentence in your assigned section(s) that makes a factual statement about a study or about the corpus. This includes numbers, findings, causal or comparative claims, and characterisations such as "X uses Y" or "X finds Z". For each one, open the full text and check it.

Write a ledger to `ledger/<section>.md` with one entry per claim:

```
### C<n> — <bibkey(s)>
- Draft: "<the sentence or clause as written>"
- Verdict: VERIFIED | CORRECTED | NOT FOUND | MISLEADING | NO FULL TEXT
- Evidence: "<short exact quote from the full text>" (section/table)
- Correct statement: <only if not VERIFIED>
- Models: <models evaluated for this result, with approximate release year>
- Measurement: <how the number or finding was computed: oracle, n tasks, runs, judge model; any validity concern>
- Status: <venue, or preprint>
```

Then add a section `## Cross-study claims` covering each sentence that generalises across studies, such as "X is the most consistently supported intervention", "the dominant problem is ...", "structure is not uniformly beneficial", or "headline numbers overstate progress". For each one, say whether the cited evidence supports it once model generation, measurement validity and peer-review status are taken into account. Propose a defensible rewording that states only what the evidence supports, with the needed qualifier (for example: "in two preprints evaluating GPT-4-era models, ...").

Finally, add `## Unsupported` listing claims that have no citation, or no evidence in the cited source, together with a suggested fix (cite, weaken, or delete).

Be exact and terse. Do not edit the .tex files.
