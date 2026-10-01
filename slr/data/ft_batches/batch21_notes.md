# Batch 21 — paper notes (reviewer 1)

### ChessEngines-PL — Do programming languages still matter to your AI coding agent teammate? Evidence at scale from chess engines (preprint, 2026) [arxiv:2606.13763]
Empirical case study. İki frontier coding agent'a (Claude Code: Opus 4.6/4.7; Codex: gpt-5-codex, gpt-5.3/5.4-codex) tek cümlelik prompt veriliyor ("build a chess engine in [LANG] ... assess its Elo"). Agent'lar 17 dilde toplam 34 engine üretiyor (29 from-scratch main corpus + 5 special-role: iki Java→X port, DSL deneyi, vb.), Python/Rust'tan COBOL, TeX, CSS, Brainfuck, Lean 4, Why3/Rocq'a kadar.
Artefact'lar gerçek multi-file repo'lar (4–234 dosya, mainstream dillerde 2–12kLOC). İnsan müdahalesi dokümante edilmiş bir protokolle kısıtlı (p1–p5 prompt sınıfları, algoritma adı vermek yasak). Değerlendirme dilden bağımsız oracle hiyerarşisi: perft node count (exact move-gen doğruluğu), UCI/cutechess ile legal oyun, Stockfish gauntlet ile Elo; ek olarak 38 feature fingerprint, token/USD maliyeti, session transcript analizi ve novelty audit.
Findings:
- Denenen her dilde en az bir çalışan, feature-rich engine çıktı; birçok dil (CSS, TeX, APL, Brainfuck) için karşılaştırılabilir açık kaynak öncül bulunamamış.
- 1900–2100 Elo bandına yalnızca mainstream compiled diller ulaşıyor; esoterik/legacy engine'ler yüzlerce–binlerce Elo aşağıda kalıyor.
- Maliyet: mainstream engine ~$2–30, zor dil kategorilerinde ~25–50 prompt ve ~$60–480.
- 34 engine'den 26'sı kendi perft harness'ini, 30'u Stockfish gauntlet'i kendiliğinden kuruyor; ama 15 self-Elo scriptinin 11'i 200–1100 Elo fazla tahmin ediyor.
- Bazı engine'ler python-chess import ederek "cheat" ediyor (chess-css-codex örneği).
Relevant Limitations:
- Tek domain (satranç) ve tek yazar tarafından yürütülmüş session'lar; n=1 per dil×agent, seed varyansı yok.
- Human-in-the-loop (p3 bug report, p5 infra isteği) var; tam otonom değil, stop-rule yargıya dayalı.
- Perft + Elo güçlü, reference implementation'dan bağımsız oracle'lar; ama fonksiyonel "doğru" tanımı dar (ör. UCI dışı özellikler ölçülmüyor).
Key Takeaway:
- Dilden bağımsız, black-box oracle hiyerarşisi (exact → ordinal) olan domain'ler, reference-free repo-generation değerlendirmesi için iyi bir şablon.
- Agent self-validation'ı (self-Elo) güvenilmez; bağımsız harness ve cheating audit şart.

### FeatLens — FeatLens: Feature-Guided Dynamic Code Graph Construction and Retrieval for Repository-Level Code Generation (preprint, 2026) [arxiv:2609.26480]
Method. Repo içinde hedef fonksiyonu üretirken bağımlılıkları retrieve etmek için feature index (NL feature açıklaması → fonksiyon entity'leri) + task-specific seed graph + personalized PageRank ile kompakt reasoning graph kuruyor; retrieval sırasında LLM token'ı yok. DevEval (90 repo, Python) üzerinde Pass@1 ve DIR@1 (dependency invocation rate); EvoCodeBench (5 repo) sadece retrieval (DR@k) için, çünkü runtime yok. Modeller: DeepSeek-V3.2, GPT-5-mini; baseline'lar BM25, UniXcoder RAG, RepoGraph, CodexGraph.
Findings:
- DR@15: 0.501 (DevEval), 0.460 (EvoCodeBench); CodexGraph 0.430.
- DevEval Pass@1: 42.24% (DeepSeek-V3.2), 55.03% (GPT-5-mini) — CodexGraph'a göre GPT-5-mini'de hafif düşük (56.35%), UniXcoder RAG ile yakın.
- Graph node'ları %61, edge'ler %86, toplam token %45.9 azalıyor.
Relevant Limitations:
- Fonksiyonel kazanç marjinal; asıl kazanç retrieval recall'da ve kod uzunluğunda.
- Tek dil (Python), EvoCodeBench'te execution yok; DevEval alt kümesi filtrelenmiş (dependency annotation'ı tam olanlar).
Key Takeaway:
- Contextual tier için tipik bir retrieval method'u; test-based Pass@1 raporlanıyor ama ölçülen asıl şey dependency reuse.

### PROOF — From Reading Code to Reading Spec: A Verified Layer for LLM-Driven Codebase Maintenance (preprint, 2026) [arxiv:2609.06383]
Method, peripheral: asıl hedef spec üzerinden codebase maintenance (out of scope), ama raporlanan değerlendirmenin tamamı in-scope: kodtan hiyerarşik NL Spec çıkar (call graph topolojisini koruyarak), sonra source'a erişmeden repo'yu yalnızca Spec'ten yeniden inşa et ve orijinal test suite'le doğrula (round-trip).
Veri: üç SWE-bench repo'su — Flask (24 dosya, 9.5K satır, 491 test), Seaborn (54 dosya, 29K, 2,381 test), Pytest (81 dosya, 38K, 4,224 test). Model: "Claude 5 Sonnet". Baseline IR'lar: RepoAgent, RPG-Encoder, EPAM. Metrikler: test pass rate (Pass@1→Pass@3, failure-driven repair turları), AST similarity (pycode_similar), 21 fonksiyon üzerinde 3 insan + LLM-judge ile Spec kalitesi.
Findings:
- Pass@3: Flask 100%, Seaborn 100%, Pytest 96.8%; Seaborn'da RepoAgent 51.3%, RPG-Encoder 38.9%.
- Pytest'te bütün yöntemler Pass@1 ≈ 0% (sıkı coupling'de integration hataları yayılıyor), repair turlarıyla 91.24%'e çıkıyor.
- AST similarity 87–96%.
Relevant Limitations:
- Sadece 3 repo, hepsi Python ve SWE-bench'ten: contamination riski çok yüksek (model Flask/Pytest'i ezbere biliyor olabilir), bu da "Spec yeterli" iddiasını zayıflatıyor.
- Repair turları test failure'larını kullanıyor; "test isolation" iddiasına rağmen feedback test sonuçlarından geliyor.
- AST similarity reference'a coupling; alternatif tasarımları cezalandırır. Update fazı (asıl motivasyon) nicel olarak değerlendirilmemiş.
Key Takeaway:
- Code→Spec→Code round-trip, behavioral reconstruction için doğal bir oracle veriyor (orijinal test suite); ama fresh, contamination-free repo'lar olmadan anlamlı değil.

### PlayCoder — PlayCoder: Making LLM-Generated GUI Code Playable (preprint, 2026) [arxiv:2604.19742]
Benchmark + method. PlayEval: 43 GUI uygulaması (Python/JS/TS; oyunlar, emulator, desktop widget'lar), repo içinde fonksiyon üretimi: input = function signature + LLM-üretimi (GPT-4o-mini) requirement + repo context + düzenlenecek dosya. Değerlendirme zinciri Exec@k → Pass@k (LLM-generated unit test'ler, orijinal testlerin coverage'ı düşük: %47 line) → Play@k (PlayTester: screenshot + mouse/keyboard ile oynayan LLM agent). PlayCoder = PlayDeveloper + PlayTester + PlayRefiner repair loop'u.
Findings:
- 10 LLM'de Play@3 tek hanede; en iyi base model Claude-Sonnet-4 Python'da Play@3 9.9%.
- PlayCoder: Claude-Sonnet-4 ile 36.8% Exec@3 / 20.3% Play@3; GPT-5-mini ile 26.8% / 9.8% (DeepCode 17.9% / 6.4%).
- PlayTester insan yargısına karşı %16 false-negative, %5 false-positive (Krippendorff α=0.79).
Relevant Limitations:
- Requirement'lar ve unit test'ler LLM tarafından reference implementasyondan türetiliyor; verdict de LLM agent → ölçümün büyük kısmı LLM içinde, white-box coupling var.
- Sayılar tutarsız: 43 uygulama vs Fig. 2'de "4,159 instances, 35 repositories".
Key Takeaway:
- GUI/game kodunda unit test ile davranışsal doğruluk arasındaki uçurum büyük; interaktif agent-based oracle faydalı ama güvenilirliği (%16 FN) raporlanmalı.

### ReactGH200 — React-ing to Grace Hopper 200: Five Open-Weights Coding Models, One React Native App, One GH200, One Weekend (preprint, 2026) [arxiv:2604.17187]
Küçük ölçekli empirical study. Beş open-weights model (Kimi-K2.5 Q3 ve Q4, GLM-5.1, Qwen3-Coder-480B, DeepSeek-V3.2; Unsloth GGUF, llama.cpp) aider whole-edit modunda tek prompt'la multi-file React Native (Expo) app üretiyor: "create react-native app that allows user to create account and login and then count kangaroos seen per day and make sure it runs on the web". Değerlendirme: `npm install && npx expo start --web` ile out-of-the-box çalışma + manuel feature checklist (auth, per-user isolation, per-day counting, history, logout, web-safety).
Findings:
- Tam spec-uyumlu tek app Kimi-K2.5 Q3'ten; SWE-Bench Pro SOTA'sı GLM-5.1 Firebase config gerektirdiği için çalışmıyor; DeepSeek-V3.2 çoğu feature'da başarısız.
- Hiçbir model `Alert.alert`'in web'de no-op olduğunu hesaba katmıyor (5/5).
- Reasoning token'ları (`</think>`) aider'ın file-path parser'ına sızıp App.js'i yanlış path'e yazdırıyor; temperature=0 reasoning modellerde hang'e yol açıyor.
Relevant Limitations:
- n=1 task, 1 seed, tek stack, re-prompt yok; SWE-Bench rank'ları ile "mispredict" iddiası istatistiksel olarak desteklenemez.
- Değerlendirme yazarın manuel checklist'i; test yok, rubric önceden tanımlı değil gibi.
Key Takeaway:
- Anekdot düzeyinde ama "runs out-of-the-box" + feature-level kontrolün patch-based benchmark'larda görünmeyen integration/platform hatalarını yakaladığını gösteriyor.

### ReCUBE — ReCUBE: Evaluating Repository-Level Context Utilization in Code Generation (preprint, 2026) [arxiv:2603.25770]
Benchmark + method. Gerçek repo'da maskelenmiş bir Python dosyasını, kalan kaynak dosyalar + dependency spec + dokümantasyonla yeniden inşa etme (prompt-free: NL task tanımı yok). 20 repo (Ocak 2025 sonrası oluşturulmuş, contamination'a karşı), functional subset'lere bölünmüş, 366 instance; RECUBE-LARGE 6 repo / 138 instance, 338K token'a kadar context. 10,785 usage-aware unit test (Claude Opus 4.1 üretimi, gold'da geçtiği Docker'da doğrulanmış; %58.7 external cross-file, %41.3 internal). Metrikler: Strict Pass Rate, Average Pass Rate. Ayarlar: full-context, +CoT, mini-SWE-agent, agent + CCE (caller-centric dependency graph toolkit).
Findings:
- En iyi model GPT-5 full-context'te yalnızca 37.57% SPR.
- Agentic exploration dar context'te faydalı, context büyüdükçe avantajı kayboluyor/tersine dönüyor.
- CCE: full-context'e göre +5.79%, vanilla agent'a göre +7.56% SPR.
- Hard task'larda caller coverage ile APR arasında anlamlı korelasyon (ρ=+0.408).
Relevant Limitations:
- Test'ler LLM üretimi ve gold dosyadan türetilmiş; internal test'ler private fonksiyon/implementasyon detayını kontrol ettiği için alternatif tasarımları cezalandırır (white-box coupling).
- Tek dil (Python), 20 repo.
Key Takeaway:
- File-level reconstruction, "repo context'i kullanma" yeteneğini NL spec'ten ayrıştırmanın temiz bir yolu; external vs internal test ayrımı reference coupling'i ölçmek için kullanılabilir.
