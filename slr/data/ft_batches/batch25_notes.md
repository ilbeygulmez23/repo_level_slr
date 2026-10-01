# Batch 25 — reviewer 1 notes

### DelphiPipe — A modular multi-agent pipeline framework for large-scale code translation (Future Generation Computer Systems, 2026) [doi:10.1016/j.future.2026.108599]
Method + erken empirical gözlem: Danfoss Power Solutions'ta süren endüstriyel projede ~5M LOC Delphi kod tabanını C#'a çeviren agentic LLM pipeline'ının mimari blueprint'i. Not: full text yok, sadece abstract üzerinden yazıldı.
Kaynak kod tabanı çevrilebilir chunk'lara bölünüyor, her chunk bağımsız olarak agent stage'lerinden geçiyor (sequential agent orchestration + dinamik LLM pipeline), sonra hedef dilde yeniden birleştiriliyor (reassembly). LLM stokastikliğine karşı processing ve validation fonksiyonları var; chunking/reassembly stratejileri formalize edilmiş. Kısa bir önceki paper'ın (Bruneel et al., 2025) genişletilmiş versiyonu; kısa versiyon corpus'ta yok.
Findings:
- Manuel çeviri tahminine göre başlangıçta ~10x hızlanma raporlanıyor (tahmini baz üzerinden).
- Computational overhead, validation dinamikleri ve translation quality üzerine "erken gözlemler" var; abstract'ta sayısal kalite metriği (compile rate, test pass) verilmiyor.
Relevant Limitations:
- Değerlendirme erken ve büyük ihtimalle niteliksel; functional equivalence için executable oracle (test, differential) kullanılıp kullanılmadığı abstract'tan belli değil.
- Tek şirket, tek dil çifti, kapalı kod tabanı: tekrarlanabilir değil, benchmark yok.
- 10x iddiası tahmini manuel eforla kıyas; kontrollü baseline yok.
- Chunk bazlı bağımsız çeviri cross-chunk tutarlılık (tipler, isimler) sorununu reassembly'ye itiyor; bunun nasıl doğrulandığı full text'te kontrol edilmeli.
Key Takeaway:
- Endüstriyel ölçekte repo-translation'ın pratikte chunk → translate → reassemble + validation pipeline'ı ile yapıldığını gösteriyor; survey'de "scale vs. doğrulanabilirlik" gerilimine örnek.
- Kanıt düzeyi zayıf (experience-report'a yakın); full text ile eval kısmı teyit edilmeli.

### DepC2Rust — Dependency-Guided Repository-Level C-to-Rust Translation with Reinforcement Alignment (ACM proceedings, 2026) [doi:10.1145/3803437.3805266]
Method (+ muhtemelen training-data): repository-level C→Rust çevirisinde cross-file referansları dependency-guided context ile ele alan ve RL (reinforcement alignment) ile modeli hizalayan yaklaşım. Not: full text yok; abstract kesik, sadece motivasyon kısmı mevcut.
Abstract'ın belirttiği üç problem: (1) mevcut LLM yaklaşımları cross-file dependency'leri ya yok sayıyor ya da tüm dosyaları context'e koyuyor; (2) karmaşık dependency ve yapılandırılmış I/O nedeniyle repo-level çevirilerde syntactic correctness ve functional equivalence doğrulaması zor; (3) büyük ölçekli C-Rust paralel veri kıtlığı. Başlıktan, çözümün dependency graph'a dayalı seçici context + RL ile alignment olduğu anlaşılıyor.
Findings:
- Abstract'ın mevcut kısmında sonuç/sayı yok; benchmark, modeller ve metrikler raporlanmıyor.
Relevant Limitations:
- Değerlendirme yöntemi (compile rate, test pass, differential) bilinmiyor; full text ile teyit gerekli.
- RL reward'ı muhtemelen compiler/test sinyaline dayanıyor; reward ile eval metriğinin aynı olması durumunda overfitting riski kontrol edilmeli.
- Paralel veri kıtlığına çözüm olarak sentetik veri üretiliyorsa, LLM-generated verinin kalitesi ve contamination sorgulanmalı.
Key Takeaway:
- Repo-level çeviride "tüm dosyalar context'e" yerine dependency-guided seçici context eğilimini örnekliyor (EvoC2Rust skeleton yaklaşımıyla karşılaştırılabilir).
- Extraction için full text şart; şimdilik yalnızca scope kararı güvenilir.

### WCA4Z-COBOL2Java — Enterprise-Scale COBOL-to-Java Translation: LLMs Augmented with Program Analysis (ICSE-SEIP, 2026) [doi:10.1145/3786583.3786915]
Method (industrial): IBM watsonx Code Assistant for Z ürününün çekirdeği olan hibrit COBOL→Java pipeline'ı; static program analysis + LLM. Not: full text yok, sadece kısa abstract.
Class Designer ve Method Designer modülleri global analizle COBOL data division'larından ve control-flow graph'lardan Java class'larını, hiyerarşileri ve method signature'larını çıkarıyor; bu metadata LLM'in procedural logic çevirisini yönlendiriyor. Yani çıktı tek fonksiyon değil, uygulama düzeyinde çok sınıflı Java kodu (monolitik COBOL + global değişkenlerden idiomatik OO yapıya).
Findings:
- Abstract'ta sayısal sonuç yok; "scalable, consistent, idiomatic" iddiaları destekleyen metrik (compile rate, test equivalence, kullanıcı çalışması) belirtilmiyor.
Relevant Limitations:
- Değerlendirme yöntemi bilinmiyor; enterprise COBOL için executable test/oracle bulmak zor, büyük ihtimalle compile + manuel/LLM-judge kalite değerlendirmesi — full text'te kontrol edilmeli.
- Kapalı ürün ve müşteri kodları: tekrarlanabilirlik düşük, bağımsız repo sayısı muhtemelen az.
- Tasarım (class/method yapısı) statik analizle önceden sabitleniyor; LLM'in katkısı method gövdeleriyle sınırlı olabilir.
Key Takeaway:
- Repo-translation'da yapısal hand-off'un (class/method metadata) free-form NL yerine program-analysis artefaktı olarak verilmesine güçlü bir endüstriyel örnek; skeleton-guided yaklaşımlarla aynı aileden.
