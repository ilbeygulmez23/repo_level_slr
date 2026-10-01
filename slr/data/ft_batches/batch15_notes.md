### SaaSBench — SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering (preprint, 2026) [arxiv:2605.17526]
Benchmark + empirical çalışma: agent'a uzun bir PRD (~4,363 satır ortalama) + ambiguity-resolution KB veriliyor, izole bir Docker ortamında sıfırdan çalışan, deploy edilmiş bir enterprise SaaS sistemi (frontend + backend + DB + auth) kurması isteniyor.
30 task, 6 SaaS domain; PRD'ler gerçek open-source seed repo'lardan (annotator + Cursor ile) tersine çıkarılmış. 8 dil, 6 DB, 13 framework. Değerlendirme DAG tabanlı: 5,370 validation node, 6,167 prerequisite edge; her node HTTP request / login / rubric-LLM-judge primitive zinciri. Skorlama binary / weighted / llm-as-judge (Claude Sonnet 4.5, temp 0); prerequisite başarısızsa node "Skipped dependency". Metrikler: Pass@1 ve Node Coverage, 6 capability dimension (Deploy, Data, API, Logic, AuthZ, Quality). Referans implementasyon tüm test suite'i geçmek zorunda.
Findings:
- En iyi: Claude Opus 4.7 + Claude Code %20.68 Pass@1; ortalama Claude Code %11.64, OpenHands %9.26.
- 480 capability unit analizinde %63.5'te stack hiç stabil çalışmıyor, %32.1 yüzeysel erişilebilir ama yapısal eksik; yalnızca %3.8'de business logic darboğaz — hataların >%95'i derin mantığa ulaşmadan.
- Harness etkisi büyük: aynı model Claude Code / Codex CLI'da OpenHands'ten daha iyi.
- Daha çok adım ≠ daha iyi: GPT-5.4 36 adımda %7.44, MiniMax M2.7 279 adımda %6.78.
Relevant Limitations:
- PRD'ler seed repo'dan reverse-engineer edilmiş, API contract'lar ve data model PRD'de sabit — test suite referans repo'ya kuplajlı; alternatif tasarımlar (farklı endpoint şekli) cezalandırılabilir.
- LLM-judge ölçümün içinde (layout vb. node'lar); judge Claude ailesi, en iyi sonuç da Claude — aile yanlılığı kontrol edilmemiş.
- Yalnızca 30 task; seed repo'lar popüler GitHub projeleri → contamination riski tartışılmıyor.
Key Takeaway:
- Uzun-horizon app üretiminde asıl darboğaz kod mantığı değil, çok bileşenli sistemi ayağa kaldırma/entegrasyon; DAG + dependency gating, erken hataların downstream'i kirletmesini engelleyen iyi bir değerlendirme deseni.

### SecRepoBench — SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories (LLM4Code 2026, 2026) [arxiv:2504.21205]
Benchmark: 27 C/C++ repo'da 318 secure code completion task'ı (15 CWE); bir fonksiyon içindeki maskelenmiş, güvenlik-hassas bölgeyi repo context'iyle doldurma.
ARVO (OSS-Fuzz) vulnerability-fix commit'lerinden türetiliyor; açıklamalar GPT-4o + manuel düzenleme, contamination için değişken yeniden adlandırma. Correctness: developer-written relevant unit test'ler; security: OSS-Fuzz PoC crash. Metrikler: pass@1, secure-pass@1, secure %. 29 standalone LLM (BM25 top-5 fonksiyon) + 15 agent (Aider, OpenHands, Claude Code).
Findings:
- En iyi standalone GPT-5 %39.3 secure-pass@1; en iyi agent OpenHands + o3 %53.5.
- Agent kazancı ağırlıkla correctness'tan (örn. OpenHands + GPT-5 +%25.5 pass@1, sadece +%4.7 secure %).
- BaxBench'e göre tüm modeller belirgin daha düşük; model sıralaması değişiyor.
Relevant Limitations:
- Görev fonksiyon-içi küçük bölge; repo üretimi değil, sadece contextual.
- Security oracle tek bir PoC — başka zafiyetleri görmüyor; unit test'ler referans patch'in geçtikleri.
Key Takeaway:
- Repo-bağımlı generation'da correctness ve security ayrı eksenler; agent'lar birincisini iyileştiriyor, ikincisini pek değil.

### SolAgent — SolAgent: A Specialized Multi-Agent Framework for Solidity Code Generation (preprint, 2026) [arxiv:2601.23009]
Method: Solidity için tool-augmented multi-agent; inner loop Forge compile+test, outer loop Slither static analysis, file-system tool'larıyla proje bağımlılıklarını çözme; trajectory'lerle Qwen3-8B distillation.
Değerlendirme SolEval+ üzerinde: SolEval'in repository-aware function-level verisinden file-level'a çevrilmiş 81 dosya, 1,188 manuel gözden geçirilmiş Foundry testi. Metrikler: compile rate, Pass@1 (geçen test oranı), gas, Slither vulnerability sayısı. Baseline'lar: vanilla LLM, Copilot, DeepCode, MetaGPT, Qwen-Agent (Claude Sonnet 4.5, GPT-5-Mini, GPT-5.1).
Findings:
- Claude Sonnet 4.5 ile %64.39 Pass@1 (vanilla %25.59, en iyi agent baseline Qwen-Agent %28.37); compile rate %95.06.
- Slither bulguları insan koduna göre %15.70 (Claude) – %39.77 (GPT-5-Mini) daha az.
- Distillation zayıf: Qwen3-8B %0.33 → %1.31 Pass@1.
Relevant Limitations:
- Testler yazarların kendi yazdığı; Slither hem refine döngüsünde hem metrikte — metric gaming riski.
- Test set sadece 81 dosya; distillation sonuçları pratikte anlamsız düzeyde.
Key Takeaway:
- Domain-özel compiler/analyzer feedback'i repo-bağlamlı generation'da genel agent'lardan çok daha belirleyici.

### SpecFirst — SpecFirst: Behavioral Specification Elicitation as a First-Class Step in Agent-Based Program Synthesis from Scratch (preprint, 2026) [arxiv:2607.27167]
Method + empirical: ProgramBench (NL doc + execute-only binary → sıfırdan davranışsal olarak eşdeğer program) üzerinde, kodlamadan önce ayrı bir spec agent'ın binary'yi probe edip yapılandırılmış SPEC.md üretmesini zorunlu kılan iki aşamalı pipeline.
Spec agent doc + binary ile black-box probing yapıyor; code synthesis agent (mini-SWE-agent, baseline ile aynı scaffold) doc + binary + SPEC.md alıyor. Dil ve mimari agent'a bırakılmış. Değerlendirme: 200 instance'ın tamamı, gizli test suite (binary çıktısıyla exact match) üzerinden ortalama test pass rate; ek olarak probing line coverage. Modeller: Qwen3.5-397B, Qwen3.6-35B, GPT-5.5-high, GPT-5.4-mini. Wilcoxon testi.
Findings:
- Pass rate artışı %6.9–21.3 (relatif), hepsi p<0.01; GPT-5.5-high %59.02 → %65.14, W/L/T 150/38/12.
- ≥%90 pass rate'e ulaşan program oranı %5.5 → %16.5 (GPT-5.5-high); Hard tier'de %30.8 → %40.0.
- Binary exploration coverage +%9.4–18.5; spec ile agent koda daha erken başlıyor.
- Maliyet +%48–130 per instance ($0.25–3.16 ek spec fazı).
Relevant Limitations:
- Differential oracle strict string eşleşme: format farkı olan doğru davranış cezalı.
- Baseline ek bütçe almıyor; iyileşmenin bir kısmı sadece daha fazla compute olabilir (cost-matched karşılaştırma yok).
- SPEC.md free-form markdown; executable/structured artefakt değil. Aynı model hem spec hem kod yazıyor.
- Tam resolved oranı raporlanan ana metrik değil; ortalama pass rate'e odaklı.
Key Takeaway:
- Requirements elicitation'ı ayrı faz yapmak from-scratch reconstruction'da model-agnostik kazanç; hand-off artefaktının yapısı (spec) doğrudan sonucu etkiliyor — structured spec'ler için güçlü motivasyon.

### State, Not Tokens — State, Not Tokens: Repository-Scale Agent Reasoning Is Bound by State Architecture (preprint, 2026) [doi:10.5281/zenodo.20709565]
Full text yok; not sadece abstract'a dayanıyor. Controlled empirical/method çalışması: repository-ölçekli agent başarısını context uzunluğu değil, worker'lar arası state akış mimarisinin belirlediğini iddia ediyor.
Görev: JavaScript → TypeScript whole-repo migration; oracle strict tsc + immutable test'ler + escape hatch yasağı. Üç kol: tek-context monolith, her tamamlanan dependency layer'ı paylaşılan ağaca commit eden "durable" kol, ve birbirinin sonucunu görmeyen stateless-RAG per-file worker'lar. Model, tool, scaffold ve oracle sabit. Ek olarak NL2Repo-Bench üzerinde harici doğrulama.
Findings:
- NL2Repo-Bench'te %91.1 ortalama test-pass rate raporluyor (yayınlanmış ~%40 SOTA'nın ~2.28 katı).
- Migration kolları arası sayısal sonuçlar abstract'ta verilmemiş.
Relevant Limitations:
- Tek yazarlı Zenodo deposit, peer review yok; NL2Repo sonucu olağanüstü yüksek ve protokol farklılıkları (bütçe, model, test erişimi) abstract'tan doğrulanamıyor.
- JS→TS migration mevcut repo üzerinde in-place bir dönüşüm; tam repo-translation'a göre görece kolay (TS, JS'in superset'i).
- Kaç repo, hangi model kullanıldığı bilinmiyor.
Key Takeaway:
- Bağımlılık katmanlarını committed artefakt olarak biriktirmek (structured state hand-off) iddiası survey için ilginç; ancak full text okunmadan kanıt değeri düşük — tam metin bulunmalı.

### SWE Refactor Bench — SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration? (preprint, 2026) [arxiv:2608.23564]
Benchmark + empirical: 20 gerçek open-source repo'nun (SQLite, zlib, libsodium, GraphHopper vb.) tamamının başka bir stack'e taşınması; 7'si language rewrite (C→Rust, C→Java, Go→Zig), 7 framework, 3 platform, 3 build toolchain. Survey açısından ilgili kısım language rewrite alt kümesi (repo-translation).
Agent offline container'da orijinal repo + hedef stack toolchain ile 6–30 saat çalışıyor. Üç aşamalı değerlendirme: (1) Migration Audit — LLM judge (gpt-5.6-sol, 3 örnek majority) eski stack'in gerçekten kalktığını denetliyor; (2) Behavioural Tests — orijinalden kaydedilmiş 130,118 fixed check (differential); (3) Agentic Verification — 6 bağımsız coding agent 1'er saat orijinal vs migrated arasında counterexample test üretiyor. 8 model, 26 model–effort config, 520 run (Claude Code / Codex harness).
Findings:
- Sadece 28/520 run (%5.4) üç aşamayı geçiyor; 13/20 task hiç çözülmüyor; en iyi claude-opus-5 47.0/100.
- Language rewrite en zor: skor 5.6, Stage II geçişi 12/100, yalnızca 4 kabul.
- 30 run "Blindness": migration yapmadan tüm fixed check'leri geçiyor; fixed suite'i tam geçen 88 run'ın 60'ı agentic verifier'larca kırılıyor.
- Judge–insan uyumu %89.7 (κ=0.795), hatalar çoğunlukla aşırı katılık yönünde.
Relevant Limitations:
- Mixed benchmark: repo-translation yalnızca 7 task; kalan 13 task in-place migration.
- Ölçümde LLM (Stage I judge) ve LLM-generated testler (Stage III) var; judge değerlendirilen sistemlerden biri (self-family bias analiz edilmiş).
- Behavioural check'ler orijinal çıktıya kuplajlı; doğru ama farklı format cezalı.
Key Takeaway:
- Behaviour-only değerlendirme translation'da "hiç çevirmeme" hack'ine açık; migration completeness ayrı gate olmalı. Agentic differential test üretimi fixed suite'in kaçırdığını yakalıyor.

### TDD-Agent — TDD-Agent: Test-Driven Reasoning for Code Generation (preprint, 2026) [arxiv:2608.16742]
Method: model önce executable test yazıyor, sonra kod ve testi execution feedback ile birlikte iteratif rafine ediyor (dual-track). Function-level etkisi LiveCodeBench'te TDD-prompt ile, repo-level etkisi RepoEval'de ölçülüyor.
RepoEval function-level alt kümesi, 8 GitHub repo, her repo için Docker; üretilen fonksiyon repoya konup ilgili unit test'ler çalıştırılıyor. Modeller GPT-5-mini, DeepSeek-V3.2, Qwen3-Coder-30B-A3B; baseline'lar In-File, RAG, RepoCoder, mini-SWE-agent.
Findings:
- 10 iterasyonda pass rate: GPT-5-mini %78.24 (mini-SWE-agent %61.31), DeepSeek %90.77 (%84.18), Qwen %59.34 (%52.97).
- 5. iterasyonda token kullanımı mini-SWE-agent ile benzer; iterasyonla üretilen testlerin coverage/mutation skoru da artıyor.
Relevant Limitations:
- RepoEval sadece 8 Python repo, eski ve muhtemelen contaminated.
- Baseline RAG yöntemleri agent değil; asıl adil kıyas mini-SWE-agent ile sınırlı.
Key Takeaway:
- Testi post-hoc validator değil ara spesifikasyon olarak kullanmak repo-bağlamlı generation'da tutarlı kazanç sağlıyor.

### TICoder — TICoder: A Repository-Level Code Generation Framework with Test-Driven Planning and Implementation-Aware Reuse (preprint, 2026) [arxiv:2606.08135]
Method: repo-level fonksiyon üretimi için test-driven iterative planning (LLM planner + LLM judge, eşik 90) ve dual-view (fonksiyonel + implementasyon) similarity ile callee retrieval + clustering/perplexity ile usage pattern seçimi.
Değerlendirme CoderEval (230 Python/43 proje, 230 Java/10 proje) ve DevEval (1,825 Python/115 proje) üzerinde Pass@1/3/5; backbone GPT-4o-mini, DeepSeek-V3, Qwen2.5-Coder-7B; baseline'lar RepoCoder, A3CodGen, AllianceCoder, RLCoder, RepoScope.
Findings:
- Ortalama ~%11 iyileşme; DevEval GPT-4o-mini Pass@1 %31.01 (AllianceCoder %25.26), DeepSeek-V3 %43.29.
- Ablation: generation'dan test case'leri çıkarmak Pass@1'i %10.42 düşürüyor.
Relevant Limitations:
- Planning ve generation'a verilen test case'lerin kaynağı net değil; benchmark'ın değerlendirme testleriyle aynıysa ciddi leakage.
- Baseline'lar RAG-only, agent baseline yok.
Key Takeaway:
- Test'i planning girdisi yapmak etkili, ama test'in oracle ile aynı olup olmadığı raporlanmazsa kazanç yorumlanamaz.
