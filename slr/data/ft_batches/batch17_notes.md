### WebDesignIter — WebDesignIter: Co-Evolving Design Knowledge for Repository-Level Front-End Code Generation (preprint, 2026) [arxiv:2607.10621]
Method çalışması: incremental front-end repo geliştirme için design knowledge'ı (mimari prensipler, modül sorumlulukları) kalıcı bir knowledge graph'ta (WebAppArchKG) tutan agent framework'ü.
İki aşama: design-informed planning (KG'den tarihsel context + mimari özet → implementation plan + test script'leri), design-aware generation (diff-based patch, sandbox execution, otomatik syntax repair, spaghetti dosyaların refactor'u, sonra KG güncelleme). Değerlendirme Web-Bench üzerinde: 50 proje × 20 sıralı NL task, her task önceki task'ların ürettiği repo state'ine bağlı; Vue/Angular/Tailwind vb. Metrikler Pass@1/Pass@2 (Web-Bench'in E2E testleri), ayrıca maintainability proxy olarak average file length. 9 foundation model (Gemini 2.5 Pro, Claude 4 Sonnet, GPT-4.1, GPT-4o, o4-mini, Qwen-Max/Plus, DeepSeek-V3/R1) + RQ4'te DeepSeek V4 ve Qwen 3.5.
Findings:
- Web-Agent baseline'ına göre ortalama +7.98pp Pass@1, +9.55pp Pass@2 (Claude 4 Sonnet: 34.90/48.10 vs 24.30/39.70).
- Ablation (Claude 4 Sonnet): design knowledge çıkarılınca Pass@1 −11.40pp; code graph −8.40pp, patch −3.50pp; ilginç şekilde sandbox'sız varyant en iyi sonucu veriyor.
- Claude Code, OpenHands, SWE-Agent, Codex CLI'ı tüm konfigürasyonlarda geçiyor; DeepSeek V4 Pro ile 33.53/53.14 Pass@1/2, ~26× daha az input token (533K vs 13,949K Claude Code). Codex CLI (GPT-5.5) sadece 8.5 Pass@1 — harness uyumsuzluğu şüphesi.
- Regression hataları %29.17 → %4.17; average file length 49.41 → 35.38.
Relevant Limitations:
- Tek benchmark (Web-Bench); 50 proje, sadece front-end.
- Genel amaçlı agent karşılaştırması Web-Bench'e özel adapte edilmemiş harness'larla; Codex CLI'ın çok düşük skorları karşılaştırmanın adilliğini sorgulatıyor.
- Maintainability sadece file length proxy'si ile ölçülüyor; planning aşamasında LLM kendi test script'lerini üretiyor (self-validation).
Key Takeaway:
- Incremental repo inşasında explicit, yapılandırılmış mimari bilgi (KG) free-form context'ten daha etkili; regression'ı düşürmenin anahtarı.
- Sequential-task benchmark'lar (Web-Bench) nl-to-app'in "evolving" varyantı için iyi bir test yatağı.

### WebGen-R1 — WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning (preprint, 2026) [arxiv:2604.20398]
Method/training çalışması: küçük bir LLM'i (Qwen2.5-Coder-7B-Instruct) multi-page website üretimi için end-to-end RL (GRPO) ile eğitiyor.
Scaffold-driven generation: sabit, önceden doğrulanmış React/Vite/Tailwind template (build config, routing skeleton, server logic sabit); model sadece değişken bileşenleri (sayfalar, komutlar, stiller) tek inference'ta üretiyor. Cascaded reward: static compliance → install/bundle/serve/render → VLM aesthetic skoru + execution log'larından functional integrity + format reward. Eğitim: WebGen-Instruct (6,667 task); 600 GPT-4.1 distilled örnekle SFT warm-up, sonra 400 RL adımı. Değerlendirme: WebGen-Bench (101 task) ve WebDev Arena'dan LLM-judge ile filtrelenmiş 119 task (OOD). Metrikler: FSR (WebVoyager GUI-agent ile test case'ler), AAS (VLM skoru), VRR (render oranı), LDPR (ESLint + dependency).
Findings:
- WebGen-R1-7B: FSR 29.21% (base 1.59%), AAS 3.94, VRR 95.89%; DeepSeek-R1 FSR 30.25% ile başa baş.
- En yüksek FSR hâlâ Claude-3.7-Sonnet (57.72%) — RL modeli functional correctness'ta frontier'ın yarısında.
- Aesthetics model boyutuyla daha kolay ölçekleniyor; functional correctness çok daha zor.
Relevant Limitations:
- Ölçüm tamamen LLM içi: FSR GUI-agent (GPT-4o), AAS VLM (GPT-4o); aynı GPT-4o hem training reward'da hem evaluation'da — reward hacking/judge bias riski ciddi.
- Sabit template yapısal problemi büyük ölçüde ortadan kaldırıyor; "project-level" iddiası mimari kararları kapsamıyor.
- WebDev Arena'da FSR raporlanmıyor (test case yok).
Key Takeaway:
- Scaffold + execution-grounded cascaded reward, repo-level RL'i hesaplanabilir kılmanın pratik yolu; ama evaluator ile reward'ın ayrıştırılması şart.

### AllianceCoder — What to Retrieve for Effective Retrieval-Augmented Code Generation? An Empirical Study and Beyond (preprint, 2025) [arxiv:2503.20589]
Empirical + method: repo-level RAG code generation'da hangi bilgi kaynağının (in-file context, invoked API'ler, similar code) işe yaradığını inceliyor; bulgulardan AllianceCoder'ı öneriyor (CoT ile sorguyu implementation adımlarına ayırıp API'leri semantic description matching ile retrieve ediyor).
Benchmark'lar CoderEval ve RepoExec (Python), metrik Pass@1/3/5 (executed tests); modeller GPT-4o-mini ve Gemini 1.5 Flash.
Findings:
- Context + gerçek invoked API (ConAPI) en iyi: RepoExec Pass@1 37.75 vs PureGPT 16.62.
- Similar code retrieval gürültü ekliyor, performansı %15'e kadar düşürüyor.
- AllianceCoder RepoCoder/RLCoder'ı geçiyor (Pass@1'de %20'ye kadar), ama oracle-API ConAPI'nin altında kalıyor (34.93 vs 37.75).
Relevant Limitations:
- Sadece Python, sadece 2 (ucuz) model; benchmark'lar eski, contamination riski.
- Fonksiyon-düzeyi hedef; repo sadece context olarak.
Key Takeaway:
- Repo-context generation'da "ne retrieve edilir" sorusu kritik: API bilgisi similar-code'dan değerli.

### ReproGap — AI-Generated Code Is Not Reproducible (Yet): An Empirical Study of Dependency Gaps in LLM-Based Coding Agents (preprint, 2025) [arxiv:2512.22387]
Empirical çalışma: coding agent'ların ürettiği projelerin temiz ortamda, sadece agent'ın bildirdiği dependency'lerle çalışıp çalışmadığını ölçüyor.
3 agent (Claude Code/Opus 4.1, OpenAI Codex, Gemini) × 100 standart prompt = 300 proje; Python 40, JavaScript 35, Java 25 prompt. Prompt açıkça tam requirements.txt/package.json/pom.xml istiyor. Üç katmanlı dependency modeli: claimed, working, runtime (SciUnit, npm tree, Maven tree). Başarısız olanlar manuel debug ediliyor (~15 dk/proje).
Findings:
- Sadece 205/300 (%68.3) proje out-of-the-box çalışıyor; Claude %73, Gemini %72, Codex %60.
- Dil farkı büyük: Python %89.2, JavaScript %61.9, Java %44.0; Gemini Java'da %28.
- Beyan edilen → runtime dependency ortalama 13.5× genişleme (≈3 vs 37 paket).
- Hataların çoğu eksik paket değil (%10.5), syntax/path/yapısal kod hataları.
Relevant Limitations:
- "Execute" = çalışıp çalışmadığı; functional correctness test edilmiyor.
- Prompt'lar yazarlar tarafından hazırlanmış, proje büyüklüğü/multi-file oranı raporlanmıyor; tek run.
- Manuel debugging süreci öznel. Venue belirsiz (AAAI copyright ibaresi var, track belirtilmemiş).
Key Takeaway:
- Repo-generation benchmark'larında environment/dependency reproducibility ayrı bir boyut olmalı; "build-run" ön koşulu bile ciddi eliyor.

### AADF — AutoGPT Devloop: An Autonomous AI Development Framework for End-to-End Software Generation, Execution, and Self-Repair (TIMES-iCON 2025, 2025) [doi:10.1109/times-icon67125.2025.11488122]
Full text yok; not abstract'a dayanıyor. Method çalışması: high-level hedefleri çalışan yazılıma çeviren self-developing agent (AADF).
Bileşenler: task decomposition, vector DB tabanlı semantic code memory, sanal ortam yönetimi, otomatik file/version control; plan → kod → execution → self-repair döngüsü. Design Science Research yaklaşımı; 15 GUI/web task, 5 zorluk seviyesi, 3 deneme (45 trial). Kullanılan LLM ve dil abstract'ta belirtilmiyor.
Findings:
- 41/45 trial (%91.1) manuel kod düzenlemesi olmadan tamamlanıyor.
- Level 1-2 ve 4'te %100; external API credential veya büyük NLP kaynak gerektiren task'larda düşüş (Level 3: %67/%33, Level 5: %67).
- Self-repair özellikle dependency çakışmaları ve eksik import'larda etkili.
Relevant Limitations:
- "Success" kriteri abstract'ta tanımlı değil; muhtemelen çalışırlık/manuel kontrol, test tabanlı değil.
- 15 task, baseline karşılaştırması yok; ölçek çok küçük.
Key Takeaway:
- Environment/dependency self-repair, end-to-end app generation'da temel başarısızlık kaynağını hedefliyor; ama kanıt zayıf.

### AgingGen — Investigating Software Aging in LLM-Generated Software Systems (preprint, 2025) [arxiv:2510.24188]
Empirical çalışma: LLM ile üretilmiş servis uygulamalarında uzun süreli çalışmada software aging (memory leak, latency artışı) olup olmadığını inceliyor.
Bolt platformu ile BaxBench prompt'larından (OpenAPI şeması + NL) 4 JavaScript/Express backend üretilmiş (image converter, credit card manager, process monitor, uptime checker). Sadece BaxBench functional testlerini geçenler 50 saatlik JMeter yük testine (10 thread) sokuluyor; memory, CPU, response time, throughput; Mann-Kendall + Sen's slope.
Findings:
- 4 uygulamanın hepsinde istatistiksel olarak anlamlı memory artışı (p≈0); en dik Credit Card App (slope 37.68e-3).
- Convert Image App en yüksek ortalama latency (2645.87 ms) ve pozitif trend; Monitor App ~25. saatten sonra artan latency.
- Aging'in şiddeti uygulama tipine göre değişiyor.
Relevant Limitations:
- Sadece 4 uygulama, tek araç (Bolt), altındaki LLM belirtilmiyor; tek run.
- Aging'in LLM kaynaklı olduğu, insan-yazımı baseline olmadan gösterilemiyor.
- BaxBench backend'leri büyük ihtimalle az dosyalı; multi-file yapı raporlanmıyor.
Key Takeaway:
- Üretilen uygulamaların non-functional, uzun vadeli davranışı (reliability) repo-generation değerlendirmesinde neredeyse hiç ölçülmüyor; bu çalışma bir metodoloji iskeleti sunuyor.
