### PtrTrans — Project-Level C-to-Rust Translation via Pointer Knowledge Graphs (PACMSE, 2026) [doi:10.1145/3808169]
Method çalışması: C projesini project-level olarak safe/idiomatic Rust'a çeviren LLM tabanlı yaklaşım (PtrTrans). Not: full text elde edilemedi; bu not yalnızca abstract'a dayanıyor.
Mevcut LLM yaklaşımları projeyi call graph'a göre fonksiyon birimlerine bölüp bottom-up çeviriyor; bu unit-by-unit paradigma pointer'ların global kullanımını göremiyor. PtrTrans, code dependency graph'ı iki tür pointer semantiğiyle zenginleştiren bir C-to-Rust Pointer Knowledge Graph kuruyor: (i) points-to flow ve struct etkileşimlerini üst seviye soyutlamaya taşıyan pointer usage bilgisi, (ii) ownership, mutability, nullability, lifetime gibi Rust-oriented annotation'lar. KG, çeviri sırasında LLM'e global context olarak veriliyor. Benchmark projelerinin sayısı/boyutu, kullanılan LLM'ler ve test setup'ı abstract'ta raporlanmamış.
Findings:
- Rule-based (c2rust tarzı) ve klasik LLM-based yöntemlere göre translated Rust'taki unsafe kullanım %99.9 azalıyor.
- Fuzzing-enhanced LLM yaklaşımlarına göre functional correctness %29.3 daha yüksek (metrik tanımı abstract'ta yok; muhtemelen test pass rate).
Relevant Limitations:
- Full text olmadan proje ölçeği, bağımsız repo sayısı ve test oracle'ının (orijinal C test suite mi, generated test mi) ne olduğu bilinmiyor.
- "Unsafe azaltma" metriği idiomaticity için proxy; unsafe'i kaldırıp davranışı bozan çeviriler correctness metriğiyle ayrıca yakalanmalı.
- Hand-off yapılandırılmış (KG annotation'ları) — bu olumlu, ama KG kurulumunun statik analiz maliyeti belirsiz.
Key Takeaway:
- Repo translation'da global, yapılandırılmış semantik artefakt (pointer KG) unit-by-unit çevirinin temel zaafını kapatıyor; survey'de "structured hand-off" argümanı için iyi örnek.
- Full text alınıp ölçek ve oracle doğrulanmalı.

### SimulatorCoder — SimulatorCoder: DNN Accelerator Simulator Code Generation and Optimization Via Large Language Models (ICASSP, 2026) [doi:10.1109/icassp55912.2026.11463415]
Method çalışması (kısa, 4 sayfalık ICASSP paper): NL functional description + architecture spec'ten DNN accelerator simulator kodu üreten LLM agent. Borderline core: çıktı SCALE-Sim'in işlevsel eşdeğeri modüler bir simulator.
Simulator üç modüle ayrılıyor (mapping, storage, interconnection network); function → class → module seviyesinde incremental üretim. Prompt'lar ICL + CoT ile domain bilgisi taşıyor; feedback-verification loop compile + execute edip hatayı LLM'e geri veriyor (max attempt sınırlı). Değerlendirme: SCALE-Sim'den manuel çıkarılan spec'lerle 138 task, Python, DeepSeek-V3 ve GPT-4o. Metrik "self-defined" Pass@k = c/n (task başına k denemeden biri tüm test case'leri geçerse başarı). Ayrıca üretilen simulator 8 workload'da (NCF, ResNet50, Transformer vb.) cycle count ve runtime açısından SCALE-Sim ile karşılaştırılıyor.
Findings:
- ICL+CoT en iyisi: DeepSeek-V3 pass@1 %91.30 / pass@5 %96.38; GPT-4o pass@1 %91.30 / pass@5 %92.75. Zero-shot pass@1 ~%81–83.
- Cycle count hatası 8 workload'da <%1 (NCF, AlphaGo Zero, YOLOv2'de %0.00; ResNet50 %0.85).
- Üretilen simulator çoğu workload'da SCALE-Sim'den daha hızlı çalışıyor.
Relevant Limitations:
- Spec'ler SCALE-Sim'den reverse-engineer edilmiş ve oracle da SCALE-Sim: değerlendirme referans implementasyona sıkı bağlı; SCALE-Sim büyük ihtimalle pretraining verisinde (contamination).
- Test case'lerin kaynağı ve sayısı açıklanmamış; multi-file çıktı açıkça belirtilmemiş, 138 task'ın modül/fonksiyon dağılımı yok.
- Tek referans sistem (1 repo), tek dil; baseline yok (sadece prompting ablation).
Key Takeaway:
- Mevcut bir aracı differential oracle olarak kullanıp domain-specific reconstruction değerlendirmek ucuz ama contamination riski yüksek; behavioral-reconstruction kategorisinde zayıf-kanıtlı örnek.

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
