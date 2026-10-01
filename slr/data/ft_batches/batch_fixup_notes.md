### Prompt-to-Product — From Prompt to Product: A Human-Centered Benchmark of Agentic App Generation Systems (ACM IUI Workshops 2026, 2025) [arxiv:2512.18080]
Benchmark + empirical çalışma: ticari prompt-to-app sistemleri (Replit, Bolt, Firebase Studio) tek NL prompt'tan full-stack web app üretiyor; değerlendirme neredeyse tamamen insan-merkezli.
96 prompt, taxonomy'ye göre (6 domain: healthcare, legal, real estate, finance, government, education × difficulty × specificity × complexity) developer forumlarından esinlenerek yazılmış; sistem başına 1 generation → 288 app artifact. Artifact'lar GitHub'a export edilip Quome Cloud'a Docker ile deploy ediliyor (bazı Replit app'lerinde manuel müdahale). Otomatik audit: HTTP GET + Playwright ile DOM görünürlük kontrolü. İnsan çalışması: 282 katılımcı, kalite filtresi sonrası 205; isolated 5'li Likert (clarity, ease of use) + side-by-side pairwise (ease, trust, visual appeal, visual appropriateness), 1,071 geçerli karşılaştırma. İstatistik: LMM, Bradley-Terry, Wilcoxon, Cliff's delta.
Findings:
- Deploy başarısı (otomatik): Firebase %84.4, Replit %75.0, Bolt %64.6; katılımcı "appeared" oranları %68.2/%68.4/%64.8; otomatik–insan uyumu %88.2.
- Isolated rating'lerde fark yok denecek kadar az (clarity 3.92–3.96); pairwise'da Firebase tüm boyutlarda önde (ease win rate %42.5 vs Bolt %31.7, Replit %26.0; trust %41.2/%29.2/%22.7).
- Pairwise değerlendirme isolated'dan belirgin şekilde daha ayırt edici.
Relevant Limitations:
- Fonksiyonel doğruluk ölçülmüyor: test yok, requirement coverage yok; "çalışıyor mu" sadece sayfanın ekranda görünmesi. Başlıktaki "completeness" algısal.
- Black-box ticari sistemler, sistem başına tek sample, model/harness bilinmiyor → sonuçlar zamana ve sürüme bağlı, tekrar üretilemez.
- Rater'lar teknik olmayan crowd; kısa etkileşim; effect size'lar küçük (|Δ|≈0.2).
Key Takeaway:
- nl-to-app değerlendirmede human pairwise preference, executable/requirement-based oracle'ın yerini tutmuyor ama tamamlayıcı; deployability bile ciddi bir filtre (%15–35 başarısızlık).

### CodeSpec — CodeSpec: Dual Executable Specifications for Agentic Long-Horizon Feature Development (preprint, 2026) [arxiv:2607.26777]
Method çalışması; ana hedef mevcut repo'ya feature ekleme (FeatureBench), yani birincil katkı EC1 alanında. Survey için dahil edilme gerekçesi ayrı ve ayrıca raporlanan bir greenfield değerlendirmesi: NL2Repo-Bench (104 task, requirements dokümanı + boş workspace → Python repo). Bu yüzden core ama peripheral.
Yöntem: feature instruction LLM ile sub-requirement'lara ayrılıyor; her biri için repo evidence'ı (design pattern, call relation, dependency) ile gerekçelendirilen "functional chain" (unit → relation → unit) kuruluyor. Her chain iki executable spec'e derleniyor: architecture spec (CheckUnit/CheckRelation/CheckDataFlow) ve behavior spec (CheckOutput/CheckBoundary/CheckState, test benzeri). Agent, iki spec de geçene ya da budget bitene kadar patch üretip feedback alıyor. Greenfield'da önce skeleton + functional unit'ler yaratılıyor, sonra gelişen kod tabanı evidence olarak kullanılıyor. Backbone DeepSeek-V4-Pro (ek olarak GPT-5.4-mini); metrikler FeatureBench'ten %Passed, #Resolved, maliyet; 10,000 bootstrap.
Findings:
- FeatureBench Lite/Fast/Full: %70.7/%55.0/%49.9; en iyi baseline RTADev %65.3/%49.7/%46.1, Claude Code %59.8/%47.0/%41.1. Maliyet artışı RTADev'e göre $0.01–0.03/task.
- NL2Repo: overall %46.6, 8 resolved (Claude Code %41.6/5, RTADev %41.3/7, OpenHands %26.4/2); Easy/Medium/Hard %70.0/%51.7/%20.4 — Hard'da kazanç sadece +1.1 puan, std (~4.7) içinde.
- Ablation (Lite): spec'siz %62.6, behavior spec'siz %64.0, architecture spec'siz %66.6; executable vs textual spec farkı uzun instruction'larda büyüyor (%71.8 vs %43.8).
Relevant Limitations:
- Spec'ler ve behavior check'leri aynı LLM tarafından üretiliyor; spec'in doğruluğu ayrıca doğrulanmıyor (self-generated oracle).
- Greenfield sonucu tek tablo, tek backbone; NL2Repo'da hard task'larda anlamlı iyileşme yok. Ablation'lar sadece 30 task'lık Lite split'te.
- Baseline'lar (Claude Code dahil) DeepSeek-V4-Pro ile koşuluyor — native olmayan model/harness kombinasyonu confound.
Key Takeaway:
- Free-form NL plan yerine executable, yapısal hand-off artefact'ları (architecture + behavior spec) long-horizon'da design drift'i azaltıyor; repo generation için structured contract fikrini destekleyen bir kanıt, ama greenfield kanıtı ikincil ve zayıf.
