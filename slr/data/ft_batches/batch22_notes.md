### SelfEvolve — Software Self-Extension with SelfEvolve: an Agentic Architecture for Runtime Code Generation (SEAMS 2026, 2026) [arxiv:2604.16314]
Method çalışması: çalışan bir sisteme, kullanıcı NL isteğiyle runtime'da yeni fonksiyon üretip restart olmadan entegre eden (importlib.reload) orchestrated agentic pipeline.
Pipeline: dispatcher → TDD test üretimi → function synthesis → sandbox execution → LLM adjudicator → ek unit test üretimi → final adjudicator; hepsi GPT-4.1. Değerlendirme 11 elle hazırlanmış problem: 4 integration task (577-783 LOC, 8-13 dosyalı mevcut Python codebase'lere entegre fonksiyon), 3 compositional, 4 data processing. Oracle: yazarların elle yazdığı pytest assertion'ları, 5 run, Pass@1.
Findings:
- SelfEvolve %92.7 (51/55); AutoGen %30.9, MetaGPT %27.3, AgentCoder %0.
- Integration task'larda 18/20; MetaGPT 10/20, AutoGen 0/20.
- TDD ablation: %92.7 vs %72.7, ortalama iterasyon 2.2 vs 4.7 (Wilcoxon p<0.001).
Relevant Limitations:
- Ölçek çok küçük: 11 problem, sadece 4'ü gerçekten repo bağımlı; hepsi yazarlar tarafından yazılmış, gerçek repo yok.
- Tek model (GPT-4.1); aynı model hem test hem kod yazıyor (yazarlar collusion riskini kabul ediyor). Baseline'ların entegrasyon mekanizması yok, karşılaştırma adil değil.
- Regression testing yok; entegrasyonun sistemin geri kalanını bozup bozmadığı ölçülmüyor.
Key Takeaway:
- Contextual tier için kenar bir örnek: "runtime feature ekleme" çerçevesi aslında repo-bağımlı fonksiyon üretimi + executable test; TDD döngüsünün faydası net ama kanıt ön-çalışma düzeyinde.

### SpecAgent — SpecAgent: A Speculative Retrieval and Forecasting Agent for Code Completion (preprint, 2025) [arxiv:2510.17925]
Method + benchmark: repository context'i inference yerine indexing time'da hazırlayan, dosyadaki muhtemel gelecek fonksiyonları "speculate" eden agent (Claude 3.7 Sonnet backbone).
Task: REPOCOD function completion (980 problem, 11 popüler Python projesi), signature+docstring+left/right context → function body, repo unit test'leriyle Pass@1. Yazarlar mevcut benchmark'lardaki "future context leakage"ı (caller'lar, import'lar hedef fonksiyonu ele veriyor) tespit edip bir function removal agent ile leakage-free synthetic repo state'leri oluşturuyor. Completion modelleri Qwen3-8B ve Qwen3-30B-A3B.
Findings:
- SpecAgent Pass@1 %27.86 (8B) / %27.96 (30B); en iyi baseline (BM25+RepoMap / BM25) ~%17.6-18.9 → +9-11 puan.
- Oracle agent üst sınırı ~%40; inference-time (leakage'li) setting SpecAgent'ı %30.9-34.3'e çıkarıyor, yani leakage sonuçları şişiriyor.
- Inference latency ~4.5s, ~50s asenkron indexing maliyeti; BM25/dense ile birleştirmek performansı düşürüyor.
Relevant Limitations:
- Baseline'lar leakage'li state'te, SpecAgent leakage-free state'te koşuyor; iki setting doğrudan kıyaslanabilir değil.
- Synthetic indexing-time state'i bir LLM agent üretiyor; ölçüm altyapısına LLM giriyor.
- Tek dil (Python), tek benchmark.
Key Takeaway:
- Repo-level completion benchmark'larında future-context leakage ciddi bir validity tehdidi; contextual tier benchmark'larını değerlendirirken dikkate alınmalı.

### PULSE — Towards Pre-generation Requirement Uncertainty Assessment for Code Generation (preprint, 2026) [doi:10.6084/m9.figshare.32854478.v1]
Peripheral method çalışması; full text yok, not yalnızca abstract'a dayanıyor. Requirement'lardaki belirsizliği generation öncesinde ölçüp yüksek belirsizlikli requirement'ları agentic clarification ile netleştiren üç aşamalı framework.
Nasıl çalışıyor: kontrollü perturbation ile belirsiz requirement varyantları üretiliyor, orta boy bir LLM oracle çıktı varyansına göre etiketliyor; RoBERTa tabanlı surrogate classifier generator çağırmadan uncertainty skoru tahmin ediyor; sonra clarification workflow. Ana değerlendirme function-level (HumanEval-ET, MBPP-ET, LiveCodeBench); genelleme ayrıca project-level DevBench üzerinde raporlanıyor.
Findings:
- Clarification pass@1'i %46'ya kadar artırıyor (hangi benchmark'ta olduğu abstract'ta belli değil).
- Uncertainty skoru pass@1 kazancıyla korele; classifier oracle ile yüksek uyumlu ve overhead'i ihmal edilebilir.
- DevBench'te "iyi genelleşiyor" deniyor; sayısal sonuç, model ve DevBench metriği abstract'ta raporlanmamış.
Relevant Limitations:
- Full text yok: DevBench kurulumu, dil ve metrik doğrulanamadı; in-scope kısmın ne kadar substantive olduğu belirsiz.
- Belirsizlik etiketi LLM çıktı varyansından geliyor (LLM ölçümün içinde).
Key Takeaway:
- Requirement kalitesinin generation öncesinde değerlendirilmesi, NL→repo pipeline'larında spec hand-off'unun kalitesiyle doğrudan ilgili; full text bulunursa DevBench kısmı yeniden kontrol edilmeli.

### VITAL-RAG — VITAL-RAG: Invariance Race for Context Allocation in Coding Agents (preprint, 2026) [arxiv:2607.26937]
Method çalışması: retrieval ile generation arasındaki bounded context "allocation" aşamasını hedefliyor; aynı code object'in tekrarlı görünümlerini (body, signature, call site) canonical object altında topluyor, yalnız yeni semantik katan bir companion tutuyor, per-object/global token budget ile render ediyor.
Değerlendirme üç katmanlı: RepoBench Recall@4K (Java/Python), RepoClassBench 227 task Token-F1/char similarity, RepoExec 355 task Pass@1 (üretilen fonksiyon projeye konup testlerle çalıştırılıyor). Backend'ler GPT-5.4, Claude Sonnet 4.6, Qwen3-8B; baseline'lar CodeRAG, GraphCoder, RepoScope "-style" reimplementasyonlar.
Findings:
- RepoBench Recall@4K 39.59 → 63.67, evidence token'ları %35.6 az.
- RepoExec Pass@1: Sonnet 4.6'da 65.63 (en iyi baseline 54.65), GPT-5.4'te 57.75 (55.49), Qwen3-8B'de 21.69 (21.13).
- RepoClassBench'te çoğunlukla en iyi ya da RepoScope ile eşit.
Relevant Limitations:
- Baseline'lar orijinal sistemlerin birebir reprodüksiyonu değil; tek generation, varyans/istatistik yok.
- RepoClassBench referansa similarity ile ölçülüyor, alternatif doğru class'ları cezalandırır.
- Executable kısım yalnız Python (RepoExec).
Key Takeaway:
- Retrieval doğru olsa bile context budget'ta redundancy kritik bilgiyi dışarı itebiliyor; repo-context-gen için allocation ayrı bir tasarım boyutu.

### YABLoCo — YABLoCo: Yet Another Benchmark for Long Context Code Generation (LLM4Code 2025, 2025) [doi:10.1109/llm4code66737.2025.00016]
Benchmark çalışması: büyük C/C++ repolarında (200K-2M+ LoC) function body generation.
4 repo (llvm-project, bullet3, openssl, redis) → 215 fonksiyon (2-15 LoC), dependency seviyesine göre none/stdlib/file/package/project kategorilerinde; docstring kalitesi 3 programcı tarafından elle filtrelenmiş. Değerlendirme: fonksiyon orijinalin yerine konup repo test suite'i Docker içinde koşuluyor → pass@10; ayrıca EM ve Edit Similarity. Modeller CodeLlama-13B, DeepSeekCoder-33B, GPT-4; context'siz ve "oracle" (çağrılan fonksiyonlar) context'li.
Findings:
- Context'siz pass@10: GPT-4 %30.4, DeepSeekCoder %22.4, CodeLlama %17.3.
- Oracle context CodeLlama'yı %29.4'e, DeepSeekCoder'ı %36.2'ye çıkarıyor; 'project' seviyesinde en büyük kazanç (15.0 → 41.7).
- bullet3'te yüksek skorlar muhtemel duplicate/memorization kaynaklı.
Relevant Limitations:
- Sadece 4 repo; 2'si The Stack'te → contamination riski.
- Testler fonksiyonu gerçekten hedefliyor mu belirsiz (test hit sayısı var, targeted test yok); zayıf testler pass@k'yı şişirebilir.
- Gerçek retrieval yok, yalnız oracle context; modeller eski.
Key Takeaway:
- C/C++ contextual tier'da nadir executable benchmark; büyük repo build/test maliyeti (fonksiyon başına container) ölçeklemenin önündeki pratik engel.
