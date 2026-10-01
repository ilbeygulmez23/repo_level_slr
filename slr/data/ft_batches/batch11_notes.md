# Batch 11 — reviewer 1 notes

Not: Bu batch'teki hiçbir kayıt için açık full text bulunamadı; tüm notlar yalnızca abstract'a dayanıyor.

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
