# Batch 28 — paper notes (reviewer 1)

### BAEs — From Stateless Code Generation to Living Ontologies (preprint, 2026) [doi:10.1145/3786167.3788408]
Method + empirical karşılaştırma: Business Autonomous Entities (BAEs) adında, bir business concept'in "living ontology"sini içinde taşıyan ontology-aware agent'lar öneriliyor. Amaç, requirement değiştiğinde kodu sıfırdan regenerate eden stateless pipeline'lar yerine domain-preserving evolution. Full text yok; not abstract'a dayanıyor.
İki katmanlı değerlendirme: (1) feasibility demo — bir BAE'nin 6 adımlı evolution'ı restart olmadan online yapması; (2) otomatik benchmark — BAEs vs GHSpec vs ChatDev, aynı prompt, seed ve model (gpt-4o-mini). Her framework için aynı 6-sprint'lik program 100 kez seri çalıştırılıyor (toplam 300 run), clarification programatik. Effectiveness için "lightweight sanity check": run'ın prompt'taki explicit structural requirement'ları karşılayan runnable bir project üretip üretmediği. Asıl metrikler: end-to-end süre, token, cached-input indirimli maliyet, LLM interaction sayısı. Dil(ler) abstract'ta belirtilmemiş.
Findings:
- BAEs süre, token, maliyet ve interaction sayısında her iki baseline'dan da belirgin şekilde düşük; effect size'lar çoğunlukla medium-large.
- BAEs time–cost düzleminde Pareto-favorable bölgede.
- Framework'ler arası maliyet farkı, total tokens ~ cost regresyonu ve cache kullanımı ile açıklanıyor.
- Fonksiyonel doğruluk oranı (sanity check pass rate) abstract'ta sayı olarak verilmemiş.
Relevant Limitations:
- Doğruluk sadece structural/runnable sanity check; test-based functional correctness yok — verimlilik karşılaştırması, kalite eşitliği varsayımı üzerine kurulu.
- Tek program, tek model (gpt-4o-mini); 100 tekrar varyansı ölçüyor ama genellenebilirliği değil.
- Senaryo kısmen incremental evolution (EC1'e yakın), ama baseline'lar sprint'lerde sıfırdan üretiyor; karşılaştırma bu asimetriden etkilenebilir.
Key Takeaway:
- Multi-sprint, evolving requirement ile repo üretimini cost/token ekseninde ölçen nadir çalışma; survey'de "efficiency/nonfunctional" boyutunun örneği.
- Ontology gibi yapılandırılmış, kalıcı bir artefact'ı hand-off olarak kullanmak free-form NL'ye alternatif.
