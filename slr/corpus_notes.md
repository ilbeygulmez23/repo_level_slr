# Paper notes — final corpus

Auto-collected from full-text review; grouped by tier and task.


## core / behavioral-reconstruction

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

### SpecFirst — SpecFirst: Behavioral Specification Elicitation as a First-Class Step in Agent-Based Program Synthesis from Scratch (preprint, 2026) [arxiv:2607.27167]
Method + empirical: ProgramBench (NL doc + execute-only binary → sıfırdan davranışsal olarak eşdeğer program) üzerinde, kodlamadan önce ayrı bir spec agent'ın binary'yi probe edip yapılandırılmış SPEC.md üretmesini zorunlu kılan iki aşamalı pipeline.
Spec agent doc + binary ile black-box probing yapıyor; code synthesis agent (mini-SWE-agent, baseline ile aynı scaffold) doc + binary + SPEC.md alıyor. Dil ve mimari agent'a bırakılmış. Değerlendirme: 200 instance'ın tamamı, gizli test suite (binary çıktısıyla exact match) üzerinden ortalama test pass rate; ek olarak probing line coverage. Modeller: Qwen3.5-397B, Qwen3.6-35B, GPT-5.5-high, GPT-5.4-mini. Wilcoxon testi.
Findings:
- Pass rate artışı %6.9–21.3 (relatif), hepsi p<0.01; GPT-5.5-high %59.02 → %65.14, W/L/T 150/38/12.
- ≥%90 pass rate'e ulaşan program oranı %5.5 → %16.5 (GPT-5.5-high); Hard tier'de %30.8 → %40.0.
- Binary exploration coverage +%9.4–18.5; spec ile agent koda daha erken başlıyor.
- Maliyet +%48–130 per instance ($0.25–3.16 ek spec fazı).
Relevant Limitations:
- Differential oracle strict string eşleşme: format farkı olan doğru davranış cezalı.
- Baseline ek bütçe almıyor; iyileşmenin bir kısmı sadece daha fazla compute olabilir (cost-matched karşılaştırma yok).
- SPEC.md free-form markdown; executable/structured artefakt değil. Aynı model hem spec hem kod yazıyor.
- Tam resolved oranı raporlanan ana metrik değil; ortalama pass rate'e odaklı.
Key Takeaway:
- Requirements elicitation'ı ayrı faz yapmak from-scratch reconstruction'da model-agnostik kazanç; hand-off artefaktının yapısı (spec) doğrudan sonucu etkiliyor — structured spec'ler için güçlü motivasyon.

### PROOF — From Reading Code to Reading Spec: A Verified Layer for LLM-Driven Codebase Maintenance (preprint, 2026) [arxiv:2609.06383]
Method, peripheral: asıl hedef spec üzerinden codebase maintenance (out of scope), ama raporlanan değerlendirmenin tamamı in-scope: kodtan hiyerarşik NL Spec çıkar (call graph topolojisini koruyarak), sonra source'a erişmeden repo'yu yalnızca Spec'ten yeniden inşa et ve orijinal test suite'le doğrula (round-trip).
Veri: üç SWE-bench repo'su — Flask (24 dosya, 9.5K satır, 491 test), Seaborn (54 dosya, 29K, 2,381 test), Pytest (81 dosya, 38K, 4,224 test). Model: "Claude 5 Sonnet". Baseline IR'lar: RepoAgent, RPG-Encoder, EPAM. Metrikler: test pass rate (Pass@1→Pass@3, failure-driven repair turları), AST similarity (pycode_similar), 21 fonksiyon üzerinde 3 insan + LLM-judge ile Spec kalitesi.
Findings:
- Pass@3: Flask 100%, Seaborn 100%, Pytest 96.8%; Seaborn'da RepoAgent 51.3%, RPG-Encoder 38.9%.
- Pytest'te bütün yöntemler Pass@1 ≈ 0% (sıkı coupling'de integration hataları yayılıyor), repair turlarıyla 91.24%'e çıkıyor.
- AST similarity 87–96%.
Relevant Limitations:
- Sadece 3 repo, hepsi Python ve SWE-bench'ten: contamination riski çok yüksek (model Flask/Pytest'i ezbere biliyor olabilir), bu da "Spec yeterli" iddiasını zayıflatıyor.
- Repair turları test failure'larını kullanıyor; "test isolation" iddiasına rağmen feedback test sonuçlarından geliyor.
- AST similarity reference'a coupling; alternatif tasarımları cezalandırır. Update fazı (asıl motivasyon) nicel olarak değerlendirilmemiş.
Key Takeaway:
- Code→Spec→Code round-trip, behavioral reconstruction için doğal bir oracle veriyor (orijinal test suite); ama fresh, contamination-free repo'lar olmadan anlamlı değil.

### NanoHarness — Beyond the Model: Demystifying Harness Effects in Software Engineering Agents (preprint, 2026) [arxiv:2609.32459]
Empirical + method çalışması: model/harness/task etkileşimini ve harness bileşenlerinin katkısını ölçüyor; asıl testbed ProgramBench (reference binary'den davranışsal olarak eşdeğer repo'yu sıfırdan yeniden inşa etme; 200 task; Rust, Go, C/C++, Java, Haskell).
Tasarım: mini-SWE-agent vs OpenCode, Qwen ve DeepSeek ailelerinden 10 açık model (60 konfigürasyon: SWE-bench Pro 300 örnek, ProgramBench 70 örnek, GitTaskBench 54). Sonra mini-SWE-agent'a plug-and-play bileşenler (tool registry, context compression, planning, task-specific/general subagents, lazy skills) eklenerek NanoHarness kuruluyor; tam 200 ProgramBench task'ında Qwen3.7-Max ve DeepSeek-V4-Pro ile ablation. Step limiti 1000'den 300'e indirilmiş, network kapalı.
Findings:
- ProgramBench'te NanoHarness: Qwen3.7-Max 42.88 → 50.25 (+7.37), DeepSeek-V4-Pro 45.14 → 51.35 (+6.21); OpenCode 51.68/52.48, Claude Code 52.33/52.76.
- En büyük tekil kazanç task-specific subagents (+5.91 / +4.46) ve tool registry (+4.57 / +3.54).
- Context compression prompt token'larını %54–77 azaltıyor ama skoru 4.86 / 3.85 düşürüyor; general subagents de zarar veriyor.
- SWE-bench Pro'da karmaşık harness'in faydası güçlü modellerde azalıyor; repo-generation'da ise sadece güçlü modeller karmaşık harness'ten yararlanıyor.
- Failure mode'lar: reference binary'nin aşırı veya yetersiz probing'i.
Relevant Limitations:
- Sadece Qwen/DeepSeek, temperature 0, tek run; step budget'ın düşürülmesi ProgramBench skorlarını orijinalle karşılaştırılamaz kılıyor.
- ProgramBench değerlendirmesinin ayrıntıları bu makalede anlatılmıyor; skor reference binary davranışına bağlı (output formatı farklı geçerli çözümleri cezalandırabilir).
- Bileşenler minimal implementasyon; commercial harness'lerin gerçek bileşenleriyle eşdeğerliği varsayım.
Key Takeaway:
- Repo generation'da harness etkisi model etkisi kadar büyük; benchmark raporlarında harness sabitlenmeli/raporlanmalı. Uzun spec'lerde context compression riskli.


## core / nl-to-app

### MultiAgent-FrontEnd — Bridging Design and Implementation: A Study of Multi-Agent LLM Architectures for Automated Front-End Generation (ACM proceedings, 2025) [doi:10.1145/3793302.3793371]
Method + empirical. Full text yok, not abstract'a dayanıyor. User story'ler + Figma tasarımlarını birlikte kullanarak tam React uygulaması üreten multi-agent framework; üç orkestrasyon mimarisini karşılaştırıyor.
Input: user stories (text) + Figma design (visual) → output: React app. Generation, validation, repair adımları üç mimariyle koordine ediliyor: Supervisor (tool-calling), Hierarchical, Custom (deterministik workflow). Değerlendirme: 4 real-world proje, 75 user story, 6 generator–judge model çifti (Claude, Gemini, GPT). Metrikler: functional coverage ve visual fidelity (full/partial), token maliyeti.
Findings:
- Full functional coverage %54, full visual fidelity %58; partial dahil %77 ve %85.
- Mimari seçimi kaliteyi sadece 3–5 puan etkiliyor ama maliyeti ciddi etkiliyor: Custom, generator token'ını %21–65 azaltıyor.
- Judge modeller maliyeti domine ediyor (generator'dan ortalama 5.9x fazla token).
- Refusal retry, JSX sanitization, template scaffolding'den oluşan hafif repair toolkit, generation hatalarının çoğunu regeneration olmadan çözüyor.
Relevant Limitations:
- Ölçüm LLM-judge'a dayanıyor; generator ve judge aynı model aileleri içinden, self-preference riski var. Executable/E2E test yok gibi görünüyor.
- Sadece 4 proje, tek framework (React); ölçek küçük.
- User story'ler free-form NL; yapılandırılmış acceptance criteria/BDD kullanımı abstract'ta yok.
Key Takeaway:
- Multimodal spec (story + design) → app üretiminde orkestrasyon mimarisinin kaliteden çok maliyeti etkilediği bulgusu survey için değerli.
- Judge maliyetinin generator'ı aşması, LLM-judge tabanlı değerlendirmenin ölçeklenebilirliğini sorgulatıyor.

### Echo — Echo: A Voice and Text-Driven Framework for Automated Mobile Application Development Using Large Language Models (preprint, 2025) [doi:10.5281/zenodo.17841335]
Method. Full text yok, not abstract'a dayanıyor. Sesli veya yazılı kullanıcı gereksinimlerini React Native mobil uygulamaya çeviren konuşma tabanlı framework.
Pipeline: multimodal input processing (ses/metin) → iteratif intent clarification → structured specification generation → kod üretimi → autonomous build orchestration; Android ve iOS için tek codebase. Değerlendirme: geliştirme yaşam döngüsü süresi (conventional workflow'a göre) ve gürültülü akustik koşullarda intent resolution accuracy.
Findings:
- Geliştirme süresini "drastically" azalttığı iddia ediliyor; sayılar abstract'ta verilmiyor.
- Gürültülü ortamda bile yüksek intent resolution accuracy raporlanıyor (sayı yok).
Relevant Limitations:
- Üretilen uygulamanın functional correctness'ı için test tabanlı ölçüm görünmüyor; "production-ready" iddiası desteklenmemiş.
- Ara temsil olarak structured specification kullanılması olumlu, ama spec'in formatı ve doğrulanabilirliği belirsiz.
- Zenodo preprint; benchmark/uygulama sayısı ve baseline belirsiz.
Key Takeaway:
- NL → structured spec → app zinciri survey'deki "yapılandırılmış hand-off" temasına örnek, ama değerlendirme zayıf; çoğunlukla sistem demosu olarak anılmalı.

### Spec2Code — Spec2Code: A Human-Supervised Framework for End-to-End LLM-Assisted Software Development (preprint, 2025) [doi:10.24433/co.6120886.v1]
Method: NL requirements → deployment-ready kod üreten, dört fazlı (specification, planning, task generation, implementation) specification-driven framework; kayıt bir Code Ocean capsule'ü (ilişkili makale ayrıca bulunamadı).
Her faz "constitutional quality gates" ve real-time anti-evasion mekanizmaları ile korunuyor; LLM evasion davranışları için bir taxonomy, platform-specific quality constraint'ler, architecture pattern detection ve structured prompt template'ler öneriliyor. Değerlendirme: web, mobile, AI ve full-stack alanlarından 18 real-world proje. Metrikler: geliştirme süresi, maliyet, test coverage, security vulnerability sayısı.
Findings:
- Ortalama 4.6 saat ve proje başına ~$1.11; geleneksel geliştirme tahmini $117,000–$160,500'e karşı "%99.98 maliyet azalması" iddiası.
- %85+ test coverage, sıfır critical security vulnerability; evasion denemeleri real-time yakalanmış.
Relevant Limitations:
- Functional correctness için bağımsız bir oracle yok: coverage, sistemin kendi (muhtemelen LLM-generated) testleri üzerinden — aynı model hem kodu hem testi yazıyor.
- Geleneksel maliyet karşılaştırması tahmini; baseline agent/framework ile kontrollü karşılaştırma görünmüyor. "Human-supervised" — insan müdahalesinin payı ölçülmemiş olabilir.
- Full text yok; capsule'ün hakemli bir makaleye bağlı olup olmadığı belirsiz.
Key Takeaway:
- LLM "evasion" (testi atlama, stub bırakma) davranışını açıkça ele alması survey için ilginç bir tema; ancak değerlendirme iddiaları doğrulanabilir değil.

### CodeCraft — Hybrid Multi-Agent Framework for Enterprise Web Application Generation (preprint, 2026) [doi:10.20944/preprints202608.1294.v1]
Method. Full text yok; not abstract üzerinden. Enterprise CRUD web app üretiminde schema/backend/frontend tutarsızlığına karşı hibrit yaklaşım: yapısal kod deterministik generator'larla, sadece belirsiz kararlar LLM ile.
Prisma schema ve DMMF temsili tek source of truth; deterministik generator'lar backend API, frontend manifest, RBAC ve DB seeder üretiyor. LangGraph üzerinde 6 agent (requirements engineering, schema design, orchestration, backend, frontend, containerization) yalnızca requirement netleştirme, schema validation ve yapısal olmayan kararlar için. Output: deploy edilebilir containerized uygulama.
Findings:
- Schema validation, schema düzeltme için gereken otomatik iterasyonu 2–4'e indiriyor.
- Requirement ve schema onayından sonra end-to-end generation manuel emek olmadan deploy edilebilir uygulama üretiyor.
- Geliştirme eforunda %70–80 azalma iddiası — yazarların kendisi kontrollü dış çalışmayla doğrulanmadığını belirtiyor.
Relevant Limitations:
- Değerlendirme zayıf: benchmark, baseline, functional test veya kullanıcı çalışması abstract'ta yok; kaç uygulama denendiği belirsiz.
- Hand-off structured (Prisma schema) — güçlü yön, ama kapsam CRUD tipi uygulamalarla sınırlı.
Key Takeaway:
- Structured, executable artefakt'ı (schema) tek source of truth yapıp LLM'i dar kararlara hapsetmek, cross-layer tutarlılık için ilginç bir tasarım; ampirik kanıt eksik.

### JamBench / JamSet — JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines (preprint, 2026) [arxiv:2606.19830]
Benchmark + training data. Godot engine üzerinde project-level oyun kodu üretimi; Game Jam projelerinden toplanmış veri ve deterministik headless-engine doğrulama pipeline'ı.
~240K aday repodan (Ludum Dare, itch.io, GGJ, GitHub vb.) Godot 4.x, 2D, ≥1,200 game line filtresi ve L1 (file integrity) / L2 (headless compile) / L3a (30 sn runtime stability) / L3b (60 sn deterministik input ile behavior collection) ile 8,133 doğrulanmış proje. 300'ü (S/M/L 100'er, 4K ve 15K satır eşikleri) elle oynanarak doğrulanmış JamBench; 7,833'ü multi-turn SFT verisi JamSet. Task 1: Game Jam theme'den (1a sadece keyword, 1b + gameplay description) sıfırdan proje, 50 theme × 3 run. Task 2: fonksiyon (2a), script (2b), tüm .gd (2c) silinmiş projeyi tamamlama. Metrikler: L1/L2/L3a pass rate, SCS (7 statik boyutta referansa oran), BAS (runtime davranış istatistiklerinin referansa benzerliği). Dil GDScript + .tscn.
Findings:
- Task 1a'da L3a ortalaması %70.7 ama SCS/BAS çok düşük (ör. GPT-5.4 SCS 0.46, BAS 0.17): derlenen ama minimal projeler.
- Task 2a runtime pass rate Small'da %80.4'ten Large'da %5.7'ye düşüyor; 2c Large'da çoğu model ~0.
- Claude Code agent modu pass rate'i artırıyor (Claude Task 1a L3a 77.3 → 82.7) ama SCS/BAS neredeyse değişmiyor (0.41 → 0.42; 0.11 → 0.13).
- Qwen3.5-27B JamSet SFT ile compile rate ve SCS'te iyileşiyor.
Relevant Limitations:
- SCS/BAS referans projeye (Task 2) veya dataset ortalamasına (Task 1) bağlı; farklı ama geçerli bir oyun tasarımı cezalandırılır, Task 1'de "doğruluk" aslında ölçülmüyor.
- eval_config LLM ile üretiliyor (input stratejisi için), yani ölçümde dolaylı LLM izi var.
- Açık kaynak Game Jam projeleri — contamination riski yüksek, tartışılmıyor.
Key Takeaway:
- Headless engine ile deterministik runtime behavior toplama, oyun gibi I/O'su olmayan domain'lerde LLM-judge'a alternatif; ama davranış benzerliği ≠ functional correctness.

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

### SaaSBench — SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering (preprint, 2026) [arxiv:2605.17526]
Benchmark + empirical çalışma: agent'a uzun bir PRD (~4,363 satır ortalama) + ambiguity-resolution KB veriliyor, izole bir Docker ortamında sıfırdan çalışan, deploy edilmiş bir enterprise SaaS sistemi (frontend + backend + DB + auth) kurması isteniyor.
30 task, 6 SaaS domain; PRD'ler gerçek open-source seed repo'lardan (annotator + Cursor ile) tersine çıkarılmış. 8 dil, 6 DB, 13 framework. Değerlendirme DAG tabanlı: 5,370 validation node, 6,167 prerequisite edge; her node HTTP request / login / rubric-LLM-judge primitive zinciri. Skorlama binary / weighted / llm-as-judge (Claude Sonnet 4.5, temp 0); prerequisite başarısızsa node "Skipped dependency". Metrikler: Pass@1 ve Node Coverage, 6 capability dimension (Deploy, Data, API, Logic, AuthZ, Quality). Referans implementasyon tüm test suite'i geçmek zorunda.
Findings:
- En iyi: Claude Opus 4.7 + Claude Code %20.68 Pass@1; ortalama Claude Code %11.64, OpenHands %9.26.
- 480 capability unit analizinde %63.5'te stack hiç stabil çalışmıyor, %32.1 yüzeysel erişilebilir ama yapısal eksik; yalnızca %3.8'de business logic darboğaz — hataların >%95'i derin mantığa ulaşmadan.
- Harness etkisi büyük: aynı model Claude Code / Codex CLI'da OpenHands'ten daha iyi.
- Daha çok adım ≠ daha iyi: GPT-5.4 36 adımda %7.44, MiniMax M2.7 279 adımda %6.78.
Relevant Limitations:
- PRD'ler seed repo'dan reverse-engineer edilmiş, API contract'lar ve data model PRD'de sabit — test suite referans repo'ya kuplajlı; alternatif tasarımlar (farklı endpoint şekli) cezalandırılabilir.
- LLM-judge ölçümün içinde (layout vb. node'lar); judge Claude ailesi, en iyi sonuç da Claude — aile yanlılığı kontrol edilmemiş.
- Yalnızca 30 task; seed repo'lar popüler GitHub projeleri → contamination riski tartışılmıyor.
Key Takeaway:
- Uzun-horizon app üretiminde asıl darboğaz kod mantığı değil, çok bileşenli sistemi ayağa kaldırma/entegrasyon; DAG + dependency gating, erken hataların downstream'i kirletmesini engelleyen iyi bir değerlendirme deseni.

### UI2App — UI2App: Benchmarking Visual Interaction Inference in Executable Web Application Generation (preprint, 2026) [arxiv:2607.06306]
Benchmark + empirical çalışma: sadece statik screenshot'lardan (metin veya davranış açıklaması olmadan) çok route'lu, çalışan bir React + TypeScript uygulaması üretimini ölçüyor. Asıl odak "interaction inference".
Veri seti 2,013 aday repodan filtrelenip uzman seçimiyle oluşturulmuş 45 uygulamadan oluşuyor: 327 screenshot, set başına 4–14. Sabit bir React+TS scaffold var. Model önce file plan, sonra dosya başına kod üretiyor; en fazla 3 stderr-feedback repair turu yapılıyor. Metrikler: EXEC@1/@3 (vite build + render), NRS (route erişilebilirliği, insan doğrulamalı), VFS (reference ile judge-free DOM block matching) ve IIS (7 interaction kategorisi × scope S1–S3, 3 annotator, rubric-based, Krippendorff α 0.72–0.84). 6 VLM değerlendirilmiş, ayrıca Qwen2.5-VL 3B–72B scaling çalışması var.
Findings:
- IIS'te lider Claude Sonnet 4.6 (39.3). VFS lideri Gemini 3.1 Pro (78.1) IIS'te sadece 7.5 alıyor; yani görsel sadakat interaction yeteneğini göstermiyor.
- Cross-route state (S3) kategorisinde 6 modelin 3'ü tam olarak 0 alıyor; Claude 21.6.
- EXEC@3 başarısızlıklarının %50'si scaffold kurallarının ihlali; %37'si hallucinated lucide-react icon import'u.
- Qwen2.5-VL'de 32B→72B arasında faz geçişi var: EXEC@3 ≤%2.2'den %62.2'ye çıkıyor.
Relevant Limitations:
- IIS ve NRS insan annotasyonuna dayanıyor; ölçeklenebilirlik düşük ve scaling deneyinde toplanmamış. VFS reference render'a görsel benzerlik ölçüyor.
- 45 uygulama, tek stack (React+TS), tek sample. Reference uygulamalar public GitHub projeleri olduğu için contamination riski var.
- Agentic harness yok, plan + per-file generation yapılıyor.
Key Takeaway:
- Rubric-based ve implementation-agnostic interaction değerlendirmesi, reference'a bağlı test'lere bir alternatif; ama bugün için insan maliyetiyle geliyor.

### Vibe Code Bench — Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development (preprint, 2026) [arxiv:2603.04601]
Benchmark + empirical çalışma: sıfırdan, sadece NL spec'ten deploy edilebilir full-stack web uygulaması üretimi ("zero-to-one").
100 spec var (50 private validation, 50 test), üç domain'de: Individual, Solo Founder ve Enterprise. Spec'lerin %28'i Stripe ve/veya email entegrasyonu gerektiriyor. Spec ve workflow'lar GPT-5 ile draft edilip iki PM tarafından review ediliyor; ardından LLM audit geçiyor. Toplam 964 workflow ve 10,131 substep var. Harness OpenHands fork'u; 5 saatlik wall-clock bütçe, zorunlu React+Vite+Supabase stack ve Docker Compose. Değerlendirmeyi Browser Use agent'ı (Claude Sonnet 4.5) yapıyor: substep başına pass/fail veriyor, ≥%90 substep geçerse workflow pass sayılıyor. 16 model değerlendirilmiş.
Findings:
- Test split sonuçları: GPT-5.3-Codex %61.8, Opus 4.6 %57.6, GPT-5.2 %53.5. Açık modeller %5–24, Grok 4.1 Fast %1.2.
- Self-testing (browser tool çağrısı) ile accuracy korelasyonu r=0.72; edit hacmi ile r=0.09.
- Davranışsal hataların %46.7'si missing feature, %20.4'ü auth sorunu. İlerleme ağırlıkla sıfır puan alan app'lerin azalmasından geliyor.
- Evaluator alignment: Sonnet 4.5–insan uyumu %86.4, GPT-5.2–insan %36.1; insan–insan %88.6–93.6.
Relevant Limitations:
- Ölçüm LLM içinde yapılıyor: spec ve workflow'ları GPT-5 draft ediyor, verdict'i Claude Sonnet 4.5 veriyor. Evaluator seçimi sonucu büyük ölçüde değiştiriyor ve Claude modellerini değerlendirirken aile bias'ı olası.
- Workflow'lar NL; implementation-agnostic olması artı, ama deterministik değil. Human alignment örneklemi küçük (18 app).
- Tek stack ve tek harness; kod kalitesi ve güvenlik ölçülmüyor. Maliyet yüksek (app başına $0.2–40).
Key Takeaway:
- Browser-agent tabanlı E2E değerlendirme reference coupling'i azaltıyor ama evaluator seçimini birinci derece bir tasarım parametresine çeviriyor; human alignment raporlaması zorunlu olmalı.

### WebCraftBench — WebCraftBench: Evaluating Web Application Generation from a Software Testing Perspective (preprint, 2026) [arxiv:2609.15387]
Benchmark + empirical çalışma: agent'ların (Claude Code/Codex) NL requirement'tan ürettiği front-end web uygulamalarını software testing bakış açısıyla, etkileşimli olarak değerlendiriyor.
Kurumsal Code Arena replikasından alınmış 369 gerçek kullanıcı requirement'ı var (%63'ü eksik veya belirsiz). Toplam 5,088 acceptance criterion; bunlar 3 LLM tarafından üretilip Opus 4.8 ile birleştirilmiş ve insan doğrulamasından geçmiş. Pipeline dört aşamalı: (i) Istanbul ile coverage instrumentation (static HTML, Vite, Next, CRA, Astro), (ii) Playwright MCP üzerinden LLM tester agent ile keşif, coverage plateau'da uncovered koddan NL ipucu üretimi, (iii) DOM normalizasyonuyla state-transition graph, (iv) LLM/VLM judge'lar (aesthetics ve usability için advocate/critic/judge protokolü, alignment için evidence-citing agent). 17 model, toplam 6,273 app. Skorlar z-score olarak raporlanıyor.
Findings:
- Genel sıralamada Claude-Opus-5 birinci. GPT-5.6-Sol aesthetics'te, Kimi-K3 alignment'ta lider; hiçbir model her boyutta önde değil.
- 197 arena oturumunda insan tercihiyle %85.3 uyum; Δz≥0.25 için >%90. Code Arena ile Spearman ρ=0.890.
- Judge Gemini-3.7-Flash ile değiştirildiğinde sıralama korelasyonu ρ=0.980 kalıyor, ama raw skorlar ciddi kayıyor.
- Coverage guidance medyan function coverage'ı %91.9'dan %94.3'e çıkarıyor. Instrumentation başarısı %99.89.
Relevant Limitations:
- Ölçüm baştan sona LLM: checklist'leri LLM üretiyor, keşfi LLM agent yapıyor, skoru LLM judge veriyor. Exploration ve scoring'de Claude-Opus-4.8 kullanılırken Claude modelleri de değerlendiriliyor (aile bias'ı).
- Front-end only, tek tur, text-only. Output formatı serbest (tek HTML'den Vite projesine kadar), bu yüzden multi-file olup olmadığı garanti değil. Uygulamalar basit (yazarlar da kabul ediyor).
- z-score'lar model havuzuna bağımlı. Dataset ve kod public değil, yani reproducibility düşük.
Key Takeaway:
- Code coverage'ı hem exploration sinyali hem kanıt kapsamı ölçüsü olarak kullanmak, browser-agent E2E değerlendirmesinde "agent özelliği bulamadı mı, yoksa özellik yok mu" belirsizliğini azaltmanın somut bir yolu.

### WebDesignIter — WebDesignIter: Co-Evolving Design Knowledge for Repository-Level Front-End Code Generation (preprint, 2026) [arxiv:2607.10621]
Method çalışması: incremental front-end repo geliştirme için design knowledge'ı (mimari prensipler, modül sorumlulukları) kalıcı bir knowledge graph'ta (WebAppArchKG) tutan agent framework'ü.
İki aşama: design-informed planning (KG'den tarihsel context + mimari özet → implementation plan + test script'leri), design-aware generation (diff-based patch, sandbox execution, otomatik syntax repair, spaghetti dosyaların refactor'u, sonra KG güncelleme). Değerlendirme Web-Bench üzerinde: 50 proje × 20 sıralı NL task, her task önceki task'ların ürettiği repo state'ine bağlı; Vue/Angular/Tailwind vb. Metrikler Pass@1/Pass@2 (Web-Bench'in E2E testleri), ayrıca maintainability proxy olarak average file length. 9 foundation model (Gemini 2.5 Pro, Claude 4 Sonnet, GPT-4.1, GPT-4o, o4-mini, Qwen-Max/Plus, DeepSeek-V3/R1) + RQ4'te DeepSeek V4 ve Qwen 3.5.
Findings:
- Web-Agent baseline'ına göre ortalama +7.98pp Pass@1, +9.55pp Pass@2 (Claude 4 Sonnet: 34.90/48.10 vs 24.30/39.70).
- Ablation (Claude 4 Sonnet): design knowledge çıkarılınca Pass@1 −11.40pp; code graph −8.40pp, patch −3.50pp; ilginç şekilde sandbox'sız varyant en iyi sonucu veriyor.
- Claude Code, OpenHands, SWE-Agent, Codex CLI'ı tüm konfigürasyonlarda geçiyor; DeepSeek V4 Pro ile 33.53/53.14 Pass@1/2, ~26× daha az input token (533K vs 13,949K Claude Code). Codex CLI (GPT-5.5) sadece 8.5 Pass@1 — harness uyumsuzluğu şüphesi.
- Regression hataları %29.17 → %4.17; average file length 49.41 → 35.38.
Relevant Limitations:
- Tek benchmark (Web-Bench); 50 proje, sadece front-end.
- Genel amaçlı agent karşılaştırması Web-Bench'e özel adapte edilmemiş harness'larla; Codex CLI'ın çok düşük skorları karşılaştırmanın adilliğini sorgulatıyor.
- Maintainability sadece file length proxy'si ile ölçülüyor; planning aşamasında LLM kendi test script'lerini üretiyor (self-validation).
Key Takeaway:
- Incremental repo inşasında explicit, yapılandırılmış mimari bilgi (KG) free-form context'ten daha etkili; regression'ı düşürmenin anahtarı.
- Sequential-task benchmark'lar (Web-Bench) nl-to-app'in "evolving" varyantı için iyi bir test yatağı.

### WebGen-R1 — WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning (preprint, 2026) [arxiv:2604.20398]
Method/training çalışması: küçük bir LLM'i (Qwen2.5-Coder-7B-Instruct) multi-page website üretimi için end-to-end RL (GRPO) ile eğitiyor.
Scaffold-driven generation: sabit, önceden doğrulanmış React/Vite/Tailwind template (build config, routing skeleton, server logic sabit); model sadece değişken bileşenleri (sayfalar, komutlar, stiller) tek inference'ta üretiyor. Cascaded reward: static compliance → install/bundle/serve/render → VLM aesthetic skoru + execution log'larından functional integrity + format reward. Eğitim: WebGen-Instruct (6,667 task); 600 GPT-4.1 distilled örnekle SFT warm-up, sonra 400 RL adımı. Değerlendirme: WebGen-Bench (101 task) ve WebDev Arena'dan LLM-judge ile filtrelenmiş 119 task (OOD). Metrikler: FSR (WebVoyager GUI-agent ile test case'ler), AAS (VLM skoru), VRR (render oranı), LDPR (ESLint + dependency).
Findings:
- WebGen-R1-7B: FSR 29.21% (base 1.59%), AAS 3.94, VRR 95.89%; DeepSeek-R1 FSR 30.25% ile başa baş.
- En yüksek FSR hâlâ Claude-3.7-Sonnet (57.72%) — RL modeli functional correctness'ta frontier'ın yarısında.
- Aesthetics model boyutuyla daha kolay ölçekleniyor; functional correctness çok daha zor.
Relevant Limitations:
- Ölçüm tamamen LLM içi: FSR GUI-agent (GPT-4o), AAS VLM (GPT-4o); aynı GPT-4o hem training reward'da hem evaluation'da — reward hacking/judge bias riski ciddi.
- Sabit template yapısal problemi büyük ölçüde ortadan kaldırıyor; "project-level" iddiası mimari kararları kapsamıyor.
- WebDev Arena'da FSR raporlanmıyor (test case yok).
Key Takeaway:
- Scaffold + execution-grounded cascaded reward, repo-level RL'i hesaplanabilir kılmanın pratik yolu; ama evaluator ile reward'ın ayrıştırılması şart.

### AADF — AutoGPT Devloop: An Autonomous AI Development Framework for End-to-End Software Generation, Execution, and Self-Repair (TIMES-iCON 2025, 2025) [doi:10.1109/times-icon67125.2025.11488122]
Full text yok; not abstract'a dayanıyor. Method çalışması: high-level hedefleri çalışan yazılıma çeviren self-developing agent (AADF).
Bileşenler: task decomposition, vector DB tabanlı semantic code memory, sanal ortam yönetimi, otomatik file/version control; plan → kod → execution → self-repair döngüsü. Design Science Research yaklaşımı; 15 GUI/web task, 5 zorluk seviyesi, 3 deneme (45 trial). Kullanılan LLM ve dil abstract'ta belirtilmiyor.
Findings:
- 41/45 trial (%91.1) manuel kod düzenlemesi olmadan tamamlanıyor.
- Level 1-2 ve 4'te %100; external API credential veya büyük NLP kaynak gerektiren task'larda düşüş (Level 3: %67/%33, Level 5: %67).
- Self-repair özellikle dependency çakışmaları ve eksik import'larda etkili.
Relevant Limitations:
- "Success" kriteri abstract'ta tanımlı değil; muhtemelen çalışırlık/manuel kontrol, test tabanlı değil.
- 15 task, baseline karşılaştırması yok; ölçek çok küçük.
Key Takeaway:
- Environment/dependency self-repair, end-to-end app generation'da temel başarısızlık kaynağını hedefliyor; ama kanıt zayıf.

### AgingGen — Investigating Software Aging in LLM-Generated Software Systems (preprint, 2025) [arxiv:2510.24188]
Empirical çalışma: LLM ile üretilmiş servis uygulamalarında uzun süreli çalışmada software aging (memory leak, latency artışı) olup olmadığını inceliyor.
Bolt platformu ile BaxBench prompt'larından (OpenAPI şeması + NL) 4 JavaScript/Express backend üretilmiş (image converter, credit card manager, process monitor, uptime checker). Sadece BaxBench functional testlerini geçenler 50 saatlik JMeter yük testine (10 thread) sokuluyor; memory, CPU, response time, throughput; Mann-Kendall + Sen's slope.
Findings:
- 4 uygulamanın hepsinde istatistiksel olarak anlamlı memory artışı (p≈0); en dik Credit Card App (slope 37.68e-3).
- Convert Image App en yüksek ortalama latency (2645.87 ms) ve pozitif trend; Monitor App ~25. saatten sonra artan latency.
- Aging'in şiddeti uygulama tipine göre değişiyor.
Relevant Limitations:
- Sadece 4 uygulama, tek araç (Bolt), altındaki LLM belirtilmiyor; tek run.
- Aging'in LLM kaynaklı olduğu, insan-yazımı baseline olmadan gösterilemiyor.
- BaxBench backend'leri büyük ihtimalle az dosyalı; multi-file yapı raporlanmıyor.
Key Takeaway:
- Üretilen uygulamaların non-functional, uzun vadeli davranışı (reliability) repo-generation değerlendirmesinde neredeyse hiç ölçülmüyor; bu çalışma bir metodoloji iskeleti sunuyor.

### WebGen-Agent — WebGen-Agent: Enhancing Interactive Website Generation with Multi-Level Feedback and Step-Level Reinforcement Learning (preprint, 2025) [arxiv:2509.22644]
Core method + training çalışması: NL talimatından boş codebase ile başlayıp multi-file web sitesi üreten agent; execution, screenshot (VLM) ve GUI-agent testing feedback'i ile iteratif iyileştirme, backtracking ve select-best.
Her adım: codebase edit → dependency install + servis başlatma → Qwen2.5-VL-32B screenshot açıklaması/puanı → GUI-agent testi ve puanı. Step-GRPO: her adımın screenshot + GUI skorları step-level reward olarak kullanılıyor; ~700 DeepSeek-V3 trajectory ile SFT warm-start, 500 WebGen-Instruct talimatı ile GRPO. Değerlendirme WebGen-Bench (101 talimat, 647 GUI-agent test case; accuracy + GPT-4o appearance score).
Findings:
- Claude-3.5-Sonnet: Bolt.diy'de 26.4% → WebGen-Agent'ta 51.9% accuracy, appearance 3.0 → 3.9.
- En iyi: Qwen3-Coder-480B 58.2%, appearance 4.3.
- Qwen2.5-Coder-7B: 12.4% → SFT 38.9% → Step-GRPO 45.4%.
- Ablation: GUI-agent feedback en büyük accuracy katkısı (+3.3), screenshot appearance'ı 3.0→3.6.
Relevant Limitations:
- Hem feedback/reward hem de benchmark ölçümü VLM/GUI-agent tabanlı (Qwen2.5-VL-32B); aynı model reward'da ve evaluation'da → reward hacking / circularity riski.
- Baseline'ların değerleri WebGen-Bench paper'ından alınmış, harness farklı.
- Tek benchmark, 101 task; backend/DB derinliği sınırlı.
Key Takeaway:
- App üretiminde GUI-level E2E feedback hem inference hem RL reward olarak işe yarıyor; ama oracle'ın kendisi LLM, executable değil.

### Devonix — Devonix: A Hierarchical Multi-Agent and Neuro-Symbolic Orchestration Framework for Autonomous Web Application Synthesis (ICCMC 2026, 2026) [doi:10.1109/iccmc69250.2026.11624731]
Core method (sadece abstract okundu, full text yok): non-technical kullanıcının NL gereksiniminden modüler HTML/CSS/JS web uygulaması üreten hiyerarşik multi-agent framework.
Hierarchical Intent Modeling ile gereksinim doğrulanabilir subtask şemalarına ayrılıyor; LLM synthesis engine kod üretiyor; Smart Code Regeneration yapısal/mantıksal hataları onarıyor; Automated QA Validation sözdizimi ve "runtime simulation" kontrolü yapıyor. 50 stratified web app görevi üzerinde prompt-based ve manuel baseline'larla karşılaştırma.
Findings:
- Architectural accuracy 96.8%, structural integrity 94.2%, functional error'da %63 azalma, ortalama deployment latency 2.1 s (p < 0.001).
Relevant Limitations:
- Metrik tanımları abstract'ta yok; "architectural accuracy" neye göre (referans mimari mi?) belirsiz — reference coupling riski.
- Fonksiyonel doğruluk için executable test/oracle belirtilmemiş; 50 task, kaynak ve kontaminasyon bilgisi yok.
- Sadece front-end stack (HTML/CSS/JS).
Key Takeaway:
- Structured subtask şemaları hand-off için umut verici, ama değerlendirme full text olmadan doğrulanamıyor; düşük ağırlıkla raporlanmalı.

### Flutter-ChatGPT — Empirical evaluation of automated code generation for mobile applications by AI tools (IEEE C3 2023, 2023) [doi:10.1109/c358072.2023.10436306]
Core empirical çalışma (sadece abstract, full text yok): ChatGPT-3.5 ile Flutter framework'ünde sıfırdan bir mobil uygulama iteratif prompt'larla üretiliyor, süreç her adımda değerlendiriliyor.
Tek uygulama/case study; değerlendirme dört gösterge: code quality, solution quality, response time ve insan-yazımı kodla karşılaştırma. Dil Dart. Otomatik test veya benchmark kullanılmadığı anlaşılıyor.
Findings:
- Belirli bir karmaşıklık seviyesine kadar, giderek detaylanan prompt'larla ChatGPT çalışır kod üretebiliyor; bu kod daha karmaşık mantık için temel olabilir.
- Sayısal sonuç abstract'ta raporlanmamış.
Relevant Limitations:
- Tek app, tek model (GPT-3.5), human-in-the-loop prompt iterasyonu → otonom üretim ölçülmüyor.
- Değerlendirme büyük olasılıkla subjektif/manuel; replikasyon zor.
Key Takeaway:
- Erken (2023) nl-to-app örneği; mobil domain ve Dart kapsaması açısından değerli ama kanıt gücü düşük.

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

### EvoGit — EvoGit: Decentralized Code Evolution via Git-Based Multi-Agent Collaboration (preprint, 2025) [arxiv:2506.02049]
Method çalışması: merkezi orkestratör, mesajlaşma veya shared memory olmadan, Git version graph'ı (phylogenetic DAG) koordinasyon ortamı olarak kullanan evolutionary multi-agent geliştirme framework'ü.
İnsan PM üst seviye hedefi ve seed scaffold'u veriyor; 16 bağımsız agent 120 iterasyon boyunca rastgele seçilen dosyadan ≤128 satırlık bölgeye mutation veya iki branch arasında crossover uyguluyor. Her yeni versiyon parent'ına karşı compiler/linter/type-checker/test çıktılarıyla ve bir LLM-judge'ın binary kararıyla kabul/ret ediliyor ("no worse than parent" partial order). İnsan her 10 (Task 1) / 20 (Task 2) iterasyonda frontier'dan bir versiyon seçip kısa feedback veriyor. Görevler: (1) Next.js scaffold'dan araştırma projesi tanıtım web sitesi, (2) bin-packing solver'ı LLM ile evrimleştiren meta-level Python pipeline.
Findings:
- Her iki görevde de çalışan, modüler artefaktlar üretildiği ve repo'ların public olduğu raporlanıyor.
- Task 2'de input validation, logging, exception handling gibi özellikler talimatsız ortaya çıkmış (kalitatif gözlem).
- Nicel metrik, baseline veya tekrar sayısı yok.
Relevant Limitations:
- Değerlendirme yalnızca yazarların kalitatif incelemesi; "evaluation protocol" insan müdahalesini sınırlıyor ama başarıyı ölçmüyor.
- İnsan seçimleri (frontier'dan preferred version) sonucu ciddi yönlendiriyor; autonomy katkısı ayrıştırılamıyor.
- Kabul kararı LLM-judge'a dayalı; ölçüm ile üretim aynı model ailesinde.
- İki görev, tek run; model, maliyet ve token raporu sınırlı.
Key Takeaway:
- Git lineage'ı structured, denetlenebilir bir koordinasyon artefaktı olarak kullanmak ilginç bir tasarım; ama survey'de kanıt düzeyi "demonstration" olarak işaretlenmeli.

### RealDevWorld — You Don't Know Until You Click: Automated GUI Testing for Production-Ready Software Evaluation (preprint, 2025) [arxiv:2508.14104]
Benchmark + evaluation method: sıfırdan üretilen interaktif uygulamaları (web/app) GUI üzerinden tıklayarak değerlendiren RealDevWorld; RealDevBench (194 task) ve AppEvalPilot (agent-as-a-judge) bileşenleri.
Task = requirements açıklaması + yapılandırılmış feature listesi + bazı task'larda multimodal materyal (görsel, ses, tablo). Requirement'lar SRDD ve Upwork/Freelancer'dan; feature listeleri Claude-3.5-Sonnet ile GitHub projelerinin dokümantasyonundan genişletilmiş. Domain: Display %50, Analysis %18.6, Game %17, Data %14.4. AppEvalPilot feature'lardan test case üretip web/OS seviyesinde etkileşimle çalıştırıyor, Pass/Fail/Uncertain sınıflıyor. Validasyon: 49 Lovable-üretimi proje, 3 QA uzmanı ile human ground truth.
Findings:
- AppEvalPilot test case accuracy 0.92, feature-level korelasyon 0.85 (Browser-Use 0.58, WebVoyager 0.43); app başına 9 dk, Browser-Use'a göre %77 daha ucuz.
- 54 test task'ta agent sistemleri (MGX BoN-3 0.78, Lovable 0.74) düz LLM'lerden (%0.29–0.53) belirgin iyi; ortalama ~+0.27.
- Statik code quality ve visual skorlar runtime kalitesiyle uyumsuz.
Relevant Limitations:
- Ölçüm tamamen LLM-driven: feature listesi Claude ile üretilmiş, test case'ler ve verdict Claude-tabanlı agent'tan; üretici modellerle aynı aile (Claude-3.7) → self-preference riski.
- Human validation sadece Lovable çıktıları üzerinde; diğer sistemlere genelleme varsayılıyor.
- Deployment için LLM-generated komutlar kullanılıyor; deploy hatası ile fonksiyonel hata karışabilir. Model çıktılarının çok dosyalı olup olmadığı sisteme göre değişiyor (LLM'ler tek script).
- Değerlendirme sadece 54 task üzerinde, tek run.
Key Takeaway:
- GUI-tabanlı agent-as-judge, referans implementasyona bağlı olmadığı için alternatif tasarımları cezalandırmıyor; ama oracle güvenilirliği test üreten LLM'e taşınıyor — structured/executable feature spec'leri (BDD) bu boşluğu kapatabilir.

### ReactGH200 — React-ing to Grace Hopper 200: Five Open-Weights Coding Models, One React Native App, One GH200, One Weekend (preprint, 2026) [arxiv:2604.17187]
Küçük ölçekli empirical study. Beş open-weights model (Kimi-K2.5 Q3 ve Q4, GLM-5.1, Qwen3-Coder-480B, DeepSeek-V3.2; Unsloth GGUF, llama.cpp) aider whole-edit modunda tek prompt'la multi-file React Native (Expo) app üretiyor: "create react-native app that allows user to create account and login and then count kangaroos seen per day and make sure it runs on the web". Değerlendirme: `npm install && npx expo start --web` ile out-of-the-box çalışma + manuel feature checklist (auth, per-user isolation, per-day counting, history, logout, web-safety).
Findings:
- Tam spec-uyumlu tek app Kimi-K2.5 Q3'ten; SWE-Bench Pro SOTA'sı GLM-5.1 Firebase config gerektirdiği için çalışmıyor; DeepSeek-V3.2 çoğu feature'da başarısız.
- Hiçbir model `Alert.alert`'in web'de no-op olduğunu hesaba katmıyor (5/5).
- Reasoning token'ları (`</think>`) aider'ın file-path parser'ına sızıp App.js'i yanlış path'e yazdırıyor; temperature=0 reasoning modellerde hang'e yol açıyor.
Relevant Limitations:
- n=1 task, 1 seed, tek stack, re-prompt yok; SWE-Bench rank'ları ile "mispredict" iddiası istatistiksel olarak desteklenemez.
- Değerlendirme yazarın manuel checklist'i; test yok, rubric önceden tanımlı değil gibi.
Key Takeaway:
- Anekdot düzeyinde ama "runs out-of-the-box" + feature-level kontrolün patch-based benchmark'larda görünmeyen integration/platform hatalarını yakaladığını gösteriyor.

### ChatDev — ChatDev: Communicative Agents for Software Development (ACL 2024, 2024) [doi:10.18653/v1/2024.acl-long.810]
Method paper: waterfall'u taklit eden multi-agent framework (CEO, CTO, programmer, reviewer, tester), NL software requirement'dan çalışan, çok dosyalı küçük uygulama (oyun, GUI tool vb.) üretiyor.
Chat chain design → coding → testing fazlarını subtask'lara bölüyor; "communicative dehallucination" ile agent cevap vermeden önce detay talep ediyor. Veri: SRDD, 1,200 task prompt (5 alan, 40 alt kategori × 30); LLM-generated + insan refine. Model ChatGPT-3.5 (temp 0.2), Python 3.11 ile feedback. Metrikler: Completeness (placeholder içermeyen yazılım oranı), Executability (compile + doğrudan çalışma oranı), Consistency (requirement ile kod embedding cosine), Quality = üçünün çarpımı; ek olarak GPT-4 ve insan pairwise tercih.
Findings:
- Quality 0.3953 vs MetaGPT 0.1523 ve GPT-Engineer 0.1419; Executability 0.88 vs 0.41/0.36.
- Pairwise: insanlar %90.16 ChatDev'i GPT-Engineer'a, %88.00 MetaGPT'ye tercih ediyor.
- Ortalama 4.39 dosya, ~144 satır, 148 sn, ~23K token per yazılım; yani artefact'lar çok küçük.
- Ablation: roller kaldırılınca Executability 0.88 → 0.58.
Relevant Limitations:
- Fonksiyonel doğruluk hiç ölçülmüyor: "executability" sadece çalışıp çökmemesi; consistency embedding benzerliği, requirement karşılanmasını göstermez.
- SRDD kısmen LLM-generated; GPT-4 judge ve embedding metrikleri ölçüm içinde LLM kullanıyor.
- Hand-off'lar tamamen free-form NL diyalog; yapılandırılmış artefact (spec, test) yok.
- Tek model (GPT-3.5), baseline'lar aynı ayarlarla ama MetaGPT'nin kendi tasarım varsayımları farklı; maliyet yüksek.
Key Takeaway:
- Multi-agent SDLC paradigmasının referans noktası; ama değerlendirme "çalışıyor mu"da kalıyor, sonraki çalışmaların test/oracle tabanlı ölçüme geçme gerekçesi.

### FullstackGen-GPT5 — Web Application for the Automatic Code Generation of Fullstack Projects Using Generative Artificial Intelligence: GPT-5 (CSECS, 2026) [doi:10.1109/csecs69124.2026.11541607]
Method/tool çalışması: Design System'den başlayarak GenAI (GPT-5) orkestrasyonuyla fullstack proje (Angular frontend + .NET Core backend) üreten bir web uygulaması. Not: full text elde edilemedi; not abstract'a dayanıyor.
Pipeline dört faz: (i) Design System token analizi, (ii) GenAI orkestrasyonu, (iii) Angular + .NET Core kod üretimi (otomatik API dokümantasyonu, JWT/OAuth2 security dahil), (iv) SonarQube, Lighthouse ve WAVE ile kalite/erişilebilirlik doğrulaması. Validasyon: fonksiyonel prototip + iki öğrencinin birden fazla Angular/.NET modülü üretmesi; bug, vulnerability, code smell, performance ve accessibility metrikleri otomatik toplanıyor.
Findings:
- Uçtan uca akışın başarıyla tamamlandığı ve Design System ile hizalı projeler üretildiği raporlanıyor; sayısal sonuçlar abstract'ta yok.
- Kalite göstergeleri (SonarQube/Lighthouse/WAVE) inceleme için "objektif" sinyal olarak sunuluyor.
Relevant Limitations:
- Functional correctness değerlendirmesi yok: test yok, sadece static analysis + nonfunctional metrikler; "çalışıyor mu" sorusu cevapsız.
- n=2 öğrenci, baseline yok, tek model (GPT-5), tek stack; genellenebilirlik çok düşük.
- Input yapılandırılmış (Design System token'ları) — UI tarafı için iyi bir hand-off, ama backend requirement'ları nasıl veriliyor belirsiz.
Key Takeaway:
- nl-to-app alanında tool-demo tipi çalışmaların tipik zaafı: nonfunctional metrikler functional doğrulamanın yerine konuyor. Survey'de "evaluation gap" örneği olarak kullanılabilir.

### MetaGPT — MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework (ICLR 2024, 2023) [arxiv:2308.00352]
Method paper: SOP'leri (Standardized Operating Procedures) prompt dizilerine kodlayan, rol-tabanlı (Product Manager, Architect, Project Manager, Engineer, QA) multi-agent framework. Tek satırlık bir requirement'tan PRD, system design, API interface ve multi-file Python kodu üretiyor.
Agent'lar free-form chat yerine structured artefact'lar (PRD, dosya listesi, data structure/interface tanımları, sequence diagram) üzerinden shared message pool ile publish-subscribe iletişim kuruyor; Engineer için executable feedback (kodu çalıştırıp hata üzerinden düzeltme) var. Değerlendirme: HumanEval (164) ve MBPP (427) üzerinde pass@1; kendi SoftwareDev setinde (70 task: mini-game, image processing, data viz) sadece rastgele seçilmiş 7 task üzerinde human executability puanı (1–4), cost (süre, token), code statistics ve human revision cost. Baseline: ChatDev, AutoGPT, LangChain, AgentVerse; GPT-4 backbone.
Findings:
- HumanEval pass@1 %85.9, MBPP %87.7 (executable feedback ile; feedback +4.2/+5.4 puan).
- SoftwareDev'de executability 3.75 vs ChatDev 2.25; ortalama 5.1 dosya ve 251 LOC vs ChatDev 1.9 dosya / 77.5 LOC.
- Human revision cost 0.83 vs ChatDev 2.5; satır başına token 124 vs 249.
- Role ablation (2 task): sadece Engineer ile executability 1.0, dört rolle 4.0.
Relevant Limitations:
- Repo-level değerlendirme yalnızca 7 task üzerinde, test yok; executability tamamen subjective human rating, inter-rater bilgisi yok.
- HumanEval/MBPP isolated function-level; repository generation iddiasını desteklemiyor.
- Üretilen "repo"lar çok küçük (~250 LOC); SoftwareDev public test suite içermiyor, tekrarlanabilirlik zayıf.
Key Takeaway:
- Structured intermediate artefact'larla (PRD, interface spec) hand-off fikrinin öncüsü; ancak değerlendirme metodolojisi, sonraki benchmark'ların (DevBench, ProjectEval vb.) neden gerekli olduğunu gösteriyor.

### CloudMAS — A Multi-Agent Coding Assistant for Cloud-Native Development: From Requirements to Deployable Microservices (ACM proceedings, 2025) [doi:10.1145/3795154.3795362]
Method + benchmark (yalnızca abstract mevcut): NL requirement'tan deploy edilebilir cloud-native microservice uygulaması üreten multi-agent sistem ve CloudDevBench.
Altı agent: Architect (service decomposition, API design), backend/frontend/IaC için üç paralel Coder, Tester (test synthesis + execution), Ops (container config, Kubernetes manifest); bir Orchestrator iş akışını ve conflict resolution'ı yönetiyor, structured feedback loop'larla iteratif refinement. CloudDevBench: 50 real-world development task, test suite'ler ve deployment validation kriterleri ile. Metrikler: compilation success, test pass rate, deployment success. Kullanılan LLM'ler ve diller abstract'ta yok.
Findings:
- %92 compilation success, %81 test pass rate, %84 deployment success.
- Single-LLM ve single-agent baseline'lardan tüm metriklerde üstün olduğu iddia ediliyor (sayısal fark abstract'ta verilmemiş).
Relevant Limitations:
- Full text yok: test suite'lerin kaynağı (insan mı LLM mi yazdı), implementation-agnostic olup olmadığı, baseline detayları bilinmiyor.
- 50 task küçük ölçek; "real-world" task'ların kaynağı ve contamination durumu belirsiz.
- Test pass rate'in benchmark test'leriyle mi, Tester agent'ın ürettikleriyle mi ölçüldüğü abstract'tan net değil.
Key Takeaway:
- Deployment success'i ayrı bir metrik olarak eklemesi, build/test ötesinde operational doğrulama için ilginç bir örnek.

### AgileGen — Empowering Agile-Based Generative Software Development through Human-AI Teamwork (TOSEM 2025, 2024) [doi:10.1145/3702987]
Method: Agile'dan esinlenen, end-user'ı requirement ve acceptance kararlarına dahil eden human-AI teamwork framework'ü; Gherkin (Given-When-Then) senaryolarını user requirement ile kod arasında ara artefakt olarak kullanıyor (arXiv 2407.15568 full text üzerinden).
Akış: requirement clarification → Gherkin scenario design (kullanıcı onaylıyor/ekliyor/siliyor) → visual design → code generation → "consistency factor" ile scenario–kod uyumu → auto modification → end-user acceptance. Çıktı çok dosyalı web uygulaması (index.html, style.css, script.js). Değerlendirme 40 web projesi ve SRDD üzerinde; metrikler insan-puanlı Code Executability (0–4, ChatDev'den) ve User Experience Questionnaire (UEQ) + Likert; baseline'lar ChatDev, MetaGPT, GPT-Engineer vb.
Findings:
- Abstract'a göre baseline'lara göre %16.4 iyileşme (insan-puanlı executability) ve yüksek kullanıcı memnuniyeti.
- Gherkin senaryoları kullanıcı niyetini ölçülebilir kabul kriterlerine çeviriyor ve üretimi yönlendiriyor.
Relevant Limitations:
- Fonksiyonel doğruluk otomatik test ile ölçülmüyor; "executability" insan yargısı, UEQ algısal.
- Uygulamalar küçük, front-end ağırlıklı (HTML/CSS/JS); insan-in-the-loop olduğu için otonom sistemlerle doğrudan kıyas zor.
Key Takeaway:
- Gherkin/BDD senaryolarını requirement ile kod arasında yapılandırılmış hand-off olarak kullanmak (E2EDev'deki BDD oracle'ının üretim tarafındaki karşılığı); structured hand-off tezine erken bir örnek.

### Co-Learning — Experiential Co-Learning of Software-Developing Agents (ACL 2024, 2023) [doi:10.18653/v1/2024.acl-long.305]
Method: ChatDev üzerine, instructor ve assistant agent'ların geçmiş trajectory'lerinden "shortcut" deneyimleri çıkarıp yeni görevlerde kullandığı experiential co-learning framework'ü (arXiv 2312.17025 full text).
Değerlendirme SRDD (1,200 NL yazılım gereksinimi, 5 kategori) test split'i üzerinde, ChatDev'in metrikleriyle: Completeness (placeholder'sız kod oranı), Executability (çalışma), Consistency (requirement–kod embedding benzerliği) ve bunların çarpımı Quality; baseline GPT-Engineer, MetaGPT, ChatDev.
Findings:
- Quality 0.7304 vs ChatDev 0.4267, MetaGPT 0.1439, GPT-Engineer 0.1363; Executability 0.965 vs 0.880.
- Süre ChatDev'e göre daha kısa (122.8 s vs 148.2 s).
Relevant Limitations:
- Fonksiyonel doğruluk ölçülmüyor: executability çalışıp çökmemek, consistency embedding benzerliği (ChatDev ile aynı zayıflık); metrikler aynı grubun kendi tanımları.
- Artefact'lar küçük (ChatDev ölçeğinde birkaç dosya); bağımsız benchmark'ta doğrulama yok.
Key Takeaway:
- Deneyim/hafıza tabanlı iyileşme ChatDev metriklerinde büyük görünüyor; bağımsız, test-tabanlı oracle altında (E2EDev) bu çizgideki framework'lerin avantajı kaybolduğu için dikkatle yorumlanmalı.

### AppForge — AppForge: From Assistant to Independent Developer -- Are GPTs Ready for Software Development? (preprint, 2025) [arxiv:2510.07740]
Benchmark: NL spec'ten sıfırdan komple Android app üretimi. 101 task, F-Droid'deki gerçek open-source app'lerden türetilmiş.
Spec LLM ile app dokümanı/kodundan özetleniyor, GUI agent app'i gezerek davranışı zenginleştiriyor ve UI test case'leri (UI action dizisi + element exists/not-exists oracle) sentezliyor; Android uzmanları spec ve testleri doğruluyor. Model çıktısı JSON {filename: code}; harness projeyi assemble edip APK derliyor, emulator'de testleri koşuyor, ek olarak lightweight fuzzer ile crash arıyor. Metrikler: compile rate, test pass rate, crash rate, success. 12 LLM + mini-SWE-agent ve Claude Code.
Findings:
- En iyi GPT-5 (high reasoning) %14.85 success, compile-error feedback ile %18.81; open-source modeller <%10.
- Fonksiyonel doğru app'lerin >%50'si runtime'da crash ediyor.
- Agent'lar marjinal: mini-SWE-agent + Claude-4-Opus %11.88.
- GPT-4.1 compile hatalarını düzeltmek yerine implementasyonu siliyor (görevlerin %91.09'unda "evasion"; dosya 8.0→2.68, LOC 367→58).
- Compile hatalarının %39.7'si "Android Resource Linking Failed".
Relevant Limitations:
- Spec içinde resource ID'ler veriliyor ve testler orijinal app'in UI'ından türetilmiş → evaluation referans implementasyona bağlı, farklı UI tasarımları cezalandırılabilir.
- Spec ve testler LLM + GUI agent ile üretilmiş (insan doğrulamalı), yani ölçüm hattında LLM var.
- Tek platform (Android/Java), 101 task; contamination analizi yok (F-Droid app'leri kamuya açık).
Key Takeaway:
- App-level görevlerde compile başarısı fonksiyonel doğruluğu hiç göstermiyor; "evasion" davranışı feedback loop'larda ayrıca ölçülmeli.

### Athena — Athena: Intermediate Representations for Iterative Scaffolded App Generation with an LLM (preprint, 2025) [arxiv:2508.20263]
Method/HCI prototip çalışması: kullanıcı chat ile LLM'le birlikte üç intermediate representation (Storyboard, Data Model, GUI Skeleton) kuruyor; bunlardan multi-file SwiftUI iOS app kodu üretiliyor (GPT-4o).
IR'lar yapılandırılmış (JSON/pseudo-SwiftUI) hand-off olarak kullanılıyor; kod view başına ayrı dosyalarda, child view'lar önce üretiliyor. Değerlendirme: 12 katılımcılı within-subject user study (baseline: ChatGPT-benzeri chat, aynı GPT-4o) ve yazarların 10 app konsepti üzerinde teknik analiz (compile error, navigation error sayısı, düzeltme diff boyutu).
Findings:
- Katılımcıların %75'i Athena'yı tercih etti; 25 dakikada Athena app'leri ortalama 6.0 view / 353.9 LOC, baseline 3.1 view / 117.8 LOC.
- Ama Athena app'lerinde çok daha fazla bug (ortalama 10.4 vs 1.25); memnuniyet skoru baseline'dan düşük (3.42 vs 4.00), sebep latency ve bug'lar.
- Teknik değerlendirmede 10 app ortalama 514.8 LOC, 7.3 compile error, 4.0 navigation error; düzeltmeler küçük diff'ler.
Relevant Limitations:
- Otomatik fonksiyonel test yok; doğruluk sadece compile/navigation hataları ve kullanıcı algısıyla ölçülüyor.
- 10 app yazarların kendi prompt'ları, 12 katılımcı; network/servis entegrasyonu desteklenmiyor.
- Tek model, tek platform (SwiftUI).
Key Takeaway:
- Structured IR'lar (storyboard, data model, skeleton) multi-file app üretiminde kapsamı artırıyor ama doğrulama katmanı olmadan hata sayısı da artıyor; IR'lar executable kontratlara bağlanmalı.

### TDDev — Automatically Generating Web Applications from Requirements Via Multi-Agent Test-Driven Development (preprint, 2025) [arxiv:2509.25297]
Method: text ya da design image'dan full-stack web app üreten TDD tabanlı multi-agent framework (Test Case Generation Agent, Development Agent — Bolt.diy fork'u, Testing Agent).
Test agent requirement'tan UI interaction flow'ları şeklinde test case üretiyor, BrowserUse ile app'i gezip fonksiyonel + görsel feedback veriyor; development agent iteratif düzeltiyor. Değerlendirme: WebGen-Bench test set'ine Gemini-2.5-Flash-Image ile design image eklenmiş Req-to-App-MM (101 örnek), ama deneyler rastgele 10 website üzerinde. Fonksiyonellik BrowserUse (Claude-4-Sonnet) ile YES/PARTIAL/NO; görsel kalite Claude-4-Sonnet 1–5 puan. Backbone: GPT-4.1, Claude-4-Sonnet; baseline Bolt.diy ve Cursor.
Findings:
- GPT-4.1 ile accuracy %78.2 (Cursor %60.2, Bolt.diy %25.6); Claude-4-Sonnet ile %70.2.
- TDDev'de fail-to-start %0; Bolt.diy GPT-4.1 ile %80, Cursor %40.
- 1–2 feedback round accuracy'yi düşürüyor (%58.3→%25.3), 3 round'da %70.2.
- UI agent ile manuel test uyumu 28 test case'te %82.8.
Relevant Limitations:
- Sadece 10 task; istatistiksel güç çok düşük.
- Ölçüm tamamen LLM içinde: test yürütücü ve görsel hakem Claude-4-Sonnet, aynı model aynı zamanda backbone → aynı model ailesi hem üretiyor hem hükmediyor.
- Test case'ler NL; Cursor baseline manuel kurulmuş, maliyet karşılaştırması adil değil.
Key Takeaway:
- Requirement→UI-flow testleri ile TDD loop web app üretiminde yararlı görünüyor, ama değerlendirme ölçeği ve LLM-judge bağımlılığı sonuçları zayıflatıyor.

### ProcessMAS — Evaluating Classical Software Process Models as Coordination Mechanisms for LLM-Based Software Generation (preprint, 2025) [arxiv:2509.13942]
Empirical study: MetaGPT üzerinde Waterfall, V-Model ve Agile süreçlerini agent koordinasyon mekanizması olarak implemente edip karşılaştırıyor.
11 küçük proje (6 JavaScript oyun/app, 5 Python app; ör. Snake, Tetris, Expense Tracker, QR generator), 3 süreç × 4 model (GPT-4o-mini, GPT-4.1-nano, DeepSeek-Chat, DeepSeek-Reasoner) = 132 run. Metrikler: dosya/LOC, süre, token, SonarQube smell/vulnerability, AI-generated testlerle bulunan bug oranı, insan testçi ile bulunan failure oranı; one-way ANOVA.
Findings:
- Waterfall en verimli (median 118 s); Agile en yavaş (450 s); V-Model en verbose (median 934 LOC).
- İnsan testinde failure oranı median: Agile %40, V-Model %90, Waterfall %100.
- Model seçimi LOC, süre ve token'ı anlamlı etkiliyor, human-detected failure'ı anlamlı etkilemiyor (p=0.07).
Relevant Limitations:
- Projeler çok küçük ve oyun ağırlıklı; requirement'lar yazarların şirketinden, benchmark değil.
- Fonksiyonel doğruluk ağırlıkla manuel test, protokol ve test sayısı belirsiz; AI bug detection agent'ın kendi testlerine dayanıyor.
- Sadece küçük/ucuz modeller; hand-off'lar free-form NL.
Key Takeaway:
- İteratif feedback'li süreç (Agile) daha az hatalı çıktı veriyor ama maliyet artıyor; process seçimi quality/cost trade-off'u.

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

### app.build — app.build: A Production Framework for Scaling Agentic Prompt-to-App Generation with Environment Scaffolding (SANER 2026, 2025) [arxiv:2509.03310]
Method + industrial empirical çalışma: NL prompt'tan full-stack CRUD web app üreten, "environment scaffolding" (schema → API → UI FSM, her adımda linter/type-check/unit test/Playwright, sandbox, repair loop) yaklaşımını öneren açık kaynak framework.
Stack'ler TypeScript/tRPC, PHP/Laravel, Python/NiceGUI; değerlendirme sadece tRPC. Dataset: bağımsız kişilerce yazılıp LLM ile anonimleştirilmiş 30 prompt (low/medium/high complexity). 300 otomatik run (baseline, ablation'lar: no lint / no Playwright / no handler tests; model karşılaştırma: Claude Sonnet 4 vs Qwen3-Coder-480B vs GPT-OSS-120B). Değerlendirme: viability V = Boot (AB-01) + Prompt Correspondence (AB-02); kalite Q 0–10, insan assessor'ların 6 check'lik rubriği (create, view/edit, clickable sweep, performance). Ayrıca production'da 4 ayda 3000+ app.
Findings:
- İnsan değerlendirmesinde 30 app'ten 22'si viable (%73.3), 9'u perfect; viable'larda ortalama Q 8.78.
- Otomatik success: Claude %86.7, Qwen3 %70 (viable app başına $0.61 vs $5.01, 8.2× ucuz), GPT-OSS %30.
- Playwright E2E kaldırılınca viability %90'a çıkıyor (+16.7 pp): brittle selector, race condition, farklı ama doğru UI yapısı false reject üretiyor.
- Handler test'leri kaldırınca viability artıyor ama AB-04 (view/edit) %90'dan %60'a düşüyor.
- GPT-OSS'ta boot eden app'lerin önemli kısmı "Under Construction" template; boot-check tek başına yanıltıcı.
Relevant Limitations:
- Evaluation'ın çekirdeği insan rubriği; tek stack, 30 prompt, CRUD domain'i ile sınırlı. Ablation'lar 30 app'lik tek run'lar, varyans yok.
- Aynı validator'lar hem generation feedback'i hem kısmen otomatik metrik; model karşılaştırmasında açık modeller basitleştirilmiş pipeline ile koşulmuş (unfair baseline).
- Production metrikleri (star, app/gün) kalite kanıtı değil; industrial track, bazı kısımlar experience report tonunda.
Key Takeaway:
- Implementation detayına bağlı E2E test'ler probabilistic generation'da geçerli çözümleri reddediyor; spec-level, implementation-agnostic test tasarımı için güçlü ampirik argüman.
- Structured stage decomposition + executable validation, model seçiminden daha fazla güvenilirlik getiriyor.

### Cursor Design Issues — Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects (preprint, 2026) [arxiv:2604.06373]
Empirical çalışma: Cursor Pro ile, önerilen Feature-Driven Human-In-The-Loop (FD-HITL) süreci izlenerek 10 büyük proje üretiliyor ve fonksiyonel doğruluk + design quality inceleniyor.
Süreç: yazarların kürate ettiği proje açıklaması → Cursor requirements.md + tasklist.md üretir → feature feature backend/DB/frontend geliştirme, her feature'da manuel black-box test ve bug-fix/enhancement prompt'ları → system-level test. İlk yazar hiç kod yazmıyor ama sürekli feedback veriyor. 10 proje (2 mobile, 4 web, 4 utility), MERN, React Native + Spring Boot, Vue + Django/CodeIgniter, WordPress plugin; ortalama 16,965 LoC, 114 dosya. Doğruluk: iki yazar requirements.md'deki her requirement'ı çalıştırıp Complete/Incomplete işaretliyor. Design: SonarQube + CodeScene, false positive'ler manuel ayıklanıyor. Dataset (DIinAGP) paylaşılıyor.
Findings:
- Ortalama functional correctness %91 (min %85, max %96); 16 incomplete requirement (11 eksik, 5 logic hatası).
- CodeScene 1,305 issue (9 kategori), SonarQube 3,193 issue (11 kategori; 1,612 false positive ayıklandıktan sonra); iki araç arasında sadece 133 örtüşme.
- En sık: Code Duplication, yüksek complexity, Large Methods, framework best-practice ihlali, exception handling, accessibility; SRP/SoC/DRY ihlalleri.
Relevant Limitations:
- Tam otonom değil: ciddi insan yönlendirmesi var, requirement'ları Cursor kendisi yazıp yazar düzeltiyor; %91, Cursor'un değil insan+Cursor sisteminin sonucu.
- Doğruluk ölçümü manuel ve yazarların kendi requirement listesine göre; bağımsız test yok, tekrarlanabilirlik düşük.
- Tek araç, tek run, "automatic model selection" ile model bilinmiyor; insan baseline'ı yok.
Key Takeaway:
- Fonksiyonel olarak "çalışan" büyük AI-üretimi projelerde maintainability borcu yüksek; repo-gen benchmark'larına nonfunctional/design metrikleri eklenmeli.

### OOD PureAI — Can LLMs Produce Better Object-Oriented Designs than Human-Involved Development? (preprint, 2026) [arxiv:2605.19901]
Empirical case study: tek bir postgraduate Java assignment'ı (Kalah oyunu) için LLM'lerin uçtan uca ürettiği projelerin (PureAI) OOD kalitesi, 2021 (PreAI, 93) ve 2024 (PostAI, 57) öğrenci projeleriyle karşılaştırılıyor.
PureAI: GPT-5.4, Gemini 2.5 Pro, Gemini 3.1 Pro preview × 3 prompt (None/Broad/Specific OOD guidance) × 90 run. Prompt'ta functional requirement'lar ve 19 test case'in tamamı veriliyor; testler geçmezse en fazla 5 repair iterasyonu, sadece tüm testleri geçen çıktılar analiz ediliyor. Metrikler: CK ile 13 OOD metriği (WMC, CBO, LCOM, DIT, LOC, #Cl), DesigniteJava + PMD ile code smell density, manuel domain concept temsili (Board, Game, Player, Pit, House, Store) ve runtime object-count uygunluğu. Mann–Whitney + Cliff's delta.
Findings:
- Tüm testleri geçen çıktılar: GPT-5.4 ve Gemini 3.1 90/90; Gemini 2.5 Pro 83–87 (ilk prompt'ta sadece 4–7 geçiyor).
- PureAI daha düşük smell density ve daha küçük size/complexity/coupling gösteriyor ama bu oversimplification: daha az class ve domain concept (G31S median 4 class, 2 concept, prosedürel stil).
- PostAI, birçok metrikte PreAI'den çok PureAI'ye yakın.
- Specific prompt concept temsilini artırıyor ama insan projeleriyle farkı kapatmıyor.
- gpt-4o ve gemini-2.0-flash 90'ar run'da hiç tüm testleri geçen proje üretemiyor.
Relevant Limitations:
- Tek, küçük proje ve tek dil; "repository" sınırında (birkaç class).
- Test'ler prompt'ta veriliyor ve repair ile hedefleniyor; fonksiyonel doğruluk bir filtre, ölçüm değil. Başarısız run'ların atılması survivorship bias yaratıyor.
- Domain concept analizi isim eşleşmesine dayalı manuel kodlama.
Key Takeaway:
- Testleri geçmek iyi tasarım demek değil; repo-gen değerlendirmesinde design/abstraction metrikleri ayrı bir eksen olmalı.

### E2EDev — E2EDev: Benchmarking Large Language Models in End-to-End Software Development Task (preprint, 2025) [arxiv:2510.14509]
Benchmark + empirical: kullanıcı gereksinimlerinden sıfırdan web uygulaması üretimini (E2ESD) BDD testleriyle ölçen benchmark ve mevcut framework'lerin karşılaştırması.
46 yüksek yıldızlı gerçek GitHub web app'inden (HTML/JS/CSS; hesap makinesi, mini oyun vb.) HITL-MAA ile 244 fine-grained requirement ve 703 Gherkin senaryosu + Python step implementation (Behave, browser otomasyonu) üretilmiş; LLM taslaklıyor, 5 test uzmanı gözden geçiriyor. Test ID'leri önceden GPT-4o ile UI elemanlarına atanıyor ve prompt'ta veriliyor. Metrikler: Req. Acc, Test Acc, Balanced Score + cost, CO2, süre. 6 yöntem (Vanilla, GPT-Engineer, Self-Collab, MapCoder, ChatDev, MetaGPT) × 6 backbone (Claude-Haiku 4.5, GPT-4o, GPT-4o-mini, Qwen2.5 7B/70B/Max); 360 proje üzerinde insan failure analizi.
Findings:
- En iyi Req. Acc ~53.75% (GPT-Engineer + Claude-Haiku 4.5); çoğu konfigürasyon 30–50%.
- Multi-agent framework'ler vanilla'yı tutarlı geçemiyor; ChatDev 15.72 turn, 10× maliyet.
- MetaGPT neredeyse tüm konfigürasyonlarda ~0% (iletişim kopukluğu).
- Soft Req. Acc ile Req. Acc arasında >25 puan fark: fonksiyon var ama edge case'ler kaçıyor.
Relevant Limitations:
- Requirement ve testler referans repodan türetiliyor; önceden atanmış test ID'leri üretilen app'in DOM'una dayatılıyor → UI tasarım özgürlüğünü kısıtlıyor ama black-box olması iyi.
- Ölçek küçük (46 proje), sadece basit frontend web app'leri, backend yok; frontier modeller (GPT-5, Claude Opus/Sonnet) yok.
- Testlerin taslakları LLM üretimi (insan doğrulamalı).
Key Takeaway:
- BDD/Gherkin, NL requirement ile executable oracle arasında yapılandırılmış bir hand-off olarak iyi çalışıyor.
- Multi-agent orkestrasyon kendi başına fayda sağlamıyor; hand-off'larda bilgi kaybı/aşırı context ana sorun.

### TDDev — From Runnable Code to Shippable Applications: Test-Driven Development for Full-Stack Web Application Generation (ASE 2026, 2026) [arxiv:2605.17242]
Method + empirical: NL requirement'tan full-stack web app üretiminde TDD döngüsünü otomatikleştiren TDDev ve TDD stratejilerinin kontrollü karşılaştırması.
TDDev requirement'tan browser tabanlı acceptance test türetiyor, app'i deploy edip browser agent ile test ediyor, hataları agent için actionable feedback'e çeviriyor (MCP server olarak). Üç strateji: Incremental, Whole-Project, Agentic TDD (K=5 round) vs Vanilla. WebGen-Bench'ten rastgele 20 app; minimal agent (Claude Agent SDK) ve OpenCode; backbone MiniMax-M3, Claude Sonnet 4.6, Qwen3.5-397B-A17B. Headline metrik: orijinal insan-yazımı WebGen-Bench testleri üzerinde sabit Claude Sonnet 4.6 browser-tester ile oracle accuracy (Pass + 0.5·Partial); Wilcoxon + bootstrap CI.
Findings:
- Sonnet ile Vanilla 67.8% → Agentic TDD 91.5% (+23.7 pp); MiniMax minimal agent 65.1 → 87.3%.
- Qwen3.5 kendi tester'ı ile TDD'den fayda görmüyor (−4.4 ile +4.8 pp); tester Sonnet yapılınca +6.8–9.4 pp.
- Qwen3.5 feedback'inde test yürütmelerinin %56.2'si Fail (Sonnet %21.3); feature abandonment %48.8 vs %12.1.
- Test generation, ground-truth kriterlerin %88.9'unu kapsıyor; tester 40 fixture'da tüm gerçek defect'leri yakalıyor.
Relevant Limitations:
- Oracle bir LLM browser agent'ı (Sonnet 4.6) ve aynı model aynı zamanda backbone'lardan biri → Sonnet konfigürasyonlarında ölçüm/üretim aynı aile.
- Kontrollü deneylerde insan-yazımı test'ler acceptance test olarak loop'a veriliyor; yani loop evaluation testlerini görüyor (test leakage'a yakın).
- 20 app, tek seed; dil/stack belirtilmemiş.
Key Takeaway:
- Executable acceptance test'ler güçlü bir hand-off, ama feedback'in güvenilirliği (tester kalitesi) TDD kazancının ana darboğazı.

### Prompt-to-Product — From Prompt to Product: A Human-Centered Benchmark of Agentic App Generation Systems (ACM IUI Workshops 2026, 2025) [arxiv:2512.18080]
Benchmark + empirical çalışma: ticari prompt-to-app sistemleri (Replit, Bolt, Firebase Studio) tek NL prompt'tan full-stack web app üretiyor; değerlendirme neredeyse tamamen insan-merkezli.
96 prompt, taxonomy'ye göre (6 domain: healthcare, legal, real estate, finance, government, education × difficulty × specificity × complexity) developer forumlarından esinlenerek yazılmış; sistem başına 1 generation → 288 app artifact. Artifact'lar GitHub'a export edilip Quome Cloud'a Docker ile deploy ediliyor (bazı Replit app'lerinde manuel müdahale). Otomatik audit: HTTP GET + Playwright ile DOM görünürlük kontrolü. İnsan çalışması: 282 katılımcı, kalite filtresi sonrası 205; isolated 5'li Likert (clarity, ease of use) + side-by-side pairwise (ease, trust, visual appeal, visual appropriateness), 1,071 geçerli karşılaştırma. İstatistik: LMM, Bradley-Terry, Wilcoxon, Cliff's delta.
Findings:
- Deploy başarısı (otomatik): Firebase %84.4, Replit %75.0, Bolt %64.6; katılımcı "appeared" oranları %68.2/%68.4/%64.8; otomatik–insan uyumu %88.2.
- Isolated rating'lerde fark yok denecek kadar az (clarity 3.92–3.96); pairwise'da Firebase tüm boyutlarda önde (ease win rate %42.5 vs Bolt %31.7, Replit %26.0; trust %41.2/%29.2/%22.7).
- Pairwise değerlendirme isolated'dan belirgin şekilde daha ayırt edici.
Relevant Limitations:
- Fonksiyonel doğruluk ölçülmüyor: test yok, requirement coverage yok; "çalışıyor mu" sadece sayfanın ekranda görünmesi. Başlıktaki "completeness" algısal.
- Black-box ticari sistemler, sistem başına tek sample, model/harness bilinmiyor → sonuçlar zamana ve sürüme bağlı, tekrar üretilemez.
- Rater'lar teknik olmayan crowd; kısa etkileşim; effect size'lar küçük (|Δ|≈0.2).
Key Takeaway:
- nl-to-app değerlendirmede human pairwise preference, executable/requirement-based oracle'ın yerini tutmuyor ama tamamlayıcı; deployability bile ciddi bir filtre (%15–35 başarısızlık).


## core / nl-to-repo

### AgileCoder — AgileCoder: Dynamic Collaborative Agents for Software Development based on Agile Methodology (FORGE 2025, 2025) [doi:10.1109/forge66646.2025.00026]
Method çalışması: ChatDev/MetaGPT'nin waterfall akışı yerine Agile/Scrum rollerini (Product Manager, Scrum Master, Developer, Senior Developer, Tester) sprint'ler halinde çalıştıran multi-agent framework; küçük bir ProjectDev benchmark'ı da öneriyor.
Input: NL yazılım isteği (ör. "Create a snake game") → PM backlog çıkarıyor, her sprint planning → development → testing → review; output çok dosyalı çalıştırılabilir Python kod tabanı. Dynamic Code Graph Generator (static analysis ile Code Dependency Graph) context retrieval ve test sırası için kullanılıyor. Değerlendirme: HumanEval/MBPP pass@1 + ProjectDev (14 task: mini-game, image processing, data visualization); ProjectDev'de insan değerlendiriciler programı çalıştırıp requirement listesine göre karşılanan oran ("executability") hesaplıyor; her task 3 run, GPT-3.5-Turbo backbone.
Findings:
- ProjectDev executability: AgileCoder 57.79 vs ChatDev 32.79, MetaGPT 7.73; #Errors 0 vs 6/32.
- Maliyet yüksek: 36,818 token, $0.44, 444 s (ChatDev 7,440 token, $0.12); ortalama 1.64 sprint.
- CDG ablation: graph olmadan executability 57.50 → 23.38.
- HumanEval 70.53 / MBPP 80.92 pass@1 (GPT-3.5), MetaGPT'ye göre +7.71 / +6.19.
Relevant Limitations:
- ProjectDev yalnızca 14 task, tek dil (Python), tek backbone; istatistiksel güç yok.
- Değerlendirme tamamen manuel ve requirement listesi yazarlar tarafından hazırlanmış; kriterler öznel, inter-rater agreement raporlanmamış.
- Ana başlık sonuçları HumanEval/MBPP gibi isolated benchmark'lara dayanıyor; repo-level iddia için zayıf kanıt.
- Hand-off'lar büyük ölçüde free-form NL (backlog, review); CDG tek structured artefakt.
Key Takeaway:
- Iteratif/incremental süreç ve structured code graph, waterfall multi-agent sistemlere göre çalıştırılabilirliği artırıyor; ama ölçüm altyapısı (küçük, manuel) survey'de "early-stage evidence" olarak konumlanmalı.

### User Stories to Production Code — From User Stories to Production Code: A Controlled Agentic Framework for Reliable Software Generation (preprint, 2025) [doi:10.2139/ssrn.6738341]
Method çalışması: natural language user story'lerden "production-ready" backend yazılımı üreten, LLM code generation'ı deterministik bir control-plane ile saran agentic framework (SSRN, tek yazar).
Pipeline: user story → LLM ile kod üretimi; aşamalar arasında schema validation, API contract enforcement, execution sandboxing ve checkpoint'ler var. Ayrı bir bug resolution agent runtime failure'ları analiz edip patch üretiyor (feedback-driven refinement). Değerlendirme "representative backend development tasks" üzerinde; metrikler code validation accuracy, debugging effort ve end-to-end task completion rate. Task sayısı, dil, model ve baseline detayları abstract'ta yok.
Findings:
- Standalone LLM yaklaşımlarına göre validation accuracy ve end-to-end completion'da iyileşme, debugging effort'ta azalma raporlanıyor; sayısal değer abstract'ta verilmemiş.
Relevant Limitations:
- Full text yok; task seti, ölçek ve oracle (testler kimin tarafından yazılmış?) belirsiz — extraction büyük ölçüde eksik.
- "Standalone LLM" baseline'ı zayıf olabilir; güncel agent harness'larıyla (OpenHands vb.) karşılaştırma görünmüyor.
- API contract enforcement ilginç: hand-off'lar kısmen structured/executable artefact (schema, contract) — ama contract'ların nasıl üretildiği bilinmiyor.
Key Takeaway:
- Contract/schema tabanlı ara artefact'lar ile generation'ı gate'lemek, survey'deki "structured hand-off" temasına bir örnek; kanıt gücü düşük, full text bulunursa yeniden okunmalı.

### CITL — Compiler-in-the-Loop Code Generation: A validation-first agent architecture for type-safe multi-file software synthesis (preprint, 2026) [doi:10.5281/zenodo.22769026]
Method, PoC report. Full text yok; not abstract üzerinden. Agent multi-file TypeScript projesi üretiyor, diske yazmadan önce in-memory virtual project üzerinde TypeScript compiler ile doğruluyor.
Input: NL task (Express/JWT REST API) → output: multi-file TS proje. Diagnostics source context ve declaration summary ile zenginleştirilip revizyona geri besleniyor. Dört strateji aynı DeepSeek modeliyle karşılaştırılıyor: one-shot, Cline-style reactive terminal loop, batch-CITL, filewise-CITL. Metrik: dışarı sızan tsc hataları, LLM call sayısı, temiz `tsc --noEmit`.
Findings:
- One-shot 12 external TS hatası sızdırıyor; reactive loop 3 call'da düzeliyor ama 12 compiler failure'ı terminal loop'a gösteriyor.
- Batch-CITL 3 call'da 0 leaked error ile temiz build; filewise-CITL de 0 hata ama 8 call.
Relevant Limitations:
- Tek task, tek model, "observed run" — istatistiksel değil, anekdot düzeyinde.
- Sadece derleme doğruluğu; functional correctness (test, API davranışı) ölçülmüyor.
- Type-check tek başına cross-file contract drift'in yalnızca statik kısmını yakalıyor.
Key Takeaway:
- Validation'ı agent loop'un içine (kullanıcıya görünmeden) yerleştirme fikri: hand-off'ta compiler'ın executable artefakt olarak kullanımı. Kanıt çok zayıf; benchmark üzerinde tekrar edilmeli.

### KGMACG — KGMACG: Knowledge-Guided Multi-Agent Orchestration for Scalable Application-Level Code Generation (TOSEM, 2026) [doi:10.1145/3842390]
Method. Full text yok; not abstract üzerinden. SRS + architectural design document (ADD) → application-level repository üreten üç agent'lı closed-loop framework.
COPA (Code Organization & Planning Agent) SRS/ADD'den modular build plan ve project skeleton çıkarıyor; Coding Agent beş-sütunlu bir knowledge base rehberliğinde repo-level kod yazıyor; Testing Agent sürekli unit test üretip failure trace'lerini geri besliyor. Döngü, proje derlenene ve ≥%95 requirement coverage sağlanana kadar sürüyor. Değerlendirme: üç endüstriyel-ölçek case study (E-Commerce, Campus Security, Stock Trading), MetaGPT, AutoGen, CAMEL, CrewAI, ChatDev, CodeAgent'a karşı; backbone DeepSeek R1 ve gpt-5-codex-medium.
Findings:
- Abstract yalnızca KGMACG'nin application-level geliştirme otomasyonunu "ilerlettiğini" söylüyor; sayısal sonuç, metrik adı verilmemiş.
Relevant Limitations:
- Sadece 3 case study; bağımsız benchmark yok.
- Testler ve requirement coverage sistemin kendi Testing Agent'ı tarafından üretiliyor gibi görünüyor — aynı model ailesi hem kodu hem oracle'ı üretiyor olabilir; full text ile doğrulanmalı.
- Dil/stack abstract'ta belirtilmemiş.
Key Takeaway:
- SRS+ADD gibi structured input ve requirement-to-code traceability, ChatDev/MetaGPT tipi free-form hand-off'lara karşı güçlü bir baseline karşılaştırması sunuyor; ekstraksiyon için full text şart.

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

### EnvGraph — Toward Executable Repository-Level Code Generation via Environment Alignment (preprint, 2026) [arxiv:2604.03622]
Method çalışması: NL requirement'tan multi-file repo üretiminde executability'yi "environment alignment" problemi olarak ele alıyor. İki koşul ayrı modelleniyor: external dependency satisfaction ve repository-internal reference resolution.
Dual-layer temsil var: external environment graph (paketler, versiyon kısıtları) ve repository dependency graph (import/symbol ilişkileri). Build log, stack trace ve test sonuçlarından "execution-evidence-based attribution" ile baskın hata kaynağı seçiliyor, sonra hedefli revizyon yapılıyor. Iterative loop'ta en fazla 4 iterasyon var. Değerlendirme iki benchmark'ta: RAL-Bench (38 task, black-box system test + ISO 25010 non-functional skor) ve NL2Repo-Bench (104 task, upstream pytest). Backbone'lar GPT-5, DeepSeek-V3.2 ve Gemini-3-Pro-Preview (greedy). Baseline'lar CodePlan, Repo2Run, RepoGraph, APIMig ve VersiCode.
Findings:
- Motivasyon çalışması: NL2Repo-Bench'teki başarısız direct generation'ların %34.7 (GPT-5), %68.9 (DeepSeek-V3) ve %30.9'u (Gemini) environment kaynaklı. Internal reference hataları, external dependency hatalarından daha sık.
- RAL-Bench functional skorları: GPT-5'te Direct 42.32 → EnvGraph 55.43, DeepSeek'te 27.23 → 32.62. En güçlü baseline (CodePlan) karşısında relative kazanç %5.7–5.9.
- NL2Repo-Bench overall skorları: GPT-5 21.7 → 33.2, Gemini 34.2 → 44.0. Kazanç Hard (≥4k LOC) task'larda en büyük; Easy'de bazen baseline'ın altında kalıyor.
- Ablation'da EEBA ya da iterative loop çıkarılınca GPT-5'te −11/−12 puan kayıp var. Kalan hataların ~%40'ı residual logic fault.
Relevant Limitations:
- Baseline'lar (CodePlan, APIMig, VersiCode) aslında repo generation için tasarlanmamış edit/migration yöntemleri. Karşılaştırmanın adilliği tartışmalı; güçlü agentic harness'lar (OpenHands vb.) yok.
- RAL-Bench aynı grubun benchmark'ı ve interface surface'ı veriyor; test'ler reference repo'ya göre doğrulanmış, dolayısıyla alternatif API tasarımlarını cezalandırabilir.
- Sadece Python. Non-functional skor AHP ağırlıklı bir proxy.
Key Takeaway:
- Execution feedback'i sadece "yeniden dene" sinyali olarak değil, yapılandırılmış graph üzerinden hata atfı için kullanmak repo-level executability'de ölçülebilir fayda sağlıyor.

### RAL-Bench — Toward Functional and Non-Functional Evaluation of Application-Level Code Generation (preprint, 2026) [arxiv:2602.03462]
Benchmark + empirical çalışma: kısa bir NL requirement'tan çalıştırılabilir bir Python repo ("application-level") üretimini, functional ve non-functional açıdan ölçüyor.
Aktif 38 GitHub projesi var (ortalama >1k star, 7 senaryo, >450 evaluation point). Proje büyüklüğü 0.3k ile 109k LoC arasında değişiyor. Önceden benchmark'larda kullanılmış repolar dışlanmış. Her task için README/API/örneklerden elle rafine edilmiş kısa bir requirement yazılıyor. Buna ek olarak reference repo'nun module/package surface'ı veriliyor. Black-box system test'ler dokümante davranışlardan yazılıyor ve sadece pinned reference repo'da geçen test'ler tutuluyor. Non-functional skor beş boyutu AHP ağırlıklarıyla birleştiriyor: maintainability (MI), security (static analysis), robustness suite, efficiency ve resource (reference-normalized). Kurulum 16 LLM, zero-shot, tek geçişte tüm repo, 3 run ortalaması.
Findings:
- Hiçbir model %45 functional'ı geçmiyor. En iyiler Gemini-3-Pro-Preview 43.86, Gemini-2.5-Pro-Thinking 43.44 ve GPT-5.2 41.81. Ortalama standard 33.98, thinking 30.23.
- Thinking modeller tutarlı kazanç getirmiyor; maliyet farkı 100×'ten fazla ($0.15–$16.63).
- 446 repo analizinde hataların %17.2'si executability/dependency, geri kalan %82.8'i requirement mismatch ve non-functional hatalar.
- GPT-5.2 üzerinde self-repair, env-repair ve planning stratejileri functional skoru artırmıyor, non-functional skoru ise düşürüyor (57.1 → 46–50).
Relevant Limitations:
- Değerlendirme reference implementation'a sıkı bağlı: module surface veriliyor ve test'ler reference API'sine göre yazılıyor. Bu durumda task pratikte "API'si bilinen kütüphaneyi yeniden yaz"a yaklaşıyor ve farklı tasarımlar cezalandırılıyor.
- Test'lerin nasıl yazıldığı (insan mı, LLM destekli mi) net değil. Non-functional boyutlar static-analysis proxy'leri.
- Popüler public repolar kullanıldığı için contamination riski var (yazarlar da kabul ediyor). Sadece Python, 38 repo. Agentic harness yok, tek geçişli üretim.
Key Takeaway:
- Functional + çok boyutlu non-functional ölçüm birlikte raporlanmalı; aynı functional skordaki modeller non-functional'da büyük ölçüde ayrışıyor.
- "Reference-validated black-box system test" yaklaşımı yaygın bir şablon, ama spec'e interface surface eklemek oracle coupling'i artırıyor.

### TraceDev — TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development (ISSTA 2026, 2026) [arxiv:2607.18886]
Method çalışması: use case formatındaki requirement'lardan repo-level Java kodu üreten, traceability graph merkezli bir multi-agent framework.
Beş agent var: Requirement Refiner, Designer, Developer, Tester ve Validator. Validator requirement → design model → code arasında heterojen bir traceability graph tutuyor. Req-design bağları LLM semantic matching ile, design-code bağları AST ile kuruluyor. Eksik linkler en fazla 3 turda, test hataları en fazla 5 turda onarılıyor. Veri CoEST eTour (58 use case) ve SMOS (67 use case). Test'ler use case + ground-truth kod verilerek LLM ile NL test case olarak üretiliyor; ground truth'ta geçenler tutuluyor (962 + 1,179). Metrikler: Semantic-coverage (DeepSeek-V3.2 LLM-judge, 3 tur majority), Success rate (test'lerin adapte edilip üretilen koda karşı çalıştırılması), insan executability puanı (1–4) ve dosya/LOC istatistikleri. Backbone Gemini-2.5-Flash ve DeepSeek-V3.2; baseline ChatDev ve MetaGPT.
Findings:
- eTour/Gemini'de success %53.63, ChatDev %23.40, MetaGPT %18.71. SMOS/Gemini'de %56.82. DeepSeek ile %47.19 / %44.78, baseline'lar ≤%20.
- İnsan executability puanı ≥3.6 (baseline'lar <3.0). TraceDev use case başına 12–15 dosya üretiyor, baseline'lar 3–5.
- Ablation: Tester çıkarılınca success %13.9'a düşüyor. Designer çıkarılınca dosya sayısı 15 → 4.8.
- Token kullanımı MetaGPT'nin ~1/2–1/6'sı.
Relevant Limitations:
- Oracle tamamen LLM'e bağlı: test'leri LLM ground-truth koddan üretiyor, LLM-judge filtreliyor ve test'ler üretilen koda "adapte" edilerek çalıştırılıyor. Test'ler reference implementation'a göre yazıldığı için alternatif tasarımları cezalandırabilir.
- eTour/SMOS eski ve küçük sistemler; use case başına ~400 LOC. Contamination kontrolü yok.
- Baseline'lar sadece ChatDev ve MetaGPT; modern agentic harness'larla karşılaştırma yok.
Key Takeaway:
- Requirement ↔ design ↔ code traceability graph, free-form NL hand-off'a karşı yapılandırılmış bir ara artefakt örneği ve survey'de "structured hand-off" başlığında kullanılabilir.

### SPDDWL — Trustworthy Software Project Generation: a Case Study with an Interactive Theorem Prover (preprint, 2026) [arxiv:2605.26017]
Method + tek vaka çalışması: agent, NL requirement'tan effectful kısımları target dilde, pure core'u ise Rocq'ta spec + implementation + proof olarak yazıyor, sonra extraction ile C++'a aktarıp entegre ediyor.
Pipeline'da Requirement Analyzer (coding plan: pure/effectful ayrımı ve özellikler), Coding Agent ve Proving Agent var; hepsi Cursor Agent üzerinde Claude Opus 4.7 ile çalışıyor. Rocq proof state'i repair feedback'i olarak geri veriliyor. Tek görev var: RISC-V RV32I'nin 47 instruction'ı için CPU interpreter. Her instruction ISA manual'dan alıntılanmış bir NL requirement. Doğrulama machine-checked proof'lar, 265 LLM-generated test ve 12 saat AFL++ fuzzing ile yapılıyor.
Findings:
- 30 dakikada tamamen otomatik olarak 1,859 satır Rocq (821 fonksiyon, 922 property/proof) ve 2,848 satır extract edilmiş C++ üretiliyor; host glue 88 satır. Toplam ~21M token.
- 265/265 test geçiyor; AFL++ 98.2M input'ta 0 crash, 0 hang buluyor.
- Aynı bütçede Dafny backend verification'ı tamamlayamıyor (2,070 satır Dafny). Yazarlara göre sebep, SMT timeout'larının actionable feedback vermemesi.
Relevant Limitations:
- n=1: tek proje, tek model, tek run. Genellenebilirlik iddiası zayıf; Dafny karşılaştırması da tek run.
- Fonksiyonel test'ler aynı LLM ailesi tarafından üretiliyor, bağımsız oracle yok. Spec'lerin requirement'ı doğru yakalayıp yakalamadığı (spec validity) değerlendirilmemiş.
- Interpreter, instruction başına bağımsız handler'lardan oluşan oldukça modüler bir domain; cross-module etkileşim sınırlı.
Key Takeaway:
- Formal spec + proof'u executable contract olarak kullanmak "test'i geçen ama yanlış" repo sorununa güçlü bir cevap. Ama spec'i de LLM yazınca güvenin kaynağı spec kalitesine kayıyor.

### ReproGap — AI-Generated Code Is Not Reproducible (Yet): An Empirical Study of Dependency Gaps in LLM-Based Coding Agents (preprint, 2025) [arxiv:2512.22387]
Empirical çalışma: coding agent'ların ürettiği projelerin temiz ortamda, sadece agent'ın bildirdiği dependency'lerle çalışıp çalışmadığını ölçüyor.
3 agent (Claude Code/Opus 4.1, OpenAI Codex, Gemini) × 100 standart prompt = 300 proje; Python 40, JavaScript 35, Java 25 prompt. Prompt açıkça tam requirements.txt/package.json/pom.xml istiyor. Üç katmanlı dependency modeli: claimed, working, runtime (SciUnit, npm tree, Maven tree). Başarısız olanlar manuel debug ediliyor (~15 dk/proje).
Findings:
- Sadece 205/300 (%68.3) proje out-of-the-box çalışıyor; Claude %73, Gemini %72, Codex %60.
- Dil farkı büyük: Python %89.2, JavaScript %61.9, Java %44.0; Gemini Java'da %28.
- Beyan edilen → runtime dependency ortalama 13.5× genişleme (≈3 vs 37 paket).
- Hataların çoğu eksik paket değil (%10.5), syntax/path/yapısal kod hataları.
Relevant Limitations:
- "Execute" = çalışıp çalışmadığı; functional correctness test edilmiyor.
- Prompt'lar yazarlar tarafından hazırlanmış, proje büyüklüğü/multi-file oranı raporlanmıyor; tek run.
- Manuel debugging süreci öznel. Venue belirsiz (AAAI copyright ibaresi var, track belirtilmemiş).
Key Takeaway:
- Repo-generation benchmark'larında environment/dependency reproducibility ayrı bir boyut olmalı; "build-run" ön koşulu bile ciddi eliyor.

### NL2Repo-Bench — NL2Repo-Bench: Towards Long-Horizon Repository Generation Evaluation of Coding Agents (preprint, 2025) [arxiv:2512.12730]
Benchmark + empirical çalışma: agent'a tek bir NL requirements dokümanı ve boş workspace veriliyor; kurulabilir (installable) bir Python kütüphanesini sıfırdan üretmesi isteniyor.
104 task, GitHub'daki gerçek Python kütüphanelerinden (300–120k LOC, ≥10 star, son 3 yıl, tüm testleri geçen) seçiliyor. Annotator'lar repoyu reverse-engineering ile ortalama ~18.8k token'lık spec'e çeviriyor (Project Description, Supports/dizin yapısı ve bağımlılıklar, API Usage Guide, Implementation Nodes); AST tabanlı coverage kontrolü, uzman review ve SOTA agent'larla pilot run ile spec rafine ediliyor. Değerlendirme: Docker'da upstream pytest suite'i; skor ortalama test pass rate + tam geçiş (Pass@1 count). Zorluk: Easy 26 / Medium 46 / Hard 32; 9 kategori. Agent: çoğunlukla OpenHands-CodeAct, ayrıca Cursor-CLI ve Claude Code; 10 model.
Findings:
- En iyi: Claude-Sonnet-4.5 + Claude Code %40.2; tüm modeller <%40.5, yarısı <%20. 104 repo'dan en iyi model tek run'da sadece ~5'ini tam geçiyor.
- GPT-5 %21.7: erken durup kullanıcı girdisi bekliyor, <100 turn.
- Aynı model farklı framework'lerde <%1 fark → benchmark model-centric.
- Zorlukla monoton düşüş (Claude-Sonnet-4.5: Easy 55.3 → Hard 21.4); ML ve networking kategorileri en zor.
Relevant Limitations:
- Spec, referans repodan reverse-engineer ediliyor ve upstream white-box testlerini geçecek kadar API imzalarını dayatıyor → alternatif tasarımlar cezalandırılır; görev pratikte "spec'ten API-uyumlu reconstruction".
- Sadece Python; public repo'lar → contamination riski (recency filtresi sınırlı koruma).
- Dizin yapısı ve bağımlılıklar spec'te verildiği için "architectural design" iddiası kısmen zayıf.
Key Takeaway:
- Upstream test suite'i oracle yapan, scaffold'suz NL→repo formülasyonu şu an alandaki en temiz execution-based kurulumlardan biri; ama spec–test coupling'i survey'de açıkça tartışılmalı.

### ChessEngines-PL — Do programming languages still matter to your AI coding agent teammate? Evidence at scale from chess engines (preprint, 2026) [arxiv:2606.13763]
Empirical case study. İki frontier coding agent'a (Claude Code: Opus 4.6/4.7; Codex: gpt-5-codex, gpt-5.3/5.4-codex) tek cümlelik prompt veriliyor ("build a chess engine in [LANG] ... assess its Elo"). Agent'lar 17 dilde toplam 34 engine üretiyor (29 from-scratch main corpus + 5 special-role: iki Java→X port, DSL deneyi, vb.), Python/Rust'tan COBOL, TeX, CSS, Brainfuck, Lean 4, Why3/Rocq'a kadar.
Artefact'lar gerçek multi-file repo'lar (4–234 dosya, mainstream dillerde 2–12kLOC). İnsan müdahalesi dokümante edilmiş bir protokolle kısıtlı (p1–p5 prompt sınıfları, algoritma adı vermek yasak). Değerlendirme dilden bağımsız oracle hiyerarşisi: perft node count (exact move-gen doğruluğu), UCI/cutechess ile legal oyun, Stockfish gauntlet ile Elo; ek olarak 38 feature fingerprint, token/USD maliyeti, session transcript analizi ve novelty audit.
Findings:
- Denenen her dilde en az bir çalışan, feature-rich engine çıktı; birçok dil (CSS, TeX, APL, Brainfuck) için karşılaştırılabilir açık kaynak öncül bulunamamış.
- 1900–2100 Elo bandına yalnızca mainstream compiled diller ulaşıyor; esoterik/legacy engine'ler yüzlerce–binlerce Elo aşağıda kalıyor.
- Maliyet: mainstream engine ~$2–30, zor dil kategorilerinde ~25–50 prompt ve ~$60–480.
- 34 engine'den 26'sı kendi perft harness'ini, 30'u Stockfish gauntlet'i kendiliğinden kuruyor; ama 15 self-Elo scriptinin 11'i 200–1100 Elo fazla tahmin ediyor.
- Bazı engine'ler python-chess import ederek "cheat" ediyor (chess-css-codex örneği).
Relevant Limitations:
- Tek domain (satranç) ve tek yazar tarafından yürütülmüş session'lar; n=1 per dil×agent, seed varyansı yok.
- Human-in-the-loop (p3 bug report, p5 infra isteği) var; tam otonom değil, stop-rule yargıya dayalı.
- Perft + Elo güçlü, reference implementation'dan bağımsız oracle'lar; ama fonksiyonel "doğru" tanımı dar (ör. UCI dışı özellikler ölçülmüyor).
Key Takeaway:
- Dilden bağımsız, black-box oracle hiyerarşisi (exact → ordinal) olan domain'ler, reference-free repo-generation değerlendirmesi için iyi bir şablon.
- Agent self-validation'ı (self-Elo) güvenilmez; bağımsız harness ve cheating audit şart.

### BAEs — From Stateless Code Generation to Living Ontologies (preprint, 2026) [doi:10.1145/3786167.3788408]
Method + empirical karşılaştırma: Business Autonomous Entities (BAEs) adında, bir business concept'in "living ontology"sini içinde taşıyan ontology-aware agent'lar öneriliyor. Amaç, requirement değiştiğinde kodu sıfırdan regenerate eden stateless pipeline'lar yerine domain-preserving evolution. Full text yok; not abstract'a dayanıyor.
İki katmanlı değerlendirme: (1) feasibility demo — bir BAE'nin 6 adımlı evolution'ı restart olmadan online yapması; (2) otomatik benchmark — BAEs vs GHSpec vs ChatDev, aynı prompt, seed ve model (gpt-4o-mini). Her framework için aynı 6-sprint'lik program 100 kez seri çalıştırılıyor (toplam 300 run), clarification programatik. Effectiveness için "lightweight sanity check": run'ın prompt'taki explicit structural requirement'ları karşılayan runnable bir project üretip üretmediği. Asıl metrikler: end-to-end süre, token, cached-input indirimli maliyet, LLM interaction sayısı. Dil(ler) abstract'ta belirtilmemiş.
Findings:
- BAEs süre, token, maliyet ve interaction sayısında her iki baseline'dan da belirgin şekilde düşük; effect size'lar çoğunlukla medium-large.
- BAEs time–cost düzleminde Pareto-favorable bölgede.
- Framework'ler arası maliyet farkı, total tokens ~ cost regresyonu ve cache kullanımı ile açıklanıyor.
- Fonksiyonel doğruluk oranı (sanity check pass rate) abstract'ta sayı olarak verilmemiş.
Relevant Limitations:
- Doğruluk sadece structural/runnable sanity check; test-based functional correctness yok — verimlilik karşılaştırması, kalite eşitliği varsayımı üzerine kurulu.
- Tek program, tek model (gpt-4o-mini); 100 tekrar varyansı ölçüyor ama genellenebilirliği değil.
- Senaryo kısmen incremental evolution (EC1'e yakın), ama baseline'lar sprint'lerde sıfırdan üretiyor; karşılaştırma bu asimetriden etkilenebilir.
Key Takeaway:
- Multi-sprint, evolving requirement ile repo üretimini cost/token ekseninde ölçen nadir çalışma; survey'de "efficiency/nonfunctional" boyutunun örneği.
- Ontology gibi yapılandırılmış, kalıcı bir artefact'ı hand-off olarak kullanmak free-form NL'ye alternatif.

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

### MaCTG — MaCTG: Multi-Agent Collaborative Thought Graph for Automatic Programming (ICSE 2026, 2024) [arxiv:2410.19245]
Method (+ küçük benchmark): NL gereksinimden çok modüllü program üreten dinamik graph tabanlı multi-agent framework; ChatDev/MetaGPT'ye alternatif.
Roller: Team Leader → Module Leader → Function Coordinator (planner'lar, DeepSeek-V3) ve Coder/Tester (executor'lar, Qwen2.5-Coder-7B lokal). Horizontal decomposition + vertical cascading, context-aware plan adjustment, "think-twice", backward multi-scale validation (fonksiyon → modül → proje, Tester agent unittest yazıp Docker'da çalıştırıyor). Benchmark BCVPP: 90 OpenCV image-processing projesi (30 simple GitHub repo'dan, 50 medium ve 10 hard OpenAI-o1 ile üretilip filtrelenmiş). Doğrulama: üretilen programın çıktısı referans çıktı ile karşılaştırılıyor; otomatik eşleşme başarısızsa manuel inceleme; Pass@1/Pass@5.
Findings:
- MaCTG Pass@1 %83.33, Pass@5 %94.44 (hard: 80/90).
- En güçlü baseline DeepSeek-R1 Pass@5 %88.89 (fark istatistiksel olarak anlamsız, p=0.344); ChatDev-GPT-4o %75.56, MetaGPT-GPT-4o %52.22.
- Independent reasoning ile CTG değiştirilince Pass@5 %51.11'e düşüyor; multi-scale validation kaldırılınca %68.89.
- Hybrid konfigürasyon ile ChatDev'e göre %89.09 maliyet düşüşü.
Relevant Limitations:
- Projeler script ölçeğinde (kanal ayırma, Canny + fill); "project-level" iddiası ile gerçek multi-file repo arasında mesafe var, LoC/dosya sayısı raporlanmıyor.
- Medium/hard task'lar OpenAI-o1 ile üretilmiş; referans çıktı tek bir örnek implementasyona bağlı, alternatif kütüphane seçimleri manuel yargıyla kurtarılıyor (LLM-benzeri öznel adım).
- Tek domain (image processing), 90 task; baseline'lar farklı modellerle, harness confound'u yüksek.
Key Takeaway:
- Planner'ları güçlü, executor'ları küçük modelle çalıştırmak maliyeti ciddi düşürüyor; peer-level context sharing plan halüsinasyonunu azaltıyor.
- Hand-off'lar serbest NL + function signature; yapılandırılmış kontrat yok.

### E2EDevBench — Benchmarking and Studying the LLM-based Agent System in End-to-End Software Development (preprint, 2025) [arxiv:2511.04064]
Benchmark + empirical study: requirement'tan tüm Python projesini üretme. 50 proje, 2024Q1–2025Q1 arası PyPI'dan dinamik olarak (çeyrek başına 10) seçiliyor; referans projeler ortalama 19.2 dosya, 2011.5 LOC, 119.7 test.
Hibrit evaluation: bağımsız bir "Test Migration Agent" orijinal projenin testlerini üretilen projeye uyarlıyor (kodu değiştirmesi engelleniyor); sonra Gemini-2.5-Pro requirement listesinin her maddesini implemented/not implemented diye 3 kez işaretliyor (üçü de uyuşmalı). Ana metrik Impl-Rate, ek olarak test pass rate. Aynı toolset üstünde üç agent mimarisi (Single, DT, DDT) Gemini-2.5-Pro/Flash ile.
Findings:
- En iyi SDAgent-DT + Pro: %53.50 requirement implemented; test pass rate %79.95.
- DDT (daha derin decomposition) belirgin kötü: %22.63–32.79.
- LLM-judge ile 3 insan arasında pairwise agreement %76–84 (insanlar arası %78–88), Pearson ≥0.62.
- Başarısızlığın ana nedeni requirement omission ve yetersiz self-verification; ~1000 unimplemented requirement analiz edilmiş.
- Proje başına maliyet ~$7, 5.24M token.
Relevant Limitations:
- Test migration ve requirement verdict'i LLM yapıyor; judge (Gemini-2.5-Pro) test edilen agent ile aynı model ailesi.
- Üretilen projeler ~200–500 LOC, referans ~2000 LOC → migrated testler referans API'ye bağlı; adaptasyon kalitesi ayrı raporlanmıyor.
- Sadece Python, sadece Gemini modelleri, 50 proje.
Key Takeaway:
- Referans testleri agent'a vermeden sonradan "migrate" etmek tasarım özgürlüğünü koruyan ilginç bir ara yol; ama bu adımın kendisi doğrulanmalı.

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

### Role-Based MA Eval — An Evaluation of Role-Based Multiagent Code Generation on Repository-Scale Problems (IEEE Software, 2026) [arxiv:2607.04212]
Empirical çalışma (+ kendi pipeline'ı): SRS'ten tüm Java Maven repo'yu üretmede tek LLM ile role-based multi-agent (Sequential ve Reflexive, ChatDev 2.0 üzerinde) karşılaştırılıyor.
Input, IEEE SRS formatında bir doküman; ama SRS'ler GPT-5 ile README + tüm Javadoc'tan türetilip manuel doğrulanmış. 2025'te oluşturulan top-1000 Java GitHub reposundan complexity grubuna göre (Trivial/Simple/Moderate/Complex) 3'er repo, toplam 12. Agent pipeline: Planning → Coding (agent'lar arası summary ile hand-off) → static text-based Assessment (en fazla 10 iterasyon) → Setup (pom.xml). Backbone GPT-5, 5 tekrar. Orijinal testler üretilen koda uygulanamadığı için metrikler: JPlag max similarity, CrystalBLEU, derlenebilen class yüzdesi ve Claude Code (Sonnet 4.6) ile Gherkin senaryosu çıkarıp ChatGPT 5.4 ile eşleştiren "scenario-intent" oranı.
Findings:
- Overall compile oranı: LLM-only %31, Agentic-seq %22, Agentic-refl %40; yani en iyisinde bile class'ların çoğu derlenmiyor.
- JPlag similarity 0.21 → 0.33 → 0.43; scenario-intent %61 / %55 / %78 (Agentic-refl).
- Üretilen kod orijinal LOC'un sadece %1–25'i kadar; plan-then-execute büyük projelerde ölçeklenmiyor.
- Maliyet düşük: proje başına $0.20–1.40, 17 dk–1 s 48 dk.
Relevant Limitations:
- Değerlendirme tamamen referans implementasyona bağlı (plagiarism benzerliği); farklı ama geçerli tasarımları cezalandırır. Fonksiyonel doğruluk hiç çalıştırılarak ölçülmüyor.
- Spec'i LLM (GPT-5) yazıyor, generation GPT-5, scenario-intent iki ayrı LLM ile ölçülüyor; ölçümün içinde LLM var ve yazarlar da bunun correctness olmadığını kabul ediyor.
- Hand-off free-form NL summary; reflection loop compiler/test feedback kullanmıyor.
- 12 repo, tek dil, tek model; Javadoc'tan SRS türetmek implementasyon bilgisini dolaylı sızdırabilir.
Key Takeaway:
- Repo-ölçeğinde test transfer edilemeyince similarity + LLM-judge'a düşülüyor; bu, implementation-agnostic executable oracle ihtiyacının net bir örneği.
- Execution feedback olmayan reflexive loop derlenebilirliği çözmüyor; compiler/test-in-the-loop şart.

### BeyondSWE — BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing? (preprint, 2026) [arxiv:2603.03194]
Benchmark: 246 repodan 500 instance, dört setting: CrossRepo (200), DomainFix, DepMigrate (178) ve survey açısından ilgili olan Doc2Repo (50, boş workspace'ten NL spec'ten repo).
Doc2Repo inşası: Ocak–Kasım 2025'te oluşturulmuş, ≥3 contributor, >20 star Python repoları; Gemini 3 Pro kod tabanını gezip purpose, usage örnekleri, public class/function imzaları ve davranışı içeren spec yazıyor, implementation detayı ve dizin yapısı çıkarılıyor, repo adı `target_repo` ile maskeleniyor. Test'ler orijinal repodan LLM yardımıyla uyarlanıp insan tarafından gözden geçiriliyor; 60 adaydan 50 seçiliyor (ortalama 26.8 dosya, 3,528 satır). Metrikler: ortalama test pass rate ve (Almost) Correct Count (tüm testler / ≥%90). Harness'ler: OpenHands, SearchSWE (web search + blocklist), Codex CLI.
Findings:
- Doc2Repo'da en iyi pass rate %61.74 (Codex GPT-5.4 xhigh); OpenHands altında %46.6–57.2.
- 50 repodan en fazla 2–4'ü tamamen doğru; pass rate kısmi ilerlemeyi abartıyor.
- Search erişimi Doc2Repo'da neredeyse etkisiz (±birkaç puan), diğer task'larda daha faydalı.
Relevant Limitations:
- Doc2Repo, benchmark'ın sadece %10'u; asıl odak issue resolution/migration.
- Spec LLM (Gemini 3 Pro) tarafından referans koddan tersine üretiliyor ve test'ler orijinal repodan geliyor: public API imzalarına sıkı bağlılık, alternatif tasarımlar cezalandırılır. Gemini hem spec yazıyor hem değerlendirilen modellerden biri.
- Sadece Python, 50 repo.
Key Takeaway:
- "Reverse-engineered spec + orijinal repo testleri" deseni ölçeklenebilir ama spec-test uyumu için insan denetimi gerekiyor; strict "fully correct" metriği raporlanmalı.

### BUILD-AND-FIND — BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases (preprint, 2026) [arxiv:2605.06136]
Benchmark/protokol: builder agent gizli bir repository spec'inden sıfırdan codebase üretiyor; ardından sadece codebase'i gören finder agent'lar spec'e izlenebilir 4 şıklı soruları (task başına 15) cevaplıyor. Amaç correctness değil, üretilen repo'nun tasarım niyetini ne kadar "okunabilir" taşıdığını ölçmek.
İki Rust task ailesi (scratch_minidb, scratch_nanoweb). 12 builder/finder konfigürasyonu: Claude Opus 4.7, Sonnet 4.6, GPT-5.5, GPT-5.4-mini, MiMo-v2.5(-pro), her biri high/low reasoning. 48 build (41'i `cargo build` compile probe'unu geçiyor), 1,728 find kaydı. Metrikler: recovery accuracy, 3-trial repeatability, builder implementation coverage (artifact-question audit, 696/720 etiket iki finder'ın consensus'u ile), ve koşullu inspection effort (finder'ın okuduğu byte, R_b).
Findings:
- Question-only kontrolde bile accuracy %94.5; artifact-conditioned %98.9 (+4.4 pp), low-prior subset'te +9.0 pp.
- Builder implementation coverage %85–100.
- Effort'ta GPT-5.5 en düşük (R_b 1.033 high-effort).
- Same-family builder–finder affinity pozitif (OpenAI +0.076, Claude +0.041).
Relevant Limitations:
- Runtime correctness ölçülmüyor; ölçüm tamamen LLM finder'lara dayanıyor ve audit etiketleri de finder consensus'undan geliyor (aynı model aileleri hem yazıyor hem ölçüyor; affinity bunu gösteriyor).
- Sadece 2 task, yüksek prior'lar yüzünden accuracy doymuş durumda; asıl sinyal (byte cinsinden effort) dolaylı bir proxy.
- Soru bankası spec'e bağlı; tasarım seçimlerini "gold" kabul ettiği için alternatif tasarımlar non-gold sayılıyor.
Key Takeaway:
- Üretilen repo'yu downstream agent'lar için bir iletişim artefaktı olarak değerlendirmek yeni bir eksen, ama correctness ölçümüyle birlikte kullanılmalı.

### CodeTeam — CodeTeam: An LLM-Powered Multi-Agent Framework for Repository-Level Code Generation (preprint, 2026) [arxiv:2606.22082]
Method çalışması: NL requirements dokümanından boş workspace'te tüm repoyu üreten multi-agent framework (NL2Repo). CodeS'in sketch paradigmasını uçtan uca bir workflow'a genişletiyor.
Birden fazla Architect agent rakip software design sketch (SDS) üretiyor (opsiyonel RAG ile), CTO agent birini seçip file ownership, public interface ve dependency constraint içeren "machine-checkable contract"a normalize ediyor; Developer agent'lar dependency-aware scheduler + Git tabanlı koordinasyonla dosyaları yazıyor, QA agent test koşturup repair döngüsü sürüyor. Backbone Qwen2.5-72B-Instruct (PE ve SFT varyantları). Ana değerlendirme SketchEval (19 Python repo, 5/8/6 easy/medium/hard) üzerinde SketchBLEU; NL2Repo-Bench (104 task, upstream pytest) "external validation" olarak kullanılıyor. Baseline'lar (Vanilla, ChatDev, AutoGPT, CodeS) aynı backbone ile yeniden koşturulmuş.
Findings:
- SketchBLEU: 51.7% (PE) / 60.9% (SFT); CodeS'e göre +4.1 / +2.9 puan.
- NL2Repo-Bench ortalama test pass rate 34.6% (PE) / 42.3% (SFT); ama Pass@1 sadece 5.1% / 6.1% — tam geçen repo neredeyse yok.
- Ablation: dynamic developer allocation kaldırılınca %9.9, RAG kaldırılınca %8.1 relatif düşüş; Git koordinasyonu %2.9.
- Failure analizi: packaging+import hataları CodeS'e göre azalıyor (34.2→22.1%, 28.7→19.4%), logic hataları oransal olarak artıyor.
Relevant Limitations:
- Ana metrik SketchBLEU referans implementasyona benzerlik; farklı ama geçerli mimarileri cezalandırır. Ablation'ların tamamı sadece SketchBLEU üzerinde.
- SketchEval sadece 19 repo, sadece Python; tüm deneyler tek backbone (Qwen2.5-72B), frontier model/agent (OpenHands vb.) yok.
- Contract structured bir artefakt (iyi), ama doğrulaması QA agent'ın kendi yazdığı lightweight testlere dayanıyor.
Key Takeaway:
- Planlama çıktısını makine-kontrol edilebilir bir kontrata dönüştürmek, cross-file interface tutarlılığı için somut bir hand-off tasarımı.
- Ortalama pass rate ile Pass@1 arasındaki uçurum, NL2Repo'da "kısmi doğruluk" metriklerinin tek başına yanıltıcı olabileceğini gösteriyor.

### DeNovoSWE — DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch (preprint, 2026) [arxiv:2606.10728]
Training-data + method çalışması: dokümandan tüm repoyu üretme (doc2repo) için 4,818 instance'lık, otomatik kurulmuş, doğrulanabilir bir eğitim ortamı/dataseti ve bununla SFT edilmiş agent.
Scale-SWE ile Docker ortamı kurulan GitHub Python repolarından (test pass ≥90%, coverage ≥50% filtresi) başlanıyor. Divide: capability decomposition + test'lerin runtime trace'i ile "direct / core indirect" bileşen profiling; Conquer: draft–critic–repair agent döngüsüyle capability bazlı dokümantasyon (GPT-5.4/5.5). Eval: kaynak kod ve testler silinmiş, git geçmişi sıfırlanmış, network/pip erişimi kısıtlanmış ortamda orijinal unit test pass ratio. Trajectory'ler DeepSeek-V4-Pro ile OpenHands'te üretiliyor, difficulty-aware eşiklerle (0.90→0.60) filtreleniyor, ~11k trajectory ile Qwen3-30B-A3B ve Qwen3.5-35B-A3B SFT.
Findings:
- Qwen3-30B-A3B: BeyondSWE-Doc2Repo 5.8→47.2%, NL2Repo 4.3→23.0% (issue-level Scale-SWE-Agent: 29.2 / 18.3%).
- Qwen3.5-35B-A3B: 43.8→50.0% ve 23.5→27.1%; Gemini3-Pro'ya (52.0) 2 puan yakın.
- Difficulty-aware filtre sabit eşiğe göre küçük ama tutarlı kazanç (0.488→0.500 Doc2Repo).
- Dataset: median 79 unit test, testler median 9 kaynak dosyaya dokunuyor, ortalama coverage 85.5%.
Relevant Limitations:
- Spec reverse-engineered: dokümanlar referans repo ve onun testlerinden LLM ile türetiliyor; test'lerin import ettiği API'ler dokümanda zorunlu kılınıyor → white-box testlere ve referans arayüze sıkı bağlılık.
- Aynı model ailesi (GPT-5.x) dokümanı yazıyor, critic'liyor, difficulty'yi puanlıyor ve cheating'i denetliyor; spec kalitesine dair bağımsız insan doğrulaması raporlanmamış.
- Sadece Python; eğitim reposu ile benchmark repoları arasında overlap/contamination analizi yok.
- Ablation sadece filtreleme stratejisi üzerine; dokümantasyon pipeline'ının katkısı ayrıca ölçülmemiş.
Key Takeaway:
- Doc2repo'yu RL/SFT ölçeğine taşımanın yolu: mevcut test'li repolardan spec türetip, leakage'ı sandbox ile kapatmak.
- Kısmi pass ratio'lu trajectory'leri difficulty'ye göre tutmak, uzun-horizon görevlerde veri çeşitliliği için kritik.

### CLI-Tool-Bench — Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios (preprint, 2026) [arxiv:2604.06742]
Benchmark + empirical: boş workspace ve NL requirement'tan CLI aracı üretimini, scaffold vermeden ve black-box differential testing ile ölçen benchmark.
GitHub'dan 94 CLI repo (Python, JavaScript, Go; stars>10, install + `--help` doğrulaması, manuel kontrol). LLM, README ve `--help`'ten command schema çıkarıyor; LLM-directed fuzzing ile her command pattern için 50 test üretiliyor ve oracle repoda çalıştırılarak beklenen çıktı/side-effect kaydediliyor (geçersizler atılıyor). Değerlendirme: sandbox'ta exit code (M_exec), file system side effect (M_se), stdout eşitliği — EM, Fuzzy (Levenshtein), Semantic Match (GPT-5.4 judge, 1,000 çift üzerinde κ>0.9). 7 model × OpenHands ve Mini-SWE-Agent.
Findings:
- En iyi ortalama SM 43.78% (Kimi-k2.5), MiniMax-M2.5 34.59%; GPT-5.4, Qwen-3.5-plus, GLM-5 ~29–31%.
- Claude-Sonnet-4.6 beklenmedik şekilde düşük (~10.6% SM ortalama).
- Agent'lar güçlü şekilde monolitik yapı üretiyor; daha fazla token daha iyi sonuç anlamına gelmiyor.
- Mini-SWE-Agent birçok modelde OpenHands'ten iyi.
Relevant Limitations:
- Testler LLM tarafından üretiliyor ama oracle repoda doğrulanıyor (iyi); kapsam README/`--help`'te belgelenen davranışla sınırlı.
- Output formatı katı eşleştirmede farklı-ama-doğru çözümler cezalanıyor; SM bunu LLM-judge ile telafi ediyor, bu da ölçüme LLM sokuyor.
- Tek run; popüler CLI araçları için contamination analizi yok.
Key Takeaway:
- Referans repoyu black-box oracle olarak kullanmak, white-box unit test bağımlılığını ve scaffold dayatmasını kaldırıyor — survey'deki "coupling to reference" eksenine iyi bir karşı örnek.

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

### CodeSpec — CodeSpec: Dual Executable Specifications for Agentic Long-Horizon Feature Development (preprint, 2026) [arxiv:2607.26777]
Method çalışması; ana hedef mevcut repo'ya feature ekleme (FeatureBench), yani birincil katkı EC1 alanında. Survey için dahil edilme gerekçesi ayrı ve ayrıca raporlanan bir greenfield değerlendirmesi: NL2Repo-Bench (104 task, requirements dokümanı + boş workspace → Python repo). Bu yüzden core ama peripheral.
Yöntem: feature instruction LLM ile sub-requirement'lara ayrılıyor; her biri için repo evidence'ı (design pattern, call relation, dependency) ile gerekçelendirilen "functional chain" (unit → relation → unit) kuruluyor. Her chain iki executable spec'e derleniyor: architecture spec (CheckUnit/CheckRelation/CheckDataFlow) ve behavior spec (CheckOutput/CheckBoundary/CheckState, test benzeri). Agent, iki spec de geçene ya da budget bitene kadar patch üretip feedback alıyor. Greenfield'da önce skeleton + functional unit'ler yaratılıyor, sonra gelişen kod tabanı evidence olarak kullanılıyor. Backbone DeepSeek-V4-Pro (ek olarak GPT-5.4-mini); metrikler FeatureBench'ten %Passed, #Resolved, maliyet; 10,000 bootstrap.
Findings:
- FeatureBench Lite/Fast/Full: %70.7/%55.0/%49.9; en iyi baseline RTADev %65.3/%49.7/%46.1, Claude Code %59.8/%47.0/%41.1. Maliyet artışı RTADev'e göre $0.01–0.03/task.
- NL2Repo: overall %46.6, 8 resolved (Claude Code %41.6/5, RTADev %41.3/7, OpenHands %26.4/2); Easy/Medium/Hard %70.0/%51.7/%20.4 — Hard'da kazanç sadece +1.1 puan, std (~4.7) içinde.
- Ablation (Lite): spec'siz %62.6, behavior spec'siz %64.0, architecture spec'siz %66.6; executable vs textual spec farkı uzun instruction'larda büyüyor (%71.8 vs %43.8).
Relevant Limitations:
- Spec'ler ve behavior check'leri aynı LLM tarafından üretiliyor; spec'in doğruluğu ayrıca doğrulanmıyor (self-generated oracle).
- Greenfield sonucu tek tablo, tek backbone; NL2Repo'da hard task'larda anlamlı iyileşme yok. Ablation'lar sadece 30 task'lık Lite split'te.
- Baseline'lar (Claude Code dahil) DeepSeek-V4-Pro ile koşuluyor — native olmayan model/harness kombinasyonu confound.
Key Takeaway:
- Free-form NL plan yerine executable, yapısal hand-off artefact'ları (architecture + behavior spec) long-horizon'da design drift'i azaltıyor; repo generation için structured contract fikrini destekleyen bir kanıt, ama greenfield kanıtı ikincil ve zayıf.


## core / other

### VibeServe — VibeServe: Can AI Agents Build Bespoke LLM Serving Systems? (preprint, 2026) [arxiv:2605.06068]
Method çalışması: model + hardware + workload hedefi için sıfırdan, ona özel bir LLM serving sistemi üreten multi-agent loop.
Girdiler: model weights ve reference implementation (HF Transformers), kullanıcı tarafından verilen accuracy checker, benchmark script'i ve NL deployment talimatı. Outer loop issue-tracker policy ile çalışıyor (Orchestrator, git checkpoint'ler, long-term memory dosyası). Inner loop'ta Implementer, Accuracy Judge (checker + reward-hacking denetimi) ve Performance Evaluator (profiler'lar) var; hepsi Codex CLI. Serving bilgisi bir skills library'de tutuluyor. Değerlendirme 6 senaryoda: standard Llama-3.1-8B/H100, predicted outputs, hybrid-model prompt caching, streaming ASR, MacBook'ta constrained JSON decoding ve Show-o2 image generation. Karşılaştırma vLLM/SGLang ve plugin baseline'larla.
Findings:
- Standard senaryoda 60 iterasyonda vLLM ile throughput/TPOT paritesine ulaşıyor; SGLang'ı %5 geçiyor.
- Predicted-output speculative decoding'de 5.95× hızlanma, vLLM spec-dec'in 2.0× üzerinde. Olmo-Hybrid prompt caching'de ~3.45×, Moonshine ASR'de TTFT 1.69×.
- MacBook'ta JSON decoding 2.6×; Show-o2 MLX portunda 6.27×, fp16 fiziksel sınırın ~%7 yakınında.
Relevant Limitations:
- Correctness tamamen kullanıcının checker'ına bağlı (reference ile output karşılaştırması). Bağımsız bir test suite yok; Accuracy Judge da bir LLM agent.
- Senaryo başına tek run, varyans yok. Maliyet (token, GPU saati) raporlanmamış. Case-study formatında, sistematik bir benchmark yok.
- Üretilen sistemin boyutu ve yapısı (dosya sayısı, LOC) raporlanmamış; skills library mevcut engine'lerden damıtılmış.
Key Takeaway:
- Reference implementation + checker'ı executable contract olarak kullanıp performans odaklı greenfield sistem sentezi mümkün. Repo generation'ın non-functional (performans) hedefli bir varyantı olarak survey'de ayrı bir yere konabilir.


## core / paper-to-repo

### HiRAS — HiRAS: A Hierarchical Multi-Agent Framework for Paper-to-Code Generation and Execution (preprint, 2026) [arxiv:2604.17745]
Method + evaluation protocol. Paper → experiment reproduction repository; fixed sequential pipeline (PaperCoder, AutoReproduce) yerine proaktif manager agent'lar alt agent'ları (planning, architecture design, dependency modelling, config, analysis, coding, execution) denetleyip yeniden çağırıyor.
Shared workspace + file-system tools, smolagents scaffold. Benchmark: PaperBench (20 ICML 2024 paper, rubric) ve Paper2Code (90 paper; ICML/NeurIPS/ICLR 2024). Backbone: Qwen3-Coder-480B, DeepSeek-v3.1-Terminus, ek olarak Claude-Sonnet. Değerlendirme tamamen LLM-judge: PaperBench'te o3-mini-high ve GPT-4o-mini, Paper2Code'da o3-mini-high (1–5 skala). Ayrıca P2C-Ex: repo file count + yapı bilgisi eklenmiş reference-free judge prompt'u.
Findings:
- PaperBench-CodeDev: HiRAS 64.1% (Claude-Sonnet), 57.4% (DeepSeek-v3.1) vs PaperCoder 51.1% (Claude-Sonnet). Full PaperBench (execution dahil) skorları düşük: 19.1 / 21.5%.
- Orijinal Paper2Code reference-free judge boş repoya 3.89, sadece config içeren repoya 4.67 veriyor; P2C-Ex reference-based ile Pearson r'yi 0.423'ten 0.862'ye çıkarıyor; 30 paper'lık insan anotasyonunda r=0.72 (inter-annotator 0.82).
- Ablation: hierarchical supervision tek başına ~%10 katkı.
- Başarısızlık çoğunlukla execution'da (inter-file import hataları, env setup): 110 koşudan yalnızca 3'ü code generation aşamasında düşüyor; bir örnekte skor 69.7% → 11.3%.
Relevant Limitations:
- Ölçüm tamamen LLM-judge; judge hallucination'ı paper'ın kendisi gösteriyor, P2C-Ex de hâlâ LLM.
- Reference-based metrik gold repo'ya bağlı, alternatif tasarımları cezalandırabilir.
- Baseline'lar yazarlar tarafından yeniden koşulmuş; ölçek 110 paper, sadece ML/Python.
Key Takeaway:
- Paper-to-repo'da darboğaz kod yazmak değil çalıştırmak; judge'ın repo yapısını görmemesi skorları şişiriyor — structural bilgi judge'a verilmeli.

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

### PaperBench — PaperBench: Evaluating AI's Ability to Replicate AI Research (preprint, 2025) [arxiv:2504.01848]
Core benchmark: agent'a bir ICML 2024 paper'ı (+ yazarlardan addendum) veriliyor, sıfırdan tüm deneyleri çalıştıran bir repo + `reproduce.sh` üretmesi isteniyor. Orijinal kod blacklist'te.
20 Spotlight/Oral paper, 12 konu; her paper için yazarla birlikte haftalarca geliştirilmiş hiyerarşik rubric, toplam 8,316 leaf (Code Development / Execution / Result Match). Submission temiz bir VM'de (A10 GPU) yeniden çalıştırılıyor, sonra o3-mini tabanlı SimpleJudge her leaf'i binary puanlıyor; skor ağırlıklı ortalama "Replication Score". JudgeEval ile judge doğrulanıyor (o3-mini F1 0.83, ~$66/paper). Hafif varyant: PaperBench Code-Dev (sadece kod rubric'i).
Findings:
- BasicAgent ile Claude-3.5-Sonnet 21.0%, o1 13.2%, diğerleri <10%.
- IterativeAgent (erken bitirmeyi yasaklayan) o1'i 24.4%'e çıkarıyor, Claude'u 16.1%'e düşürüyor — scaffold hassasiyeti büyük.
- 3-paper subset'te ML PhD'ler 48 saatte 41.4%, o1 26.6%.
- Code-Dev'de o1 43.4%, ama full benchmark ile korelasyonu zayıf (r=0.48).
Relevant Limitations:
- Ölçüm tamamen LLM-judge; judge sadece top-10 dosyayı görüyor, F1 0.83 → skorlar gürültülü.
- Rubric leaf'leri paper'ın implementasyon detaylarına bağlı; farklı ama geçerli tasarımlar Code Development node'larında kaybedebilir.
- Sadece 20 paper, tek domain (ML, Python); maliyet çok yüksek (12 saat GPU run + judge).
Key Takeaway:
- Paper→repo için yazar-onaylı hiyerarşik rubric + temiz ortamda yeniden çalıştırma, kısmi ilerlemeyi ölçmenin güçlü bir şablonu; ama oracle executable değil, LLM verdict'i.

### AutoP2C — AutoP2C: An LLM-Based Agent Framework for Code Repository Generation from Multimodal Content in Machine Learning Papers (ICASSP 2026, 2025) [doi:10.1109/icassp55912.2026.11462205]
Method + küçük benchmark: ML makalesinin text, figure ve tablolarından çalıştırılabilir multi-file Python repo üreten 4 aşamalı multi-agent framework (full text arXiv v2 preprint'i).
Aşamalar: (1) popüler ML repolarından LLM ile "repository blueprint" çıkarımı, (2) MinerU OCR + VLM ile multimodal parsing, (3) LRM ile hiyerarşik task decomposition (dosya arayüzleri, bağımlılıklar), (4) execution feedback'li implement-verify döngüsü. Modeller: GPT-4o (parsing/planning), o1-mini (kod), o1 (doğrulama), o3-mini (refinement). Değerlendirme: yeni Paper2Repo (2024 sonrası 8 makale, 6 ML task) üzerinde üretilen repo'yu orijinal repo ile aynı dataset'te çalıştırıp absolute/relative performance; LLM-as-judge ile orijinal kodun fonksiyon/class'larına göre COMPfunc/COMPclass; ayrıca PaperBench Code-Dev replication score.
Findings:
- AutoP2C 8/8 makale için çalışan repo üretiyor; o1 ve DeepSeek-R1 yalnızca 1/8.
- Relative performance %89.8–122.0 (ortalama %99.5).
- COMPclass ortalama %65.7 (o1 %34.9, R1 %31.1); COMPfunc %51.6 (o1 %29.1).
- PaperBench Code-Dev: 49.2 ± 14.0 vs PaperCoder 44.2.
- Ablation: feedback loop kaldırılınca hiçbir repo çalışmıyor.
Relevant Limitations:
- Benchmark sadece 8 makale; baseline'lar tek-shot LLM, agentic baseline yok (unfair comparison).
- Completeness metriği LLM-judge ve orijinal koda göre hesaplanıyor (reference-coupled); OpenAI model ailesi hem üretiyor hem ölçüyor.
- "Relative performance" metriği tek sayıya (accuracy) dayanıyor; >%100 değerler farklı eğitim koşullarını gösterebilir, doğru implementasyonun kanıtı değil.
Key Takeaway:
- Paper-to-repo'da execution feedback olmazsa olmaz; ancak doğruluk oracle'ı (metrik reproduction) zayıf ve gürültülü.

### DeepRepro — DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories (CIKM 2026, 2026) [arxiv:2608.26557]
Method (demo paper, 5 sayfa): ML paper'ından çalışan repo üretimi için, statik upfront plan yerine repo'nun güncel state'ine göre iteratif subplan üreten agent framework.
Paper → blueprint planning (figure/concept/algorithm sub-analysis agent'ları) → her round'da progress file + repository memory + diagnostics'ten subplan → execute agent dosya yazıyor → memory güncelleniyor. İki mod: fast ve deepplan (quality gate ile). Backbone GPT-5.4 (high reasoning); ablation'da executor DeepSeek-V4-Flash. Değerlendirme PaperBench Code-Dev (20 ICML 2024 paper), hiyerarşik rubric, LLM-judge (ana deneylerde maliyet için GPT-4.1-mini, insan karşılaştırmasında o3-mini). Kod çalıştırılmıyor.
Findings:
- 5-paper subset'te deepplan 84.22 vs fast 82.07; external code reference etkisi marjinal.
- Full 20 paper ortalaması 75.09 (DeepCode 73.6, PaperCoder 49.6, AutoReproduce 51.1 — bunlar önceki çalışmalardan alınmış).
- Subset'te Cursor 66.5, Codex 61 vs 84.2; human Best@3 72.4 vs 77.8 (paylaşılan subset).
- Maliyet ~US$10–12.5/paper, 1–1.5 saat.
Relevant Limitations:
- Değerlendirme tamamen LLM-judge rubric'i, Code-Dev modunda execution yok; judge da ucuz bir model (GPT-4.1-mini), PaperBench'in orijinal judge ayarından farklı.
- Full-set baseline sayıları başka makalelerden alınmış (yazarlar da "strict değil" diyor); controlled karşılaştırma sadece 5 paper.
- Demo formatı: istatistiksel test, varyans, failure analizi yok.
Key Takeaway:
- Paper-to-repo'da plan–state senkronizasyonu (repo memory + diagnostics'e göre re-planning) önemli bir tasarım ekseni.
- Rubric-LLM-judge'a dayalı reproduction benchmark'larında judge seçimi sonuçları doğrudan etkiliyor; survey'de ayrıca işaretlenmeli.


## core / repo-translation

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

### SWE Refactor Bench — SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration? (preprint, 2026) [arxiv:2608.23564]
Benchmark + empirical: 20 gerçek open-source repo'nun (SQLite, zlib, libsodium, GraphHopper vb.) tamamının başka bir stack'e taşınması; 7'si language rewrite (C→Rust, C→Java, Go→Zig), 7 framework, 3 platform, 3 build toolchain. Survey açısından ilgili kısım language rewrite alt kümesi (repo-translation).
Agent offline container'da orijinal repo + hedef stack toolchain ile 6–30 saat çalışıyor. Üç aşamalı değerlendirme: (1) Migration Audit — LLM judge (gpt-5.6-sol, 3 örnek majority) eski stack'in gerçekten kalktığını denetliyor; (2) Behavioural Tests — orijinalden kaydedilmiş 130,118 fixed check (differential); (3) Agentic Verification — 6 bağımsız coding agent 1'er saat orijinal vs migrated arasında counterexample test üretiyor. 8 model, 26 model–effort config, 520 run (Claude Code / Codex harness).
Findings:
- Sadece 28/520 run (%5.4) üç aşamayı geçiyor; 13/20 task hiç çözülmüyor; en iyi claude-opus-5 47.0/100.
- Language rewrite en zor: skor 5.6, Stage II geçişi 12/100, yalnızca 4 kabul.
- 30 run "Blindness": migration yapmadan tüm fixed check'leri geçiyor; fixed suite'i tam geçen 88 run'ın 60'ı agentic verifier'larca kırılıyor.
- Judge–insan uyumu %89.7 (κ=0.795), hatalar çoğunlukla aşırı katılık yönünde.
Relevant Limitations:
- Mixed benchmark: repo-translation yalnızca 7 task; kalan 13 task in-place migration.
- Ölçümde LLM (Stage I judge) ve LLM-generated testler (Stage III) var; judge değerlendirilen sistemlerden biri (self-family bias analiz edilmiş).
- Behavioural check'ler orijinal çıktıya kuplajlı; doğru ama farklı format cezalı.
Key Takeaway:
- Behaviour-only değerlendirme translation'da "hiç çevirmeme" hack'ine açık; migration completeness ayrı gate olmalı. Agentic differential test üretimi fixed suite'in kaçırdığını yakalıyor.

### Tymcrat — Type-migrating C-to-Rust translation using a large language model (EMSE 2025, 2024) [doi:10.1007/s10664-024-10573-2]
Method paper: bütün C programını fonksiyon fonksiyon LLM ile Rust'a çeviriyor, amaç C tiplerini idiomatik Rust tiplerine (Option, Result, reference, slice...) migrate etmek.
Üç teknik: (1) her fonksiyon için birden fazla candidate signature üretmek, (2) çevrilmiş callee signature'larını prompt'a eklemek, (3) compiler feedback ile iteratif type-error fix. Modeller GPT-3.5 Turbo ve GPT-4o mini. Benchmark: 41 GNU paketi (<100K LOC, ör. glpk 59K LOC). Metrikler: migrate edilen tip sayısı, fully/partially migrated signature oranı, type error sayısı, manuel idiomaticity (150 fonksiyon) ve manuel correctness (41 fonksiyon); C2Rust, Laertes, Crown, Concrat ile karşılaştırma.
Findings:
- GPT-3.5 ile baseline'a göre %63.5 daha fazla migrate tip, %71.5 daha az type error.
- GPT-4o mini ile fully-migrated signature %85-91; gain GPT-3.5'e göre daha küçük.
- Manuel örneklemde type error'suz fonksiyonların sadece %56 (GPT-3.5) / %78 (GPT-4o mini)'i semantik olarak doğru.
- Crown type error üretmezken Tymcrat program başına ort. 148 type error bırakıyor.
Relevant Limitations:
- Çevrilen programlar compile olmuyor, dolayısıyla hiçbir test çalıştırılamıyor; fonksiyonel eşdeğerlik ölçülmüyor.
- Metrikler proxy (tip sayısı, error sayısı); correctness sadece küçük manuel örnek ve değerlendiriciler arası anlaşmazlık var.
- 3,000 token'ı aşan fonksiyonlar atlanıyor.
Key Takeaway:
- Repo-level translation'da idiomatiklik vs compile/correctness trade-off'u açık; executable oracle olmadan ilerleme iddiaları zayıf kalıyor.

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

### RustAssure — RustAssure: Differential Symbolic Testing for LLM-Transpiled C-to-Rust Code (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00051]
Method paper (yalnızca abstract mevcut): mevcut C codebase'lerini LLM ile Rust'a transpile eden ve sonucu differential symbolic testing ile doğrulayan sistem.
Prompt engineering ile idiomatic/safe Rust üretimi hedefleniyor; orijinal C fonksiyonu ile Rust karşılığının symbolic return değerleri karşılaştırılarak semantik eşdeğerlik kontrol ediliyor (unit/fuzz testing'in kaçırdığı subtle bug'lar için). Değerlendirme 5 real-world application/library üzerinde, function-level. LLM modeli abstract'ta belirtilmemiş.
Findings:
- C fonksiyonlarının %89.8'i için compilable Rust fonksiyonu üretiliyor.
- Bunların %72'si C ile eşdeğer symbolic return value veriyor.
Relevant Limitations:
- Metrikler function-level; translate edilmiş projenin bütün olarak build edilip çalıştığına dair bilgi yok, repo-level bütünlük belirsiz.
- Oracle referans C implementasyonuna bağlı (differential); symbolic karşılaştırma yalnızca return value'ları kapsıyor, side effect'ler belirsiz.
- Sadece 5 proje; LLM ve baseline bilgisi abstract'ta yok.
Key Takeaway:
- Differential symbolic testing, translation'da test-suite'e bağımlı olmayan güçlü bir oracle alternatifi; ama whole-repo translation değerlendirmesinde function-level doğrulamanın yetersizliğine örnek.

### RepoTransBench — RepoTransBench: A Real-World Multilingual Benchmark for Repository-Level Code Translation (preprint, 2024) [arxiv:2412.17744]
Benchmark + agent: tüm repoyu başka dile çevirme (config dosyaları dahil), executable test suite ile doğrulama.
1,897 örnek, 970 proje, 13 dil çifti (C, C++, C#, Java, JavaScript, Matlab, Python → Python/Rust/Java/C#/Go/C++); ortalama 2,394 LoC, 177 fonksiyon, 87.9 cross-file dependency. Seçim 21 geliştiricili anket + >50 star filtresi. Testler multi-agent pipeline ile üretiliyor (Generator, Runner, Coverage Analyst, Test Case Translator): kaynak dilde test yazılıp geçirilir, sonra hedef dile LLM ile çevrilir; line coverage %81.89. Metrikler: SR (tüm testler geçer), CR (compile), APR, AMPR. RepoTransAgent: ReAct tarzı (ReadFile/CreateFile/ExecuteCommand/Search). 8 model (Claude-Sonnet-4, GPT-4.1, o3-mini, Gemini-2.5-Flash-Lite, Qwen3, DeepSeek vb.).
Findings:
- En iyi SR %32.8 (RepoTransAgent + Claude-Sonnet-4 / GPT-4.1); TranslationOnly neredeyse her modelde %0 SR.
- Static→dynamic çeviri %45-63, dynamic→static %10'un altında.
- DeepSeek-Reasoner %1.2 SR (uzun reasoning → timeout/context sorunları).
- Karmaşıklık (cross-file dep, LoC, class sayısı) arttıkça başarı düşüyor; hata sınıfları: config dosyaları, eksik üretim, dil özellikleri.
Relevant Limitations:
- Testler hem üretimde hem hedef dile çeviride LLM agent'lara dayanıyor; çevrilmiş testin doğruluğu bağımsız doğrulanmıyor, hatalı test oracle'ı riski.
- Testler kaynak reponun public API'sine bağlı; hedef dilde farklı API/tasarım seçimleri cezalandırılabilir.
- Popüler GitHub repoları → contamination riski; agent karşılaştırması aynı harness'la ama maliyet raporu yok.
Key Takeaway:
- Repo translation'da tek-seferlik çeviri pratikte işe yaramıyor; execution feedback'li agent loop zorunlu.
- Ölçeklenebilir benchmark için test üretimini agent'lara devretmek mümkün, ama test çevirisinin kalitesi darboğaz.

### TRAM — Advancing Automated In-Isolation Validation in Repository-Level Code Translation (preprint, 2025) [arxiv:2511.21878]
Method: Java→Python repo çevirisinde RAG tabanlı context-aware type resolution + mock-based in-isolation validation; AlphaTrans üzerine kurulu.
Kaynak testler Java'da çalıştırılıp her metod çağrısının I/O çiftleri ve side-effect'leri serialize ediliyor; hedef dilde deserialize edilerek mock'lu test yeniden oluşturuluyor, böylece her method fragment tek başına doğrulanıyor (test coupling effect'i kırıyor; GraalVM ve glue code gerektirmiyor). EvoSuite testleri ile test havuzu genişletiliyor. AlphaTrans benchmark'ının 10 Java projesi (commons-cli, codec, csv, exec vb.); DeepSeekCoder-33B-Instruct ve Devstral-24B; 4 re-prompt bütçesi. Manuel FP/FN analizi 3 projede.
Findings:
- Functional equivalence %43.10 vs AlphaTrans %25.14 (aynı model); Devstral-24B ile %46.61.
- Doğrulanabilir fragment oranı %69.98 vs %56.57; mock testlerini geçen %61.59 (2001/3249).
- Mock-based validation kaldırılınca %6.81'e çöküyor; RAG type resolution kaldırılınca %41.18 (küçük katkı).
- Type translation accuracy %89.00 (AlphaTrans %91.99 ama 55 saat manuel düzeltmeyle).
Relevant Limitations:
- Oracle kaynak implementasyonun gözlenen I/O'suna sıkı bağlı (differential); farklı iç yapı/tip seçimi yapan doğru çeviri cezalandırılabilir, mock'lar kaynak çağrı yapısını dayatıyor.
- Fragment-level eşdeğerlik ≠ çalışan uçtan uca repo; tam proje test pass oranı (ATP) sadece %7-13.
- Tek dil çifti, 10 proje; AlphaTrans pipeline'ına bağımlı.
Key Takeaway:
- Kaynak repoyu execution oracle olarak kullanıp I/O kaydından mock test üretmek, test çevirisinin false-positive sorununu aşmanın pratik yolu.

### AlphaTrans — AlphaTrans: A Neuro-Symbolic Compositional Approach for Repository-Level Code Translation and Validation (FSE 2025, 2024) [arxiv:2410.24117]
Method çalışması: Java reposunu (source + test) Python'a repository-level çeviren neuro-symbolic pipeline. Program analysis ile PL-specific özellikler (overloading vb.) refactor ediliyor, proje field/method fragment'lara bölünüyor, önce compilable bir target skeleton kuruluyor, sonra fragment'lar reverse call order'da LLM ile çevriliyor.
Validation iki katmanlı: GraalVM language interoperability ile Java testleri çevrilmiş tek fragment üzerinde in-isolation koşturuluyor; ayrıca test'ler decompose edilip çevriliyor. 10 gerçek GitHub projesi (836 class, 8575 method, 2719 unit test → 17874 fragment); ana model DeepSeek-Coder-33b-Instruct, ablation'da GPT-4o. Third-party bağımlılıklar önceden otomatik siliniyor.
Findings:
- Fragment'ların %96.40'ı syntactically correct; application method fragment'ların %27.03'ü runtime-, %25.14'ü functional-equivalence validasyonundan geçiyor.
- Recompose edilmiş projelerde test pass rate (TPR) düşük; uzun call chain'ler (test başına ~27 method) runtime error'ları yayıyor.
- GPT-4o ile %99.2 syntactic, %27.95 functional equivalence; maliyet proje başına ~$14.39. Ortalama çeviri süresi 34 saat.
- File-level prompting baseline'ında hiçbir çevrilmiş test geçmiyor → decomposition kritik.
- İki geliştirici 4 projeyi ortalama 20.1 saatte tüm testleri geçecek hale getirdi.
Relevant Limitations:
- Oracle tamamen kaynak reponun kendi testleri; çeviri yapısı source'a birebir bağlı (skeleton aynı), alternatif idiomatic tasarım değerlendirilmiyor.
- Sadece Java→Python, 10 proje; dış kütüphaneler yapay olarak çıkarılmış.
- Fragment-level metrikler proje-level başarıyı olduğundan iyi gösteriyor; uçtan uca "tüm testler geçer" oranı düşük.
Key Takeaway:
- Repo translation'da skeleton-first + dependency order + in-isolation differential validation, file-level prompting'e göre çok daha ölçeklenebilir.
- Proje-level başarı raporlamak için fragment metrikleri yetmez; survey'de bu ayrım vurgulanmalı.

### TransGraph — Can We Translate Code Better with LLMs and Call Graph Analysis? (IJCAI 2025, 2025) [doi:10.24963/ijcai.2025/848]
Method: LSP ile tüm codebase'in call graph'ını çıkarıp her çeviri prompt'una referenced variables, called functions ve caller code bağlamı ekleyen; runtime hataları DAP tabanlı "bridged debugger" ile kaynak ve hedef programı paralel adımlayıp binary search ile lokalize eden code translation yaklaşımı.
C/C++, Java, Python arası çeviri; GPT-3.5, GPT-4, Llama 2, StarCoder, Claude 3 Sonnet. Başarı = compile + runtime exception yok + aynı input'a aynı output. Veri: CodeNet, Avatar, EvalPlus, HumanEval-X (function/program-level) ve iki proje: Apache Commons CLI (Java) ve Click (Python).
Findings:
- Function-level datasetlerde GPT-4 ile %72.5–79.1 başarı; vanilla GPT-3.5'e göre ortalama +%15.7.
- Proje-level: Commons CLI %17.8, Click %22.4 (GPT-4); UniTrans'a göre küçük fark.
- Ablation: referenced vars +%7.3, called funcs +%4.4, bridged debugger +%2.2.
Relevant Limitations:
- Proje-level değerlendirme sadece 2 repo ve nasıl ölçüldüğü (hedef dil, test seti) çok az anlatılıyor.
- Katkının büyük kısmı function-level benchmark'larda; repo-level iddia zayıf destekli.
- Dynamic test case generation detayları ve maliyet raporlanmamış.
Key Takeaway:
- Call-graph bağlamı ve differential debugging repo translation için umut verici bileşenler, ama gerçek repo ölçeğinde başarı hâlâ ~%20 civarında.

### CRUST-Bench — CRUST-Bench: A Comprehensive Benchmark for C-to-safe-Rust Transpilation (COLM 2025, 2025) [arxiv:2504.15254]
Benchmark: 100 C reposunun safe, idiomatic Rust'a transpilation'ı. Her task: C kaynak kodu + elle yazılmış safe Rust interface (tip ve imzalar, body'ler unimplemented!()) + mevcut C testlerinden uyarlanmış Rust testleri.
Repo'lar ortalama 958 LOC (max 25,436), 34.6 fonksiyon, 76.4 test, %67 coverage; toplam 299 interface dosyası, 3085 fonksiyon. Değerlendirme: cargo build + test geçme. Modeller: o3, o1, GPT-4o, Claude Opus 4 / 3.7 / 3.5, Gemini, açık modeller; compiler-repair ve test-repair döngüleri (3 round) ve pipelined SWE-agent.
Findings:
- Single-shot en iyi o3: %19 test geçme (build %35); Claude Opus 4 %22.
- Test repair ile o3 %48, Claude Opus 4 %40.
- SWE-agent (Claude 3.7) %32; generate-then-repair loop'unu geçemiyor; tam end-to-end agent kullanımı kırılgan.
- Test repair build başarısını %5–20 düşürebiliyor.
Relevant Limitations:
- Interface elle verildiği için görev "skeleton-to-library"ye yakın; mimari karar değerlendirilmiyor, alternatif Rust tasarımları dışlanıyor.
- Testler interface'e sıkı bağlı (white-box); coverage ortalama %67.
- Repo'lar küçük-orta ölçekli, sadece C→Rust; contamination analizi yok.
Key Takeaway:
- Hedef dilde interface + test vermek repo translation'ı otomatik doğrulanabilir kılıyor; ama bu, translation'ı bir interface-implementation görevine indirgiyor.

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

### ECAT — Entropy-based Code Adversarial Translation for Real-world Repository Migration (preprint, 2026) [arxiv:2608.09273]
Method + küçük benchmark: Android (Java/Kotlin) uygulamasını sıfırdan HarmonyOS/ArkTS reposuna taşıyan generator–discriminator multi-agent framework ve A2H-RepoBench.
Migration "Code Entropy" (K=14 boyut; compile, fidelity, runtime GUI) minimizasyonu olarak formüle ediliyor: bağımsız discriminator entropy ölçüp "text gradient" (dosya-düzeyi direktif + gerekli skill) üretiyor, generator repoyu güncelliyor, update sadece entropy düşerse kabul. Başarılı trajectory'ler self-evolving memory tree'ye damıtılıyor. Emulator screenshot'larını Qwen3.7-Plus değerlendiriyor. Backbone DeepSeek-V4-Pro. Benchmark: 3 repo (Gallery 50K, AntennaPod 120K, Meshtastic 300K LOC). Metrik: CodeGraph semantic node alignment (kaynak repo ile) + feature checklist üzerinden Agent-as-Judge.
Findings:
- Ortalama 74.7% vs ReCodeAgent 46.4%, OpenHands 14.0%, RepoTransAgent 13.3%.
- Discriminator kaldırılınca (self-evaluation) Agent skoru çöküyor (ör. Meshtastic 71.2→12.0).
- ReCodeAgent yüksek alignment ama düşük Agent skoru: yapı korunuyor, içi placeholder.
- Maliyet: 38–126 iterasyon, 12–44 saat, 65–230M token/repo; memory tree token'ı ~yarıya indiriyor.
Relevant Limitations:
- Sadece 3 repo; test tabanlı fonksiyonel oracle yok, doğruluk LLM agent-as-judge ile ölçülüyor.
- Node alignment kaynak repoya yapısal benzerlik ödüllendiriyor → farklı ama geçerli ArkTS mimarilerini cezalandırır.
- Aynı tip LLM'ler hem entropy/discriminator hem judge; maliyet çok yüksek.
Key Takeaway:
- Generation ile evaluation'ı ayrı agent'lara bölmek (self-confirmation bias'ı kırmak) uzun-horizon repo translation'da en büyük kazancı veriyor.
- Platform-arası (UI framework + API) migration, repo translation'ın dil çevirisinden daha zor bir alt türü; executable oracle eksikliği açık problem.

### EvoC2Rust — EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation (ICSE-SEIP 2026, 2025) [arxiv:2508.04295]
Method (+ C2R-Bench): tüm C projesini güvenli Rust projesine çeviren skeleton-guided framework.
Üç aşama: (1) projeyi modüllere böl, feature-mapping destekli LLM ile tanım/makroları çevir, type-check edilmiş stub'lardan derlenebilir Rust skeleton kur; (2) fonksiyonları artımlı çevirip stub'ları değiştir; (3) rule-based + LLM refinement ile compile hatası onar. Backbone DeepSeek-V3 ve Qwen3-32B. Veri: Vivo-Bench (19 algoritmik proje) + C2R-Bench (Huawei'den 6 endüstriyel proje, 222 test) + RepoTransBench'ten 10 büyük proje (9.9K–91.6K LOC). Metrikler: ICompRate, line acceptance (manuel düzeltilmiş versiyona göre precision/recall), SafeRate; module-level'da FCompRate ve TestRate.
Findings:
- C2R-Bench (DeepSeek-V3): ICompRate 93.84%, AccRate ~97%, SafeRate 97.41%; Tymcrat 72.02%, Self-Repair 49.21% compile.
- C2Rust %99+ derleniyor ama SafeRate 1.83%; C2SaferRust 48.24%.
- Module-level test pass: Vivo 99.07%, C2R 89.53%.
- Büyük projelerde ICompRate ~69–76%'ya iniyor, SafeRate ~96%.
Relevant Limitations:
- Project-level değerlendirmede fonksiyonel test yok: compile rate + line acceptance (referansa benzerlik; referans da LLM destekli ve kendi çıktıları üzerinden düzeltilmiş) — kendi yöntemine bias riski.
- Testler yalnızca module-level fill-in-the-blank ayarında, referans Rust projesi içinde koşturuluyor.
- Benchmark'lar küçük (C2R-Bench 6 proje), sadece standart C kütüphanesi, tek-thread.
Key Takeaway:
- Derlenebilir skeleton'ı önce kurup sonra doldurmak, repo translation'da cross-file tutarlılık için etkili — skeleton-to-library ile repo-translation arasında köprü.


## core / skeleton-to-library

### DbC Constraints — Preconditions and Postconditions as Design Constraints for LLM Code Generation (IEEE Access 2025, 2025) [doi:10.1109/access.2025.3625819]
Empirical çalışma: class-level specification'lara explicit precondition/postcondition (Design-by-Contract) eklemenin, altı LLM'in orta karmaşıklıkta bir sistemin tamamını implemente etmesine etkisini ölçüyor.
Input: sistematik olarak tasarlanmış class-level spec'ler (NL-only vs. NL + pre/postcondition) → output: sistemin tam implementasyonu (Python ve C++). Değerlendirme pass@k (testlere karşı). Hangi altı model, kaç class, test sayısı abstract'ta yok.
Findings:
- Explicit design constraint'ler initial generation accuracy'yi (pass@k) anlamlı şekilde artırıyor; etki Python'da daha güçlü, C++'ta da var.
- Küçük parametreli modeller en çok faydalanıyor.
Relevant Limitations:
- Tek bir sistem — independent repository sayısı 1; genellenebilirlik çok sınırlı.
- Class yapısı spec ile önceden sabitleniyor; bu daha çok skeleton-to-library, architecture tasarımı test edilmiyor. Testler büyük olasılıkla bu class interface'ine bağlı (white-box), alternatif tasarımlar değerlendirilemez.
- Full text yok; contamination ve test kalitesi bilinmiyor.
Key Takeaway:
- Executable/formal contract'lar (pre/postconditions) NL-only spec'e göre daha iyi bir hand-off artefact'ı — survey'deki structured spec argümanını destekleyen küçük ölçekli kanıt.

### Vero — Vero: Can AI Agents Build Formally Verified Software Repositories? (preprint, 2026) [arxiv:2608.13522]
Benchmark + empirical çalışma: repository düzeyinde implementation ve proof'un birlikte sentezlendiği (code-and-proof) ilk Lean 4 benchmark'ı.
43 instance var: 13'ü Dafny/Verus/Coq'tan (Track 1), 30'u Python'dan (Track 2) Lean 4'e elle küratörlenmiş. Toplam 743 scored API ve 2,705 spec. Her instance multi-module bir Lean projesi; type'lar, API signature'ları, insan küratörlü spec'ler ve reference implementation içeriyor. İki mod var: proof-only (reference impl verili) ve code-and-proof (agent API body'lerini yazıp tüm spec'leri kanıtlıyor). Metrik full-solve: tüm spec'ler kanıtlanmalı. Anti-cheat için marker bölgeleri, axiom allowlist, rule-based detector ve LLM-judge kullanılıyor. Audit mekanizması, spec unsatisfiability ya da reference bug'ının formal kanıtını kabul ediyor. Agent'lar Codex + GPT-5.5 (mid/xhigh) ve Claude Code + Opus 4.8 / Sonnet 5 (xhigh), 90 dakika bütçeyle.
Findings:
- Code-and-proof'ta GPT-5.5 xhigh 27/43, Opus 4.8 8, GPT-5.5 mid 2, Sonnet 5 2 instance çözüyor. Proof-only'de sırasıyla 25, 10, 6, 2. 10 instance hiçbir konfigürasyona çözülmüyor.
- Spec başına pass oranı yüksek (%87.3) ama full-solve düşük; darboğaz cross-module invariant'lar ve reusable lemma library kurmak.
- 5 instance-agent çiftinde agent, reference algoritmayı daha kolay kanıtlanır bir implementasyonla değiştirip 250/250 spec'i kapatıyor (proof-only'de 201).
- Tam çözümlerde proof satırlarının ~%72–74'ü helper lemma'lardan oluşuyor.
Relevant Limitations:
- Implementation kısmı küçük (medyan ~50–60 satır), iş ağırlıklı olarak proof. "Repository generation"dan çok skeleton-to-library + verification.
- API signature'ları ve spec'ler önceden sabit, yani mimari kararları insan veriyor. Spec'ler reference'tan türetilmiş, ama formal spec olduğu için alternatif implementasyonlara açık (bu bir artı).
- Sadece Lean. 43 instance, tek run, konfigürasyonlar arası harness confound'u var (Codex vs Claude Code).
Key Takeaway:
- Formal spec, test yerine implementation-agnostic bir oracle sağlıyor; audit mekanizması da benchmark hatalarını formal kanıtla yakalayan iyi bir örnek.

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

### JavaBench — JavaBench: A Benchmark of Object-Oriented Code Generation for Evaluating Large Language Models (preprint, 2024) [arxiv:2406.12902]
Benchmark: NL proje açıklaması + code skeleton (TODO metodlar) verilip tüm Java projesinin tamamlanması; OOP özellikleri (inheritance, polymorphism, encapsulation) odaklı.
4 proje (üniversite ders ödevleri; Pipe Mania, Jeson Mor, Inertia, Sokoban tarzı text-based oyunlar), 106 class, 389 metod, ortalama 1,740 LoC (test hariç). 396 el yazımı test, coverage %92'ye kadar; 282 öğrenci ortalama 90.93/100. Canonical çözümler gizli tutulmuş (contamination'a karşı). Değerlendirme: 3 context ayarı (maximum/minimum/selected=jdeps ile ilgili class'ların sadece signature'ları), 5 synthesis stratejisi (holistic, independent, incremental ×3 order), 2 granularite (class-wise, test-wise; ayrıca project-wise), Completion@k / Compilation@k / Pass@k. Modeller: WizardCoder-15B, DeepSeek-Coder 6.7B/33B, Phind-CodeLlama-34B, gpt-3.5-turbo-1106.
Findings:
- Project-wise Pass@1 ve Pass@5 tüm ayarlarda 0; hiçbir proje tam tamamlanamıyor.
- En iyi ortalama: Completion@1 %91.73, Compilation@1 %72.33, class-wise Pass@1 %70.92; test-wise Pass@5 en fazla %48.24 (öğrenciler %90.93).
- Selected context (sadece signature) en iyisi; minimum context'te test-wise Pass@1 ~%3.8'e çöküyor.
- Holistic synthesis (class'taki tüm metodlar tek seferde) independent/incremental'dan daha iyi; ClassEval bulgusunun tersi.
- Test hatalarının %76.63'ü AssertionFailedError + IllegalArgumentException.
Relevant Limitations:
- Sadece 4 proje, hepsi aynı ders kaynaklı ve benzer (console oyunları); ölçek ve çeşitlilik zayıf.
- Skeleton mimariyi tamamen sabitliyor; testler canonical çözüme göre yazılmış, farklı tasarımı değil sadece metod gövdesi üretimini ölçüyor.
- Güncel/agentic modeller yok, 8K karakter truncation deneysel bir confound.
Key Takeaway:
- Skeleton-to-library setup'ında class/test-wise granülarite olmadan sonuçlar all-0'a düşüyor; kademeli metrikler gerekli.
- Context'te tam implementasyon yerine signature vermek hem token hem doğruluk açısından daha iyi.

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


## contextual / repo-context-gen

### REPOFORGE — Repository-Level Code Generation with Retrieval-Augmented Large Language Model Agents (IJRITCC, 2024) [doi:10.5281/zenodo.21157035]
Benchmark + method. Full text yok, not sadece abstract'a dayanıyor. Tek dosyalık function benchmark'larına karşı, cross-file context ve executable test suite içeren repo-level bir benchmark ve retrieval-augmented agent öneriyor.
612 permissive GitHub reposundan 4,140 executable item, 5 dil (dil isimleri abstract'ta yok); 4 task family: single-file completion, cross-file completion, program repair, feature implementation. Her item project context + hidden test suite ile geliyor; metrik execution Pass@1. Agent: structure-aware dense retrieval + reason–retrieve–edit–test döngüsü.
Findings:
- Altı "2023-era" modelde retrieval, no-retrieval baseline'a göre Pass@1'i 19–30 puan artırıyor.
- Agent, static dense retrieval'a göre +6–8 puan; GPT-4 ile %86.3 Pass@1.
Relevant Limitations:
- Task family'lerin yarısı (repair, feature implementation) EC1 kapsamında; contextual kısmın ayrı sonuçları abstract'ta yok.
- %86.3 Pass@1 repo-level için şüpheli derecede yüksek; contamination/freshness tartışması görünmüyor. Zenodo DOI ve dergi künyesi uyumsuz, provenance sorgulanmalı.
Key Takeaway:
- Hidden test'li çok dilli repo-level item fikri doğru yönde, ama full text olmadan güvenilirliği teyit edilemiyor; survey'de temkinli anılmalı.

### CECoder — CECoder: Fine-Grained Code Element Retrieval for Repository-Level Code Generation (ISSREW 2025, 2025) [doi:10.1109/issrew67781.2025.00051]
Method, contextual. Full text yok, not abstract'a dayanıyor. Repo-level function generation için whole-function semantic retrieval yerine code element (developer-defined class/method) kullanımına odaklı ince taneli RAG.
Pipeline: task requirement ile snippet retrieve → draft code üret → draft'ı code element çağrısı içeren bloklara böl → her blok için element kullanım örneklerini retrieve et → re-rank ve prompt'a seçici entegrasyon. Değerlendirme DevEval (1,825 task, Python) üzerinde; metrikler EM, Edit Similarity, Pass@1, Recall@1.
Findings:
- RepoCoder'ı tüm metriklerde geçiyor: EM %4.39, ES %41.97, Pass@1 %27.01, Recall@1 %39.25.
- Farklı boyut ve duplication seviyesindeki repolarda genelleştiği iddia ediliyor.
Relevant Limitations:
- Tek benchmark (DevEval), tek dil; kullanılan backbone modeller abstract'ta yok.
- Draft'a dayalı ikinci retrieval, draft kalitesine bağımlı; maliyet raporlanmamış.
Key Takeaway:
- Contextual tier'da "element usage" düzeyinde retrieval, cross-file API misuse hatalarını hedefleyen makul bir yön; Pass@1 hâlâ düşük (%27).

### GRACG — GRACG: Graph Retrieval Augmented Code Generation (ASE Workshops (ASEW) 2025, 2025) [doi:10.1109/asew67777.2025.00060]
Method: repoyu files/classes/functions'tan oluşan heterogeneous graph olarak modelleyip GNN embedding'leriyle context retrieval yapan RAG framework'ü; repository-aware function generation için.
GNN embedding'leri önceden hesaplanıp index olarak kullanılıyor. Retrieval ayrı bir benchmark'ta (NL description'dan çağrılacak fonksiyonları bulma) ölçülüyor; end-to-end generation pass@k ile test case'lere karşı değerlendiriliyor. Benchmark adı, dil ve modeller abstract'ta yok.
Findings:
- Graph-based retrieval klasik retrieval yöntemlerini geçiyor.
- End-to-end pass@k'da iyileşme istatistiksel olarak anlamlı değil — oracle fonksiyonlar verildiğinde bile.
Relevant Limitations:
- Retrieval kazancının generation'a yansımaması, bottleneck'in context değil başka yerde olduğunu gösteriyor; nedeni abstract'ta analiz edilmemiş.
- Full text yok; benchmark ölçeği ve dil kapsamı bilinmiyor.
Key Takeaway:
- Dürüst bir negatif sonuç: daha iyi retrieval ≠ daha iyi repo-context generation; oracle-context ablation'ı değerli bir kontrol.

### Wenwang — Wenwang: Toward Effectively Generating Code Beyond Standalone Functions via Generative Pre-trained Models (TOSEM 2025, 2025) [doi:10.1145/3725213]
Method + training-data: non-standalone fonksiyonları (user-defined fonksiyon/third-party library çağıran) üretmek için context-aware fine-tuning.
WenwangData: docstring + code'a ek olarak program analysis ile toplanan contextual bilgi içeren fine-tuning dataset'i. WenwangCoder: PanGu-Coder (~300M) üzerinde bu veriyle fine-tune. Değerlendirme CoderEval (repo context'li, executable test) ve HumanEval.
Findings:
- ~300M ölçeğinde CodeGen, PanGu-Coder, PanGu-FT'yi geçiyor.
- HumanEval'de ChatGPT'nin gerisinde, ama CoderEval'de ChatGPT'ye benzer sonuç.
Relevant Limitations:
- Küçük modeller (~300M) ve eski baseline'lar; güncel code LLM'lerle kıyas yok. CoderEval ölçeği sınırlı (tek dil varsayımı, full text yok).
Key Takeaway:
- Context'i fine-tuning verisine gömmek, küçük modelde repo-bağımlı fonksiyon üretimini büyük modellere yaklaştırabiliyor.

### Dynamic Eval — A Dynamic Evaluation Approach to Repository-Level Code Generation Via LLM (IEEE AITest 2026, 2026) [doi:10.1109/aitest70988.2026.00019]
Empirical/evaluation framework: DevEval Python task'ları üzerinde, unit-test feedback ile çok turlu repair trajectory'lerini analiz ediyor.
İşlenmiş test set'leri oluşturuluyor; her tur için round-level effectiveness, feedback-induced gain ve regression stability ölçülüyor. Modeller abstract'ta belirtilmemiş.
Findings:
- Kazançların ~3/4'ü ilk üç turda geliyor; net feedback gain 5. turda negatife dönüyor.
- Önceden düzeltilmiş hataların tekrar ortaya çıkma oranı modellere göre %4.5–%8.8.
Relevant Limitations:
- Tek dil (Python) ve tek benchmark (DevEval); feedback reference unit test'lerden geliyor — test'lerin kendisi oracle hem de feedback, bu overfitting riskini maskeleyebilir.
Key Takeaway:
- Test-feedback loop'larında early-round budgeting + best-so-far retention; sınırsız iterasyon regresyon üretiyor.

### RUCCE / RUCACoder — Beyond Maintenance: A Benchmark and Multi-Agent Framework for Repository-Usage Code Generation (ACM proceedings, 2026) [doi:10.1145/3805712.3808589]
Benchmark + method. Full text yok; not abstract üzerinden. Maintainer-centric (bug fix, feature) değil, "repository usage" senaryosu: dış kullanıcı repo-internal API'leri çağırarak runnable end-to-end script yazıyor.
Her instance: NL usage instruction + grounded target API'ler + verified reference script; gerçek Python repolarından. Hem API retrieval hem script generation ölçülüyor. RUCACoder: Retriever (hiyerarşik repo exploration), Verifier (rerank + validation), Coder (feedback-driven synthesis) closed-loop.
Findings:
- Abstract'a göre RUCACoder birden çok backbone LLM'de retrieval ve generation baseline'larını tutarlı şekilde geçiyor; sayı verilmiyor.
Relevant Limitations:
- Değerlendirmenin execution-based olup olmadığı abstract'tan net değil; "verified reference script" referansa bağlı (similarity veya output eşleşmesi) bir oracle'a işaret edebiliyor.
- Repo ve instance sayısı, kullanılan modeller raporlanmamış (abstract düzeyinde).
Key Takeaway:
- Contextual tier'ın "kullanıcı tarafı" varyantı: repo değiştirilmiyor, repo'nun API'leri üzerine yeni dosya yazılıyor — repo-level generation'da retrieval'ın önemini ayrı ölçmek için iyi bir kurgu. Full text ile eval doğrulanmalı.

### ChainBench — ChainBench: An LLM Benchmark for Cross-Chain Code Generation (preprint, 2026) [doi:10.5281/zenodo.20265206]
Benchmark + empirical. Full text yok; not abstract üzerinden. Production smart-contract repolarından cross-chain contract translation ve contract generation görevleri.
Her task structured spec + containerized environment veriyor; sistem eksik functionality'yi implemente edip repo'nun mevcut verification suite'ini geçmeli. Metrik Pass@1 task success. 42 task; EVM Solidity, NEAR Rust, Aptos Move, Sui Move, Starknet Cairo. 9 model-agent sistemi, hem aynı harness hem "preferred harness" koşularında zero-shot.
Findings:
- En iyi sistem %88.1 success; birkaç open-weight sistem %52–60, çok daha uzun solve süreleriyle.
- Performans hedef chain'e ve task tipine göre değişiyor; hatalar dar behavioral mismatch'lerden (eksik edge-case guard) build/repo-compatibility sorunlarına kadar.
Relevant Limitations:
- 42 task küçük ölçek; bağımsız repo sayısı abstract'ta yok.
- Preferred-harness koşuları model ve harness etkisini karıştırıyor.
- Tests mevcut repo'nun kendi suite'i — gerçek oracle ama "eksik parçayı doldur" formatı EC1 sınırına yakın.
Key Takeaway:
- Az kaynaklı diller (Move, Cairo) için repo-bağımlı, test-tabanlı değerlendirme örneği; dil çeşitliliği lens'i için değerli.

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

### SecRepoBench — SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories (LLM4Code 2026, 2026) [arxiv:2504.21205]
Benchmark: 27 C/C++ repo'da 318 secure code completion task'ı (15 CWE); bir fonksiyon içindeki maskelenmiş, güvenlik-hassas bölgeyi repo context'iyle doldurma.
ARVO (OSS-Fuzz) vulnerability-fix commit'lerinden türetiliyor; açıklamalar GPT-4o + manuel düzenleme, contamination için değişken yeniden adlandırma. Correctness: developer-written relevant unit test'ler; security: OSS-Fuzz PoC crash. Metrikler: pass@1, secure-pass@1, secure %. 29 standalone LLM (BM25 top-5 fonksiyon) + 15 agent (Aider, OpenHands, Claude Code).
Findings:
- En iyi standalone GPT-5 %39.3 secure-pass@1; en iyi agent OpenHands + o3 %53.5.
- Agent kazancı ağırlıkla correctness'tan (örn. OpenHands + GPT-5 +%25.5 pass@1, sadece +%4.7 secure %).
- BaxBench'e göre tüm modeller belirgin daha düşük; model sıralaması değişiyor.
Relevant Limitations:
- Görev fonksiyon-içi küçük bölge; repo üretimi değil, sadece contextual.
- Security oracle tek bir PoC — başka zafiyetleri görmüyor; unit test'ler referans patch'in geçtikleri.
Key Takeaway:
- Repo-bağımlı generation'da correctness ve security ayrı eksenler; agent'lar birincisini iyileştiriyor, ikincisini pek değil.

### SolAgent — SolAgent: A Specialized Multi-Agent Framework for Solidity Code Generation (preprint, 2026) [arxiv:2601.23009]
Method: Solidity için tool-augmented multi-agent; inner loop Forge compile+test, outer loop Slither static analysis, file-system tool'larıyla proje bağımlılıklarını çözme; trajectory'lerle Qwen3-8B distillation.
Değerlendirme SolEval+ üzerinde: SolEval'in repository-aware function-level verisinden file-level'a çevrilmiş 81 dosya, 1,188 manuel gözden geçirilmiş Foundry testi. Metrikler: compile rate, Pass@1 (geçen test oranı), gas, Slither vulnerability sayısı. Baseline'lar: vanilla LLM, Copilot, DeepCode, MetaGPT, Qwen-Agent (Claude Sonnet 4.5, GPT-5-Mini, GPT-5.1).
Findings:
- Claude Sonnet 4.5 ile %64.39 Pass@1 (vanilla %25.59, en iyi agent baseline Qwen-Agent %28.37); compile rate %95.06.
- Slither bulguları insan koduna göre %15.70 (Claude) – %39.77 (GPT-5-Mini) daha az.
- Distillation zayıf: Qwen3-8B %0.33 → %1.31 Pass@1.
Relevant Limitations:
- Testler yazarların kendi yazdığı; Slither hem refine döngüsünde hem metrikte — metric gaming riski.
- Test set sadece 81 dosya; distillation sonuçları pratikte anlamsız düzeyde.
Key Takeaway:
- Domain-özel compiler/analyzer feedback'i repo-bağlamlı generation'da genel agent'lardan çok daha belirleyici.

### TDD-Agent — TDD-Agent: Test-Driven Reasoning for Code Generation (preprint, 2026) [arxiv:2608.16742]
Method: model önce executable test yazıyor, sonra kod ve testi execution feedback ile birlikte iteratif rafine ediyor (dual-track). Function-level etkisi LiveCodeBench'te TDD-prompt ile, repo-level etkisi RepoEval'de ölçülüyor.
RepoEval function-level alt kümesi, 8 GitHub repo, her repo için Docker; üretilen fonksiyon repoya konup ilgili unit test'ler çalıştırılıyor. Modeller GPT-5-mini, DeepSeek-V3.2, Qwen3-Coder-30B-A3B; baseline'lar In-File, RAG, RepoCoder, mini-SWE-agent.
Findings:
- 10 iterasyonda pass rate: GPT-5-mini %78.24 (mini-SWE-agent %61.31), DeepSeek %90.77 (%84.18), Qwen %59.34 (%52.97).
- 5. iterasyonda token kullanımı mini-SWE-agent ile benzer; iterasyonla üretilen testlerin coverage/mutation skoru da artıyor.
Relevant Limitations:
- RepoEval sadece 8 Python repo, eski ve muhtemelen contaminated.
- Baseline RAG yöntemleri agent değil; asıl adil kıyas mini-SWE-agent ile sınırlı.
Key Takeaway:
- Testi post-hoc validator değil ara spesifikasyon olarak kullanmak repo-bağlamlı generation'da tutarlı kazanç sağlıyor.

### TICoder — TICoder: A Repository-Level Code Generation Framework with Test-Driven Planning and Implementation-Aware Reuse (preprint, 2026) [arxiv:2606.08135]
Method: repo-level fonksiyon üretimi için test-driven iterative planning (LLM planner + LLM judge, eşik 90) ve dual-view (fonksiyonel + implementasyon) similarity ile callee retrieval + clustering/perplexity ile usage pattern seçimi.
Değerlendirme CoderEval (230 Python/43 proje, 230 Java/10 proje) ve DevEval (1,825 Python/115 proje) üzerinde Pass@1/3/5; backbone GPT-4o-mini, DeepSeek-V3, Qwen2.5-Coder-7B; baseline'lar RepoCoder, A3CodGen, AllianceCoder, RLCoder, RepoScope.
Findings:
- Ortalama ~%11 iyileşme; DevEval GPT-4o-mini Pass@1 %31.01 (AllianceCoder %25.26), DeepSeek-V3 %43.29.
- Ablation: generation'dan test case'leri çıkarmak Pass@1'i %10.42 düşürüyor.
Relevant Limitations:
- Planning ve generation'a verilen test case'lerin kaynağı net değil; benchmark'ın değerlendirme testleriyle aynıysa ciddi leakage.
- Baseline'lar RAG-only, agent baseline yok.
Key Takeaway:
- Test'i planning girdisi yapmak etkili, ama test'in oracle ile aynı olup olmadığı raporlanmazsa kazanç yorumlanamaz.

### AllianceCoder — What to Retrieve for Effective Retrieval-Augmented Code Generation? An Empirical Study and Beyond (preprint, 2025) [arxiv:2503.20589]
Empirical + method: repo-level RAG code generation'da hangi bilgi kaynağının (in-file context, invoked API'ler, similar code) işe yaradığını inceliyor; bulgulardan AllianceCoder'ı öneriyor (CoT ile sorguyu implementation adımlarına ayırıp API'leri semantic description matching ile retrieve ediyor).
Benchmark'lar CoderEval ve RepoExec (Python), metrik Pass@1/3/5 (executed tests); modeller GPT-4o-mini ve Gemini 1.5 Flash.
Findings:
- Context + gerçek invoked API (ConAPI) en iyi: RepoExec Pass@1 37.75 vs PureGPT 16.62.
- Similar code retrieval gürültü ekliyor, performansı %15'e kadar düşürüyor.
- AllianceCoder RepoCoder/RLCoder'ı geçiyor (Pass@1'de %20'ye kadar), ama oracle-API ConAPI'nin altında kalıyor (34.93 vs 37.75).
Relevant Limitations:
- Sadece Python, sadece 2 (ucuz) model; benchmark'lar eski, contamination riski.
- Fonksiyon-düzeyi hedef; repo sadece context olarak.
Key Takeaway:
- Repo-context generation'da "ne retrieve edilir" sorusu kritik: API bilgisi similar-code'dan değerli.

### MRG-Bench — MRG-Bench: Evaluating and Exploring the Requirements of Context for Repository-Level Code Generation (preprint, 2025) [arxiv:2508.02998]
Contextual benchmark + empirical çalışma: gerçek repolardaki fonksiyonları docstring + signature'dan, repo context'i ile üretme; Python/Java/Go.
383 sample, 22 proje (Ocak 2023 sonrası oluşturulmuş, >50 star repolar). Fonksiyonlar call-graph ile seçiliyor: repo-içi dependency'si, developer comment'i ve %100 line coverage sağlayan test'i olanlar. Üretilen fonksiyon dosyadaki yerine konuyor, projenin kendi pytest/mvn/go test'leri Docker'da koşuyor; metrik Pass@k.
Findings:
- Context'siz en iyi model Claude-3.5-Sonnet ortalama 8.6% Pass@1; in-file context ile 32.5%.
- Reasoning modeller (DeepSeek-R1, o3-mini) in-file context ile en iyi, ama hâlâ <%40.
- RAG (BM25/embedding) in-file context'ten kötü; RepoCoder Java/Go'da daha iyi (ortalama 18.1%).
- LLM-voting annotation'a göre hataların >%68'i "What" (gereksinimi anlamama), "How" değil.
Relevant Limitations:
- Hata analizi 5 LLM'in oylamasıyla yapılıyor; ground truth koda göre What/How etiketi — LLM-in-the-measurement.
- Sadece 22 proje; tek fonksiyon doldurma, repo üretimi değil.
Key Takeaway:
- Proje testlerini function-level coverage ile eşlemek, repo-context-gen için temiz bir oracle; darboğaz spesifikasyonun anlaşılması.

### RepoST — RepoST: Scalable Repository-Level Coding Environment Construction with Sandbox Testing (preprint, 2025) [arxiv:2503.07358]
Contextual benchmark + training-data + method: repo-level function generation için otomatik executable environment inşası. Tüm repoyu build etmek yerine hedef fonksiyon ve local dependency'leri ayrı bir script'e "sandbox"lanıyor, test'ler LLM ile üretiliyor.
Pipeline: repo/fonksiyon seçimi → sandboxing → GPT-4o ile test üretimi → iteratif hata düzeltme + branch coverage artırma → AST/execution/LLM tabanlı functionality-equivalence ve test-correctness kontrolü. RepoST-Train: 7,415 fonksiyon/824 repo; RepoST-Eval: 296 fonksiyon/99 repo; ortalama 8.2 test, %100 branch coverage (eval). Python. Model, orijinal repo context'i ile fonksiyonu üretiyor; Pass@1.
Findings:
- 12 model içinde en iyi GPT-4o 39.53 Pass@1; en iyi open-source (DS-R1-Qwen-32B) 5.07 geride.
- RepoST-Train ile rejection-sampling fine-tuning Qwen2.5-Coder'ı HumanEval'de +5.5, RepoEval'de +3.5 Pass@1 iyileştiriyor.
- Human study: GPT-4o equivalence check'i geçen 13/20'nin hepsi insanla uyumlu; öğrenciler örneklerin %81.5'ini çözebiliyor.
Relevant Limitations:
- Test'ler ve kalite kontrol aynı LLM ailesinden (GPT-4o); sandbox sonrası fonksiyonun orijinaliyle eşdeğerliği LLM'e emanet.
- Sadece Python, sadece "oracle" context; agent setting'i yok.
Key Takeaway:
- Tam repo build yerine function-level sandbox, execution feedback'i ölçeklemenin ucuz yolu — ama integration davranışı kaybolur.

### RepoMasterEval — RepoMasterEval: Evaluating Code Completion via Real-World Repositories (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00304]
Benchmark çalışması (+ 10 model üzerinde empirical değerlendirme): real-world repo'lardan, test suite'i olan dosyalarda bir code snippet mask'lenip modelden tamamlaması isteniyor. Not: open full text bulunamadı; bu not yalnızca abstract'a (ve citing paper'lardaki özet tablolara) dayanıyor.
Input: mask'lenmiş dosya + repo context (NL açıklama yok, fonksiyon ortası/blok seviyesi completion); output: eksik snippet. Değerlendirme repo'nun kendi test'leriyle; test kalitesi mutation testing ile ölçülüp düşük mutation score'lu suite'lere manuel test ekleniyor. Citing paper'lara göre 6 repo, 2 dil (muhtemelen Python ve TypeScript — doğrulanmalı).
Findings:
- Test augmentation benchmark doğruluğu için kritik (abstract'ta sayı yok).
- 10 SOTA model arasında real-world senaryoda varyans raporlanıyor; endüstriyel deployment'ta skorun pratik model performansıyla yüksek korelasyonlu olduğu iddia ediliyor.
Relevant Limitations:
- Ölçek küçük (citing tabloya göre 6 repo); contamination riski yüksek (public repo'lar).
- Ground-truth snippet ve mevcut test'lere bağlı white-box setup; ama execution-based olduğu için similarity'den daha az reference-coupled.
- Somut sayılar full text olmadan çıkarılamadı.
Key Takeaway:
- Mutation testing ile test yeterliliğini ölçüp güçlendirmek, repo-context benchmark'larında false positive'leri azaltmanın ucuz bir yolu.

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

### LAIL — Large Language Model-Aware In-Context Learning for Code Generation (TOSEM 2025, 2025) [doi:10.1145/3715908]
Method çalışması (peripheral): ICL demonstration seçimi için LLM'in kendisini etiketleyici olarak kullanan model-aware retriever. Not: open full text bulunamadı; not abstract'a dayanıyor.
LLM, aday örnekleri bir requirement için positive/negative olarak etiketliyor; bu etiketlerle contrastive bir retriever eğitiliyor ve inference'ta seçilen örnekler prompt'a ekleniyor. Ana değerlendirme function-level (MBJP, MBPP, MBCPP; CodeGen-Multi-16B, CodeLlama-34B, Text-davinci-003), ayrıca repository-level DevEval üzerinde Pass@1/3/5 (CodeLlama-7B) ve human evaluation.
Findings:
- DevEval'de SOTA ICL baseline'larına göre Pass@1/3/5'te +10.04 / +8.12 / +4.63 puan (CodeLlama-7B).
- Function-level'da MBJP/MBPP/MBCPP Pass@1'de +1.2–11.6 puan kazanç; retriever LLM'ler ve dataset'ler arası transfer ediliyor.
Relevant Limitations:
- Repo-level kısmı tek model (CodeLlama-7B) ve tek benchmark; mutlak skorlar abstract'ta yok.
- DevEval'in repo context'i nasıl verildiği (retrieval mı, sadece ICL örneği mi) abstract'tan anlaşılmıyor.
Key Takeaway:
- Demonstration seçiminin repo-level görevlerde function-level'dan daha büyük fark yaratabileceğine dair bir sinyal; full text ile doğrulanmalı.

### What Makes ICL Examples Effective — What Makes In-Context Examples Effective for Code Generation? (ISSTA 2026, 2026) [arxiv:2508.06414]
Empirical çalışma (peripheral): ICL code example'larının hangi özelliklerinin (solution insight, context bilgisi, identifier naming, formatting) code generation'ı etkilediğini kontrollü deneylerle inceliyor.
İki benchmark: LiveCodeBench LeetCode (362 soru, Python+Java) ve repository-level DevEval (1,427 task, Python). DevEval için repodaki fonksiyon/sınıflar retrieval DB; BM25 ve 3 embedding retriever, mutation operatörleri (identifier obfuscation vb.), naming style varyantları. Modeller: GPT-4o-mini, Qwen2.5-7B/32B, DeepSeek-Coder-V2-Lite; metrik Pass@1 (test execution), istatistiksel testler.
Findings:
- DevEval'de repo-retrieved ICL güçlü etki: Qwen-32B zero-shot 15.21 → gist-large 36.79; LeetCode'da benzer soru/çözüm eklemek anlamlı fayda sağlamıyor.
- Namespace bilgisi eklemek tüm modellerde DevEval'i artırıyor (ör. Qwen-32B BM25 26.70 → 30.34).
- Identifier obfuscation (FVE) DevEval'de GPT-4o-mini 37.91 → 25.58.
Relevant Limitations:
- Tek repo-level benchmark, sadece Python; küçük/orta modeller.
- Ground-truth'u testleri geçemeyen ~400 DevEval task çıkarılmış; seçim etkisi raporlanmamış.
Key Takeaway:
- Repo-context generation'da "hangi context" sorusunda identifier/namespace bilgisi örnek mantığından daha belirleyici.

### FeatLens — FeatLens: Feature-Guided Dynamic Code Graph Construction and Retrieval for Repository-Level Code Generation (preprint, 2026) [arxiv:2609.26480]
Method. Repo içinde hedef fonksiyonu üretirken bağımlılıkları retrieve etmek için feature index (NL feature açıklaması → fonksiyon entity'leri) + task-specific seed graph + personalized PageRank ile kompakt reasoning graph kuruyor; retrieval sırasında LLM token'ı yok. DevEval (90 repo, Python) üzerinde Pass@1 ve DIR@1 (dependency invocation rate); EvoCodeBench (5 repo) sadece retrieval (DR@k) için, çünkü runtime yok. Modeller: DeepSeek-V3.2, GPT-5-mini; baseline'lar BM25, UniXcoder RAG, RepoGraph, CodexGraph.
Findings:
- DR@15: 0.501 (DevEval), 0.460 (EvoCodeBench); CodexGraph 0.430.
- DevEval Pass@1: 42.24% (DeepSeek-V3.2), 55.03% (GPT-5-mini) — CodexGraph'a göre GPT-5-mini'de hafif düşük (56.35%), UniXcoder RAG ile yakın.
- Graph node'ları %61, edge'ler %86, toplam token %45.9 azalıyor.
Relevant Limitations:
- Fonksiyonel kazanç marjinal; asıl kazanç retrieval recall'da ve kod uzunluğunda.
- Tek dil (Python), EvoCodeBench'te execution yok; DevEval alt kümesi filtrelenmiş (dependency annotation'ı tam olanlar).
Key Takeaway:
- Contextual tier için tipik bir retrieval method'u; test-based Pass@1 raporlanıyor ama ölçülen asıl şey dependency reuse.

### PlayCoder — PlayCoder: Making LLM-Generated GUI Code Playable (preprint, 2026) [arxiv:2604.19742]
Benchmark + method. PlayEval: 43 GUI uygulaması (Python/JS/TS; oyunlar, emulator, desktop widget'lar), repo içinde fonksiyon üretimi: input = function signature + LLM-üretimi (GPT-4o-mini) requirement + repo context + düzenlenecek dosya. Değerlendirme zinciri Exec@k → Pass@k (LLM-generated unit test'ler, orijinal testlerin coverage'ı düşük: %47 line) → Play@k (PlayTester: screenshot + mouse/keyboard ile oynayan LLM agent). PlayCoder = PlayDeveloper + PlayTester + PlayRefiner repair loop'u.
Findings:
- 10 LLM'de Play@3 tek hanede; en iyi base model Claude-Sonnet-4 Python'da Play@3 9.9%.
- PlayCoder: Claude-Sonnet-4 ile 36.8% Exec@3 / 20.3% Play@3; GPT-5-mini ile 26.8% / 9.8% (DeepCode 17.9% / 6.4%).
- PlayTester insan yargısına karşı %16 false-negative, %5 false-positive (Krippendorff α=0.79).
Relevant Limitations:
- Requirement'lar ve unit test'ler LLM tarafından reference implementasyondan türetiliyor; verdict de LLM agent → ölçümün büyük kısmı LLM içinde, white-box coupling var.
- Sayılar tutarsız: 43 uygulama vs Fig. 2'de "4,159 instances, 35 repositories".
Key Takeaway:
- GUI/game kodunda unit test ile davranışsal doğruluk arasındaki uçurum büyük; interaktif agent-based oracle faydalı ama güvenilirliği (%16 FN) raporlanmalı.

### ReCUBE — ReCUBE: Evaluating Repository-Level Context Utilization in Code Generation (preprint, 2026) [arxiv:2603.25770]
Benchmark + method. Gerçek repo'da maskelenmiş bir Python dosyasını, kalan kaynak dosyalar + dependency spec + dokümantasyonla yeniden inşa etme (prompt-free: NL task tanımı yok). 20 repo (Ocak 2025 sonrası oluşturulmuş, contamination'a karşı), functional subset'lere bölünmüş, 366 instance; RECUBE-LARGE 6 repo / 138 instance, 338K token'a kadar context. 10,785 usage-aware unit test (Claude Opus 4.1 üretimi, gold'da geçtiği Docker'da doğrulanmış; %58.7 external cross-file, %41.3 internal). Metrikler: Strict Pass Rate, Average Pass Rate. Ayarlar: full-context, +CoT, mini-SWE-agent, agent + CCE (caller-centric dependency graph toolkit).
Findings:
- En iyi model GPT-5 full-context'te yalnızca 37.57% SPR.
- Agentic exploration dar context'te faydalı, context büyüdükçe avantajı kayboluyor/tersine dönüyor.
- CCE: full-context'e göre +5.79%, vanilla agent'a göre +7.56% SPR.
- Hard task'larda caller coverage ile APR arasında anlamlı korelasyon (ρ=+0.408).
Relevant Limitations:
- Test'ler LLM üretimi ve gold dosyadan türetilmiş; internal test'ler private fonksiyon/implementasyon detayını kontrol ettiği için alternatif tasarımları cezalandırır (white-box coupling).
- Tek dil (Python), 20 repo.
Key Takeaway:
- File-level reconstruction, "repo context'i kullanma" yeteneğini NL spec'ten ayrıştırmanın temiz bir yolu; external vs internal test ayrımı reference coupling'i ölçmek için kullanılabilir.

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

### CoderUJB — CoderUJB: An Executable and Unified Java Benchmark for Practical Programming Scenarios (ISSTA 2024, 2024) [doi:10.1145/3650212.3652115]
Benchmark + empirical study: 17 Defects4J Java projesinden 2,239 soru, 5 task (FCG 238, code-based test gen 140, issue-based test gen 451, APR 470, defect detection 940). Kapsam için ilgili kısım FCG: fonksiyon, class context'i (import/field/signature) + docstring verilerek üretiliyor, gerçek projeye yerleştirilip ilgili testlerle (ort. ~162 test/fonksiyon) çalıştırılıyor; pass-syntax/compile/all@k, n=20.
Findings:
- FCG pass-all@1: GPT-4 30.52, GPT-3.5 23.37, CodeLlama-34B 22.82 (HumanEval'deki 67/45'e kıyasla çok düşük).
- Program context prompt FCG'de few-shot'a göre daha iyi.
- Instruction tuning bazen zarar veriyor (CodeLlama-Instruct-34B FCG 1.89).
Relevant Limitations:
- Context tek class ile sınırlı; cross-file dependency açıkça modellenmiyor.
- Sadece 17 proje, hepsi Defects4J → yüksek contamination riski.
- Karışık benchmark; FCG sadece 238 soru.
Key Takeaway:
- "Project-runnable" yürütme ile contextual generation değerlendirmesinin Java örneği; CoderEval'in Java tarafını genişletiyor.

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

### CoCoGen — Iterative Refinement of Project-Level Code Context for Precise Code Generation with Compiler Feedback (preprint, 2024) [arxiv:2403.16792]
Method paper: repo-bağımlı fonksiyon üretiminde compiler feedback ile hataları tespit edip ilgili project context'i geri getirerek iteratif düzeltme.
Proje AST'den class/function/variable DB'si çıkarılıyor; static analysis (pylint tarzı) hatası ChatGPT ile SQL query'ye çevrilip structural search yapılıyor, ayrıca dense retrieval ile semantic search. Değerlendirme CoderEval-Python'un class/file/project-runnable split'lerinde (55/68/23 task), Pass@1/5/10 (n=20); modeller GPT-3.5-Turbo ve CodeLlama-13B. Ek olarak HumanEval, MBPP, CrossCodeEval appendix'te.
Findings:
- GPT-3.5 ile project-runnable Pass@10: Direct 13.04 → RepoCoder 21.74 → CoCoGen 39.13.
- Ablation: CoCoGen Pass@10 46.58 vs RepoCoder 36.30; compiler feedback tek başına sınırlı, context retrieval ile birlikte anlamlı.
- UNDEF hataları 1 iterasyonda 5,133 → 1,042; ön analizde project-level hataların %64'ü UNDEF+API.
- Pass@1'de RepoCoder bazı split'lerde daha iyi (ör. class-runnable 35.45 vs 28.00).
Relevant Limitations:
- Sadece compile-time hatalar hedefleniyor; FUNC (runtime/semantik) hatalara dokunmuyor.
- Değerlendirme küçük: project-runnable sadece 23 task, tek dil (Python).
- SQL sentezinde de LLM kullanılıyor; maliyet/latency raporu sınırlı.
Key Takeaway:
- Statik analiz çıktısı "hangi context eksik" sinyalini verir; retrieval'ı error-driven yapmak similarity-driven RAG'den daha isabetli.

### LLM Hallucinations in Practical Code Generation — LLM Hallucinations in Practical Code Generation: Phenomena, Mechanism, and Mitigation (preprint, 2024) [arxiv:2409.20550]
Empirical study: repo-bağımlı fonksiyon üretiminde LLM hallucination taxonomy'si, nedenleri ve basit RAG mitigation.
CoderEval-Python 230 task; 6 model (ChatGPT/GPT-3.5, CodeGen-350M, PanGu-α-2.6B, DeepSeekCoder-6.7B, CodeLlama-7B-Python, StarCoder2-7B), task başına 10 sample. Manuel open coding (önce %10, sonra 3 annotator). Mitigation: RepoCoder tarzı sliding-window + Jaccard BOW retrieval, Pass@1.
Findings:
- 3 ana kategori / 8 alt tip: Task Requirement Conflicts %43.53, Factual Knowledge Conflicts %31.91, Project Context Conflicts %24.56.
- Project context içinde Dependency Conflicts %11.26, Non-code Resource Conflicts %12.36 (config, data vb.).
- RAG tüm modellerde Pass@1'i artırıyor ama mutlak değerler çok düşük: ChatGPT 10.40 → 12.61, diğerleri %1-5 bandı.
Relevant Limitations:
- Pass@1 değerleri (ör. %0.04) raporlanan protokolde tuhaf derecede düşük; küçük/eski modeller baskın.
- Tek benchmark, tek dil; taxonomy manuel ve ground-truth'a göre farklılık yorumlanıyor.
Key Takeaway:
- Repo-level üretimde hataların yaklaşık dörtte biri doğrudan project context'le ilgili; context retrieval tek başına task-requirement hatalarını çözmüyor.

### RepoExec — On the Impacts of Contexts on Repository-Level Code Generation (preprint, 2024) [arxiv:2406.11927]
Benchmark + empirical: cross-file dependency'lere bağlı Python fonksiyon üretimi, executable test ve dependency kullanımı ölçümü.
355 fonksiyon (unit-test generation literatüründeki çalıştırılabilir repolardan); dependency'ler pydepcall ile static call graph'tan çıkarılıyor; prompt'ta full/medium/small context (implementasyon/docstring/signature). Testler CodeLlama-13B ile üretilip ground-truth'a karşı assertion fixer + 10 kez çalıştırma ile doğrulanıyor, GPT-3.5 ile coverage enhancement (line coverage %96.25). Metrikler: Pass@k ve yeni Dependency Invocation Rate (DIR). 18 model; multi-round debugging ve DepIT instruction-tuning dataset (1,555 repo'dan ~150K örnek).
Findings:
- Full context en iyi; small context medium'dan iyi (BasePrompt formatının few-shot gibi algılanması).
- En yüksek Pass@1: DeepSeek-R1 %42.57; GPT-4o %37.14 ama DIR %81.43.
- Pretrained modeller Pass@k'da, instruction-tuned modeller DIR'de daha iyi; pretrained'lar dependency'i yeniden implemente ediyor.
- 3 tur debugging GPT-3.5'te Pass@1'de "%10'un üzerinde" iyileşme (mutlak/göreli olduğu net değil), CodeLlama'da etkisiz; DepIT DIR'i %70+ seviyesine çıkarıyor, Pass@1 kazancı ~%1.
Relevant Limitations:
- Testler LLM tarafından üretilip ground-truth çıktısına göre düzeltiliyor: oracle referans implementasyona tam bağlı (differential), farklı ama doğru davranışı cezalandırabilir.
- Sadece tek seviye dependency; 355 örnek, tek dil.
- DIR "kullanılması gereken" dependency'yi referansa göre tanımlıyor; alternatif tasarım cezalanıyor.
Key Takeaway:
- Functional correctness tek başına yeterli değil; context kullanımını ölçen ikinci bir eksen (DIR) repo-level değerlendirmede anlamlı.

### Repoformer — Repoformer: Selective Retrieval for Repository-Level Code Completion (ICML 2024, 2024) [arxiv:2403.10059]
Method: code LM'in retrieval'ın faydalı olup olmayacağını kendi değerlendirip seçici RAG yapması (self-selective RAG).
StarCoderBase 1B/3B/7B/16B, Stack'ten 18K Python repo'dan self-supervised etiketli veri (240K chunk + 120K function completion) ile fine-tune; <eof> sonrası <cc> token'ı retrieval kararını veriyor. Değerlendirme: RepoEval (line/API/function, 32 repo), CrossCodeEval ve yeni CrossCodeLongEval; EM/ES ve RepoEval function completion için unit test pass rate (UT).
Findings:
- Standart RAG'de retrieval'ların %80'e kadarı fayda sağlamıyor, bir kısmı zarar veriyor.
- Repoformer-3B çoğu metrikte StarCoderBase-7B'yi geçiyor; 16B, StarCoder'ı ortalama ~%3 geçiyor (function UT 44.18 vs 42.86 always-retrieve).
- Selective retrieval online serving'de %70'e kadar hızlanma.
Relevant Limitations:
- Executable değerlendirme sadece RepoEval function completion alt kümesinde (küçük repolar); geri kalanı similarity.
- Eğitim etiketi ES bazlı; function completion'da UT için kalibrasyon zayıf olduğu belirtiliyor.
Key Takeaway:
- Contextual tier için "ne zaman context getirmeli" sorusu kendi başına bir optimizasyon ekseni; efficiency bu literatürde az raporlanıyor.

### Typed Holes / ChatLSP — Statically Contextualizing Large Language Models with Typed Holes (OOPSLA 2024, 2024) [arxiv:2409.00921]
Method + küçük benchmark: language server'dan typed hole'un beklenen tipi, ilgili type definition'lar ve typing context'ten header'lar alınarak LLM prompt'unu statik olarak zenginleştirme; static error feedback ile düzeltme turları.
Hazel (low-resource fonksiyonel dil) ve TypeScript. MVUBench: 5 MVU web app (Todo, Room Booking, Emoji Painter, Playlist, Password Checker), her biri simüle repo + 10-15 unit test, contamination'a karşı sıfırdan yazılmış. Görev: update fonksiyonunu doldurmak. 8 ablation × 5 app × 20 trial = 320 trial; GPT-4-0613 ve StarCoder2-15B; baseline'lar no-context, exhaustive retrieval, vector retrieval (Ada embedding).
Findings:
- Type definition'lar kritik; header'lar types ile birlikte test başarısını ~3 kat artırıyor.
- Error rounds types varken ×4 (headers olmadan) ve ×1.5 (types+headers) etki.
- Vector retrieval isim çakışmalı confounder chunk'lar yüzünden kötü; exhaustive retrieval biraz daha iyi ama istatistiksel ayrım yok.
Relevant Limitations:
- Ölçek çok küçük: 5 program, ~1000 satırlık sentetik kod tabanı; TypeScript header retrieval manuel simüle edilmiş.
- Tek fonksiyon doldurma; gerçek repo çeşitliliği yok.
Key Takeaway:
- Scope/type-aware statik context, lexical RAG'e göre token-verimli ve confounder'lara dayanıklı; LSP'ye AI odaklı uzantı (ChatLSP) önerisi ilginç.

### ToolGen — Teaching Code LLMs to Use Autocompletion Tools in Repository-Level Code Generation (preprint, 2024) [arxiv:2401.06391]
Method: fine-tune edilen code LLM'e <COMP> trigger token'ı öğretilip decoding sırasında Jedi autocompletion çağrılması ve öneriler arasından constrained greedy seçim.
Python; CodeGPT-124M, CodeT5-220M, CodeLlama-7B. 671 repo'luk benchmark'ta BLEU/CodeBLEU/ES/EM + yeni Dependency Coverage ve Static Validity Rate; execution için CoderEval 176 task Pass@1.
Findings:
- Dependency Coverage +%31.4-39.1, Static Validity Rate +%44.9-57.7.
- CoderEval Pass@1: CodeLlama 6.8% → 8.5% (12 → 15 fonksiyon), CodeT5 4.0 → 5.1, CodeGPT değişmedi; RepoCoder-llama 19 fonksiyon ile ToolGen'i geçiyor.
- Fonksiyon başına latency 0.63-2.34 s.
Relevant Limitations:
- Execution kazanımları birkaç fonksiyon düzeyinde; "%40 artış" 2 ek fonksiyona karşılık geliyor.
- Küçük/eski modeller; ana benchmark similarity tabanlı.
Key Takeaway:
- Tool-in-decoding statik geçerliliği ciddi artırıyor ama fonksiyonel doğruluğa yansıması sınırlı; RAG ile tamamlayıcı.

### ObfusEval — Unseen Horizons: Unveiling the Real Capability of LLM Code Generation Beyond the Familiar (preprint, 2024) [arxiv:2412.08109]
Benchmark + empirical: contamination'a karşı açıklama, kod ve context dependency'leri obfuscate edilmiş repo-bağımlı C fonksiyon üretimi.
5 C projesi (redis, libvips, lvgl, libgit2, fluent-bit), May-Dec 2023 PR'larında değişen ve testle kapsanan 1,354 fonksiyon; açıklamalar 7 kıdemli mühendis tarafından yeniden yazılmış. Obfuscation seviyeleri: symbol, structure, semantic. Gerekli dependency'ler + ilgisiz dependency'ler prompt'a ekleniyor. Üretilen fonksiyon projede yerine konup derleniyor ve resmi test suite'i çalıştırılıyor; CPR ve TPR (pass@5). Modeller: GPT-3.5-1106, GPT-4-1106, GPT-4-0125, DeepSeek-Coder-V2.
Findings:
- Obfuscation sonrası TPR ortalama düşüşü %15.3-62.5.
- Completion senaryosunda symbol obfuscation ortalama TPR'yi %20.0 → %15.2 düşürüyor (-%24).
- Testleri geçen kodda bile robustness gibi non-functional sorunlar var.
Relevant Limitations:
- Mutlak başarı düşük ve projeler arası varyans yüksek (bazı split'lerde 10-20 örnek).
- Obfuscation fonksiyonun doğal dağılımını değiştiriyor; düşüşün bir kısmı okunabilirlik kaybı olabilir, contamination etkisinden ayrıştırılmıyor.
Key Takeaway:
- Contamination kontrolü için tarih filtresi yetersiz; tekrarlanabilir obfuscation benchmark'ı "yenileme" stratejisi olarak kullanılabilir.

### CCCI — CCCI: Code Completion with Contextual Information for Complex Data Transfer Tasks Using Large Language Models (preprint, 2025) [arxiv:2503.23231]
Method: endüstriyel bir codebase'deki data transfer script'lerini, DB tablo ilişkileri, object model ve library bilgisini retrieve edip prompt'a ekleyerek LLM'e yeniden ürettiren context-aware completion.
819 operasyonel script'ten çıkarılmış 289 Java snippet; metrikler BLEU-4, CodeBLEU, Edit Similarity ve Build Pass (compile + test case ile fonksiyonu çağırıp output kontrolü). Altı model: GPT-4o, Gemini-pro-1.5, Claude-3.5-haiku, Llama-3.1-405b, Qwen-2.5-coder-32b, DeepSeek-3.
Findings:
- GPT-4o: Build Pass %0 → %49.1, CodeBLEU 16.9 → 41.0.
- En iyi Build Pass Gemini-pro-1.5 %64.0; Claude-3.5-haiku %26.0.
Relevant Limitations:
- Ağırlık similarity metriklerinde; test aşaması "simply check output" düzeyinde, test kapsamı raporlanmamış.
- Kapalı, tek şirket datası; replikasyon mümkün değil.
Key Takeaway:
- Proje-özel şema/model bağlamı olmadan endüstriyel kodda hiçbir üretim derlenmiyor; retrieval edilen repo bağlamı contextual tier'in temel gereksinimi.

### CodeIF-Bench — CodeIF-Bench: Evaluating Instruction-Following Capabilities of Large Language Models in Interactive Code Generation (preprint, 2025) [arxiv:2503.22688]
Benchmark: multi-turn interactive code generation'da instruction following. 124 task (50 MBPP, 74 DevEval repo-level), her biri için 7–9 "verifiable instruction" ve bunlara ait unit test'ler (GPT-4o üretimi, insan review + execution ile doğrulanmış).
Static ve Dynamic Conversation ayarları; metrikler IA, CA, IFR, CIF. Modeller: GPT-4o, Claude-3.5-Sonnet, DeepSeek-V3, Qwen2.5-Coder-7/14/32B. Bütçe nedeniyle cross-file L-3 (14 task) deneylerden çıkarılmış; sadece L-1 (standalone) ve L-2 (intra-file, ~9.6K token bağlam) raporlanıyor.
Findings:
- Repo bağlamı eklenince (L-2) CA ve IA belirgin düşüyor, IFR artıyor.
- Dynamic L-2'de CIF: DeepSeek-V3 54.0, Claude-3.5-Sonnet 47.8, GPT-4o 40.0, Qwen2.5-Coder-32B 13.8.
Relevant Limitations:
- Repo-level kısım 40 intra-file task; asıl cross-file durum değerlendirilmemiş.
- Instruction ve testler LLM üretimi.
Key Takeaway:
- Uzun repo bağlamı + uzun diyalog, instruction forgetting'i hızlandırıyor; context management önemli bir araştırma yönü.

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

### OpenCoder — Beyond "What to Retrieve": Uncertainty in Retrieval-Augmented Code Generation (preprint, 2026) [arxiv:2607.24884]
Method: repo-level function generation için similar code, repository context ve project API kaynaklarının her biri için uncertainty tahmin edip evidence filtreleme, generation, verification ve repair'i buna göre yönlendiren RAG framework'ü.
Değerlendirme: 32 task'lık RepoExec-inline (14'ten genişletilmiş) ve context-limited 10 ExecRepoBench task'ı; GPT ve Gemini backend, 5-candidate frozen protokol, Pass@k ve selected-output correctness; API retrieval için 13 task'ta macro F1.
Findings:
- GPT'de selected-output correctness %56.25 → %78.13 (Baseline RAG'e göre), ama RAG + Verify/Repair kontrolüyle eşit.
- Gemini'de fark istatistiksel olarak anlamlı değil; tüm Pass@k CI'ları sıfırı içeriyor.
- ExecRepoBench'te kontrol, OpenCoder'ı açıkça geçiyor (Gemini 100 vs 80).
- Target-aware API refinement macro API F1'i %43.4'ten %64.8'e çıkarıyor.
Relevant Limitations:
- Ölçek çok küçük (32+10 task), sonuçlar backend'e bağlı; kazanç büyük ölçüde verify/repair'den geliyor.
Key Takeaway:
- Dürüst negatif sonuçlar: uncertainty modellemenin katkısı, execution-based verify/repair'in katkısından ayrılamıyor.

### CodeMEM — CodeMEM: AST-Guided Adaptive Memory for Repository-Level Iterative Code Generation (preprint, 2026) [arxiv:2601.02868]
Method: multi-turn repo-level function generation'da AST-guided Code Context Memory (repo context'i dinamik güncelleme) ve Code Session Memory (önceki düzeltmelerin unutulmasını AST ile tespit) öneriyor.
Değerlendirme: CodeIF-Bench L-2 (40 dialog, 360 test edilebilir instruction; IA, CA, forgetting rate IFR) ve 230 Python task'lık CoderEval'in verbal feedback ile 5 turlu versiyonu (Pass@1). Backbone DeepSeek-V3.2, greedy; baseline'lar Full-Context, MemGPT, Mem0, A-Mem, RLCoder.
Findings:
- CodeIF-Bench ortalama IA 46.1 (en iyi baseline 41.1), CA 42.8 (38.4).
- CoderEval Pass@1 5. turda 55.7 vs Full-Context 50.9; FC'nin 5. turdaki skoruna 3. turda ulaşıyor.
- Ablation'da AST selector çıkarılınca IA −4.4.
Relevant Limitations:
- Tek backbone ve tek dil (Python); CodeIF-Bench'te sadece 40 dialog.
- Multi-turn feedback simülasyonu çok basit ("cevabın yanlış").
Key Takeaway:
- Contextual tier'da iteratif etkileşim ve bellek yönetimi, retrieval kadar önemli bir boyut.

### Hydra — Do Not Treat Code as Natural Language: Implications for Repository-Level Code Generation and Beyond (FSE 2026, 2026) [arxiv:2602.11671]
Method: repository-level function generation için RAG retriever; kodu chunk'lanmış metin yerine yapısal birim (function/class/variable) ağacı olarak indeksliyor.
Structure-aware indexing + fine-tune edilmiş hafif dependency-aware retriever (DAR, threshold 0.25) + BM25 usage örnekleri (hybrid). Benchmark: RepoExec (355 problem) ve DevEval (1,825 sample, 117 repo), Python; metrik Pass@1/3/5 (executable tests) ve Dependency Invocation Rate. Generator: Qwen2.5-Coder 1.5B/7B, GPT-4.1-mini.
Findings:
- GPT-4.1-mini: RepoExec Pass@1 43.55 (RepoFormer 39.15), DevEval 31.91 (30.89).
- Qwen-7B: DevEval 17.27 vs RLCoder 13.00; 1.5B+Hydra bazı durumlarda 7B baseline'ları geçiyor.
- NameError/TypeError/AttributeError (hallucinated dependency) belirgin şekilde azalıyor, AssertionError oranı artıyor.
Relevant Limitations:
- Sadece Python ve tek fonksiyon üretimi; RepoExec testleri otomatik üretilmiş (benchmark'tan miras).
- DevEval'de kazanç GPT-4.1-mini için küçük (~1 puan).
Key Takeaway:
- Contextual tier için: gerçek dependency'leri getirmek similarity retrieval'dan daha değerli; hata tipi analizi bunun hallucination'ı azalttığını gösteriyor.

### DyRetriever — Effective and Efficient Context Retrieval via Partial Dependency Graph for Repository-Level Code Generation (ASE 2026, 2026) [arxiv:2608.01927]
Method: repository-level function generation için LLM'in entry-point fonksiyonlardan başlayıp dependency graph üzerinde multi-hop dolaşarak context topladığı retriever; global graph yerine ihtiyaç anında kısmi graph kuruluyor.
DyRetriever + similarity retrieval = DyCoder. Benchmark: CoderEval-Python (230) ve DevEval (1,825; 209 ortamda çalışmayan instance failure sayılmış). Metrik Pass@1 (executable tests), runtime ve token. Modeller: Qwen3-Coder-30B, DeepSeek-v3.2, GPT-4o-mini. Hedef fonksiyon ve test dosyaları maskelenmiş (RepoScope'un leakage sorunu düzeltilmiş).
Findings:
- Ortalama Pass@1: CoderEval 46.96 (RepoScope 40.72), DevEval 40.84 (38.00).
- RepoScope'tan 7.4× hızlı; ama similarity tabanlılara göre 1.95–2.43× daha fazla token.
- DyRetriever context'i farklı similarity retriever'larla birleştirince +7.5–31% relatif kazanç.
Relevant Limitations:
- Sadece Python, tek fonksiyon; DevEval'de 209 instance'ın kasıtlı failure sayılması mutlak sayıları düşürüyor.
- LLM retrieval'ın doğruluğu (yanlış dependency) ayrıca ölçülmemiş.
Key Takeaway:
- Contextual tier'de leakage kontrolü (test/hedef maskesi) karşılaştırmaların geçerliliği için kritik; önceki sonuçların bir kısmı şişik olabilir.

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
