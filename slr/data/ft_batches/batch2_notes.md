### CodeRAG-Bench — CodeRAG-Bench: Can Retrieval Augment Code Generation? (preprint, 2024) [arxiv:2406.14497]
Benchmark + empirical çalışma: retrieval-augmented code generation (RACG) için birleşik testbed. Repo-level kısım survey için yalnızca contextual bir alt bileşen.
8 mevcut dataset'i (HumanEval, MBPP, LiveCodeBench, DS-1000, ODEX, RepoEval, SWE-bench-Lite, CodeSearchNet) tek pipeline'da topluyor; ~9k task, 25M dokümanlık datastore (tutorials, library docs, StackOverflow, GitHub files). Repo-level kısmı: RepoEval function split (373 örnek, execution-based; ilk kez reproducible execution sağlandığı iddiası) + SWE-bench-Lite (300). Tamamı Python. 10 retriever × 10 LM; metrikler NDCG@10 ve pass@1.
Findings:
- RepoEval'de canonical (gold) snippet'ler tüm modellere +7.5–17.2 puan kazandırıyor (ör. GPT-4o 32.4 → 46.1).
- Güçlü retriever (OpenAI-embedding + rerank) ile RACG, RepoEval'de gold setup'ı bile geçebiliyor (StarCoder2-7B: 26.5 → 53.9).
- SWE-bench-Lite'ta GPT-4o gold dokümanla 2.3 → 30.7; retrieval ile 21.7, yani retriever hâlâ darboğaz.
Relevant Limitations:
- Repo-level task'lar yeni değil, RepoEval'den alınmış; tek bir function split ve tek dil.
- RepoEval testleri reference implementation'a bağlı; function-level fill-in, gerçek repo üretimi değil.
- Canonical doküman = eksik fonksiyonun kendisi olduğu için "gold" ayarı leakage'a yakın bir üst sınır.
Key Takeaway:
- Repo-context generation'da retrieval kalitesi model boyutundan daha belirleyici olabiliyor; contextual tier'da context acquisition'ı ayrı bir değişken olarak raporlamak gerekiyor.

### CoderEval — CoderEval: A Benchmark of Pragmatic Code Generation with Generative Pre-trained Models (ICSE 2024, 2024) [arxiv:2302.00288]
Benchmark: standalone olmayan (repo'ya bağımlı) fonksiyon üretimini ölçen ilk execution-based benchmark'lardan biri.
43 Python projesinden 230 ve 10 Java projesinden 230 fonksiyon; her örnekte orijinal docstring + 13 mühendisin yazdığı human-labeled docstring, signature, reference code, all_context/oracle_context. Altı dependency seviyesi (self_contained → project_runnable). Docker tabanlı project-level execution platform; eksik coverage için elle ek testler. Metrikler Pass@k (n=10) ve oracle_context token'larını ölçen Acc@k. Modeller: CodeGen-350M, PanGu-Coder-300M, gpt-3.5-turbo.
Findings:
- ChatGPT CoderEval-Python Pass@1 %21.0 (HumanEval'de %39.2); Java'da %35.4.
- Standalone vs non-standalone fark büyük: ChatGPT Python'da %35.9'a karşı %15.5 Pass@1.
- Popüler 100 projede fonksiyonların >%70'i non-standalone.
Relevant Limitations:
- Ana deneylerde prompt'a context verilmiyor; yani ölçülen şey repo-context kullanımı değil, context'siz tahmin.
- Modeller artık çok eski/küçük; 460 örnek, Java tarafı yalnızca 10 proje.
- Testler proje testleri + elle yazılmış; reference implementation'a bağlı.
Key Takeaway:
- Contextual tier'ın referans noktası; dependency seviyesine göre ayrıştırma sonraki benchmark'larda (DevEval, EvoCodeBench) standart hale geliyor.

### CodeS — CodeS: Natural Language to Code Repository via Multi-Layer Sketch (preprint, 2024) [arxiv:2403.16443]
Method + benchmark + training data: NL2Repo görevini tanımlayıp README'den tüm repoyu üreten üç aşamalı sketch framework'ü öneriyor.
Pipeline: README → RepoSketcher (dizin ağacı + import bilgisi) → FileSketcher (boş gövdeli file sketch) → SketchFiller (fonksiyon gövdeleri). PE (GPT-3.5, CodeLlama, DeepSeekCoder, StarCoder2) ve SFT versiyonları; SFT için Ağustos 2023 öncesi 100 repodan 7,806 instruction örneği. SketchEval: Ağustos 2023 sonrası 19 Python reposu (5 easy / 8 medium / 6 hard). Metrik SketchBLEU = CodeBLEU'nun repo-level uyarlaması (BLEU, weighted BLEU, dizin+AST tree match, dataflow match). Ek olarak 30 katılımcılı VSCode user study (Gomoku, Blog), Pylint skoru ve manuel review.
Findings:
- SFT CodeLlama-34B SketchBLEU %63.31; PE %49.32; sketch'siz Vanilla %17–30.
- ChatDev/AutoGPT/AgentGPT (GPT-3.5) ~%42–45; CodeS-GPT-3.5 %47.63, farkı özellikle hard repolarda.
- ChatDev hiçbir zaman 8 dosya/842 satırı geçmiyor; CodeS 25 dosya/7,334 satıra çıkabiliyor.
Relevant Limitations:
- Değerlendirme tamamen reference repo'ya similarity; hiçbir execution/test yok, farklı ama doğru tasarımlar cezalandırılıyor.
- 19 repo, tek dil; benchmark ve method aynı yazarlardan.
- User study'de katılımcı başına 3 kişi/proje; istatistiksel güç düşük.
Key Takeaway:
- Hiyerarşik, structured hand-off (repo sketch → file sketch) NL2Repo için etkili bir decomposition, ama fonksiyonel doğruluk kanıtı olmadan "etkinlik" iddiası zayıf kalıyor.

### Codev-Bench — Codev-Bench: How Do LLMs Understand Developer-Centric Code Completion? (preprint, 2024) [arxiv:2410.01353]
Benchmark: endüstriyel completion aracının (Tongyi Lingma) kullanım verisinden türetilen senaryolarla repo-level code completion.
Codev-Agent (Qwen tabanlı) son 4 ayda oluşturulmuş repoları crawl ediyor, environment kuruyor, mevcut unit testlerin dynamic call chain'inden örnek çıkarıyor. 10 Python reposu, 296 code block; 4 senaryo (full block, inner block — %20'si boş ground truth, incomplete suffix, RAG). Metrikler unit-test Pass@1 ve edit similarity.
Findings:
- Code LLM'ler FIM modunda genelde önde: Codegemma-7B Scenario 1 %53.85, Scenario 2 %77.36.
- Incomplete suffix senaryosunda herkes çöküyor (en iyi ~%7).
- Pass@1 ile ES korelasyonu çoğu senaryoda <0.85; ES yanıltıcı.
Relevant Limitations:
- Çok küçük ölçek (10 repo) ve tek dil; "under review", detaylar sınırlı.
- Testler mevcut repo testlerinden; stop-point hataları fonksiyonel yetenekle karışıyor.
Key Takeaway:
- Contextual tier'da similarity metriklerinin execution ile tutarsız olduğunu gösteren bir veri noktası daha.

### Commit0 — Commit0: Library Generation from Scratch (preprint, 2024) [arxiv:2412.01769]
Benchmark (+ prototip agent SDE-I): stub'lanmış bir Python kütüphanesini spec ve unit testlerden sıfırdan yeniden yazma.
54 Python kütüphanesi (lite split: 16). Public fonksiyonların gövdeleri `pass` ile boşaltılıyor, private fonksiyonlar tamamen siliniyor; agent'a PDF spec (10k–300k token), starter repo ve unit testler veriliyor. Interactive environment: Docker'da unit test, ruff lint, pytest-cov coverage feedback. Değerlendirme yalnızca unit test pass rate. SDE-I: import DAG'ine göre topological sıra, Aider üzerinden modül modül doldurma, sonra lint ve test feedback ile refinement.
Findings:
- SDE-I + Claude 3.5 Sonnet lite'ta Stage 1 %17.8 → Stage 3 %29.3 (~$99); all split'te Stage 1 %6.1.
- OpenHands (test ID'leri ve komutlar verilerek) lite %42.95, all %15.25.
- Lint feedback açık modellerde performansı düşürüyor; topological sıra yerine random sıra daha iyi (%22 vs %17) — hatalı bağımlılık implementasyonu boşundan daha zararlı.
- 10-gram overlap analizi: modeller fonksiyonları ya tamamen ezberliyor ya hiç.
Relevant Limitations:
- Testler orijinal kütüphanenin white-box testleri; private fonksiyon/iç yapı beklentileri alternatif tasarımları cezalandırabilir.
- Popüler PyPI kütüphaneleri: ciddi contamination, yazarlar da ezberlemeyi gösteriyor.
- Agent'a testler veriliyor; test-driven overfitting ile gerçek spec anlama ayrıştırılmıyor. Maliyet çok yüksek (Claude all split sadece Stage 1).
Key Takeaway:
- Skeleton-to-library görevinin kanonik benchmark'ı; oracle olarak mevcut testleri kullanmak ölçeklenebilir ama contamination ve white-box bağımlılığı temel sorun.

### DevEval — DevEval: A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories (preprint, 2024) [arxiv:2405.19856]
Benchmark: gerçek repo dağılımına hizalanmış repo-level fonksiyon üretimi.
117 Python reposundan (10 domain) 1,874 örnek; 13 geliştirici 674 adam-saatle requirement yazmış. Her örnek: signature, requirement, repo, reference code, path'li reference dependency, testler. Ayarlar: without context, local file completion, local file infilling. Metrikler Pass@k ve dependency Recall@k. 8 LLM (gpt-4, gpt-3.5, DeepSeek Coder, StarCoder 2, CodeLLaMa).
Findings:
- En iyi Pass@1: gpt-4 infilling %53.04; context'siz %17.40.
- Local file context Pass@1'i gpt-4'te %205 (completion) ve %173 (infilling) artırıyor.
- Dependency dağılımı (intra-class/intra-file/cross-file %38/%32/%30) 500 repoya yakın.
Relevant Limitations:
- Yalnızca local file context; cross-file retrieval denenmiyor, oysa dependency'lerin %30'u cross-file.
- PyPI repoları, zaman filtresi yok: contamination riski (EvoCodeBench bunu düzeltmeye çalışıyor).
- Testler reference implementation'dan türetilmiş.
Key Takeaway:
- Contextual tier için en büyük manuel anotasyonlu set; Recall@k dependency kullanımını ayrı ölçmek için yararlı bir ek sinyal.

### EvoCodeBench — EvoCodeBench: An Evolving Code Generation Benchmark with Domain-Specific Evaluations (NeurIPS 2024 D&B, 2024) [arxiv:2410.22821]
Benchmark: DevEval pipeline'ının contamination'a karşı periyodik güncellenen (evolving) versiyonu; ilk sürüm EvoCodeBench-2403. (arxiv:2404.00599 aynı çalışmanın önceki versiyonu.)
Ekim 2023–Mart 2024 arası oluşturulmuş 25 Python reposundan 275 örnek; requirement'lar gpt-4 ile üretilip insan kontrolünden geçiyor (önceki versiyonda 50 örnekte gpt-4 vs insan 5/41/4 win/tie/lose). Örnek başına ort. 6 test. 10 domain etiketi; Pass@k, Recall@k ve Domain-Specific Improvement (DSI). 8 LLM.
Findings:
- gpt-4 en iyi Pass@1 %20.73 (DevEval'de %53.04); context'siz %7.27.
- CDD ile leakage oranı %0.7–2.2 (HumanEval'de gpt-3.5 için %41.47).
- 50 gpt-4 hatasının 29'u logic error, 20'si eksik context (başka dosyalardaki API'ler).
- Similar-function RAG gpt-4'ü %8.31 → %12.29'a çıkarıyor.
Relevant Limitations:
- Domain analizleri çok küçük alt kümelerde (Text Processing'de ±%100 DSI), istatistiksel anlamı zayıf.
- LLM-generated requirement: spec'i yazan model ailesi (gpt-4) aynı zamanda değerlendirilen model.
- 25 repo ile ölçek küçük; "evolving" iddiası bu makalede tek sürümle sınırlı.
Key Takeaway:
- Freshness'ı pipeline'a gömmek contextual benchmark'larda skorları dramatik biçimde düşürüyor; DevEval'deki yüksek skorların bir kısmı contamination olabilir.

### ExecRepoBench — ExecRepoBench: Multi-level Executable Code Completion Evaluation (preprint, 2024) [arxiv:2412.11990]
Benchmark + training data + model: executable repo-level completion benchmark ve AST tabanlı multi-level completion instruction corpus'u.
50 aktif Python reposundan 1.2K örnek (span/single-line/multi-line random + expression/statement/function grammar-based); repo unit testleriyle Pass@1 ve ES. Repo-Instruct: the-stack-v2'den ~1.5M repo, ~3M completion örneği (7 dil); Qwen2.5-Coder-7B üzerinde fine-tune → Qwen2.5-Coder-Instruct-C. 30+ model değerlendiriliyor.
Findings:
- Qwen2.5-Coder-Instruct-C ortalama Pass@1 %44.2; en yakın rakip StarCoder-7B %33.8, DS-Coder-33B %32.8.
- ES ile Pass@1 uyumsuz: Granite-Coder-8B ES ~1.9 ama Pass@1 %29.1.
Relevant Limitations:
- Fonksiyon düzeyi completion Pass@1 tüm modellerde düşük (%12–30); random span alt kümeleri çok küçük (34–42 örnek).
- Önerilen model kendi benchmark'ında değerlendiriliyor; decontamination sadece 20-gram exact match.
- Benchmark tek dil, eğitim verisi çok dilli.
Key Takeaway:
- Contextual completion için executable ölçüm şart; ES tabanlı eski completion benchmark'ları (CrossCodeEval vb.) sıralamayı yanıltabiliyor.

### HumanEvo — HumanEvo: An Evolution-Aware Benchmark for More Realistic Evaluation of Repository-Level Code Generation (preprint, 2024) [arxiv:2406.06918]
Benchmark + empirical study: repo-level fonksiyon üretiminde context'in fonksiyonun commit edildiği andaki repo durumundan alınması gerektiğini gösteriyor.
30 projeden (PyPI top-5000, GitHub top-200 Java) 10k+ PR tarandı; 400 task (200 Python, 200 Java), her biri PR'dan önceki commit'e rollback edilebiliyor. Context acquisition: Jaccard retrieval ve static analysis (local, +import, +sibling, +sim). Execution-based Pass@1, 3 tekrar ortalaması. 7 LLM (CodeLlama 7/13/34B, DeepSeekCoder 6.7/33B, GPT-3.5, GPT-4).
Findings:
- Evolution-ignored ayar performansı %10.0–61.1 şişiriyor (future context leakage).
- Retrieval ile GPT-4 Python %34.5 → %26.5, Java %20.5 → %14.5.
- Inter-class bağımlılıklarda düşüş ort. %30.9, intra-class'ta %14.0.
Relevant Limitations:
- Mutlak skorlar düşük ve Java tarafı özellikle zayıf; 200'er örnekle yüzde değişimleri gürültülü.
- Context window 4096 ile sınırlı; güncel long-context modellerde etki farklı olabilir.
- Testler PR'ın kendi testleri; reference implementation'a bağlı.
Key Takeaway:
- Repo-context benchmark'larında temporal leakage ciddi bir ölçüm hatası; contextual tier değerlendirmelerinde repo snapshot'ı raporlanmalı.

### HyperAgent — HyperAgent: Generalist Software Engineering Agents to Solve Coding Tasks at Scale (preprint, 2024) [arxiv:2409.16299]
Method: Planner/Navigator/Code Editor/Executor'dan oluşan generalist multi-agent sistem. Ağırlık SWE-bench ve Defects4J'de (EC1 kapsamı); survey için yalnızca RepoExec bölümü relevant.
RepoExec: 355 Python örneği, otomatik üretilmiş testler (%96.25 coverage). HyperAgent'a RepoExec'in gold context'leri verilmiyor, agent repo'yu kendisi geziyor. Baseline'lar: WizardLM2/GPT-3.5 + RAG/BM25 ve full-context CodeLlama/StarCoder. Pass@1, Pass@5, maliyet.
Findings:
- HyperAgent-Lite-3 Pass@1 %38.33, Pass@5 %53.33 (tüm modellerde en iyi Pass@5), ~$0.18/örnek.
- Full-context CodeLlama-34B Pass@1 %42.93 ile hâlâ önde; RAG baseline'ları %24–34.
Relevant Limitations:
- RepoExec'te kullanılan HyperAgent-Lite-3 konfigürasyonu config tablosunda (Table 7) tanımlı değil; hangi LLM'lerin kullanıldığı raporlanmamış, bu yüzden baseline'larla model-harness confound'u ayrıştırılamıyor.
- RepoExec testleri LLM-generated; kalite doğrulaması bu makalede yok.
- Repo-level üretim makalenin küçük bir parçası, ablation yok.
Key Takeaway:
- Agentic navigation, gold context olmadan full-context üst sınıra yaklaşabiliyor; ama contextual tier için zayıf bir kanıt, ancak bir veri noktası olarak kullanılmalı.
