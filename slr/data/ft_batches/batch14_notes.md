### ProjDevBench — ProjDevBench: Benchmarking AI Coding Agents on End-to-End Project Development (preprint, 2026) [arxiv:2602.01655]
Benchmark + empirical study: coding agent'lara NL proje gereksinimi veriliyor, ortaya çıkan repo (CMake'li C++ projesi) Online Judge (OJ) üzerinde test ediliyor ve LLM code review ile denetleniyor.
~2.800 üniversite OJ probleminden scope + quality filtresiyle 20 problem, 8 kategori (data structure, interpreter, management system, storage vb.). İki setting: project-completion (partial codebase verilir, "Easy", 15 task) ve project-creation (sıfırdan, "Hard", sadece 5 task). Final skor = %80 OJ execution score (ağırlıklı geçen test) + %20 code review (rule-based script + LLM review; forbidden library, FS-as-DB hilesi vb.). 6 agent (Cursor, Copilot, Claude Code, Augment, Codex CLI, Gemini CLI) × GPT-5 / Sonnet-4.5 / Gemini-3-Pro + Claude Code'da GLM-4.6, Kimi-k2, DeepSeek-V3.2; her konfigürasyon tek run.
Findings:
- En iyi: Codex+GPT-5 final 77.85 (Hard'da exec 69.22); Gemini CLI Hard'da 35.53'e, Copilot+Sonnet 36.63'e düşüyor.
- Tüm submission'ların sadece %27.38'i Accepted; %41.86 Wrong Answer, %13.91 TLE.
- Token (ρ=−0.73) ve turn sayısı (ρ=−0.67) skorla negatif korele; ortalama 138 turn, 4.81M token/problem.
- LLM code review vs insan: binary kurallarda accuracy 0.852, Cohen's κ 0.710.
Relevant Limitations:
- From-scratch kısmı yalnızca 5 task; Table 6'ya göre referans çözümlerin ~yarısı tek dosya — "project-level" iddiası kısmen zayıf.
- OJ testleri I/O-exact; spec I/O formatını sabitlediği için alternatif tasarımlara açık ama format sapmasını cezalandırıyor.
- Code review skoru LLM-judge; ağırlığı düşük ama agent ile aynı model aileleri judge olabilir, hangi modelin judge olduğu net değil.
- Tek run, 20 task, tek dil (C++); eğitim OJ'si olduğundan contamination riski tartışılmıyor.
Key Takeaway:
- OJ-tarzı hidden test + verdict-level feedback (TLE/MLE/memory leak) repo üretiminde non-functional hataları görünür kılıyor; ama scale ve from-scratch payı küçük.

### RealSec-bench — RealSec-bench: A Benchmark for Evaluating Secure Code Generation in Real-World Repositories (preprint, 2026) [arxiv:2601.22706]
Contextual benchmark: gerçek Java repolarında, security-neutral docstring'den fonksiyon üretimi; hem fonksiyonel doğruluk hem güvenlik ölçülüyor.
Top-4000 Maven repo → CodeQL ile 532 high-risk repo → 20k+ aday → coverage filtresi, GPT-4.1 + uzman FP eleme → 30 repodan 105 instance, 19 CWE (%56.2 log injection), 34-hop'a kadar dataflow. Metrikler: Pass@k (mevcut unit testler), Secure@k (CodeQL + multi-LLM voter/judge ile FP adjudication), SecurePass@k. 5 model (GPT-4.1, GPT-4.1-mini, Claude-3.7-Sonnet, DeepSeek-V3, Qwen3-235B); baseline, RAG (BM25, RLCoder, CodeQL dataflow), güvenlik guideline prompt'u.
Findings:
- En iyi Pass@1 %16.19 (Claude-3.7-Sonnet); SecurePass@1 tüm modellerde <%8.
- Crypto görevlerinde Pass@1 %38.89'a kadar ama SecurePass ~%0.
- RAG fonksiyonelliği biraz artırıyor, güvenliğe katkısı ihmal edilebilir; guideline prompt'u compile hatalarını artırabiliyor.
- LLM judge pipeline'ı 89 alert üzerinde precision 81.7%, recall 98.0%.
Relevant Limitations:
- Güvenlik verdict'i LLM-judge'a bağlı; docstring'ler de LLM üretimi (insan kontrollü).
- Context window 4096 token — repo-level iddiası için dar; %56 tek CWE tipi.
- 105 task, tek dil (Java); Pass@k sadece mevcut (kapsamı sınırlı) unit testlere dayanıyor.
Key Takeaway:
- Repo-context fonksiyon üretiminde fonksiyonel ve güvenlik doğruluğu ayrışıyor; "passes tests" yeterli bir oracle değil.

### ReCodeAgent — ReCodeAgent: A Multi-agent Workflow for Language-Agnostic Translation and Validation of Large-Scale Repositories (ASE 2026, 2026) [arxiv:2604.07341]
Method: tüm repoyu başka bir dile çeviren ve doğrulayan, PL-agnostic multi-agent workflow (Analyzer, Planning, Translator, Validator).
Input: kaynak dilde proje + hedef dil. Analyzer MCP tool'larıyla (Tree-sitter tabanlı get_file_structure, LSP) projeyi analiz edip 3rd-party kütüphane eşlemesi yapıyor; Planning translation unit'leri ve hedef skeleton'ı çıkarıyor; Translator kod + testleri birlikte çeviriyor; Validator testleri çalıştırıyor ve coverage-gap'e göre kaynak ve hedef dilde ek test üretiyor (her iki dilde çalıştırılıp eşleşme kontrolü). Claude Sonnet 4.5 + Claude Code SDK. Değerlendirme: önceki çalışmalardan (Oxidizer, AlphaTrans, Skel, Crust) 118 proje, 230K+ LoC, 4 PL çifti (C→Rust, Go→Rust, Java→Python, Python→JS); metrik: compilation success, validated developer testlerde test pass rate (testler çalışma sonrasına kadar gizli).
Findings:
- CS %99.4 (baseline %96.9); validated developer testlerde TPR %86.5 vs %25.7 (1.822/2.107 test).
- Crust'ta 100 projeden 89'u derleniyor (SWE-agent 41); ortak 40 projede TPR %88.0 vs %78.3.
- Ablation: Analyzer/Planning/Validator çıkarılınca TPR sırasıyla −22.7/−25.3/−30.3 puan; tek-agent baseline'lar ~%25.
- Ortalama maliyet $15.3, 57 dk/proje.
Relevant Limitations:
- Testler developer testlerine ve agent'ın kendi ürettiği testlere dayanıyor; kaynak test coverage'ı düşükse (ör. fileupload %38.7) doğrulama zayıf.
- Baseline'lar farklı mimariler; aynı LLM ile yeniden koşulmuş olsalar da agent harness (Claude Code) avantajı karışık.
- Benchmark projeleri muhtemelen Claude'un pretraining verisinde (yazarlar da belirtiyor); tek model.
Key Takeaway:
- Planlama + ayrı validator agent, repo-translation'da kritik; kaynak repoyu oracle olarak kullanıp iki dilde test çalıştırmak doğrulamayı genişletiyor.

### Repo0 — Repo0: Design-Driven Zero-to-All Code Generation (preprint, 2026) [arxiv:2608.19854]
Method: NL gereksinimden sıfırdan repo üretiminde mimariyi statik plan değil, sürekli evrilen bir state olarak ele alan framework.
Mimari state bir Dual-DAG: requirement-level DAG + component-level DAG + alignment. Structural action'lar (add, split, merge, revise, save) cohesion/coupling metrikleri ve requirement coverage ile yönlendiriliyor (split eşiği 2/3, merge 0.7; Commit0 Lite'tan iki held-out repo ile ayarlanmış), convergence sonrası TDD ile kod üretimi. Değerlendirme RepoCraft (RPG ile gelen) 6 Python repo (paraphrased isimlerle; ör. requests→HttpEasy, django→PyWebEngine), task açıklamaları iki mühendis tarafından yapı ipuçlarından arındırılmış. Metrikler RPG pipeline'ı: Functionality Coverage/Novelty (LLM matching), Pass Rate (adapted ground-truth testler, LLM ile yeniden yazılmış), Voting Rate (majority-vote semantic). Backbone: GPT-5 mini, DeepSeek V3.2; baseline'lar mini-SWE-agent, Paper2Code, RPG.
Findings:
- RPG'ye göre Coverage +4.55–20.08, Pass Rate +7.61–29.74 puan; ör. django GPT-5 mini'de Pass 74.36 vs 47.33.
- Ablation'da en büyük düşüş Structural Evolution çıkarılınca (django Pass −13.33).
- Kısıtsız LLM-kararlı structural action'lar over-decomposition yapıp doğruluğu düşürüyor.
Relevant Limitations:
- Ana tabloda sadece 3 repo; diğer 3'ü supplementary'de. Tek dil, tek benchmark.
- Test rewriting ve voting cross-model LLM ile — ölçüm içinde LLM var; Pass Rate adapted referans testlere bağlı, referans API'ye yakın tasarımı ödüllendiriyor.
- Eşik ayarı "golden architecture'a en yakın" diye manuel seçilmiş — referans mimariye bias.
Key Takeaway:
- Mimariyi explicit, evrilen yapısal bir artefakt (graph) olarak tutmak NL→repo'da tek-seferlik plana göre belirgin kazanç sağlıyor.

### RepoGenesis — RepoGenesis: Benchmarking End-to-End Microservice Generation from Readme to Repository (preprint, 2026) [arxiv:2601.13943]
Benchmark + training data: README.md (endpoint, schema, auth, port vb.) → deploy edilebilir web microservice repo'su (Python/Java).
Toplam 106 repo: Verified 30 (6 gerçek GitHub + 24 expert-supervised; 18 domain, 11 framework) + Train 76. 1.258 endpoint, 2.335 test. Testler black-box HTTP testleri; expert-supervised repolarda LLM-üretimi, 3 LLM reviewer + insan "Area Chair" review-rebuttal döngüsüyle filtrelenmiş (Krippendorff α 0.69). Metrikler: Pass@1, API Coverage (AC), Deployment Success Rate (DSR); 5 run ortalaması. 4 açık agent (DeepCode, MetaGPT, MS-Agent, Qwen-Agent) × GPT-5.1/Claude-Sonnet-4.5/Qwen3-30B + 3 IDE (Antigravity, Cursor, Copilot).
Findings:
- En iyi Pass@1: Copilot(Claude) Python %23.67, Java %21.45; MetaGPT %3'ün altında.
- AC–DSR gap: MetaGPT AC ~%73 ama DSR ≤%13 (Python); Copilot DSR %95.45.
- Hatalar: cross-file consistency %50.2, architectural coherence %26.0, dependency management %23.8.
- GenesisAgent-8B (Qwen3-8B, 16.396 trajectory ile SFT) GPT-5 mini'ye "comparable" — ama ikisi de Pass@1 ~%4.
Relevant Limitations:
- Verified setin %80'i expert-supervised, testleri LLM-üretimi; README insan yazımı ama test ve review aynı LLM ailelerinden.
- Train setinde insan adjudication yok; fine-tuning sonucu çok düşük mutlak değerlerde kıyas.
- IDE'lerde model sabit değil (platforma göre değişebiliyor) — model/harness karışıyor.
- 30 değerlendirme reposu; black-box API testi tasarım serbestliği tanıyor (olumlu).
Key Takeaway:
- Interface-level (HTTP) black-box testleri NL→app için implementation-agnostic oracle sağlıyor; deploy edilebilirlik ile fonksiyonel doğruluk ayrı ölçülmeli.

### RepoMind — RepoMind: Enhancing Repository-Level Code Generation via LLM Reasoning over Structured Repository Documentation (ACM proceedings, 2026) [doi:10.1145/3794763.3794823]
Method (sadece abstract; full text yok): repo-context fonksiyon üretimi için doküman tabanlı API retrieval.
RepoDocs Agent bottom-up, çok-granülerli hiyerarşik repo dokümantasyonu üretiyor; Reasoning-Retrieval Agent bu doküman üzerinden katman katman gezip ilgili API setini buluyor; vector retriever'ın semantik benzer API'leriyle birleştirilip generation context'i oluşturuluyor. Değerlendirme CoderEval ve DevEval üzerinde Pass@1.
Findings:
- Abstract'a göre SOTA'ya göre Pass@1'de %13.50'ye kadar relative iyileşme; mutlak değerler, backbone modeller ve baseline'lar raporlanmıyor (abstract'ta).
Relevant Limitations:
- Full text yok; model, maliyet (çok sayıda LLM çağrısı ile doküman üretimi) ve ablation bilgisi doğrulanamıyor.
- CoderEval/DevEval eski, contamination riski; tek-fonksiyon ölçeği.
Key Takeaway:
- LLM'in ürettiği yapısal repo dokümantasyonu retrieval için ara artefakt olarak kullanılıyor — repo-level üretimde "önce anla, sonra üret" yaklaşımı.

### RepoMod-Bench — RepoMod-Bench: A Benchmark for Code Repository Modernization via Implementation-Agnostic Testing (preprint, 2026) [arxiv:2602.22518]
Benchmark + empirical: tam kaynak repo verilip boş dizine hedef dilde fonksiyonel eşdeğer implementasyon üretilmesi isteniyor; değerlendirme gizli, implementation-agnostic interface testleriyle.
21 gerçek repo (hello-world-api 14 LOC'tan qalculate 211K LOC'a), 8 dil (C, C++, Go, Java, Python, Rust, TS, JS), toplam 1.6M LOC, 11.616 test. Sadece standart interface'li projeler (CLI: stdin/stdout/exit code; REST API) seçiliyor; kaynak repo testleri pytest formatına dönüştürülüp implementation-spesifik olanlar eleniyor. Metrikler: Build Success, Pass Rate. Agent'lar: Claude Code (Opus 4.5), Codex CLI (GPT-5.2), OpenCode × iki model; 4 saat timeout, tek run (84 run).
Findings:
- Pass rate: Claude Code %48.2, OpenCode-GPT-5.2 %43.0, OpenCode-Claude %42.0, Codex CLI %30.4; build ≥%95.
- Scaling collapse: <10K LOC %91.3, 10–50K %66.9, >50K %15.3; uncrustify (162K) tüm agent'larda %0.
- Aynı model ile harness farkı büyük: OpenCode-GPT-5.2 Codex CLI'yi 12.6 puan geçiyor.
- Hata modları: single critical bug, early exit (hugo için 1.059 satır), dil ekosistemi uyumsuzlukları (RE2 vs Rust regex).
Relevant Limitations:
- Tek run, 21 repo; pass rate tek bir kritik bug'a aşırı duyarlı (yazarlar da belirtiyor).
- Testler kaynak testlerden türetildiği için davranışsal eşdeğerlik ölçülüyor ama coverage kaynak test suite'iyle sınırlı; kütüphaneler/GUI kapsam dışı.
- Popüler OSS projeler — contamination tartışılmıyor.
Key Takeaway:
- Sistem sınırında (CLI/REST) test etmek dil-bağımsız, gizlenebilir bir oracle veriyor; repo büyüklüğü şu an en güçlü zorluk belirleyicisi.

### RepoScope — RepoScope: Leveraging Call Chain-Aware Multi-View Context for Repository-Level Code Generation (ICSE 2026, 2026) [arxiv:2507.14791]
Method: repo-context fonksiyon üretimi için statik analiz tabanlı, call-chain-aware 4-view context retrieval (training-free, tek LLM çağrısı).
Repository Structural Semantic Graph (RSSG) kurulup call chain prediction ile muhtemel callee'ler, caller'lar, benzer fonksiyonlar ve benzer fragment'lar alınıyor; structure-preserving serialization ile prompt'a konuyor (4096 token). CoderEval Python (207 örnek) ve DevEval (1.742 örnek) üzerinde Pass@1; RepoEval API-level'da EM/ES. Backbone: GPT-4o mini, Claude-3.5-Haiku, Qwen3-235B, DeepSeek-V3; baseline'lar RepoCoder, DRACO, CodeAgent, RLCoder, SimpleRAG.
Findings:
- CoderEval DeepSeek-V3 Pass@1 59.42 (en iyi baseline 50.72); DevEval Claude-3.5-Haiku 41.56 vs DRACO 30.48 (+%36.35 relative).
- Benzer veya daha az input token ile tüm backbone'larda en iyi.
Relevant Limitations:
- Hatalı örnekler çıkarılmış (CoderEval 230→207), sadece Python.
- Baseline prompt uzunlukları eşitlenmeye çalışılmış ama RepoCoder/CodeAgent'ta kontrol edilemiyor.
- Benchmark'lar eski, contamination riski; RepoEval kısmı similarity-only.
Key Takeaway:
- Yapısal (call-chain) context, similarity-based retrieval'dan tutarlı şekilde daha faydalı; statik analiz ucuz ve güçlü bir baseline.

### RepoZero — RepoZero: Can LLMs Generate a Code Repository from Scratch? (NeurIPS 2026 D&B, 2026) [arxiv:2605.07122]
Benchmark + method: agent'a kaynak reponun API spec'i + 4 white-box test örneği veriliyor, repoyu başka bir dilde (Py→JS, C/C++→Rust) sıfırdan yeniden implemente etmesi isteniyor; doğrulama kaynak ve hedef reponun çıktılarının strict string-level eşleşmesi.
Kaynak repolar manuel seçiliyor; LLM, API çağıran test dosyaları (her biri 1–20 API çağrısı, her dosya bir sample) ve input-output case'leri üretiyor; her case kaynak repoda 20 kez çalıştırılıp exception/non-deterministic olanlar atılıyor, <10 geçerli case'li sample'lar çıkarılıyor. Py2JS 400, C2Rust 200 sample; zorluk etiketi LLM majority vote. Harici paket ve cross-language bridge yasak, Docker sandbox. Scaffold'lar OpenHands-bash ve Mini-SWE-Agent; 12 model (Claude-4.6-Sonnet, DeepSeek V3.x/V4, GLM-5/5.1, Kimi-K2.5/2.6 vb.). Ayrıca ACE: kaynak repoyu oracle yapan code-test evolution döngüsü.
Findings:
- En iyi: Claude-4.6-Sonnet + Mini-SWE-Agent Py2JS %54.70, C2Rust %47.58; çoğu model %20–45.
- Mini-SWE-Agent, OpenHands-bash'i tutarlı şekilde geçiyor (ör. GLM-5 Py2JS 45.52 vs 27.46).
- ACE (DeepSeek V3.1): OpenHands 26.08→42.88, Mini-SWE 43.76→52.06 (Retry-2).
- Çalıştırılabilir kodun ~%40'ı kaynak reponun deterministik çıktısını tutturamıyor.
Relevant Limitations:
- Bir "sample" tam repo değil, bir test dosyasının kullandığı API alt kümesi; kaç bağımsız kaynak repo olduğu ana metinde net değil.
- Strict string-level eşleşme format farklı ama doğru çözümleri cezalandırıyor; harici paket yasağı yapay.
- Test dosyaları ve zorluk etiketleri LLM üretimi (oracle kaynak repo olduğu için doğruluk kısmen güvence altında).
Key Takeaway:
- Referans repoyu oracle olarak kullanmak, insan emeği olmadan doğrulanmış, ölçeklenebilir test üretmenin yolu; cross-language zorunluluğu leakage'a karşı pratik bir savunma.
