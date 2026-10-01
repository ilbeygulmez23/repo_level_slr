### Role-Based MA Eval — An Evaluation of Role-Based Multiagent Code Generation on Repository-Scale Problems (IEEE Software, 2026) [arxiv:2607.04212]
Empirical çalışma (+ kendi pipeline'ı): SRS'ten tüm Java Maven repo'yu üretmede tek LLM ile role-based multi-agent (Sequential ve Reflexive, ChatDev 2.0 üzerinde) karşılaştırılıyor.
Input, IEEE SRS formatında bir doküman; ama SRS'ler GPT-5 ile README + tüm Javadoc'tan türetilip manuel doğrulanmış. 2025'te oluşturulan top-1000 Java GitHub reposundan complexity grubuna göre (Trivial/Simple/Moderate/Complex) 3'er repo, toplam 12. Agent pipeline: Planning → Coding (agent'lar arası summary ile hand-off) → static text-based Assessment (en fazla 10 iterasyon) → Setup (pom.xml). Backbone GPT-5, 5 tekrar. Orijinal testler üretilen koda uygulanamadığı için metrikler: JPlag max similarity, CrystalBLEU, derlenebilen class yüzdesi ve Claude Code (Sonnet 4.6) ile Gherkin senaryosu çıkarıp ChatGPT 5.4 ile eşleştiren "scenario-intent" oranı.
Findings:
- Overall compile oranı: LLM-only %31, Agentic-seq %22, Agentic-refl %40; yani en iyisinde bile class'ların çoğu derlenmiyor.
- JPlag similarity 0.21 → 0.33 → 0.43; scenario-intent %61 / %55 / %78 (Agentic-refl).
- Üretilen kod orijinal LOC'un sadece %1–25'i kadar; plan-then-execute büyük projelerde ölçeklenmiyor.
- Maliyet düşük: proje başına $0.20–1.40, 17 dk–1 s 48 dk.
Relevant Limitations:
- Değerlendirme tamamen referans implementasyona bağlı (plagiarism benzerliği); farklı ama geçerli tasarımları cezalandırır. Fonksiyonel doğruluk hiç çalıştırılarak ölçülmüyor.
- Spec'i LLM (GPT-5) yazıyor, generation GPT-5, scenario-intent iki ayrı LLM ile ölçülüyor; ölçümün içinde LLM var ve yazarlar da bunun correctness olmadığını kabul ediyor.
- Hand-off free-form NL summary; reflection loop compiler/test feedback kullanmıyor.
- 12 repo, tek dil, tek model; Javadoc'tan SRS türetmek implementasyon bilgisini dolaylı sızdırabilir.
Key Takeaway:
- Repo-ölçeğinde test transfer edilemeyince similarity + LLM-judge'a düşülüyor; bu, implementation-agnostic executable oracle ihtiyacının net bir örneği.
- Execution feedback olmayan reflexive loop derlenebilirliği çözmüyor; compiler/test-in-the-loop şart.

### app.build — app.build: A Production Framework for Scaling Agentic Prompt-to-App Generation with Environment Scaffolding (SANER 2026, 2025) [arxiv:2509.03310]
Method + industrial empirical çalışma: NL prompt'tan full-stack CRUD web app üreten, "environment scaffolding" (schema → API → UI FSM, her adımda linter/type-check/unit test/Playwright, sandbox, repair loop) yaklaşımını öneren açık kaynak framework.
Stack'ler TypeScript/tRPC, PHP/Laravel, Python/NiceGUI; değerlendirme sadece tRPC. Dataset: bağımsız kişilerce yazılıp LLM ile anonimleştirilmiş 30 prompt (low/medium/high complexity). 300 otomatik run (baseline, ablation'lar: no lint / no Playwright / no handler tests; model karşılaştırma: Claude Sonnet 4 vs Qwen3-Coder-480B vs GPT-OSS-120B). Değerlendirme: viability V = Boot (AB-01) + Prompt Correspondence (AB-02); kalite Q 0–10, insan assessor'ların 6 check'lik rubriği (create, view/edit, clickable sweep, performance). Ayrıca production'da 4 ayda 3000+ app.
Findings:
- İnsan değerlendirmesinde 30 app'ten 22'si viable (%73.3), 9'u perfect; viable'larda ortalama Q 8.78.
- Otomatik success: Claude %86.7, Qwen3 %70 (viable app başına $0.61 vs $5.01, 8.2× ucuz), GPT-OSS %30.
- Playwright E2E kaldırılınca viability %90'a çıkıyor (+16.7 pp): brittle selector, race condition, farklı ama doğru UI yapısı false reject üretiyor.
- Handler test'leri kaldırınca viability artıyor ama AB-04 (view/edit) %90'dan %60'a düşüyor.
- GPT-OSS'ta boot eden app'lerin önemli kısmı "Under Construction" template; boot-check tek başına yanıltıcı.
Relevant Limitations:
- Evaluation'ın çekirdeği insan rubriği; tek stack, 30 prompt, CRUD domain'i ile sınırlı. Ablation'lar 30 app'lik tek run'lar, varyans yok.
- Aynı validator'lar hem generation feedback'i hem kısmen otomatik metrik; model karşılaştırmasında açık modeller basitleştirilmiş pipeline ile koşulmuş (unfair baseline).
- Production metrikleri (star, app/gün) kalite kanıtı değil; industrial track, bazı kısımlar experience report tonunda.
Key Takeaway:
- Implementation detayına bağlı E2E test'ler probabilistic generation'da geçerli çözümleri reddediyor; spec-level, implementation-agnostic test tasarımı için güçlü ampirik argüman.
- Structured stage decomposition + executable validation, model seçiminden daha fazla güvenilirlik getiriyor.

### AutoP2C — AutoP2C: An LLM-Based Agent Framework for Code Repository Generation from Multimodal Content in Machine Learning Papers (ICASSP 2026, 2025) [doi:10.1109/icassp55912.2026.11462205]
Method + küçük benchmark: ML makalesinin text, figure ve tablolarından çalıştırılabilir multi-file Python repo üreten 4 aşamalı multi-agent framework (full text arXiv v2 preprint'i).
Aşamalar: (1) popüler ML repolarından LLM ile "repository blueprint" çıkarımı, (2) MinerU OCR + VLM ile multimodal parsing, (3) LRM ile hiyerarşik task decomposition (dosya arayüzleri, bağımlılıklar), (4) execution feedback'li implement-verify döngüsü. Modeller: GPT-4o (parsing/planning), o1-mini (kod), o1 (doğrulama), o3-mini (refinement). Değerlendirme: yeni Paper2Repo (2024 sonrası 8 makale, 6 ML task) üzerinde üretilen repo'yu orijinal repo ile aynı dataset'te çalıştırıp absolute/relative performance; LLM-as-judge ile orijinal kodun fonksiyon/class'larına göre COMPfunc/COMPclass; ayrıca PaperBench Code-Dev replication score.
Findings:
- AutoP2C 8/8 makale için çalışan repo üretiyor; o1 ve DeepSeek-R1 yalnızca 1/8.
- Relative performance %89.8–122.0 (ortalama %99.5).
- COMPclass ortalama %65.7 (o1 %34.9, R1 %31.1); COMPfunc %51.6 (o1 %29.1).
- PaperBench Code-Dev: 49.2 ± 14.0 vs PaperCoder 44.2.
- Ablation: feedback loop kaldırılınca hiçbir repo çalışmıyor.
Relevant Limitations:
- Benchmark sadece 8 makale; baseline'lar tek-shot LLM, agentic baseline yok (unfair comparison).
- Completeness metriği LLM-judge ve orijinal koda göre hesaplanıyor (reference-coupled); OpenAI model ailesi hem üretiyor hem ölçüyor.
- "Relative performance" metriği tek sayıya (accuracy) dayanıyor; >%100 değerler farklı eğitim koşullarını gösterebilir, doğru implementasyonun kanıtı değil.
Key Takeaway:
- Paper-to-repo'da execution feedback olmazsa olmaz; ancak doğruluk oracle'ı (metrik reproduction) zayıf ve gürültülü.

### Cursor Design Issues — Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects (preprint, 2026) [arxiv:2604.06373]
Empirical çalışma: Cursor Pro ile, önerilen Feature-Driven Human-In-The-Loop (FD-HITL) süreci izlenerek 10 büyük proje üretiliyor ve fonksiyonel doğruluk + design quality inceleniyor.
Süreç: yazarların kürate ettiği proje açıklaması → Cursor requirements.md + tasklist.md üretir → feature feature backend/DB/frontend geliştirme, her feature'da manuel black-box test ve bug-fix/enhancement prompt'ları → system-level test. İlk yazar hiç kod yazmıyor ama sürekli feedback veriyor. 10 proje (2 mobile, 4 web, 4 utility), MERN, React Native + Spring Boot, Vue + Django/CodeIgniter, WordPress plugin; ortalama 16,965 LoC, 114 dosya. Doğruluk: iki yazar requirements.md'deki her requirement'ı çalıştırıp Complete/Incomplete işaretliyor. Design: SonarQube + CodeScene, false positive'ler manuel ayıklanıyor. Dataset (DIinAGP) paylaşılıyor.
Findings:
- Ortalama functional correctness %91 (min %85, max %96); 16 incomplete requirement (11 eksik, 5 logic hatası).
- CodeScene 1,305 issue (9 kategori), SonarQube 3,193 issue (11 kategori; 1,612 false positive ayıklandıktan sonra); iki araç arasında sadece 133 örtüşme.
- En sık: Code Duplication, yüksek complexity, Large Methods, framework best-practice ihlali, exception handling, accessibility; SRP/SoC/DRY ihlalleri.
Relevant Limitations:
- Tam otonom değil: ciddi insan yönlendirmesi var, requirement'ları Cursor kendisi yazıp yazar düzeltiyor; %91, Cursor'un değil insan+Cursor sisteminin sonucu.
- Doğruluk ölçümü manuel ve yazarların kendi requirement listesine göre; bağımsız test yok, tekrarlanabilirlik düşük.
- Tek araç, tek run, "automatic model selection" ile model bilinmiyor; insan baseline'ı yok.
Key Takeaway:
- Fonksiyonel olarak "çalışan" büyük AI-üretimi projelerde maintainability borcu yüksek; repo-gen benchmark'larına nonfunctional/design metrikleri eklenmeli.

### BeyondSWE — BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing? (preprint, 2026) [arxiv:2603.03194]
Benchmark: 246 repodan 500 instance, dört setting: CrossRepo (200), DomainFix, DepMigrate (178) ve survey açısından ilgili olan Doc2Repo (50, boş workspace'ten NL spec'ten repo).
Doc2Repo inşası: Ocak–Kasım 2025'te oluşturulmuş, ≥3 contributor, >20 star Python repoları; Gemini 3 Pro kod tabanını gezip purpose, usage örnekleri, public class/function imzaları ve davranışı içeren spec yazıyor, implementation detayı ve dizin yapısı çıkarılıyor, repo adı `target_repo` ile maskeleniyor. Test'ler orijinal repodan LLM yardımıyla uyarlanıp insan tarafından gözden geçiriliyor; 60 adaydan 50 seçiliyor (ortalama 26.8 dosya, 3,528 satır). Metrikler: ortalama test pass rate ve (Almost) Correct Count (tüm testler / ≥%90). Harness'ler: OpenHands, SearchSWE (web search + blocklist), Codex CLI.
Findings:
- Doc2Repo'da en iyi pass rate %61.74 (Codex GPT-5.4 xhigh); OpenHands altında %46.6–57.2.
- 50 repodan en fazla 2–4'ü tamamen doğru; pass rate kısmi ilerlemeyi abartıyor.
- Search erişimi Doc2Repo'da neredeyse etkisiz (±birkaç puan), diğer task'larda daha faydalı.
Relevant Limitations:
- Doc2Repo, benchmark'ın sadece %10'u; asıl odak issue resolution/migration.
- Spec LLM (Gemini 3 Pro) tarafından referans koddan tersine üretiliyor ve test'ler orijinal repodan geliyor: public API imzalarına sıkı bağlılık, alternatif tasarımlar cezalandırılır. Gemini hem spec yazıyor hem değerlendirilen modellerden biri.
- Sadece Python, 50 repo.
Key Takeaway:
- "Reverse-engineered spec + orijinal repo testleri" deseni ölçeklenebilir ama spec-test uyumu için insan denetimi gerekiyor; strict "fully correct" metriği raporlanmalı.

### NanoHarness — Beyond the Model: Demystifying Harness Effects in Software Engineering Agents (preprint, 2026) [arxiv:2609.32459]
Empirical + method çalışması: model/harness/task etkileşimini ve harness bileşenlerinin katkısını ölçüyor; asıl testbed ProgramBench (reference binary'den davranışsal olarak eşdeğer repo'yu sıfırdan yeniden inşa etme; 200 task; Rust, Go, C/C++, Java, Haskell).
Tasarım: mini-SWE-agent vs OpenCode, Qwen ve DeepSeek ailelerinden 10 açık model (60 konfigürasyon: SWE-bench Pro 300 örnek, ProgramBench 70 örnek, GitTaskBench 54). Sonra mini-SWE-agent'a plug-and-play bileşenler (tool registry, context compression, planning, task-specific/general subagents, lazy skills) eklenerek NanoHarness kuruluyor; tam 200 ProgramBench task'ında Qwen3.7-Max ve DeepSeek-V4-Pro ile ablation. Step limiti 1000'den 300'e indirilmiş, network kapalı.
Findings:
- ProgramBench'te NanoHarness: Qwen3.7-Max 42.88 → 50.25 (+7.37), DeepSeek-V4-Pro 45.14 → 51.35 (+6.21); OpenCode 51.68/52.48, Claude Code 52.33/52.76.
- En büyük tekil kazanç task-specific subagents (+5.91 / +4.46) ve tool registry (+4.57 / +3.54).
- Context compression prompt token'larını %54–77 azaltıyor ama skoru 4.86 / 3.85 düşürüyor; general subagents de zarar veriyor.
- SWE-bench Pro'da karmaşık harness'in faydası güçlü modellerde azalıyor; repo-generation'da ise sadece güçlü modeller karmaşık harness'ten yararlanıyor.
- Failure mode'lar: reference binary'nin aşırı veya yetersiz probing'i.
Relevant Limitations:
- Sadece Qwen/DeepSeek, temperature 0, tek run; step budget'ın düşürülmesi ProgramBench skorlarını orijinalle karşılaştırılamaz kılıyor.
- ProgramBench değerlendirmesinin ayrıntıları bu makalede anlatılmıyor; skor reference binary davranışına bağlı (output formatı farklı geçerli çözümleri cezalandırabilir).
- Bileşenler minimal implementasyon; commercial harness'lerin gerçek bileşenleriyle eşdeğerliği varsayım.
Key Takeaway:
- Repo generation'da harness etkisi model etkisi kadar büyük; benchmark raporlarında harness sabitlenmeli/raporlanmalı. Uzun spec'lerde context compression riskli.

### OpenCoder — Beyond "What to Retrieve": Uncertainty in Retrieval-Augmented Code Generation (preprint, 2026) [arxiv:2607.24884]
Method: repo-level function generation için similar code, repository context ve project API kaynaklarının her biri için uncertainty tahmin edip evidence filtreleme, generation, verification ve repair'i buna göre yönlendiren RAG framework'ü.
Değerlendirme: 32 task'lık RepoExec-inline (14'ten genişletilmiş) ve context-limited 10 ExecRepoBench task'ı; GPT ve Gemini backend, 5-candidate frozen protokol, Pass@k ve selected-output correctness; API retrieval için 13 task'ta macro F1.
Findings:
- GPT'de selected-output correctness %56.25 → %78.13 (Baseline RAG'e göre), ama RAG + Verify/Repair kontrolüyle eşit.
- Gemini'de fark istatistiksel olarak anlamlı değil; tüm Pass@k CI'ları sıfırı içeriyor.
- ExecRepoBench'te kontrol, OpenCoder'ı açıkça geçiyor (Gemini 100 vs 80).
- Target-aware API refinement macro API F1'i %43.4'ten %64.8'e çıkarıyor.
Relevant Limitations:
- Ölçek çok küçük (32+10 task), sonuçlar backend'e bağlı; kazanç büyük ölçüde verify/repair'den geliyor.
Key Takeaway:
- Dürüst negatif sonuçlar: uncertainty modellemenin katkısı, execution-based verify/repair'in katkısından ayrılamıyor.

### BUILD-AND-FIND — BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases (preprint, 2026) [arxiv:2605.06136]
Benchmark/protokol: builder agent gizli bir repository spec'inden sıfırdan codebase üretiyor; ardından sadece codebase'i gören finder agent'lar spec'e izlenebilir 4 şıklı soruları (task başına 15) cevaplıyor. Amaç correctness değil, üretilen repo'nun tasarım niyetini ne kadar "okunabilir" taşıdığını ölçmek.
İki Rust task ailesi (scratch_minidb, scratch_nanoweb). 12 builder/finder konfigürasyonu: Claude Opus 4.7, Sonnet 4.6, GPT-5.5, GPT-5.4-mini, MiMo-v2.5(-pro), her biri high/low reasoning. 48 build (41'i `cargo build` compile probe'unu geçiyor), 1,728 find kaydı. Metrikler: recovery accuracy, 3-trial repeatability, builder implementation coverage (artifact-question audit, 696/720 etiket iki finder'ın consensus'u ile), ve koşullu inspection effort (finder'ın okuduğu byte, R_b).
Findings:
- Question-only kontrolde bile accuracy %94.5; artifact-conditioned %98.9 (+4.4 pp), low-prior subset'te +9.0 pp.
- Builder implementation coverage %85–100.
- Effort'ta GPT-5.5 en düşük (R_b 1.033 high-effort).
- Same-family builder–finder affinity pozitif (OpenAI +0.076, Claude +0.041).
Relevant Limitations:
- Runtime correctness ölçülmüyor; ölçüm tamamen LLM finder'lara dayanıyor ve audit etiketleri de finder consensus'undan geliyor (aynı model aileleri hem yazıyor hem ölçüyor; affinity bunu gösteriyor).
- Sadece 2 task, yüksek prior'lar yüzünden accuracy doymuş durumda; asıl sinyal (byte cinsinden effort) dolaylı bir proxy.
- Soru bankası spec'e bağlı; tasarım seçimlerini "gold" kabul ettiği için alternatif tasarımlar non-gold sayılıyor.
Key Takeaway:
- Üretilen repo'yu downstream agent'lar için bir iletişim artefaktı olarak değerlendirmek yeni bir eksen, ama correctness ölçümüyle birlikte kullanılmalı.

### OOD PureAI — Can LLMs Produce Better Object-Oriented Designs than Human-Involved Development? (preprint, 2026) [arxiv:2605.19901]
Empirical case study: tek bir postgraduate Java assignment'ı (Kalah oyunu) için LLM'lerin uçtan uca ürettiği projelerin (PureAI) OOD kalitesi, 2021 (PreAI, 93) ve 2024 (PostAI, 57) öğrenci projeleriyle karşılaştırılıyor.
PureAI: GPT-5.4, Gemini 2.5 Pro, Gemini 3.1 Pro preview × 3 prompt (None/Broad/Specific OOD guidance) × 90 run. Prompt'ta functional requirement'lar ve 19 test case'in tamamı veriliyor; testler geçmezse en fazla 5 repair iterasyonu, sadece tüm testleri geçen çıktılar analiz ediliyor. Metrikler: CK ile 13 OOD metriği (WMC, CBO, LCOM, DIT, LOC, #Cl), DesigniteJava + PMD ile code smell density, manuel domain concept temsili (Board, Game, Player, Pit, House, Store) ve runtime object-count uygunluğu. Mann–Whitney + Cliff's delta.
Findings:
- Tüm testleri geçen çıktılar: GPT-5.4 ve Gemini 3.1 90/90; Gemini 2.5 Pro 83–87 (ilk prompt'ta sadece 4–7 geçiyor).
- PureAI daha düşük smell density ve daha küçük size/complexity/coupling gösteriyor ama bu oversimplification: daha az class ve domain concept (G31S median 4 class, 2 concept, prosedürel stil).
- PostAI, birçok metrikte PreAI'den çok PureAI'ye yakın.
- Specific prompt concept temsilini artırıyor ama insan projeleriyle farkı kapatmıyor.
- gpt-4o ve gemini-2.0-flash 90'ar run'da hiç tüm testleri geçen proje üretemiyor.
Relevant Limitations:
- Tek, küçük proje ve tek dil; "repository" sınırında (birkaç class).
- Test'ler prompt'ta veriliyor ve repair ile hedefleniyor; fonksiyonel doğruluk bir filtre, ölçüm değil. Başarısız run'ların atılması survivorship bias yaratıyor.
- Domain concept analizi isim eşleşmesine dayalı manuel kodlama.
Key Takeaway:
- Testleri geçmek iyi tasarım demek değil; repo-gen değerlendirmesinde design/abstraction metrikleri ayrı bir eksen olmalı.

### CodeMEM — CodeMEM: AST-Guided Adaptive Memory for Repository-Level Iterative Code Generation (preprint, 2026) [arxiv:2601.02868]
Method: multi-turn repo-level function generation'da AST-guided Code Context Memory (repo context'i dinamik güncelleme) ve Code Session Memory (önceki düzeltmelerin unutulmasını AST ile tespit) öneriyor.
Değerlendirme: CodeIF-Bench L-2 (40 dialog, 360 test edilebilir instruction; IA, CA, forgetting rate IFR) ve 230 Python task'lık CoderEval'in verbal feedback ile 5 turlu versiyonu (Pass@1). Backbone DeepSeek-V3.2, greedy; baseline'lar Full-Context, MemGPT, Mem0, A-Mem, RLCoder.
Findings:
- CodeIF-Bench ortalama IA 46.1 (en iyi baseline 41.1), CA 42.8 (38.4).
- CoderEval Pass@1 5. turda 55.7 vs Full-Context 50.9; FC'nin 5. turdaki skoruna 3. turda ulaşıyor.
- Ablation'da AST selector çıkarılınca IA −4.4.
Relevant Limitations:
- Tek backbone ve tek dil (Python); CodeIF-Bench'te sadece 40 dialog.
- Multi-turn feedback simülasyonu çok basit ("cevabın yanlış").
Key Takeaway:
- Contextual tier'da iteratif etkileşim ve bellek yönetimi, retrieval kadar önemli bir boyut.
