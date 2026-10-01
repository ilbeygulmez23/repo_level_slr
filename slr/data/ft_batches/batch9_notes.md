### GameASG-Bench — GameASG-Bench: Benchmarking Autonomous Software Generation for Game Development (preprint, 2026) [arxiv:2609.21293]
Benchmark + empirical çalışma: NL gameplay spec'ten browser-native, çalıştırılabilir bir oyun (tek self-contained `index.html`) üretilmesini değerlendiriyor. Asıl fikir "testability'yi generation task'ın parçası yapmak": evaluation interface spec'i (`window.__gameTest`: reset / loadScenario / input / getSnapshot) generation'dan ÖNCE sabitleniyor, agent oyunu bu interface ile birlikte implemente ediyor.
Her task'ta üç doküman var (target.md prompt, game-spec.md gameplay requirement, tdd.md evaluation interface). 47 task, 12 genre, 32 2D / 15 3D. Değerlendirme iki katmanlı: L1 source-level (336 check, çoğu regex) ve L2 headless Chromium'da prepare-act-observe behavioral check'ler (885 check; 102 P0, 534 P1, 249 P2), semantic snapshot + gerçek mouse/keyboard input + Canvas/WebGL runtime evidence. Ana metrik strict task success: tüm L1 + tüm applicable L2 P0/P1 geçmeli. Her task'ın insan tarafından doğrulanmış reference implementation'ı var; 47/47 reference kabul ediliyor. Harness: Claude Code ve Codex CLI, her konfigürasyon tek run.
Findings:
- 9 agent stack'te L1 %97.7–99.6 iken strict success %14.9–55.3; en iyi GPT-6-Astra/Codex CLI 26/47, Claude-Opus-5 24/47, en düşük MiniMax-M3 7/47.
- Ortalama check pass rate ile strict success sıralamaları ayrışıyor (GPT-5.6-Sol L2 %91.3 > Opus %90.4 ama 21 vs 24 strict).
- DeepSeek-V4-Flash'ta full tool access 18/47, kısıtlı tool'larla 6–9; turn budget 30→120 ile 7→18.
- Reasoning effort non-monotonic: high 19/47, max 18/47 (%26.9 daha az reasoning token ile).
- Claude Code ve Codex CLI ikisi de 18/47 ama sadece 10 task ortak — harness choice aggregate'te görünmeyen varyans yaratıyor.
Relevant Limitations:
- Output tek dosya `index.html`; "multi-file repository" kapsamının sınırında, mimari/modülerlik ölçülmüyor.
- Evaluation interface semantics'i (snapshot field'ları, scenario isimleri) önceden dikte ediliyor; private implementation serbest olsa da interface'e bağlılık alternatif tasarımları kısıtlıyor. L1 regex check'leri yüzeysel (yorum/string'de de match olur, yazarlar kabul ediyor).
- Test'ler insan yazımı (LLM-judge yok, artı), ama her konfigürasyon tek run — varyans raporlanmamış; harness farkı gürültüden ayrılamıyor.
- Scale küçük: 47 task, tek domain (browser oyunları), JS/HTML.
Key Takeaway:
- "Test interface'ini spec'in parçası olarak önceden ilan et" yaklaşımı, reference-implementation'a bağlı white-box test sorununa yapılandırılmış (executable contract) bir cevap; survey'de spec-as-contract örneği olarak kullanılabilir.
- Ortalama pass rate yerine strict/all-required metrik raporlamanın gerekliliğini net gösteriyor.

### Generative Compilation — Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code (preprint, 2026) [arxiv:2607.13921]
Method çalışması: LLM decoding sırasında partial program'ı "sealor" ile derlenebilir hale getirip rustc diagnostic'lerini generation bitmeden modele geri veriyor; black-box modellerle çalışıyor, Featherweight Rust üzerinde Lean'de soundness/completeness ispatı var.
Değerlendirme iki repo-level Rust task'ında, Agentless-benzeri sabit harness ile: Translation (CRUST-Bench'in 20 zor instance'ı, C library'si dosya dosya Rust'a çevriliyor, üretilen dosya golden solution repo'ya gömülüp unit test'lerle test ediliyor) ve UpdatedAPI (son 6 ayda API'si değişen crate'ler için GPT 5.3/Codex ile üretilip manuel filtrelenmiş 30 single-file crate, ort. 5.9 fonksiyon body, ort. 3.23 test). Metrikler: compiler error rate ve functional correctness; 7 model (Opus 4.8, GPT 5.3 Codex, Gemini 3.5 Flash, Kimi K2.7, GLM 5.2, Qwen 3.5 397B/9B), 2 sample.
Findings:
- Ortalama compiler error: LLM %65.9 → PC %20.7 → GC %13.1; 14 konfigürasyonun 9'unda PC'ye karşı anlamlı iyileşme.
- Functional correctness 14'ün 11'inde en iyi GC; örn. GLM 5.2 UpdatedAPI %53.3→%71.7, Kimi K2.7 Translation %39.9→%53.9. Frontier modellerde kazanç küçük (Opus Translation 61.0→62.3).
- Runtime overhead 233s'den 135s'ye düşüyor.
Relevant Limitations:
- Repo-context bağımlılığı var ama sınırlı: Translation'da interface'ler sabit, UpdatedAPI benchmark'ı LLM ile üretilmiş ve küçük (30 task, ~3 test).
- Katkı decoding/feedback mekanizması; repo generation kapasitesi değil. Sadece Rust.
Key Takeaway:
- Compiler'ı generation döngüsünün içine almak zayıf/open-weight modellerde belirgin fayda sağlıyor; repo-level pipeline'larda feedback granularity'si bir tasarım parametresi.

### HCAG — HCAG: Hierarchical Abstraction and Retrieval-Augmented Generation on Theoretical Repositories with LLMs (preprint, 2026) [arxiv:2603.20299]
Method çalışması (+ post-training için dataset): algorithmic game theory (AGT) domain'inde NL senaryo tanımından tam, çalıştırılabilir agent-based simulation framework üretmek için hierarchical RAG + multi-agent discussion.
Offline fazda LLM, repo'ları (OpenSpiel, GLEE-sim vb.) ve teorik metinleri recursive olarak özetleyip multi-level knowledge base kuruyor; online fazda top-down retrieval ile architectural skeleton seçiliyor, sonra modüller Match/Generate/Decompose ile bottom-up dolduruluyor ("architecture-then-module"). Task'lar haber metinlerinden LLM ile sentezlenmiş 100 oyun senaryosu. Metrikler: Code Quality (ayrı bir "expert LLM" judge, 0–1), Text Similarity (golden reference'a edit similarity), Requirement Pass Rate (simülasyon ortamında çalıştırma + agent davranışının stratejik dinamiklere uyumu), Average Time. Baseline'lar: RepoCoder, CodeRAG, ARKS, PKG, LLM-understand vb.; ana deney GPT-5.2.
Findings:
- HCAG (depth 4) CQ 0.788, TS 0.525, RPR 0.60; en iyi baseline llm-understand RPR 0.48, CodeRAG 0.32, RepoCoder 0.36.
- Maliyet yüksek: HCAG 3235s vs RepoCoder 2135s, düz baseline 48s.
- Multi-agent debate RPR'yi 0.53→0.63'e çıkarıyor (5 agent, 20 round; süre ~5200s).
- HCAG verisiyle fine-tune RPR 0.55→0.61.
Relevant Limitations:
- Ölçüm büyük ölçüde LLM'e bağlı: task'lar LLM-sentezli, ground-truth trace'ler LLM üretimi, CQ LLM-judge; RPR'nin "semantic fidelity" kısmının nasıl karar verildiği belirsiz.
- TS golden reference'a benzerlik ölçüyor — retrieval-ağırlıklı yöntemi ödüllendiriyor, alternatif tasarımları cezalandırıyor.
- Raporlama tutarsız: Table 2'deki hierarchical-4 satırı Table 1'deki GPT-5.2 sonucuyla birebir aynı, oysa ablation'ların DeepSeek-R1 ile yapıldığı söyleniyor; base-model satırları (0.53/0.55/0.54) birbirini tutmuyor. Dil, repo boyutu, test detayı raporlanmamış.
- Tek domain (AGT); dataset "will be open-sourced".
Key Takeaway:
- Architecture-first scaffolding + hierarchical retrieval, sıfırdan repo üretiminde plan-then-fill paradigmasının bir örneği; ama evaluation zayıf ve LLM-coupled, sonuçlar ihtiyatla alınmalı.
