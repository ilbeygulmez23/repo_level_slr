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
