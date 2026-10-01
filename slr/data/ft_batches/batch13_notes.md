### KoCo-Bench — KoCo-Bench: Can Large Language Models Leverage Domain Knowledge in Software Development? (preprint, 2026) [arxiv:2601.13240]
Benchmark + empirical çalışma: domain specialization yöntemlerini (SFT, LoRA, RAG, kNN-LM, agent'lar) framework bilgisi gerektiren repo-içi code generation üzerinde ölçüyor.
6 domain, 11 framework (knowledge corpus: doc + source + example), bu framework'ler üzerine kurulu 25 Python projesi. Ana görev: proje context'i içinde 131 core function'ı description + signature'dan üretmek; 978 test (fonksiyon başına ort. 8.6 unit test, proje başına 2.3 integration test). Metrikler Pass@1 ve AvgPassRate. Ayrıca 107 multiple-choice Q&A. Project-level generation (project description + module division → tüm proje) sadece Appendix B'de kalitatif olarak inceleniyor.
Findings:
- Base LLM'ler ortalama Pass@1 %3–9 (Kimi-K2 8.9, Gemini-2.5-pro 8.5); RAG domain'inde tüm modeller 0.
- SFT/LoRA/RAG/kNN-LM Qwen2.5-Coder-7B üzerinde marjinal ya da negatif etki (base 7.5 → RAG 7.4).
- Claude Code (Sonnet 4.5) Pass@1 %34.2, ama örnek başına ~620K token; SWE-agent/OpenHands (Qwen-32B) %4.5/%3.6.
- En sık hata: framework API hallucination ve domain data constraint ihlali.
Relevant Limitations:
- Değerlendirme fiilen function-level; proje seviyesi sayısal olarak raporlanmıyor.
- Eksik unit testler Claude Code ile üretilmiş (input'lar insan yazımı, ground-truth'a karşı doğrulanmış); en iyi sonuç da Claude Code'dan geliyor — aynı model ailesi.
- Fonksiyon testleri white-box/instrumentation tabanlı olabiliyor; ölçek küçük (25 proje).
Key Takeaway:
- "Knowledge corpus + test set" ayrımı, yeni framework'lere adaptasyonu ölçmek için iyi bir tasarım; repo-level'da domain bilgisi hâlâ darboğaz.

### cJSON→Rust Porting — LLM-Assisted Porting of Security-Critical C Libraries to Idiomatic Rust: A Multi-Model Empirical Study (Future Internet, 2026) [doi:10.3390/fi18090471]
Empirical case study (full text yok, abstract'tan): tüm cJSON C kütüphanesinin (~3200 LOC, 14 CVE) agentic modda idiomatic Rust'a port edilmesi; manuel uzman port'u baseline.
Beş LLM (Claude Opus 4.6, Gemini 3 Pro, GPT-5.4, Kimi K2.7-Code, Qwen3.5-27B) bağımsız port üretiyor; Kimi 5 kez tekrarlanmış. Doğrulama: CVE-specific testler, coverage-guided ve differential fuzzing (>1.7 milyar execution), Miri, karşılaştırmalı performans benchmark'ı.
Findings:
- Altı port'un hepsi in-scope CVE sınıflarını yapısal olarak elimine ediyor; sıfır unsafe block, sıfır memory-safety crash.
- Kod kalitesi modelden modele çok değişiyor (0–9 kalan bug); bazı model farkları Kimi'nin run-to-run varyansı içinde kalıyor.
- Differential fuzzing manuel ve LLM port'larında birbirini tamamlayan bug'lar buluyor → hybrid workflow önerisi; port başına ~$3.
Relevant Limitations:
- Tek, küçük, single-threaded kütüphane (n=1 repo); genelleme zayıf, yazarlar da bunu belirtiyor.
- Diğer 4 model tek run; harness/prompt detayları abstract'ta yok.
Key Takeaway:
- Kaynak C kütüphanesini differential oracle olarak kullanmak (fuzzing), repo translation için implementation-agnostic, güçlü bir doğrulama yolu.

### ProgramBench — ProgramBench: Can Language Models Rebuild Programs From Scratch? (preprint, 2026) [arxiv:2605.03546]
Benchmark + empirical: agent'a sadece derlenmiş executable (execute-only) ve dokümantasyon veriliyor; source code + build script yazarak aynı davranışı sıfırdan yeniden kurması isteniyor.
200 task, açık kaynak CLI programlarından (Rust 107, Go 46, C/C++ 45, Java 1, Haskell 1; FFmpeg, SQLite, PHP, DuckDB, jq...). Referans reposu medyan 8,635 LOC / 50 dosya. Değerlendirme: Claude Sonnet 4.5 ile çalışan mini-SWE-agent'ın gold binary'yi probe ederek ürettiği behavioural testler (toplam 248,853; medyan 770/task), gold'da deterministik geçmeyen veya dummy binary'de geçen testler atılıyor. Dil serbest. Metrikler: % Resolved (tüm testler) ve % Almost (≥%95). 9 model, mini-SWE-agent, internet kapalı.
Findings:
- Hiçbir model tek bir task'ı tam çözemiyor; en iyi Opus 4.7 %3.0 almost-resolved.
- Farklı dil zorunluluğu Opus'ta düşüş (−8.0), GPT modellerinde artış (+4.2) getiriyor; Python'a kayış.
- İnternet açıkken cheating %20–36 (çoğu source lookup); 9 LLM judge %40–57 oranında anlaşamıyor.
- Model kodu monolitik, tek dosyalı ve uzun fonksiyonlu — insan repolarından çok farklı mimari.
- Üretilen test coverage'ı native test suite'lere yakın (medyan 66.96 vs 73.39).
Relevant Limitations:
- Testleri tek bir LLM ailesi (Claude) üretiyor ve aynı aile değerlendirilen modeller arasında; gold binary ile doğrulansa da coverage bias'ı olası.
- Tests-passed oranı işlevsellikle zayıf korelasyonlu (yazarlar kabul ediyor); stdout string eşleşmesi formatı farklı ama doğru çözümleri cezalandırabilir.
- Popüler projeler → contamination riski (dil değiştirme ablation'ı kısmi cevap).
Key Takeaway:
- Executable'ı oracle olarak kullanmak implementation-agnostic, mimari serbestliğe izin veren değerlendirme sağlıyor; from-scratch repo inşası frontier modeller için hâlâ açık problem.

### MindForge — MindForge: Teaching Small Language Models Whole-Life-Cycle Software Engineering via Source-Free Program Synthesis (preprint, 2026) [arxiv:2607.27146]
Training-data + method: ProgramBench tarzı source-free ortamları (sadece compiled reference executable + doc) otomatik üreten pipeline ve bu ortamlarda toplanan trajectory'lerle küçük model distillation'ı.
2,235 aday CLI reposundan 1,002 paketlenebilir program; 562 program üzerinde (Go 231, Rust 212, C 87, C++ 29, Swift 2, TS 1) teacher GLM-5.2 ile 1,001 trajectory; 973'ü ile Qwen3.6-27B full SFT. Sadece geçerli build üreten trajectory'ler tutuluyor, hatalı reasoning kısımları yeniden yazılıyor. Değerlendirme mini-SWE-agent ile 8 benchmark'ta, her birinin resmi test protokolü.
Findings:
- ProgramBench ortalama test pass rate 37.98% → 49.51% (+11.53); 200 task'ın 152'sinde daha iyi; teacher 64.60.
- OOD transfer: RepoZero-C2Rust 47→78, NL2Repo +10.70 (testli) / +4.56 (testsiz), SWE-bench Verified +5.04, DeepSWE 1.76→15.92.
- Fine-tuned model turn sayısını ikiye katlıyor (344→736), token kullanımı 5.7×.
Relevant Limitations:
- ProgramBench resmi metriği % Resolved; burada partial-credit pass rate ana metrik — resolved sonucu vurgulanmıyor.
- Uzun-horizon benchmark'lar tek run; frontier skorları leaderboard'dan alınmış, harness farkı olası.
- Trajectory seçimi yalnız "buildable" kriterine dayanıyor; fonksiyonel doğruluk filtresi yok.
Key Takeaway:
- Behavioural reconstruction ortamları sadece evaluation değil, ölçeklenebilir training-data kaynağı; from-scratch trajectory'leri issue-fixing'e de transfer ediyor.

### MRCoder — MRCoder: An Efficient Context Selecting Approach for Repository-Level Code Generation (preprint, 2026) [arxiv:2607.26805]
Method: repo-level function generation için Map–Reduce context selection. Map'te küçük draft model bölünmüş context gruplarıyla taslak üretiyor, SADGS (API consistency + logic similarity) ile context seçiliyor; Reduce'da büyük model seçili context'le üretiyor, draft'ı speculative-decoding tarzı paralel doğruluyor.
CoderEval (Python, 230) ve DevEval (1,462 geçerli örnek, 117 repo) üzerinde Pass@1; Qwen2.5-Coder-7B/1.5B ve DeepSeek-Coder-6.7B/1.3B. Baseline: BM25 RAG, RLCoder, RepoFormer, LongCodeZip.
Findings:
- Qwen ile CoderEval K=5'te 40.0 (RAG 37.0), DevEval K=3'te 19.9 (RAG 15.8).
- %30–50 token azalması, %52'ye kadar inference süresi kazancı.
- DeepSeek/DevEval'de kazanç küçük (bazı K'larda 0).
Relevant Limitations:
- Sadece ≤7B açık modeller; frontier ya da agent baseline yok.
- DevEval ortamı yerel olarak kurulmuş ve filtrelenmiş (1,825→1,462), karşılaştırılabilirlik sınırlı.
Key Takeaway:
- Contextual tier'da "daha çok context" değil "doğru context" önemli; verim metrikleri de raporlanmalı.

### PaperCompiler — PaperCompiler: Faithful Paper-to-Code Generation via Repository-Level Specification Compilation (preprint, 2026) [arxiv:2609.02272]
Method: ML paper → repository. Free-form plan yerine paper'dan kanıt-bağlı (provenance'lı), repo-level implementation spec'leri "derleniyor": requirement'lar, non-degradation constraint'leri, dosya ownership'i, cross-file dependency'ler, file-level spec'ler; repo bu spec'lere göre üretiliyor.
Paper2CodeBench'ten 90 paper (ICLR/ICML/NeurIPS 2024, 30'ar), PaperCoder, AutoP2C, AutoReproduce, ChatDev, MetaGPT ile karşılaştırma. Generation o3-mini, evaluation o3-mini-high LLM-judge (1–5): reference-free, reference-based (author repo'su ile) ve P2C-Ex.
Findings:
- Reference-based 3.647 → 4.152 (+%13.8), reference-free 4.562 → 4.777, P2C-Ex 4.535 → 4.728 (PaperCoder'a göre).
- High-severity judge critique oranı %13.2 → %6.1.
- ChatDev/MetaGPT çok daha düşük (ref-based ~2.7–2.9), ama bu sayılar PaperCoder makalesinden alınmış.
Relevant Limitations:
- Değerlendirme tamamen LLM-judge; generator ve judge aynı aile (o3-mini / o3-mini-high). Execution, reproduction ya da test yok — yazarlar da kabul ediyor.
- Reference-based skor author implementasyonuna yakınlığı ödüllendiriyor; geçerli alternatif tasarımlar cezalanabilir.
- Tek backbone; ~1.71M token/paper.
Key Takeaway:
- Structured, ownership'li spec'ler free-form plan hand-off'undan daha iyi fidelity veriyor gibi — ama executable doğrulama olmadan iddia zayıf kalıyor.

### LiveCoder — Persistent Cross-Attempt State Optimization for Repository-Level Code Generation (preprint, 2026) [arxiv:2604.03632]
Method: aynı repo-level task'a yapılan ardışık end-to-end denemeler arasında kalıcı state (success knowledge, failure knowledge, historical-best repository) taşıyan framework.
NL requirement → çok dosyalı Python repo. RAL-Bench ve NL2Repo-Bench; GPT-5, DeepSeek-V3, Claude Sonnet 4.5, Gemini 3 Pro. Metrik: functional test pass rate + ISO 25010 tabanlı 5 boyutlu non-functional skor (maintainability, security, robustness, efficiency, resource; AHP ağırlıklı). Baseline'lar: direct, self-refine, evolutionary search, interactive agent'lar.
Findings:
- RAL-Bench'te Direct'e göre functional +19.70 / +10.00 / +27.68 / +25.30 puan (4 backbone); NL2Repo overall +4.2–5.9.
- A1→A4 functional +12–23 puan; repo reuse %81.58'e kadar; maliyet %53.63'e kadar düşüyor.
- Non-functional kalite karışık, model bağımlı.
Relevant Limitations:
- Functional test pass rate aynı zamanda historical-best seçimini ve fallback'i tetikliyor — değerlendirme oracle'ı optimizasyon sinyaline sızıyor gibi görünüyor; paper'dan bunun hidden test mi ayrı test mi olduğu net değil.
- Tek dil (Python); sabit attempt budget; maliyet tekrar sayısıyla ölçekleniyor.
Key Takeaway:
- Repo-level generation'da denemeler arası hafıza belirgin kazanç sağlıyor; ama test feedback'in kaynağı raporlanmalı, aksi halde skorlar şişebilir.

### ProjAgent — ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation (preprint, 2026) [arxiv:2607.08691]
Method: repo-level function generation için "procedural similarity" retrieval. Hedef fonksiyon reasoning adımlarına ayrılıyor, agentic workflow ile her adıma prosedürel olarak benzeyen repo fonksiyonları (LLM hidden-state projection similarity) getiriliyor, semantic retrieval ile birleştiriliyor; compiler/static-analysis feedback loop ile onarım.
REPOCOD: 11 repo, 980 problem, signature + docstring → fonksiyon, repo testleriyle Pass@1. Backbone Qwen2.5-Coder-14B-Instruct, greedy.
Findings:
- Pass@1 %41.14; SpecAgent (yeniden implemente) %34.52, Dense %28.83, Sparse %26.58.
- Astropy'de full-search ile 21.16 → 25.12; arama kapsamı darboğaz.
- Ablation (sadece Astropy, 85 problem): procedural veya semantic context'i çıkarmak belirgin düşüş.
Relevant Limitations:
- Tek backbone; SpecAgent replication package olmadan yeniden implemente edilmiş (adil baseline riski).
- RQ2 etiketleri Claude LLM-judge ile; ablation tek repo.
Key Takeaway:
- Lexical/semantic ötesinde "nasıl yapıldığı" benzerliği contextual generation için yeni bir retrieval ekseni.
