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

### EnterpriseGenAI — Leveraging Generative AI for Accelerating Enterprise Application Development: Insights from ChatGPT (APSEC 2024, 2024) [doi:10.1109/apsec65559.2024.00052]
Method/experience-tipi çalışma (full text yok, sadece abstract): meta-model tabanlı prompting ile requirement'ları LLM (ChatGPT) üzerinden refined requirement ve design specification'a, oradan enterprise application koduna dönüştürüyor.
Input requirement → refined requirements → design spec → code; "small yet complex applications" üretildiği söyleniyor. Veri seti boyutu, diller, uygulama sayısı ve değerlendirme metrikleri abstract'ta raporlanmamış.
Findings:
- Abstract sayısal sonuç vermiyor; sadece yaklaşımın küçük uygulamalara uygulandığı belirtiliyor.
Relevant Limitations:
- Full text olmadan değerlendirme yöntemi (test, insan, build-run) belirlenemiyor; muhtemelen case-study düzeyinde.
- Hand-off'lar meta-model ile yapılandırılmış olabilir, ama bu abstract'tan doğrulanamıyor.
Key Takeaway:
- Meta-model/spec ara artefact'ı fikri structured hand-off lensi için ilgili; extraction için full text gerekli (düşük güvenli include).
