### RUCCE / RUCACoder — Beyond Maintenance: A Benchmark and Multi-Agent Framework for Repository-Usage Code Generation (ACM proceedings, 2026) [doi:10.1145/3805712.3808589]
Benchmark + method. Full text yok; not abstract üzerinden. Maintainer-centric (bug fix, feature) değil, "repository usage" senaryosu: dış kullanıcı repo-internal API'leri çağırarak runnable end-to-end script yazıyor.
Her instance: NL usage instruction + grounded target API'ler + verified reference script; gerçek Python repolarından. Hem API retrieval hem script generation ölçülüyor. RUCACoder: Retriever (hiyerarşik repo exploration), Verifier (rerank + validation), Coder (feedback-driven synthesis) closed-loop.
Findings:
- Abstract'a göre RUCACoder birden çok backbone LLM'de retrieval ve generation baseline'larını tutarlı şekilde geçiyor; sayı verilmiyor.
Relevant Limitations:
- Değerlendirmenin execution-based olup olmadığı abstract'tan net değil; "verified reference script" referansa bağlı (similarity veya output eşleşmesi) bir oracle'a işaret edebiliyor.
- Repo ve instance sayısı, kullanılan modeller raporlanmamış (abstract düzeyinde).
Key Takeaway:
- Contextual tier'ın "kullanıcı tarafı" varyantı: repo değiştirilmiyor, repo'nun API'leri üzerine yeni dosya yazılıyor — repo-level generation'da retrieval'ın önemini ayrı ölçmek için iyi bir kurgu. Full text ile eval doğrulanmalı.

### ChainBench — ChainBench: An LLM Benchmark for Cross-Chain Code Generation (preprint, 2026) [doi:10.5281/zenodo.20265206]
Benchmark + empirical. Full text yok; not abstract üzerinden. Production smart-contract repolarından cross-chain contract translation ve contract generation görevleri.
Her task structured spec + containerized environment veriyor; sistem eksik functionality'yi implemente edip repo'nun mevcut verification suite'ini geçmeli. Metrik Pass@1 task success. 42 task; EVM Solidity, NEAR Rust, Aptos Move, Sui Move, Starknet Cairo. 9 model-agent sistemi, hem aynı harness hem "preferred harness" koşularında zero-shot.
Findings:
- En iyi sistem %88.1 success; birkaç open-weight sistem %52–60, çok daha uzun solve süreleriyle.
- Performans hedef chain'e ve task tipine göre değişiyor; hatalar dar behavioral mismatch'lerden (eksik edge-case guard) build/repo-compatibility sorunlarına kadar.
Relevant Limitations:
- 42 task küçük ölçek; bağımsız repo sayısı abstract'ta yok.
- Preferred-harness koşuları model ve harness etkisini karıştırıyor.
- Tests mevcut repo'nun kendi suite'i — gerçek oracle ama "eksik parçayı doldur" formatı EC1 sınırına yakın.
Key Takeaway:
- Az kaynaklı diller (Move, Cairo) için repo-bağımlı, test-tabanlı değerlendirme örneği; dil çeşitliliği lens'i için değerli.

### CITL — Compiler-in-the-Loop Code Generation: A validation-first agent architecture for type-safe multi-file software synthesis (preprint, 2026) [doi:10.5281/zenodo.22769026]
Method, PoC report. Full text yok; not abstract üzerinden. Agent multi-file TypeScript projesi üretiyor, diske yazmadan önce in-memory virtual project üzerinde TypeScript compiler ile doğruluyor.
Input: NL task (Express/JWT REST API) → output: multi-file TS proje. Diagnostics source context ve declaration summary ile zenginleştirilip revizyona geri besleniyor. Dört strateji aynı DeepSeek modeliyle karşılaştırılıyor: one-shot, Cline-style reactive terminal loop, batch-CITL, filewise-CITL. Metrik: dışarı sızan tsc hataları, LLM call sayısı, temiz `tsc --noEmit`.
Findings:
- One-shot 12 external TS hatası sızdırıyor; reactive loop 3 call'da düzeliyor ama 12 compiler failure'ı terminal loop'a gösteriyor.
- Batch-CITL 3 call'da 0 leaked error ile temiz build; filewise-CITL de 0 hata ama 8 call.
Relevant Limitations:
- Tek task, tek model, "observed run" — istatistiksel değil, anekdot düzeyinde.
- Sadece derleme doğruluğu; functional correctness (test, API davranışı) ölçülmüyor.
- Type-check tek başına cross-file contract drift'in yalnızca statik kısmını yakalıyor.
Key Takeaway:
- Validation'ı agent loop'un içine (kullanıcıya görünmeden) yerleştirme fikri: hand-off'ta compiler'ın executable artefakt olarak kullanımı. Kanıt çok zayıf; benchmark üzerinde tekrar edilmeli.

### HiRAS — HiRAS: A Hierarchical Multi-Agent Framework for Paper-to-Code Generation and Execution (preprint, 2026) [arxiv:2604.17745]
Method + evaluation protocol. Paper → experiment reproduction repository; fixed sequential pipeline (PaperCoder, AutoReproduce) yerine proaktif manager agent'lar alt agent'ları (planning, architecture design, dependency modelling, config, analysis, coding, execution) denetleyip yeniden çağırıyor.
Shared workspace + file-system tools, smolagents scaffold. Benchmark: PaperBench (20 ICML 2024 paper, rubric) ve Paper2Code (90 paper; ICML/NeurIPS/ICLR 2024). Backbone: Qwen3-Coder-480B, DeepSeek-v3.1-Terminus, ek olarak Claude-Sonnet. Değerlendirme tamamen LLM-judge: PaperBench'te o3-mini-high ve GPT-4o-mini, Paper2Code'da o3-mini-high (1–5 skala). Ayrıca P2C-Ex: repo file count + yapı bilgisi eklenmiş reference-free judge prompt'u.
Findings:
- PaperBench-CodeDev: HiRAS 64.1% (Claude-Sonnet), 57.4% (DeepSeek-v3.1) vs PaperCoder 51.1% (Claude-Sonnet). Full PaperBench (execution dahil) skorları düşük: 19.1 / 21.5%.
- Orijinal Paper2Code reference-free judge boş repoya 3.89, sadece config içeren repoya 4.67 veriyor; P2C-Ex reference-based ile Pearson r'yi 0.423'ten 0.862'ye çıkarıyor; 30 paper'lık insan anotasyonunda r=0.72 (inter-annotator 0.82).
- Ablation: hierarchical supervision tek başına ~%10 katkı.
- Başarısızlık çoğunlukla execution'da (inter-file import hataları, env setup): 110 koşudan yalnızca 3'ü code generation aşamasında düşüyor; bir örnekte skor 69.7% → 11.3%.
Relevant Limitations:
- Ölçüm tamamen LLM-judge; judge hallucination'ı paper'ın kendisi gösteriyor, P2C-Ex de hâlâ LLM.
- Reference-based metrik gold repo'ya bağlı, alternatif tasarımları cezalandırabilir.
- Baseline'lar yazarlar tarafından yeniden koşulmuş; ölçek 110 paper, sadece ML/Python.
Key Takeaway:
- Paper-to-repo'da darboğaz kod yazmak değil çalıştırmak; judge'ın repo yapısını görmemesi skorları şişiriyor — structural bilgi judge'a verilmeli.

### CodeCraft — Hybrid Multi-Agent Framework for Enterprise Web Application Generation (preprint, 2026) [doi:10.20944/preprints202608.1294.v1]
Method. Full text yok; not abstract üzerinden. Enterprise CRUD web app üretiminde schema/backend/frontend tutarsızlığına karşı hibrit yaklaşım: yapısal kod deterministik generator'larla, sadece belirsiz kararlar LLM ile.
Prisma schema ve DMMF temsili tek source of truth; deterministik generator'lar backend API, frontend manifest, RBAC ve DB seeder üretiyor. LangGraph üzerinde 6 agent (requirements engineering, schema design, orchestration, backend, frontend, containerization) yalnızca requirement netleştirme, schema validation ve yapısal olmayan kararlar için. Output: deploy edilebilir containerized uygulama.
Findings:
- Schema validation, schema düzeltme için gereken otomatik iterasyonu 2–4'e indiriyor.
- Requirement ve schema onayından sonra end-to-end generation manuel emek olmadan deploy edilebilir uygulama üretiyor.
- Geliştirme eforunda %70–80 azalma iddiası — yazarların kendisi kontrollü dış çalışmayla doğrulanmadığını belirtiyor.
Relevant Limitations:
- Değerlendirme zayıf: benchmark, baseline, functional test veya kullanıcı çalışması abstract'ta yok; kaç uygulama denendiği belirsiz.
- Hand-off structured (Prisma schema) — güçlü yön, ama kapsam CRUD tipi uygulamalarla sınırlı.
Key Takeaway:
- Structured, executable artefakt'ı (schema) tek source of truth yapıp LLM'i dar kararlara hapsetmek, cross-layer tutarlılık için ilginç bir tasarım; ampirik kanıt eksik.

### JamBench / JamSet — JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines (preprint, 2026) [arxiv:2606.19830]
Benchmark + training data. Godot engine üzerinde project-level oyun kodu üretimi; Game Jam projelerinden toplanmış veri ve deterministik headless-engine doğrulama pipeline'ı.
~240K aday repodan (Ludum Dare, itch.io, GGJ, GitHub vb.) Godot 4.x, 2D, ≥1,200 game line filtresi ve L1 (file integrity) / L2 (headless compile) / L3a (30 sn runtime stability) / L3b (60 sn deterministik input ile behavior collection) ile 8,133 doğrulanmış proje. 300'ü (S/M/L 100'er, 4K ve 15K satır eşikleri) elle oynanarak doğrulanmış JamBench; 7,833'ü multi-turn SFT verisi JamSet. Task 1: Game Jam theme'den (1a sadece keyword, 1b + gameplay description) sıfırdan proje, 50 theme × 3 run. Task 2: fonksiyon (2a), script (2b), tüm .gd (2c) silinmiş projeyi tamamlama. Metrikler: L1/L2/L3a pass rate, SCS (7 statik boyutta referansa oran), BAS (runtime davranış istatistiklerinin referansa benzerliği). Dil GDScript + .tscn.
Findings:
- Task 1a'da L3a ortalaması %70.7 ama SCS/BAS çok düşük (ör. GPT-5.4 SCS 0.46, BAS 0.17): derlenen ama minimal projeler.
- Task 2a runtime pass rate Small'da %80.4'ten Large'da %5.7'ye düşüyor; 2c Large'da çoğu model ~0.
- Claude Code agent modu pass rate'i artırıyor (Claude Task 1a L3a 77.3 → 82.7) ama SCS/BAS neredeyse değişmiyor (0.41 → 0.42; 0.11 → 0.13).
- Qwen3.5-27B JamSet SFT ile compile rate ve SCS'te iyileşiyor.
Relevant Limitations:
- SCS/BAS referans projeye (Task 2) veya dataset ortalamasına (Task 1) bağlı; farklı ama geçerli bir oyun tasarımı cezalandırılır, Task 1'de "doğruluk" aslında ölçülmüyor.
- eval_config LLM ile üretiliyor (input stratejisi için), yani ölçümde dolaylı LLM izi var.
- Açık kaynak Game Jam projeleri — contamination riski yüksek, tartışılmıyor.
Key Takeaway:
- Headless engine ile deterministik runtime behavior toplama, oyun gibi I/O'su olmayan domain'lerde LLM-judge'a alternatif; ama davranış benzerliği ≠ functional correctness.

### KGMACG — KGMACG: Knowledge-Guided Multi-Agent Orchestration for Scalable Application-Level Code Generation (TOSEM, 2026) [doi:10.1145/3842390]
Method. Full text yok; not abstract üzerinden. SRS + architectural design document (ADD) → application-level repository üreten üç agent'lı closed-loop framework.
COPA (Code Organization & Planning Agent) SRS/ADD'den modular build plan ve project skeleton çıkarıyor; Coding Agent beş-sütunlu bir knowledge base rehberliğinde repo-level kod yazıyor; Testing Agent sürekli unit test üretip failure trace'lerini geri besliyor. Döngü, proje derlenene ve ≥%95 requirement coverage sağlanana kadar sürüyor. Değerlendirme: üç endüstriyel-ölçek case study (E-Commerce, Campus Security, Stock Trading), MetaGPT, AutoGen, CAMEL, CrewAI, ChatDev, CodeAgent'a karşı; backbone DeepSeek R1 ve gpt-5-codex-medium.
Findings:
- Abstract yalnızca KGMACG'nin application-level geliştirme otomasyonunu "ilerlettiğini" söylüyor; sayısal sonuç, metrik adı verilmemiş.
Relevant Limitations:
- Sadece 3 case study; bağımsız benchmark yok.
- Testler ve requirement coverage sistemin kendi Testing Agent'ı tarafından üretiliyor gibi görünüyor — aynı model ailesi hem kodu hem oracle'ı üretiyor olabilir; full text ile doğrulanmalı.
- Dil/stack abstract'ta belirtilmemiş.
Key Takeaway:
- SRS+ADD gibi structured input ve requirement-to-code traceability, ChatDev/MetaGPT tipi free-form hand-off'lara karşı güçlü bir baseline karşılaştırması sunuyor; ekstraksiyon için full text şart.
