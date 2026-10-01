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
