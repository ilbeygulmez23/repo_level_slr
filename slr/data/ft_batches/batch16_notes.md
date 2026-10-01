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
