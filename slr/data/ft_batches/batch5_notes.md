### CBA User Study — Exploring the Challenges and Opportunities of AI-assisted Codebase Generation (preprint, 2025) [arxiv:2508.07966]
Empirical bir user study: "codebase AI assistant" (CBA) denen, NL prompt'tan tüm codebase üreten araçların geliştiriciler tarafından nasıl kullanıldığını ve neden yetersiz kaldığını inceliyor.
16 katılımcı (8 grad student, 8 profesyonel) counterbalanced tasarımla GPT-Engineer (gpt-3.5-turbo, clarification kapalı) veya GitHub Copilot ile 3'er task yapıyor; task'lar Short-Create (1–2 dosya), Long-Create (3+ dosya), Short-Edit, Long-Edit (ör. hesap makinesi, kronometre, to-do app; JS/Python). Toplam 48 prompt inductive coding ile analiz ediliyor; değerlendirme tamamen insan: katılımcı kodu çalıştırıp 1–5 satisfaction veriyor, think-aloud + interview. Ek olarak 21 ticari CBA'nın feature'ları survey ediliyor.
Findings:
- Genel satisfaction düşük: mean 2.8, median 3 (1–5); çıktıların sadece ~%50'si beklentiyi karşılıyor.
- Dissatisfaction nedenleri: functionality (%77), code quality (%42), communication (%25).
- Prompt'ların %98'i functional requirement içeriyor ama sadece 3'ü test case, 9'u error handling içeriyor — robustness kriterleri sistematik olarak eksik.
- Imperative ton satisfaction ile pozitif (r=0.31), implementation guidance negatif (r=-0.37) korelasyonlu.
- Altı challenge: missing code, unusable output, inadequate communication, ignored requirements, ignored context, missing instructions.
Relevant Limitations:
- n=16, küçük ve yazarların yazdığı task'lar; otomatik test/oracle yok, "doğruluk" tamamen katılımcı algısı.
- GPT-Engineer gpt-3.5-turbo ile, 2025 itibarıyla eski; Copilot ile karşılaştırma harness/model confound'lu.
- Create ve edit task'ları aynı çalışmada; repo-generation kısmı ayrı raporlanıyor ama sayısal karşılaştırma sınırlı.
Key Takeaway:
- Kullanıcılar NL prompt'larda test ve acceptance kriteri neredeyse hiç vermiyor; bu, structured/executable spec (BDD, test) hand-off'unun neden gerekli olduğuna dair insan-tarafı kanıt.

### FastCoder — FastCoder: Accelerating Repository-level Code Generation via Efficient Retrieval and Verification (preprint, 2025) [arxiv:2502.17139]
Method: repo-level code generation için lossless inference acceleration (draft-verification / retrieval-based speculative decoding).
Multi-source datastore (genel + project-specific), retrieval timing kontrolü, parallel retrieval ve context/LLM-preference-aware cache. DeepSeek-Coder 1.3B/6.7B ve CodeLlama 7B/13B üzerinde DevEval (Pass@1) ve RepoEval (sadece Edit Similarity, Pass@k scriptleri yok) ile ölçülüyor; ana metrik speedup.
Findings:
- DevEval'de 2.30×, RepoEval'de 2.53× speedup; baseline'lara göre %88'e kadar daha iyi; sample başına ~12.7s kazanç.
- Self-speculative decoding standalone'da ~1.5× verirken repo-level'da neredeyse hiç hızlandırmıyor.
Relevant Limitations:
- Doğruluk by design autoregressive ile aynı; repo-context generation kalitesine katkısı yok, sadece hız.
- Küçük/eski modeller; DevEval'den 200 sample'lık analiz.
Key Takeaway:
- Survey için kenar vaka: contextual tier'da ama katkı nonfunctional (latency); kategori tablosunda ayrı işaretlenmeli.

### AutoExperiment — From Reproduction to Replication: Evaluating Research Agents with Progressive Code Masking (preprint, 2025) [arxiv:2506.19724]
Benchmark: agent'a paper + n fonksiyonu maskelenmiş ML repo + deney komutu veriliyor; eksik fonksiyonları yazıp deneyi çalıştırması ve sonucu raporlaması isteniyor.
4 MLRC-replicated paper, 85 maskelenmiş Python fonksiyonu (ort. 26.3 satır); n=1..5, her n için max 100 sample. Oracle: gold kodla aynı komutun çıktısı, tüm test case'lerde ≤%5 relatif fark (differential). ReAct agent, Docker sandbox, 50 step / 30 dk / $1 limit.
Findings:
- n=1'de Claude-3.7 %36.5, GPT-4o %35.3; n=2'de %9.6'ya düşüyor, n=5'te neredeyse sıfır.
- Pass@1→Pass@5: GPT-4o 35.3→48.2; self-verifier gap'in küçük bir kısmını kapatıyor.
- Dinamik agent, fixed agentless harness'ı geçiyor (GPT-4o 8.3 vs 35.3).
Relevant Limitations:
- Sadece 4 paper/repo — ölçek çok küçük; contamination (public repo'lar) tartışılmıyor.
- Oracle referans implementasyona bağlı; paper'dan farklı ama geçerli tasarım sayısal sapma üretirse cezalandırılır.
Key Takeaway:
- "Maskelenen fonksiyon sayısı" zorluk knob'u olarak contextual→core (paper-to-repo) arasında sürekli bir eksen sunuyor.

### GraphCodeAgent — GraphCodeAgent: Dual Graph-Guided LLM Agent for Retrieval-Augmented Repo-Level Code Generation (preprint, 2025) [arxiv:2504.10046]
Method: requirement graph + structural-semantic code graph ile multi-hop retrieval yapan agent; hedef repo içindeki fonksiyonu NL requirement'tan üretmek.
Agent, implicit bağımlılıkları (predefined API'ler, multi-hop kod) ve web search ile domain bilgisini topluyor. DevEval (1,825 sample, 117 repo) ve CoderEval üzerinde Pass@1; GPT-4o, Gemini-1.5-Pro, QwQ-32B.
Findings:
- DevEval'de GPT-4o ile Pass@1 58.14 (%43.81 relatif artış); CoderEval'de 53.91.
- Cross-file kategoride 43.31 vs RepoCoder 22.29.
- QwQ-32B'de 54.14 vs ScratchCG 18.57.
Relevant Limitations:
- Sadece Python ve mevcut benchmark'lar; DevEval/CoderEval contamination riski tartışmaya açık.
- Web search tool'u retrieval'a harici bilgi sokuyor; baseline'larla karşılaştırma tool erişimi açısından eşit değil.
Key Takeaway:
- Requirement-side graph, NL→kod eşleşmesindeki "implicit subtask" boşluğunu kapatmada code graph'tan bağımsız katkı sağlıyor.

### KG-RepoGen — Knowledge Graph Based Repository-Level Code Generation (preprint, 2025) [arxiv:2505.14394]
Method: repoyu knowledge graph olarak temsil edip hybrid (graph + semantic) retrieval ile bağlam veren kısa bir çalışma.
EvoCodeBench'te (275 sample, 25 repo, Python) fonksiyon gövdesi `pass` ile değiştirilip hedef node'dan 2-hop subgraph retrieve ediliyor; reference test'lerle Pass@1.
Findings:
- Claude 3.5 Sonnet ile Pass@1 %36.36, GPT-4o %33.45, GPT-4 %32.00; EvoCodeBench baseline'ları (GPT-4 %7.27–20.73) çok geride.
- CodeXGraph (GPT-4o %36.02, 212/275 sample) ile yaklaşık başabaş.
Relevant Limitations:
- Baseline'lar orijinal paper'dan kopyalanmış, farklı model/ortam; ablation yok.
- Tek benchmark, tek dil; NL query pipeline'ı değerlendirmede devre dışı bırakılmış.
Key Takeaway:
- Graph-based retrieval'ın kazancı büyük ölçüde "no-context"e karşı; güçlü RAG baseline'larına karşı üstünlük kanıtlanmamış.

### ParEval-Repo — ParEval-Repo: A Benchmark Suite for Evaluating LLMs with Repository-level HPC Translation Tasks (ICPP 2025, 2025) [arxiv:2506.20938]
Benchmark + empirical: tüm HPC repolarını (build system dahil) paralel programlama modelleri arasında çeviriyor.
6 uygulama (nanoXOR 109 SLoC → llm.c 3,039 SLoC), 3 çift (CUDA→OpenMP offload, CUDA→Kokkos, OpenMP threads→offload), toplam 16 task; XSBench hariç hedef dilde public port yok (contamination kontrolü). Yöntemler: file-by-file non-agentic, 4-agent top-down (dependency/chunk/context/translation), SWE-agent. Modeller: Gemini 1.5 Flash, GPT-4o mini, o4-mini, Llama-3.3-70B, QwQ-32B. Metrikler: build@1, pass@1 (uygulamanın kendi doğrulama testleri), "Code-only" vs "Overall" (LLM'in build dosyası dahil), expected token cost Eκ.
Findings:
- Hiçbir yöntem/model microXOR'dan büyük uygulamada pass@k>0 elde edemiyor.
- Overall skor Code-only'den tutarlı şekilde düşük: build system (Makefile/CMake) üretimi ana darboğaz.
- Non-agentic, sığdığı yerde top-down agent'ı geçiyor (daha fazla bağlam); SWE-agent build üretiyor ama hiç doğru çeviri yok (tab→space Makefile'ı bozuyor).
- En sık hatalar: CMake konfigürasyonu, undeclared identifier, cross-file argüman/tip uyuşmazlığı.
Relevant Limitations:
- Çok küçük ölçek (6 repo), çoğu custom mini-app; zayıf/küçük modeller (bütçe $200).
- Top-down agent'ta hand-off'lar LLM-generated NL özetler — interface tutarsızlığı hatalarıyla uyumlu.
- Performans (speedup) ölçülmüyor, sadece doğruluk.
Key Takeaway:
- Repo-level çeviride darboğaz kod değil build sistemi ve dosyalar arası interface tutarlılığı; structured interface contract hand-off'u için güçlü motivasyon.

### ProjectEval — ProjectEval: A Benchmark for Programming Agents Automated Evaluation on Project-Level Code Generation (preprint, 2025) [arxiv:2503.07010]
Benchmark: NL'den tüm projeyi (web sitesi veya console/batch program) üretme ve kullanıcı etkileşimi simülasyonuyla otomatik değerlendirme.
20 mission (7'si SoftwareDev/ProjectDev'den), 284 test (ort. 14.2); 3 input seviyesi: L1 NL prompt, L2 NL checklist, L3 kod skeleton. Checklist, testler ve canonical solution GPT-4o ile üretilip insan tarafından review ediliyor. Testler Selenium (web) / subprocess (console) ile black-box; üretilen koda bağlı isimler (URL, class name) için agent'tan "parameter value" isteniyor. Ek olarak CodeBLEU/cosine similarity ile checklist, skeleton, kod karşılaştırması. Python; cascade vs direct generation.
Findings:
- Pass@5 çok düşük: GPT-4o ort. %12.49 (en iyi), Gemini 1.5 Pro %6.65, açık modeller <%2.
- OpenHands (GPT-4o) 8 task'ı AgentStuckInLoop vb. ile bitiremiyor.
- CodeBLEU sonuçları Pass@K ile çelişiyor — similarity metrikleri doğruluğu yansıtmıyor.
Relevant Limitations:
- Sadece 20 proje, tek dil; testler ve spec LLM (GPT-4o) ile üretilmiş, aynı aile değerlendirilen modeller arasında.
- Parameter-value mekanizması agent'ın kendi raporuna dayanıyor; yanlış parametre doğru kodu da fail ettirebilir. Testler chained, bir fail sonrakileri öldürüyor.
- Similarity metrikleri canonical solution'a bağlı, alternatif tasarımları cezalandırıyor.
Key Takeaway:
- UI-level black-box test + parameter description, implementation-agnostic değerlendirme için umut verici ama parametre bağlama adımı yeni bir kırılganlık noktası.

### RealBench — RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices (FSE 2026, 2026) [arxiv:2604.22659]
Benchmark + empirical: NL requirement + UML (package + class diagram) system design'dan tüm repoyu üretme.
61 gerçek Python repo (2024-12 sonrası, >10 star, 20 PyPI topic), 4 boyut seviyesi (ort. 1,201 LOC); UML'ler SciTools Understand ile koddan çıkarılıp insanla doğrulanıyor; repo başına ort. 50 insan-doğrulamalı test (function/method/class-level, %79.76 line coverage, GPT-4o yardımıyla). 3 strateji: holistic, incremental (module-by-module), RAG. 6 model (GPT-4o, Claude Sonnet 4, Gemini 2.5 Flash, DeepSeek-V3, Qwen3-235B, Qwen2.5-Coder-7B). Metrikler: completion rate, execution pass rate, test pass rate + insan puanlı Requirement@k / Architecture@k (0–4).
Findings:
- En iyi ortalama: completion %91.18, execution pass %45.00, test pass %19.39.
- Test pass <500 LOC'da %40+, >2000 LOC'da <%15.
- Küçük repolarda holistic, büyüklerde incremental en iyi; UML ablation'ları detaylı design'ın kritik olduğunu gösteriyor.
Relevant Limitations:
- UML koddan reverse-engineered ve testler class/method-level white-box: referans implementasyonun sınıf/metot isimlerine sıkı bağlı, alternatif tasarımlar cezalanır.
- Requirement@k/Architecture@k insan puanı, ölçeklenebilirliği sınırlı; sadece Python.
Key Takeaway:
- Structured design (UML) hand-off'u repo-gen'i kolaylaştırıyor ama değerlendirme bu design'a coupled; spec ile oracle'ın aynı referanstan türemesi survey'de işaretlenmeli.

### RPG/ZeroRepo — RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation (ICLR 2026, 2026) [arxiv:2509.16198]
Method + benchmark: NL planning yerine Repository Planning Graph (capability → folder/file → class/function + data-flow edge'leri) ile sıfırdan repo üretimi (ZeroRepo) ve RepoCraft benchmark'ı.
ZeroRepo: EpiCoder Feature Tree (1.5M capability) üzerinde explore–exploit ile proposal graph, sonra file skeleton + data flow + interface encoding, en son topological sırayla TDD ile kod üretimi (fonksiyon başına ≤8 debug iterasyonu). RepoCraft: 6 referans proje (scikit-learn, pandas, sympy, statsmodels, requests, django; isimleri paraphrase edilmiş), referans testlerden türetilmiş 1,052 task. Değerlendirme: o3-mini ile localization + majority-vote semantic check + adapte edilmiş ground-truth test çalıştırma; coverage, novelty, pass/vote rate, LOC.
Findings:
- ZeroRepo (o3-mini) coverage %81.5, pass %69.7; Claude Code %54.2 / %33.9; MetaGPT/ChatDev pass <%7.
- Qwen3-Coder ile 36K LOC, 445K token — Claude Code'un 3.9×'i.
- Gold projeler pipeline'da %81.0 pass / %92.0 vote: evaluator'ın kendisi ~%19 false negative üretiyor.
Relevant Limitations:
- Evaluation LLM-in-the-loop: localization ve test adaptasyonu o3-mini ile; ZeroRepo da o3-mini ile — aynı model ailesi üretip ölçüyor.
- 6 çok ünlü repo: paraphrase'e rağmen contamination kuvvetli; referans kategori listesi functionality'yi bu repolara bağlıyor.
- Baseline'lara aynı iterasyon bütçesi verilmiş ama ZeroRepo'nun feature-tree bilgi tabanı gibi ek kaynakları var; LOC büyüklüğü kalite göstergesi değil.
Key Takeaway:
- Structured, executable plan (graph) hand-off'u NL plan'a göre long-horizon repo-gen'de büyük fark yaratıyor; referans repo testlerini LLM ile adapte etmek implementation-agnostic değerlendirmenin pratik ama gürültülü bir yolu.

### RustRepoTrans — RustRepoTrans: Repository-level Context Code Translation Benchmark Targeting Rust (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00057]
Benchmark: hedef Rust reposunun bağlamı (fonksiyon/tip/değişken/kütüphane bağımlılıkları) verilerek C/Java/Python fonksiyonunu Rust'a çevirme (incremental translation).
375 task, gerçek "Rust'a yeniden yazılmış" proje çiftlerinden; fonksiyon eşleştirme similarity + GPT-4o + manuel doğrulama. Hedef reponun Rust testleriyle Pass@1; 7 LLM (DeepSeek-R1, DeepSeek-V3, Claude-3.5, GPT-4, Qwen2.5-Coder-32B, vb.) + ince taneli metrikler (noise robustness, syntactic difference).
Findings:
- En iyi DeepSeek-R1 %51.5 Pass@1; CodeTransOcean'daki %73.7'ye göre %22.2 düşüş.
- Başarısızlıkların %67.6'sı dependency çözümleme hataları; compile error oranı %92.3'e kadar.
Relevant Limitations:
- Fonksiyon-düzeyi; imza ve bağımlılıklar hedef repo tarafından sabit, alternatif mimarilere yer yok.
- arXiv 2411.13990 preprint versiyonu ile duplicate riski (EC7 kontrolü).
Key Takeaway:
- Full-repo translation ile function-level arasında ölçülebilir ara seviye; repo-level çeviride ana hata kaynağı bağımlılık/interface çözümleme.
