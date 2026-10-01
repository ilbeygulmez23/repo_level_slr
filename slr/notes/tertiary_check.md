# Tertiary check: existing secondary studies (PARTIAL, 2026-09-30)

Status: incomplete. The arXiv API rate-limited the search and OpenAlex/web searches did not run. IDs, titles and first authors below were confirmed via the arXiv API; overlap notes come from prior knowledge and must be checked against the full texts. The same secondary studies will also surface in the main search (EC6); re-run a dedicated `ti:survey` search before claiming a gap.

| ID | First author | Year | Title | Overlap |
|---|---|---|---|---|
| 2510.04905 | Tao | 2025 | Retrieval-Augmented Code Generation: A Survey with Focus on Repository-Level Approaches | **Closest.** Covers repository level through retrieval; likely no 0-to-1 generation or evaluation validity. |
| 2508.00083 | Dong | 2025 | A Survey on Code Generation with LLM-based Agents | Close. Agent-centric and broad. |
| 2505.05283 | K. Wang | 2025 | SDLC Perspective: A Survey of Benchmarks for Code LLMs and Agents | Close for benchmarks; an inventory, not a validity analysis. |
| 2510.09721 | Guo | 2025 | Survey on Benchmarks and Solutions in SE of LLM-Empowered Agentic Systems | Moderate. |
| 2510.12399 | Ge | 2025 | A Survey of Vibe Coding with LLMs | Moderate. |
| 2609.12012 | Liang | 2026 | Test-Driven Approaches to SE with LLMs: A Survey | Check. Tests as specifications. |
| 2409.02977 | J. Liu | 2024 | LLM-Based Agents for SE: A Survey | Moderate; corpus ends mid-2024. |
| 2409.09030 | Y. Wang | 2024 | Agents in SE: Survey, Landscape, and Vision | Low–moderate. |
| 2408.02479 | Jin | 2024 | From LLMs to LLM-based Agents for SE | Low–moderate. |
| 2406.00515 | J. Jiang | 2024 | A Survey on LLMs for Code Generation | Low–moderate. |
| 2408.16498 | L. Chen | 2024 | A Survey on Evaluating LLMs in Code Generation Tasks | Low–moderate. |
| 2503.01245 | Huynh | 2025 | LLMs for Code Generation: A Comprehensive Survey | Low. |
| 2312.10101 | Schonholtz | 2023 | A Review of Repository Level Prompting for LLMs | Low; precursor. |
| 2512.22256 | Z. Jiang | 2025 | Agentic Software Issue Resolution with LLMs: A Survey | Out of scope; cite to justify EC1. |
| 2505.08903 | Hu | 2025 | Assessing and Advancing Benchmarks for Evaluating LLMs in SE Tasks (TOSEM) | Benchmark inventory. |

To verify: Hou et al. TOSEM 2024 (2308.10620); He et al. multi-agent SE (2404.04834); any 2026 surveys on repo-level completion or AI software engineers.

Draft gap statement (pending verification): existing secondary studies cover repository context for retrieval/completion, LLM agents for SE broadly, or benchmark inventories. None systematically synthesises whole-repository generation from specifications together with its planning/design representations and the validity of its execution-based evaluation.
