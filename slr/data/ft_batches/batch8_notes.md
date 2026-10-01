### CodeTeam — CodeTeam: An LLM-Powered Multi-Agent Framework for Repository-Level Code Generation (preprint, 2026) [arxiv:2606.22082]
Method çalışması: NL requirements dokümanından boş workspace'te tüm repoyu üreten multi-agent framework (NL2Repo). CodeS'in sketch paradigmasını uçtan uca bir workflow'a genişletiyor.
Birden fazla Architect agent rakip software design sketch (SDS) üretiyor (opsiyonel RAG ile), CTO agent birini seçip file ownership, public interface ve dependency constraint içeren "machine-checkable contract"a normalize ediyor; Developer agent'lar dependency-aware scheduler + Git tabanlı koordinasyonla dosyaları yazıyor, QA agent test koşturup repair döngüsü sürüyor. Backbone Qwen2.5-72B-Instruct (PE ve SFT varyantları). Ana değerlendirme SketchEval (19 Python repo, 5/8/6 easy/medium/hard) üzerinde SketchBLEU; NL2Repo-Bench (104 task, upstream pytest) "external validation" olarak kullanılıyor. Baseline'lar (Vanilla, ChatDev, AutoGPT, CodeS) aynı backbone ile yeniden koşturulmuş.
Findings:
- SketchBLEU: 51.7% (PE) / 60.9% (SFT); CodeS'e göre +4.1 / +2.9 puan.
- NL2Repo-Bench ortalama test pass rate 34.6% (PE) / 42.3% (SFT); ama Pass@1 sadece 5.1% / 6.1% — tam geçen repo neredeyse yok.
- Ablation: dynamic developer allocation kaldırılınca %9.9, RAG kaldırılınca %8.1 relatif düşüş; Git koordinasyonu %2.9.
- Failure analizi: packaging+import hataları CodeS'e göre azalıyor (34.2→22.1%, 28.7→19.4%), logic hataları oransal olarak artıyor.
Relevant Limitations:
- Ana metrik SketchBLEU referans implementasyona benzerlik; farklı ama geçerli mimarileri cezalandırır. Ablation'ların tamamı sadece SketchBLEU üzerinde.
- SketchEval sadece 19 repo, sadece Python; tüm deneyler tek backbone (Qwen2.5-72B), frontier model/agent (OpenHands vb.) yok.
- Contract structured bir artefakt (iyi), ama doğrulaması QA agent'ın kendi yazdığı lightweight testlere dayanıyor.
Key Takeaway:
- Planlama çıktısını makine-kontrol edilebilir bir kontrata dönüştürmek, cross-file interface tutarlılığı için somut bir hand-off tasarımı.
- Ortalama pass rate ile Pass@1 arasındaki uçurum, NL2Repo'da "kısmi doğruluk" metriklerinin tek başına yanıltıcı olabileceğini gösteriyor.

### DeepRepro — DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories (CIKM 2026, 2026) [arxiv:2608.26557]
Method (demo paper, 5 sayfa): ML paper'ından çalışan repo üretimi için, statik upfront plan yerine repo'nun güncel state'ine göre iteratif subplan üreten agent framework.
Paper → blueprint planning (figure/concept/algorithm sub-analysis agent'ları) → her round'da progress file + repository memory + diagnostics'ten subplan → execute agent dosya yazıyor → memory güncelleniyor. İki mod: fast ve deepplan (quality gate ile). Backbone GPT-5.4 (high reasoning); ablation'da executor DeepSeek-V4-Flash. Değerlendirme PaperBench Code-Dev (20 ICML 2024 paper), hiyerarşik rubric, LLM-judge (ana deneylerde maliyet için GPT-4.1-mini, insan karşılaştırmasında o3-mini). Kod çalıştırılmıyor.
Findings:
- 5-paper subset'te deepplan 84.22 vs fast 82.07; external code reference etkisi marjinal.
- Full 20 paper ortalaması 75.09 (DeepCode 73.6, PaperCoder 49.6, AutoReproduce 51.1 — bunlar önceki çalışmalardan alınmış).
- Subset'te Cursor 66.5, Codex 61 vs 84.2; human Best@3 72.4 vs 77.8 (paylaşılan subset).
- Maliyet ~US$10–12.5/paper, 1–1.5 saat.
Relevant Limitations:
- Değerlendirme tamamen LLM-judge rubric'i, Code-Dev modunda execution yok; judge da ucuz bir model (GPT-4.1-mini), PaperBench'in orijinal judge ayarından farklı.
- Full-set baseline sayıları başka makalelerden alınmış (yazarlar da "strict değil" diyor); controlled karşılaştırma sadece 5 paper.
- Demo formatı: istatistiksel test, varyans, failure analizi yok.
Key Takeaway:
- Paper-to-repo'da plan–state senkronizasyonu (repo memory + diagnostics'e göre re-planning) önemli bir tasarım ekseni.
- Rubric-LLM-judge'a dayalı reproduction benchmark'larında judge seçimi sonuçları doğrudan etkiliyor; survey'de ayrıca işaretlenmeli.

### DeNovoSWE — DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch (preprint, 2026) [arxiv:2606.10728]
Training-data + method çalışması: dokümandan tüm repoyu üretme (doc2repo) için 4,818 instance'lık, otomatik kurulmuş, doğrulanabilir bir eğitim ortamı/dataseti ve bununla SFT edilmiş agent.
Scale-SWE ile Docker ortamı kurulan GitHub Python repolarından (test pass ≥90%, coverage ≥50% filtresi) başlanıyor. Divide: capability decomposition + test'lerin runtime trace'i ile "direct / core indirect" bileşen profiling; Conquer: draft–critic–repair agent döngüsüyle capability bazlı dokümantasyon (GPT-5.4/5.5). Eval: kaynak kod ve testler silinmiş, git geçmişi sıfırlanmış, network/pip erişimi kısıtlanmış ortamda orijinal unit test pass ratio. Trajectory'ler DeepSeek-V4-Pro ile OpenHands'te üretiliyor, difficulty-aware eşiklerle (0.90→0.60) filtreleniyor, ~11k trajectory ile Qwen3-30B-A3B ve Qwen3.5-35B-A3B SFT.
Findings:
- Qwen3-30B-A3B: BeyondSWE-Doc2Repo 5.8→47.2%, NL2Repo 4.3→23.0% (issue-level Scale-SWE-Agent: 29.2 / 18.3%).
- Qwen3.5-35B-A3B: 43.8→50.0% ve 23.5→27.1%; Gemini3-Pro'ya (52.0) 2 puan yakın.
- Difficulty-aware filtre sabit eşiğe göre küçük ama tutarlı kazanç (0.488→0.500 Doc2Repo).
- Dataset: median 79 unit test, testler median 9 kaynak dosyaya dokunuyor, ortalama coverage 85.5%.
Relevant Limitations:
- Spec reverse-engineered: dokümanlar referans repo ve onun testlerinden LLM ile türetiliyor; test'lerin import ettiği API'ler dokümanda zorunlu kılınıyor → white-box testlere ve referans arayüze sıkı bağlılık.
- Aynı model ailesi (GPT-5.x) dokümanı yazıyor, critic'liyor, difficulty'yi puanlıyor ve cheating'i denetliyor; spec kalitesine dair bağımsız insan doğrulaması raporlanmamış.
- Sadece Python; eğitim reposu ile benchmark repoları arasında overlap/contamination analizi yok.
- Ablation sadece filtreleme stratejisi üzerine; dokümantasyon pipeline'ının katkısı ayrıca ölçülmemiş.
Key Takeaway:
- Doc2repo'yu RL/SFT ölçeğine taşımanın yolu: mevcut test'li repolardan spec türetip, leakage'ı sandbox ile kapatmak.
- Kısmi pass ratio'lu trajectory'leri difficulty'ye göre tutmak, uzun-horizon görevlerde veri çeşitliliği için kritik.

### Hydra — Do Not Treat Code as Natural Language: Implications for Repository-Level Code Generation and Beyond (FSE 2026, 2026) [arxiv:2602.11671]
Method: repository-level function generation için RAG retriever; kodu chunk'lanmış metin yerine yapısal birim (function/class/variable) ağacı olarak indeksliyor.
Structure-aware indexing + fine-tune edilmiş hafif dependency-aware retriever (DAR, threshold 0.25) + BM25 usage örnekleri (hybrid). Benchmark: RepoExec (355 problem) ve DevEval (1,825 sample, 117 repo), Python; metrik Pass@1/3/5 (executable tests) ve Dependency Invocation Rate. Generator: Qwen2.5-Coder 1.5B/7B, GPT-4.1-mini.
Findings:
- GPT-4.1-mini: RepoExec Pass@1 43.55 (RepoFormer 39.15), DevEval 31.91 (30.89).
- Qwen-7B: DevEval 17.27 vs RLCoder 13.00; 1.5B+Hydra bazı durumlarda 7B baseline'ları geçiyor.
- NameError/TypeError/AttributeError (hallucinated dependency) belirgin şekilde azalıyor, AssertionError oranı artıyor.
Relevant Limitations:
- Sadece Python ve tek fonksiyon üretimi; RepoExec testleri otomatik üretilmiş (benchmark'tan miras).
- DevEval'de kazanç GPT-4.1-mini için küçük (~1 puan).
Key Takeaway:
- Contextual tier için: gerçek dependency'leri getirmek similarity retrieval'dan daha değerli; hata tipi analizi bunun hallucination'ı azalttığını gösteriyor.

### E2EDev — E2EDev: Benchmarking Large Language Models in End-to-End Software Development Task (preprint, 2025) [arxiv:2510.14509]
Benchmark + empirical: kullanıcı gereksinimlerinden sıfırdan web uygulaması üretimini (E2ESD) BDD testleriyle ölçen benchmark ve mevcut framework'lerin karşılaştırması.
46 yüksek yıldızlı gerçek GitHub web app'inden (HTML/JS/CSS; hesap makinesi, mini oyun vb.) HITL-MAA ile 244 fine-grained requirement ve 703 Gherkin senaryosu + Python step implementation (Behave, browser otomasyonu) üretilmiş; LLM taslaklıyor, 5 test uzmanı gözden geçiriyor. Test ID'leri önceden GPT-4o ile UI elemanlarına atanıyor ve prompt'ta veriliyor. Metrikler: Req. Acc, Test Acc, Balanced Score + cost, CO2, süre. 6 yöntem (Vanilla, GPT-Engineer, Self-Collab, MapCoder, ChatDev, MetaGPT) × 6 backbone (Claude-Haiku 4.5, GPT-4o, GPT-4o-mini, Qwen2.5 7B/70B/Max); 360 proje üzerinde insan failure analizi.
Findings:
- En iyi Req. Acc ~53.75% (GPT-Engineer + Claude-Haiku 4.5); çoğu konfigürasyon 30–50%.
- Multi-agent framework'ler vanilla'yı tutarlı geçemiyor; ChatDev 15.72 turn, 10× maliyet.
- MetaGPT neredeyse tüm konfigürasyonlarda ~0% (iletişim kopukluğu).
- Soft Req. Acc ile Req. Acc arasında >25 puan fark: fonksiyon var ama edge case'ler kaçıyor.
Relevant Limitations:
- Requirement ve testler referans repodan türetiliyor; önceden atanmış test ID'leri üretilen app'in DOM'una dayatılıyor → UI tasarım özgürlüğünü kısıtlıyor ama black-box olması iyi.
- Ölçek küçük (46 proje), sadece basit frontend web app'leri, backend yok; frontier modeller (GPT-5, Claude Opus/Sonnet) yok.
- Testlerin taslakları LLM üretimi (insan doğrulamalı).
Key Takeaway:
- BDD/Gherkin, NL requirement ile executable oracle arasında yapılandırılmış bir hand-off olarak iyi çalışıyor.
- Multi-agent orkestrasyon kendi başına fayda sağlamıyor; hand-off'larda bilgi kaybı/aşırı context ana sorun.

### DyRetriever — Effective and Efficient Context Retrieval via Partial Dependency Graph for Repository-Level Code Generation (ASE 2026, 2026) [arxiv:2608.01927]
Method: repository-level function generation için LLM'in entry-point fonksiyonlardan başlayıp dependency graph üzerinde multi-hop dolaşarak context topladığı retriever; global graph yerine ihtiyaç anında kısmi graph kuruluyor.
DyRetriever + similarity retrieval = DyCoder. Benchmark: CoderEval-Python (230) ve DevEval (1,825; 209 ortamda çalışmayan instance failure sayılmış). Metrik Pass@1 (executable tests), runtime ve token. Modeller: Qwen3-Coder-30B, DeepSeek-v3.2, GPT-4o-mini. Hedef fonksiyon ve test dosyaları maskelenmiş (RepoScope'un leakage sorunu düzeltilmiş).
Findings:
- Ortalama Pass@1: CoderEval 46.96 (RepoScope 40.72), DevEval 40.84 (38.00).
- RepoScope'tan 7.4× hızlı; ama similarity tabanlılara göre 1.95–2.43× daha fazla token.
- DyRetriever context'i farklı similarity retriever'larla birleştirince +7.5–31% relatif kazanç.
Relevant Limitations:
- Sadece Python, tek fonksiyon; DevEval'de 209 instance'ın kasıtlı failure sayılması mutlak sayıları düşürüyor.
- LLM retrieval'ın doğruluğu (yanlış dependency) ayrıca ölçülmemiş.
Key Takeaway:
- Contextual tier'de leakage kontrolü (test/hedef maskesi) karşılaştırmaların geçerliliği için kritik; önceki sonuçların bir kısmı şişik olabilir.

### ECAT — Entropy-based Code Adversarial Translation for Real-world Repository Migration (preprint, 2026) [arxiv:2608.09273]
Method + küçük benchmark: Android (Java/Kotlin) uygulamasını sıfırdan HarmonyOS/ArkTS reposuna taşıyan generator–discriminator multi-agent framework ve A2H-RepoBench.
Migration "Code Entropy" (K=14 boyut; compile, fidelity, runtime GUI) minimizasyonu olarak formüle ediliyor: bağımsız discriminator entropy ölçüp "text gradient" (dosya-düzeyi direktif + gerekli skill) üretiyor, generator repoyu güncelliyor, update sadece entropy düşerse kabul. Başarılı trajectory'ler self-evolving memory tree'ye damıtılıyor. Emulator screenshot'larını Qwen3.7-Plus değerlendiriyor. Backbone DeepSeek-V4-Pro. Benchmark: 3 repo (Gallery 50K, AntennaPod 120K, Meshtastic 300K LOC). Metrik: CodeGraph semantic node alignment (kaynak repo ile) + feature checklist üzerinden Agent-as-Judge.
Findings:
- Ortalama 74.7% vs ReCodeAgent 46.4%, OpenHands 14.0%, RepoTransAgent 13.3%.
- Discriminator kaldırılınca (self-evaluation) Agent skoru çöküyor (ör. Meshtastic 71.2→12.0).
- ReCodeAgent yüksek alignment ama düşük Agent skoru: yapı korunuyor, içi placeholder.
- Maliyet: 38–126 iterasyon, 12–44 saat, 65–230M token/repo; memory tree token'ı ~yarıya indiriyor.
Relevant Limitations:
- Sadece 3 repo; test tabanlı fonksiyonel oracle yok, doğruluk LLM agent-as-judge ile ölçülüyor.
- Node alignment kaynak repoya yapısal benzerlik ödüllendiriyor → farklı ama geçerli ArkTS mimarilerini cezalandırır.
- Aynı tip LLM'ler hem entropy/discriminator hem judge; maliyet çok yüksek.
Key Takeaway:
- Generation ile evaluation'ı ayrı agent'lara bölmek (self-confirmation bias'ı kırmak) uzun-horizon repo translation'da en büyük kazancı veriyor.
- Platform-arası (UI framework + API) migration, repo translation'ın dil çevirisinden daha zor bir alt türü; executable oracle eksikliği açık problem.

### CLI-Tool-Bench — Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios (preprint, 2026) [arxiv:2604.06742]
Benchmark + empirical: boş workspace ve NL requirement'tan CLI aracı üretimini, scaffold vermeden ve black-box differential testing ile ölçen benchmark.
GitHub'dan 94 CLI repo (Python, JavaScript, Go; stars>10, install + `--help` doğrulaması, manuel kontrol). LLM, README ve `--help`'ten command schema çıkarıyor; LLM-directed fuzzing ile her command pattern için 50 test üretiliyor ve oracle repoda çalıştırılarak beklenen çıktı/side-effect kaydediliyor (geçersizler atılıyor). Değerlendirme: sandbox'ta exit code (M_exec), file system side effect (M_se), stdout eşitliği — EM, Fuzzy (Levenshtein), Semantic Match (GPT-5.4 judge, 1,000 çift üzerinde κ>0.9). 7 model × OpenHands ve Mini-SWE-Agent.
Findings:
- En iyi ortalama SM 43.78% (Kimi-k2.5), MiniMax-M2.5 34.59%; GPT-5.4, Qwen-3.5-plus, GLM-5 ~29–31%.
- Claude-Sonnet-4.6 beklenmedik şekilde düşük (~10.6% SM ortalama).
- Agent'lar güçlü şekilde monolitik yapı üretiyor; daha fazla token daha iyi sonuç anlamına gelmiyor.
- Mini-SWE-Agent birçok modelde OpenHands'ten iyi.
Relevant Limitations:
- Testler LLM tarafından üretiliyor ama oracle repoda doğrulanıyor (iyi); kapsam README/`--help`'te belgelenen davranışla sınırlı.
- Output formatı katı eşleştirmede farklı-ama-doğru çözümler cezalanıyor; SM bunu LLM-judge ile telafi ediyor, bu da ölçüme LLM sokuyor.
- Tek run; popüler CLI araçları için contamination analizi yok.
Key Takeaway:
- Referans repoyu black-box oracle olarak kullanmak, white-box unit test bağımlılığını ve scaffold dayatmasını kaldırıyor — survey'deki "coupling to reference" eksenine iyi bir karşı örnek.

### EvoC2Rust — EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation (ICSE-SEIP 2026, 2025) [arxiv:2508.04295]
Method (+ C2R-Bench): tüm C projesini güvenli Rust projesine çeviren skeleton-guided framework.
Üç aşama: (1) projeyi modüllere böl, feature-mapping destekli LLM ile tanım/makroları çevir, type-check edilmiş stub'lardan derlenebilir Rust skeleton kur; (2) fonksiyonları artımlı çevirip stub'ları değiştir; (3) rule-based + LLM refinement ile compile hatası onar. Backbone DeepSeek-V3 ve Qwen3-32B. Veri: Vivo-Bench (19 algoritmik proje) + C2R-Bench (Huawei'den 6 endüstriyel proje, 222 test) + RepoTransBench'ten 10 büyük proje (9.9K–91.6K LOC). Metrikler: ICompRate, line acceptance (manuel düzeltilmiş versiyona göre precision/recall), SafeRate; module-level'da FCompRate ve TestRate.
Findings:
- C2R-Bench (DeepSeek-V3): ICompRate 93.84%, AccRate ~97%, SafeRate 97.41%; Tymcrat 72.02%, Self-Repair 49.21% compile.
- C2Rust %99+ derleniyor ama SafeRate 1.83%; C2SaferRust 48.24%.
- Module-level test pass: Vivo 99.07%, C2R 89.53%.
- Büyük projelerde ICompRate ~69–76%'ya iniyor, SafeRate ~96%.
Relevant Limitations:
- Project-level değerlendirmede fonksiyonel test yok: compile rate + line acceptance (referansa benzerlik; referans da LLM destekli ve kendi çıktıları üzerinden düzeltilmiş) — kendi yöntemine bias riski.
- Testler yalnızca module-level fill-in-the-blank ayarında, referans Rust projesi içinde koşturuluyor.
- Benchmark'lar küçük (C2R-Bench 6 proje), sadece standart C kütüphanesi, tek-thread.
Key Takeaway:
- Derlenebilir skeleton'ı önce kurup sonra doldurmak, repo translation'da cross-file tutarlılık için etkili — skeleton-to-library ile repo-translation arasında köprü.

### TDDev — From Runnable Code to Shippable Applications: Test-Driven Development for Full-Stack Web Application Generation (ASE 2026, 2026) [arxiv:2605.17242]
Method + empirical: NL requirement'tan full-stack web app üretiminde TDD döngüsünü otomatikleştiren TDDev ve TDD stratejilerinin kontrollü karşılaştırması.
TDDev requirement'tan browser tabanlı acceptance test türetiyor, app'i deploy edip browser agent ile test ediyor, hataları agent için actionable feedback'e çeviriyor (MCP server olarak). Üç strateji: Incremental, Whole-Project, Agentic TDD (K=5 round) vs Vanilla. WebGen-Bench'ten rastgele 20 app; minimal agent (Claude Agent SDK) ve OpenCode; backbone MiniMax-M3, Claude Sonnet 4.6, Qwen3.5-397B-A17B. Headline metrik: orijinal insan-yazımı WebGen-Bench testleri üzerinde sabit Claude Sonnet 4.6 browser-tester ile oracle accuracy (Pass + 0.5·Partial); Wilcoxon + bootstrap CI.
Findings:
- Sonnet ile Vanilla 67.8% → Agentic TDD 91.5% (+23.7 pp); MiniMax minimal agent 65.1 → 87.3%.
- Qwen3.5 kendi tester'ı ile TDD'den fayda görmüyor (−4.4 ile +4.8 pp); tester Sonnet yapılınca +6.8–9.4 pp.
- Qwen3.5 feedback'inde test yürütmelerinin %56.2'si Fail (Sonnet %21.3); feature abandonment %48.8 vs %12.1.
- Test generation, ground-truth kriterlerin %88.9'unu kapsıyor; tester 40 fixture'da tüm gerçek defect'leri yakalıyor.
Relevant Limitations:
- Oracle bir LLM browser agent'ı (Sonnet 4.6) ve aynı model aynı zamanda backbone'lardan biri → Sonnet konfigürasyonlarında ölçüm/üretim aynı aile.
- Kontrollü deneylerde insan-yazımı test'ler acceptance test olarak loop'a veriliyor; yani loop evaluation testlerini görüyor (test leakage'a yakın).
- 20 app, tek seed; dil/stack belirtilmemiş.
Key Takeaway:
- Executable acceptance test'ler güçlü bir hand-off, ama feedback'in güvenilirliği (tester kalitesi) TDD kazancının ana darboğazı.
