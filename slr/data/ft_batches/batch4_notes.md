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
