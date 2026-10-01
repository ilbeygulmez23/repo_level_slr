### BioCoder — BioCoder: a benchmark for bioinformatics code generation with large language models (Bioinformatics, 2024) [arxiv:2308.16458]
Benchmark: bioinformatics domain'inde repo context'ine bağımlı fonksiyon/method üretimi.
1,720 bioinformatics repo'dan 1,026 Python fonksiyonu + 1,243 Java method'u, ek olarak 253 Rosalind problemi (toplam 2,269 + Rosalind). Prompt'a imports, global variables, class declarations ve cross-file dependency'ler parse edilip konuyor (ortalama ~2,600 token). Değerlendirme: golden code ile üretilen kod aynı context file'da, fuzz ile rastgele üretilen input'larla çalıştırılıp output karşılaştırılıyor (Docker, AWS); Pass@K. Ayrıca StarCoder kendi training split'leri ile fine-tune ediliyor.
Findings:
- GPT-4 "Necessary Only" prompt ile Python Pass@1 %38.4, Java %45.0; açık modeller çoğunlukla %0-8, Java'da neredeyse 0.
- Fine-tuned StarCoder Python Summary Only Pass@20 %27→%39.6.
- Prompt uzunluğu arttıkça (~500 token sonrası) performans düşüyor; hataların çoğu syntax/runtime error.
Relevant Limitations:
- Oracle tamamen golden code'a bağlı (differential); sadece int/float/string/bool fuzz tipleri, output string eşleşmesi → farklı ama geçerli davranışlar cezalanabilir.
- Context prompt'a hazır veriliyor; model repoyu keşfetmiyor, retrieval sorunu yok.
- Fonksiyon açıklamaları LLM ile yeniden yazılmış; GitHub kaynaklı olduğu için contamination riski (appendix'te ablation var).
Key Takeaway:
- Reference implementation + fuzz input, test yazmadan ölçeklenebilir oracle üretmenin ucuz yolu; ama repo-level yerine function-level kalıyor.

### ML-Bench — ML-Bench: Evaluating Large Language Models and Agents for Machine Learning Tasks on Repository-Level Code (preprint, 2023) [arxiv:2311.09835]
Benchmark: mevcut bir ML repo'sunu kütüphane gibi kullanıp kullanıcı talimatına göre çalıştırılabilir bash komutu/Python kodu üretme.
18 GitHub ML repo'sundan 9,641 örnek (8,577+736 train; test 214 script + 46 code, 14 repo). İki setup: ML-LLM-Bench (Oracle segment / BM25 / tüm repo context → kod, hazır Docker ortamında execution ile Pass@K) ve ML-Agent-Bench (boş sandbox'ta env kurulumu, veri indirme, çalıştırma; success rate, test setinin 1/4'ü).
Findings:
- ML-LLM-Bench'te sadece GPT-4o Pass@5'te %50'yi geçiyor; insan annotator'lar %86.76.
- Bash script üretimi Python koddan zor; hatalar çoğunlukla hallucinated argüman/var olmayan dosya.
- Agent'larda OpenDevin+GPT-4o %76.47, SWE-Agent+GPT-4 %42.64, AutoGen %8.82.
- CodeLlama instruction tuning ile 8.85→15.76.
Relevant Limitations:
- Çıktı çoğunlukla tek satırlık CLI çağrısı; kod "yazma"dan çok repo kullanımı/parametre seçimi ölçülüyor.
- Talimatlar ChatGPT ile üretilmiş, reference code template'lerden; argüman eşleşmesi referansa bağlı.
- Agent sonuçları 68 örneklik alt kümede, farklı harness/model kombinasyonları → confound.
Key Takeaway:
- Contextual tier'ın sınırında; repo-level "kullanım" görevleri için execution tabanlı değerlendirme örneği, ama repo üretimi için doğrudan model değil.

### RepoCoder — RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation (preprint, 2023) [arxiv:2303.12570]
Method + benchmark: sliding-window retrieval ile önceki generation'ı query olarak kullanan iterative retrieval-generation; RepoEval benchmark'ı.
RepoEval: 2022 sonrası oluşturulmuş Python repo'larından line (1,600), API invocation (1,600; EM/ES) ve function body (373 örnek, 6 küçük repo, repo'nun kendi unit test'leri ile Pass Rate). Modeller GPT-3.5-Turbo ve CodeGen (350M/2B/6B).
Findings:
- In-File baseline'a göre line/API'de EM >%10 artış; 2+ iterasyon vanilla RAG'i geçiyor.
- Function body'de GPT-3.5 In-File %23.32 → RepoCoder (2 iter) %42.63, Oracle ile eşit.
Relevant Limitations:
- Execution tabanlı kısım sadece 373 örnek / 6 repo; asıl sonuçların çoğu similarity metrikleri.
- Function body tek fonksiyon, test'ler white-box repo test'leri; ölçek küçük.
Key Takeaway:
- "Önceki çıktıyla tekrar retrieve et" fikri sonraki repo-level context yöntemlerinin baseline'ı oldu; RepoEval-function execution'lı contextual değerlendirmenin erken örneği.

### CARD — A Lightweight Framework for Adaptive Retrieval In Code Completion With Critique Model (preprint, 2024) [arxiv:2406.10263]
Method: RAG tabanlı code completion'da retrieval'ın gerekli olup olmadığına ve adaylar arasından seçime karar veren LightGBM critic (logit/entropy feature'ları).
RepoCoder pipeline'ı üzerine plug-in; RepoEval (line/API 1,000'er, function 373 unit test'li) ve yeni RepoEval-M (8 repo, C/Java/JS/Python, 4,000 line completion). Modeller CodeLlama-7B ve DeepSeek-Coder-7B; metrikler EM/ES, function için UT pass rate, latency.
Findings:
- Retrieval sayısında line %21-46, API %14-40, function %6-46.5 tasarruf; latency %16-83 azalıyor.
- Function UT: CodeLlama RG1 %34.3 → CARD-RG4 %37.0; DeepSeek %36.5 → %38.0.
Relevant Limitations:
- Katkı verimlilik odaklı; execution'lı kısım sadece RepoEval function (373, Python), iyileşmeler küçük.
- Critic ES hedefiyle eğitiliyor → similarity'ye bağlı.
Key Takeaway:
- Contextual tier'da marjinal; retrieval maliyet/etkinlik dengesi için referans, repo üretimi için doğrudan değil.

### Qt-FrameworkGen — A Study of Coding Framework Generation by ChatGPT (CONF-SPML 2025, 2025) [doi:10.54254/2755-2721/2025.18277]
Empirical çalışma: ChatGPT-4o'nun C++/Qt framework'ünde masaüstü uygulama üretimi, üç granularity'de (project, class, function).
10 requirement (Calculator, To-do List, Restaurant/Library/Inventory Management vb.). Project seviyesinde tek uzun NL prompt ile tüm proje; class seviyesinde arayüz arayüz adım adım; function seviyesinde slot fonksiyonları tek tek, entegrasyon geliştiricide. Değerlendirme: her unit için 10 test case (Correctness), 8 extreme senaryo (Robustness: uzun input, concurrency, kaynak yoğunluğu), 5 öğrencinin UI puanı (Appearance Usability). Qt 6.7.1, MinGW.
Findings:
- Correctness: function 0.96, class 0.88, project 0.79.
- Robustness: 0.72 → 0.59 → 0.41; usability: 0.91 → 0.75 → 0.48.
- Hatalar çoğunlukla eksik header/dependency; ek prompt veya manuel düzeltme ile çözülüyor.
Relevant Limitations:
- Test'lerin kim tarafından, nasıl yazıldığı raporlanmıyor; çıktıların/kodun paylaşıldığı belirtilmiyor, tekrarlanabilirlik düşük.
- Tek model, tek framework, 10 görev; istatistiksel analiz yok, 5 kişilik UI rating.
- Project seviyesinde "kaç dosya/sınıf" ve build başarısı ayrı raporlanmıyor; manuel müdahalenin etkisi ölçülmemiş.
- Granularity arttıkça insan katkısı artıyor, yani seviyeler arası karşılaştırma confounded.
Key Takeaway:
- Granularity–insan müdahalesi ekseni ilginç bir çerçeve, ama kanıt zayıf; survey'de sadece "NL → GUI app, düşük kaliteli empirik" örneği olarak anılmalı.

### REPOCOD — Can Language Models Replace Programmers for Coding? REPOCOD Says 'Not Yet' (ACL 2025, 2024) [arxiv:2410.21647]
Benchmark + empirical: büyük Python projelerinde docstring'den bütün fonksiyon üretimi, developer test'leri ile.
11 popüler repo (≥2k star, ortalama 2,610 dosya), 980 görev; %50.8'i repo-level dependency gerektiriyor; görev başına ortalama 314 developer test'i, canonical solution ortalama 331.6 token. Test seçimi pipeline'ı süreyi 216.9 → 22.6 saate indiriyor. Context ayarları: BM25, Dense, current file, baseline; oracle olarak Callees ve RAGDense-oracle. 10 LLM (GPT-4o, Claude 3.5 Sonnet, DeepSeek-V2.5 vb.), Pass@1.
Findings:
- Hiçbir model %30'u geçmiyor; GPT-4o en iyi %27.4, açık modeller <%20.
- Repo-level context gerektiren görevlerde en düşük skor; retrieval recall yüksekse (0.5-1) GPT-4o %41.
- Callees (dependency) vermek RAG'den kötü; RAGDense-oracle ile bile %28.6.
Relevant Limitations:
- Tek dil; fonksiyonlar popüler repolardan → contamination riski tartışılmıyor (makalede yok).
- Test'ler white-box repo test'leri; agent/iteratif setup yok, sadece tek-shot RAG.
Key Takeaway:
- Bağımlılık yoğun, uzun fonksiyonlar contextual tier'ın hâlâ zor olduğunu gösteriyor; retrieval kalitesi temel darboğaz.

### CatCoder — CatCoder: Repository-Level Code Generation with Relevant Code and Type Context (preprint, 2024) [arxiv:2406.03283]
Method: statically typed dillerde retrieval'a ek olarak static analyzer (Eclipse JDT.LS, rust-analyzer) ile type context çıkarıp prompt'a ekleme.
Java: CoderUJB'den (Defects4J kaynaklı) standalone olmayan 199 fonksiyon, defects4j test ile. Rust: yeni RustEval, 13 crate'ten 90 fonksiyon, doc test'lerle. Metrikler compile@k ve pass@k; baseline'lar Vanilla, In-File, RepoCoder (yeniden implemente). Varsayılan model CodeLlama-13B-Instruct, genellenebilirlik için 7-8B arası birkaç açık model.
Findings:
- Java pass@1: Vanilla 14.9, In-File 35.3, RepoCoder 41.0, CatCoder 44.7; Rust 10.8 / 41.6 / 49.4 / 52.7.
- RepoCoder'a göre compile@k'de %14.44, pass@k'de %17.35'e kadar iyileşme; tüm modellerde tutarlı.
Relevant Limitations:
- Rust doc test'leri zayıf oracle (genelde tek örnek); görevler kısa (ortalama 10-17 NLOC).
- Sadece küçük açık modeller; Defects4J repo'ları eski → contamination.
Key Takeaway:
- Compiler/type bilgisini structured context olarak vermek retrieval'dan daha güvenilir; statik tipli dillerde repo-level üretim için ucuz kazanç.

### RepoClassBench — Class-Level Code Generation from Natural Language Using Iterative, Tool-Enhanced Reasoning over Repository (preprint, 2024) [arxiv:2405.01573]
Benchmark + method: repo içinde cross-file dependency'si olan bütün class'ı NL açıklamadan üretme; RRR (Retrieve-Repotools-Reflect) tool'lu agent.
RepoClassBench: 130 Java (10 repo), 97 Python (10 repo, kısmen SWE-bench repo'ları), 60 C# (tek repo, StabilityMatrix) class; her class repo'nun başka kısımlarına referans veriyor ve test ile kapsanıyor. Eski repolarda symbol'ler paraphrase ediliyor. NL açıklamalar GPT-4 ile üretiliyor: DETAILED (method body'leri görerek) ve SKETCHY (body'siz). RRR 6 static-analysis tool'u (get_imports, get_class_info, get_signature...) + oracle (test/compiler) feedback ile iteratif. Metrikler Pass@1, test rate, compile rate; GPT-4.
Findings:
- DETAILED Java Pass@1: Basic 2.2, Reflexion 18.6, RepoCoder 54.7, RRR 77.6; C# RRR 33.9; Python RRR 29.4.
- SKETCHY'de düşüş: Java RRR 70.6, Python 19.2.
Relevant Limitations:
- Spec'ler ground-truth class body'sinden GPT-4 ile reverse-engineer ediliyor (DETAILED'da implementasyon sızıyor).
- RRR feedback için değerlendirmede kullanılan test'leri kullanıyor gibi; held-out test ayrımı yok → skor şişebilir.
- C# tek repo; tek model (GPT-4).
Key Takeaway:
- Structured repo tool'ları (symbol lookup) similarity retrieval'dan çok daha etkili; ama değerlendirme test'lerini feedback olarak kullanmak bağımsızlığı bozuyor.

### CodeAgent — CodeAgent: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges (preprint, 2024) [arxiv:2401.07339]
Method + benchmark: repo içinde fonksiyon/class üretimi için 5 tool'lu (WebSearch, DocSearch, symbol navigation, format checker, code interpreter) LLM agent framework'ü, 4 strateji (ReAct, Tool-Planning, OpenAIFunc, Rule-based).
CodeAgentBench: 5 Python repo'dan (numpy-ml, tinydb, websockets vb.) 101 fonksiyon/class, ortalama 57 satır, 3.1 dependency; ~600 kişi-saat manuel hazırlık; repo'nun pytest/unittest suite'i ile Pass@1. 9 LLM (GPT-4, GPT-3.5, Claude-2, CodeLlama-34B...). HumanEval'de de ek değerlendirme.
Findings:
- GPT-4-turbo NoAgent %21.8 → Rule-based %37.6 (+15.8); GPT-3.5 %19.8 → %31.7.
- İyileşme 2.0-15.8 puan; Vicuna-13B'de etkisiz, Tool-Planning en zayıf strateji.
- numpyml alt kümesinde Copilot 8, CodeWhisperer 5 çözüm vs. CodeAgent+GPT-4 22.
Relevant Limitations:
- WebSearch tool'u açık repo'ların orijinal kodunu bulabilir → leakage/contamination kontrolü yok.
- 101 görev, 5 repo, tek dil; ticari ürün karşılaştırması farklı arayüz/harness ile adil değil.
Key Takeaway:
- Tool'lu agent contextual üretimi belirgin iyileştiriyor, ama web erişimi olan agent'larda benchmark izolasyonu kritik.
