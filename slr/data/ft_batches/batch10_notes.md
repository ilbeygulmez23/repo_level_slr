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

### AgileCoder — AgileCoder: Dynamic Collaborative Agents for Software Development based on Agile Methodology (FORGE 2025, 2025) [doi:10.1109/forge66646.2025.00026]
Method. Full text yok, not abstract'a dayanıyor. ChatDev/MetaGPT tarzı multi-agent yazılım geliştirme framework'ünü waterfall yerine Agile sprint yapısıyla kuruyor.
Input: kullanıcı gereksinimi (NL) → output: iteratif olarak büyüyen, multi-file codebase. Roller: Product Manager, Developer, Tester vb.; iş sprint'lere bölünüyor, her sprint'te incremental ilerleme. Ana teknik katkı Dynamic Code Graph Generator: codebase evrildikçe Code Dependency Graph güncelleniyor ve agent'lara tüm codebase yerine ilgili dosyalar veriliyor (context verimliliği). Değerlendirme iki eksenli: (1) HumanEval ve MBPP, (2) "real-world software development scenarios" (abstract'ta dataset adı/ölçeği ve metrikler verilmiyor; executability tarzı metrikler muhtemel ama teyit edilemedi). Dil büyük olasılıkla Python.
Findings:
- ChatDev ve MetaGPT'yi her iki eksende geçtiği iddia ediliyor; sayısal sonuçlar abstract'ta yok.
- Code dependency graph, büyük projelerde tüm codebase'i prompt'a koyma verimsizliğini hedefliyor.
Relevant Limitations:
- HumanEval/MBPP function-level; repo generation iddiasını ölçmüyor, multi-agent overhead'ini burada değerlendirmek yanıltıcı.
- Real-world senaryo seti küçük ve yazarların kendi hazırladığı set olabilir; test/oracle'ın kim tarafından yazıldığı (LLM mi insan mı) belirsiz.
- Agent'lar arası hand-off'lar free-form NL (user story/sprint backlog); graph yalnızca kod bağımlılığı için yapısal.
Key Takeaway:
- Süreç modeli (Agile vs waterfall) ve dependency graph ile context seçimi, ChatDev/MetaGPT hattının doğal devamı; survey'de "process-inspired multi-agent" grubunda karşılaştırılmalı.
- Full text ile ProjectDev tarzı değerlendirme detayları teyit edilmeli.

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
