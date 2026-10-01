### CodexGraph — CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases (NAACL 2025, 2025) [doi:10.18653/v1/2025.naacl-long.7]
Method çalışması; repo'yu static analysis ile Neo4j code graph'a (MODULE/CLASS/FUNCTION node'ları, CONTAINS/INHERITS/USES edge'leri) çeviriyor, LLM agent Cypher query yazarak context topluyor. Bizim için peripheral: asıl hedef genel repo-level RACG; in-scope kısım EvoCodeBench (repo-dependent function generation, Pass@1 ile test yürütme).
Kurulum: CrossCodeEval Lite Python (1000, EM/ES, similarity), SWE-bench Lite (257), EvoCodeBench (212 örnek, env sorunları yüzünden bir kısmı atılmış). Modeller GPT-4o, DeepSeek-Coder-V2, Qwen2-72B; baseline NO-RAG, BM25, AutoCodeRover.
Findings:
- EvoCodeBench'te GPT-4o ile Pass@1 36.02 (AutoCodeRover 28.78, NO-RAG 27.83); Recall@1 ise ~11.9 ile NO-RAG'dan farksız.
- Qwen2 ile agent yöntemler NO-RAG'ın altında kalıyor (14.62 vs 19.34) — yöntem güçlü backbone'a bağımlı.
- Token maliyeti daha yüksek (EvoCodeBench'te 24.5k vs 21.4k).
Relevant Limitations:
- EvoCodeBench örneklerinin bir kısmı dışlanmış; sonuçlar tam set değil. Tek dil (Python), tek seed/temperature.
- Evaluation mevcut benchmark'ların reference testlerine bağlı; yeni oracle katkısı yok.
Key Takeaway:
- Yapısal (graph) context arayüzü contextual generation için retrieval'dan daha genellenebilir, ama kazanç model kapasitesine koşullu.

### ASML Case Study — Evaluating Large Language Models for Functional and Maintainable Code in Industrial Settings: A Case Study at ASML (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00287]
Endüstriyel empirical çalışma + proprietary benchmark: ASML leveling repo'sundan 156 "garage" (data component glue code) dosyası; import hiyerarşisinden toplanan context dosyaları (Qwen2.5-Coder-32B ile özetlenmiş, BGE-M3 ile sıralanmış) verilip garage üretiliyor.
Değerlendirme: CodeBLEU/BLEU/ROUGE, yeni build@k (üretilen dosya repo içinde derleniyor mu), unit test pass@k, TICS kalite ihlalleri, manuel inceleme. RQ'lar: prompting (zero/one/few-shot, CoT), generic vs code-specific, model boyutu (Qwen2.5-Coder 0.5B–32B).
Findings:
- Few-shot build@5 0.28, zero-shot 0.08; CoT varyantları benzer (0.21–0.24).
- Hiçbir garage unit testleri geçmiyor: pass@k = 0 her konfigürasyonda; sadece 42/156 (%27) garage'ın testi var.
- CodeGemma build@5 0.551 vs Gemma 0.019; DeepSeek'te tersi — similarity ile buildability ayrışıyor.
- 1.5B model k=3,5'te build@k'da 14B/32B'yi geçiyor.
Relevant Limitations:
- Test coverage çok düşük; functional correctness fiilen ölçülemiyor, build@k proxy'ye kalıyor. Dil ve kod açıkça raporlanmıyor, replikasyon imkânsız.
- Similarity metriği referans implementasyona bağlı.
Key Takeaway:
- Endüstriyel repo-context'te "derlenebilirlik" bile ciddi darboğaz; test eksikliği oracle problemini öne çıkarıyor.

### Oxidizer — Scalable, Validated Code Translation of Entire Projects using Large Language Models (OOPSLA 2025, 2025) [doi:10.1145/3729315]
Method çalışması: Go projelerini bütün olarak Rust'a çeviren Oxidizer. Proje fragment'lara (function, type definition) bölünüyor, dependency graph post-order'da çevriliyor, her fragment ayrı ayrı doğrulanıyor.
İki ana fikir: (1) feature mapping — Go'ya özgü yapılar (interface, error handling vb.) için önceden tanımlı rule'lar LLM çevirisini yönlendiriyor; (2) type-compatibility — imza seviyesinde erken kontrol. Doğrulama: kaynak projenin unit testleri çalıştırılarak her fonksiyon için I/O snapshot'ları toplanıyor, Rust tarafında bu snapshot'larla otomatik unit test üretiliyor (differential oracle). LLM: Claude 3 Sonnet. Benchmark: 7 GitHub Go projesi (>100 yıldız, 3rd-party bağımlılıksız), 314–6642 LOC, max 369 fonksiyon.
Findings:
- Ortalama %99 compile, %73 fonksiyon I/O-equivalent (63–86%).
- Feature mapping olmadan algoritma tüm benchmark'larda abort ediyor, equivalence %0; type check olmadan %61.
- Paralel çalışmaya (AlphaTrans, ~%26) göre belirgin yüksek, runtime crash yok.
Relevant Limitations:
- Equivalence kaynak test suite'in coverage'ına bağlı; test edilmeyen fonksiyonlar otomatik başarısız (histogram %43 coverage).
- Fonksiyon-seviyesi I/O eşleşmesi, kaynak yapıyı (1:1 function mapping) dayatıyor; farklı ama doğru tasarımlar cezalandırılır.
- Sadece 7 küçük proje, tek dil çifti, tek model; baseline'larla doğrudan aynı benchmark üzerinde kıyas yok.
Key Takeaway:
- Kaynak repo'yu oracle olarak kullanıp fragment-level differential doğrulama, repo translation'ı ölçeklenebilir kılıyor; rule+LLM hibriti kritik.

### SolContractEval — SolContractEval: A Benchmark for Evaluating Contract-Level Solidity Code Generation (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00235]
Benchmark (sadece abstract'tan; full text yok). Gerçek on-chain kontratlardan 124 contract-level task, 9 domain; input: tüm context dependency'leri + yapılandırılmış contract framework + kısa task prompt; geliştiriciler tarafından annotate ve cross-validate edilmiş.
Değerlendirme: historical transaction replay ile dinamik functional correctness (gerçek işlemleri tekrar oynatıp davranışı karşılaştırma). 6 LLM.
Findings:
- Claude-3.7-Sonnet en iyi; sayısal sonuçlar abstract'ta yok.
- Modeller genel-amaçlı dillerdeki class-level performanslarının altında; inter-contract dependency ve Solidity'ye özgü özelliklerde zorlanıyor.
Relevant Limitations:
- Full text okunmadı; metrik detayları, task başına context boyutu raporlanamadı.
- Transaction replay orijinal kontratın davranışına bağlı; farklı ama geçerli implementasyonlar replay'de sapabilir. Olası contamination (on-chain kaynak kod public).
Key Takeaway:
- Tarihsel transaction'ları oracle olarak kullanmak, domain-specific contextual generation için insan eli değmeyen yürütmeye dayalı değerlendirme örneği.
