### Skeleton-Guided-Translation — Skeleton-Guided-Translation: A Benchmarking Framework for Code Repository Translation with Fine-Grained Quality Evaluation (preprint, 2025) [arxiv:2501.16050]
Benchmark + method çalışması: repository-level Java → C# translation için TransRepo-Bench ve "önce skeleton, sonra tam repo" iki adımlı translation framework'ü.
Input: kaynak Java repo + hedef C# repo skeleton'ı (tüm fonksiyon gövdeleri trivial `return 0;/null` ile değiştirilmiş ama compile eden yapı; dosya yapısı, interface'ler, static değerler korunuyor). Output: tam C# repo. Skeleton ve unit test'ler GPT-4o ile çevrilip büyük manuel düzeltmeyle derlenebilir hale getirilmiş; NUnit + YAML build config. Benchmark 13 task, hepsi tek bir kaynak repodan (java-design-patterns) alınmış alt projeler. Fine-grained evaluation: her unit test'in çağırdığı kod Java tarafında instrumentation ile bulunuyor, C# karşılığı compile garantili skeleton'a kopyalanıp `dotnet build/test` çalıştırılıyor. Metrikler: build success rate ve unit test pass rate (compile olanlar içinde). Modeller: GPT-4o, GPT-4o-mini, GPT-4-turbo, Qwen-plus, Claude-3.5-Sonnet, DeepSeek-V3; 3 iterasyonlu refinement.
Findings:
- En iyi build rate DeepSeek-V3 %71.14; unit test pass rate ortalaması en iyi DeepSeek-V3 %22.32, GPT-4o %21.50, Claude-3.5 %19.76.
- Iterative refinement her zaman iyileştirmiyor (GPT-4-turbo build rate %60.54 → %50.00); error propagation.
- RepoTransBench tarzı bütün-repo build+test değerlendirmesinde 13 task'ın sadece 2'si sıfır dışı skor alıyor; skeleton'suz translation'da bağımlılıklar çözülemiyor, skorlar sıfıra düşüyor.
Relevant Limitations:
- Skeleton hedef reponun yapısını birebir dayatıyor: interface/dosya yapısı reference'a kilitli, alternatif tasarımlar değerlendirilemez; asıl zor kısım (mimari mapping) insanlar tarafından çözülüyor.
- Ölçek çok küçük: 13 task, tek kaynak repo (design pattern örnekleri), tek dil çifti.
- Test ve skeleton'lar GPT-4o ile çevrilip manuel düzeltilmiş; evaluated modeller arasında GPT-4o da var.
- Sonuçlar çoğunlukla figure'larda, agent kullanımı iddiası net raporlanmamış.
Key Takeaway:
- Structured, compile eden bir skeleton'u hand-off artefaktı olarak vermek hem translation'ı hem partial-credit evaluation'ı mümkün kılıyor; ama bu aynı zamanda görevi "skeleton-to-library"ye indirgiyor.

### SolEval — SolEval: Benchmarking Large Language Models for Repository-level Solidity Smart Contract Generation (EMNLP 2025, 2025) [doi:10.18653/v1/2025.emnlp-main.218]
Benchmark + empirical: repository context'e bağımlı Solidity function generation için ilk benchmark.
Input: function signature + insan-annotasyonlu NL requirement + repo context (dışarıda tanımlı interface/fonksiyon/değişkenler) + RAG ile 1 örnek; output fonksiyon repoya enjekte edilip Foundry test'leriyle çalıştırılıyor. 1,507 sample, 28 repo (OpenZeppelin, Solady vb.), 6 domain. Metrikler: Pass@k, Compile@k, Gas@k (gas fee), Vul@k (Slither). 16 LLM (6.7B–671B).
Findings:
- En iyi DeepSeek-V3: Pass@1 %21.72, Pass@10 %26.29; GPT-4o Pass@10 %23.70.
- RAG + context küçük ama tutarlı katkı (DeepSeek-V3 Pass@1 %20.17 → %21.72); gas/vuln ile korelasyon yok.
- Doğruluk ile gas verimliliği arasında trade-off; DeepSeek-R1-Distill-7B Solidity'de CodeLlama-7B'nin altında.
- Qwen-7B SFT: Pass@5 %16.67 → %58.83 (ayrı 21 repoluk test set üzerinde).
Relevant Limitations:
- Reference unit test'lere bağlı; Gas@k reference'a göre ölçülüyor.
- SFT verisi evaluated modellerin başarılı çıktılarından; ayrı test set'in ölçeği küçük.
Key Takeaway:
- Contextual tier'ı düşük kaynaklı bir dile taşıyor; nonfunctional metrikler (gas, vuln) domain'e özgü kalite boyutu ekliyor.

### SR-Eval — SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement Refinement (preprint, 2025) [arxiv:2509.18808]
Benchmark: requirement'ların turn turn açıldığı iterative code generation; function-level ve repository-level parçalar ayrı raporlanıyor.
Repo-level kısım: DevEval (Python) ve MRGBench (Java) fonksiyonlarından, cross-file bağımlılığı olanlar bilinçli olarak çıkarılmış (sadece intra-file context); contamination check ile 24 task atılmış. Multi-agent pipeline final requirement'ı 2–5 turn'e ayırıyor; her turn için LLM test üretip çalıştırıyor, distinctiveness (önceki turn'ün kodu fail etmeli) ve LLM Evaluator ile semantic alignment kontrolü, gerekirse insan müdahalesi. Repo-level: 89 Python (41 repo) + 40 Java (5 repo) task. 11 LLM, 3 prompting stratejisi; metrikler per-turn accuracy ve completion rate.
Findings:
- Repo-level'da en iyi completion rate Python %6.74, Java %20.00; accuracy %39.45 / %23.39.
- Golden context (önceki turn'ler doğru) ile Java accuracy %65.17'ye çıkıyor; hata birikimi ana sorun.
- Distinctiveness validation'ı kaldırmak accuracy'yi ~%13 şişiriyor; test kalitesi skoru doğrudan etkiliyor.
Relevant Limitations:
- Test'ler ve requirement bölünmesi LLM üretimi; aynı model ailesi spec, test ve verdict'e dokunuyor.
- Cross-file bağımlılıklar hariç tutulmuş; repo-level kısım aslında local-context function generation. Java 5 repo.
Key Takeaway:
- Iterative requirement refinement contextual tier'a yeni bir eksen ekliyor; discriminative test üretimi yöntemi yeniden kullanılabilir.

### EvoDev — Towards Iterative End-to-End Software Development: A Feature-Driven Multi-Agent Framework (preprint, 2025) [arxiv:2511.02399]
Method + küçük benchmark: feature-driven development'tan esinlenen iterative multi-agent framework ve Android app dataset'i APPDev.
Input: NL requirement + Android Studio scaffold projesi → output: build edilebilir Kotlin Android app. EvoDev requirement'ı user-valued feature'lara ayırıp Feature Map (DAG) kuruyor; her node'da business logic, design ve implementation katmanlı context tutuluyor ve bağımlılıklar boyunca propagate ediliyor. LangGraph üzerinde, Claude Code tarzı search-substitute edit. APPDev: 15 app, ortalama 13.5 functional requirement, 3 zorluk seviyesi, endüstri kontrolünden geçmiş acceptance checklist. Değerlendirme tamamen manuel: 4 evaluator, anonim APK'lar, 4'lü Likert (function completeness + visual/usability/stability/satisfaction); ~500 kişi-saat.
Findings:
- Claude-4-Sonnet ile EvoDev: build %100, Function Completeness 3.57; Claude Code 73.3% / 2.27 (+%57.3); MetaGPT ve GPT-Engineer hiç build edemiyor.
- Single-agent'a göre iyileşme: GPT-4.1 2.05 → 3.25 (%58.5), Claude-3.5 2.16 → 2.76; Qwen3-Coder neredeyse sıfır (1.18).
- Claude modelleri Shoot'em Up oyununda şüpheli yüksek single-agent skoru; yazarlar overfitting olarak yorumluyor.
Relevant Limitations:
- Otomatik test yok; Likert tabanlı insan değerlendirmesi, 15 app ile istatistiksel güç düşük, tekrar üretmesi pahalı.
- Baseline'lar (MetaGPT, GPT-Engineer) Android'e uygun değil; sıfır skorlar kıyası zayıflatıyor.
- Hand-off'lar yarı-structured (feature DAG) ama katman içerikleri free-form NL.
Key Takeaway:
- Dependency-aware feature decomposition, waterfall pipeline'lara karşı güçlü; ama app-level evaluation hâlâ insan emeğine dayanıyor, executable acceptance test eksikliği açık.

### ProjectGen — Towards Realistic Project-Level Code Generation via Multi-Agent Collaboration and Semantic Architecture Modeling (preprint, 2025) [arxiv:2511.03404]
Benchmark + method: CodeProjectEval dataset'i ve architecture → skeleton → code filling aşamalı multi-agent ProjectGen.
CodeProjectEval: Commit0 (9), DevEval (7), CoderEval (2) kaynaklı 18 Python repo; ortalama 12.7 dosya, 2,388.6 LOC. Input: PRD + UML (Pyreverse) + architecture design doc (directory tree + dosya/fonksiyon açıklamaları) + az sayıda check test; evaluation için ayrık ortalama 186 unit test (%90.7 coverage). ProjectGen, Semantic Software Architecture Tree (SSAT) adlı tree-structured, machine-parsable ara temsil kullanıyor; her aşamada generation + judge agent, memory-based context. Ayrıca DevBench Python subset. Backbone: DeepSeek-V3, GPT-4o. Metrikler: geçen test sayısı ve SketchBLEU.
Findings:
- DevBench: ProjectGen 52/124 test (DeepSeek-V3), MetaGPT 33, CodeS 25, ChatDev 0.
- CodeProjectEval: ProjectGen 160 (DeepSeek-V3) / 310 (GPT-4o) test / toplam 3,348; baseline'lar 0–35.
- 18 task'ın 13'ünde hiçbir yaklaşım tek test geçemiyor; başarı neredeyse sadece <1,000 LOC projelerde. GPT-4o'nun 310'unun 285'i tek repodan (pyjwt).
- SketchBLEU yaklaşımları ayırt etmiyor (MetaGPT ve ProjectGen ~%91–92).
Relevant Limitations:
- Input'ta reference repoden türetilmiş directory tree ve fonksiyon açıklamaları var; görev reference mimariye kilitli, test'ler white-box.
- Kaynak repolar Commit0/DevEval/CoderEval'den: contamination riski yüksek, freshness yok.
- Toplam skorlar birkaç outlier repo tarafından domine ediliyor.
Key Takeaway:
- Structured architecture ara temsili free-form NL hand-off'tan daha iyi çalışıyor; ama benchmark, NL-to-repo'dan çok "detaylı tasarım dokümanından reference reponun yeniden üretilmesi".

### SWE-Playground — Training Versatile Coding Agents in Synthetic Environments (preprint, 2025) [arxiv:2512.12216]
Training-data/environment çalışması: GitHub'a bağımlı olmadan, LLM'lerle sıfırdan sentetik proje ve task üreten pipeline.
Pipeline: project proposal (Gemini 2.5 Pro, GPT-4.1, Claude Sonnet 4 ensemble) → PR boyutunda step-by-step task'lar ve checklist → agent scaffold/stub + Docker → ayrı agent strict unit test üretiyor → implementation agent (OpenHands + Claude Sonnet 4) test'leri geçmeye çalışıyor; test'ler sonra orijinalleriyle değiştirilip reward hacking engelleniyor. Commit-0 formatı için üretilen repoların fonksiyon gövdeleri `pass` ile değiştirilip yeniden implementasyon trajectory'si toplanıyor (test ile filtrelenmeden). 28 proje, 704 trajectory (280 genel, 213 issue resolution, 183 issue reproduction, 28 library generation). Qwen2.5-Coder 7B/32B SFT; evaluation SWE-bench Verified, SWT-Bench Lite, Commit-0 Lite.
Findings:
- Commit-0 Lite: 7B 1.82 → 2.95, 32B 2.31 → 3.64; SWE-Gym, R2E-Gym, SWE-smith'ten yüksek.
- SWE-bench Verified: 7B 1.8 → 17.0, 32B 7.0 → 31.2 (SWE-smith-32B 40.2 ile 5k trajectory'nin gerisinde).
- Data efficiency: 704 trajectory ile 3.3k'lık R2E-Gym'e yakın; sadece genel from-scratch trajectory'ler bile üç benchmark'ta kazanç sağlıyor.
Relevant Limitations:
- Commit-0 mutlak skorları çok düşük (%3 civarı); library-generation için sadece 28 trajectory, iddia edilen etki küçük.
- Tüm oracle zinciri LLM üretimi (spec, test, implementation); test'ler implementation'a erişimli agent'lara veriliyor.
- Sadece Python; tek scaffold (OpenHands).
Key Takeaway:
- Sentetik from-scratch repo üretimi hem eğitim ortamı hem potansiyel ölçeklenebilir benchmark kaynağı; ama spec/test doğruluğu doğrulanmadan kalıyor.

### WebGen-Bench — WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch (preprint, 2025) [arxiv:2505.03733]
Benchmark + training data: LLM agent'larının NL instruction'dan sıfırdan multi-file website üretmesi.
101 test instruction (3 ana, 13 alt kategori; Upwork/Freelancer'dan esinlenen 10,152 proje açıklamasından GPT-4o ile üretilmiş), teknik detay içermiyor, agent framework seçimini kendi yapıyor. 647 test case (instruction başına 4–11), GPT-4o draft + iki PhD öğrencisi tarafından düzeltilmiş; her biri operation + expected outcome. Test'leri WebVoyager UI agent'ı (Qwen2.5-VL-32B) yürütüp YES/PARTIAL/NO veriyor; accuracy = (YES + 0.5·PARTIAL)/toplam. Ayrıca GPT-4o ile 1–5 appearance score. Frameworks: Bolt.diy, OpenHands, Aider. WebGen-Instruct: 6,667 instruction; 600 rejection-sampled Bolt.diy trajectory ile Qwen2.5-Coder SFT (WebGen-LM).
Findings:
- En iyi genel kombinasyon Bolt.diy + DeepSeek-R1 %27.8, Claude-3.5-Sonnet %26.4 (appearance 3.0); GPT-4o %12.8.
- WebGen-LM-32B %38.2 ile tüm proprietary modelleri geçiyor.
- Functional testing en düşük, design validation en yüksek accuracy: yüzeysel görünüm kolay, iç fonksiyonalite zor.
- UI agent ile insan annotasyonu arasında %86.1–94.4 alignment.
Relevant Limitations:
- Ölçümde iki LLM katmanı: VLM agent verdict ve GPT-4o appearance judge; test case'ler de GPT-4o draft.
- Black-box ve implementation'dan bağımsız (alternatif tasarımları cezalandırmıyor), ama NL expected outcome yorumlamaya açık.
- 101 instruction; "start failed" oranları (%38.6'ya kadar) framework/harness confound'u.
Key Takeaway:
- Reference implementation'sız, requirement-başına E2E test + UI agent executor, nl-to-app evaluation için ölçeklenebilir bir şablon; ama judge güvenilirliği sürekli doğrulanmalı.

### ABC-Bench — ABC-Bench: Benchmarking Agentic Backend Coding in Real-World Development (preprint, 2026) [arxiv:2601.11077]
Benchmark: gerçek backend repolarında maskelenmiş API endpoint'lerini implemente etme + (bir kısmında) environment/Docker kurulumu, external API test'leriyle doğrulama.
ABC-Pipeline: 2,000 MIT repodan GPT-5 destekli agent API grupları seçiyor, connectivity + functional API test'leri üretiyor, Docker ortamı sentezliyor, çözüm patch'i yazıp implementation'ı maskeliyor; test'ler orijinalde geçmeli, maskelide fail etmeli. 600 aday → 224 task, 8 dil, 19 framework; 92'sinde environment setup dosyaları siliniyor. Agent OpenHands içinde; servis ayrı container'da build edilip HTTP request'lerle test ediliyor. 3 run, pass@1.
Findings:
- Claude Sonnet 4.5 %63.2, DeepSeek-V3.2 %50.1, GPT-5 %49.4, Qwen3-8B %8.3.
- Rust'ta çoğu model %0; sadece Claude Sonnet 4.5 ve GPT-5 %30 üstü.
- Environment task'larında darboğaz build/start (S1): GPT-5 ve DeepSeek-V3.2 S1 < %50 ama S2 > %80.
- Framework etkisi büyük: mini-SWE-agent GPT-5'i %20 altına düşürüyor; turn sayısı ile başarı r = 0.87.
Relevant Limitations:
- Test'ler, çözüm patch'i ve mask aynı GPT-5 agent'ından; test kalitesi insanla doğrulanmamış.
- Görev mevcut repoda local implementation; repo generation değil, contextual tier'ın agentic ucu.
Key Takeaway:
- Black-box API-level E2E doğrulama ve deployment adımı, contextual evaluation'ı "çalışan servis" seviyesine taşıyor; environment configuration ayrı bir yetenek olarak ölçülmeli.

### ACTOR — Adaptive Critical Token-Aware Retrieval for Repository-Level Code Generation (preprint, 2026) [arxiv:2609.01601]
Method: generation sırasında "critical token"ları tespit edip sadece o noktalarda repository retrieval tetikleyen RAG framework'ü.
Token-level labeling (mismatch, uncertainty/entropy, attention influence) ile eğitilen classifier critical pozisyonları buluyor; UniXcoder dense retriever position-aware weighting ile. Evaluation: RepoExec (355 Python task) ve CoderEval (230 Python task), Pass@1/3/5 unit test'lerle. Generator'lar küçük: DeepSeek-Coder 1.3B/6.7B, CodeLlama 7B/13B; baseline RawPrompt, RawRAG, RepoCoder, RLCoder; context 1K token.
Findings:
- En yüksek skor CodeLlama-13B CoderEval Pass@5 %39.57; göreli kazanç en fazla +%15.4 (CodeLlama-7B CoderEval Pass@5), RepoExec'te +%8.4.
- DSCoder-6.7B RepoExec Pass@1'de RLCoder'ın altında (-%1.4); kazançlar mutlak olarak 1–4 puan.
- Ek latency ~3.3 ms.
Relevant Limitations:
- Sadece küçük base modeller ve Python; güncel frontier modeller veya agentic setting yok.
- CoderEval/RepoExec eski benchmark'lar; contamination tartışılmıyor.
Key Takeaway:
- Retrieval'ı task-level yerine token-level tetiklemek küçük ama tutarlı kazanç veriyor; contextual tier'da retrieval tasarımının hâlâ açık bir araştırma alanı olduğunu gösteriyor.
