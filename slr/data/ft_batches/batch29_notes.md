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
