### MRG-Bench — MRG-Bench: Evaluating and Exploring the Requirements of Context for Repository-Level Code Generation (preprint, 2025) [arxiv:2508.02998]
Contextual benchmark + empirical çalışma: gerçek repolardaki fonksiyonları docstring + signature'dan, repo context'i ile üretme; Python/Java/Go.
383 sample, 22 proje (Ocak 2023 sonrası oluşturulmuş, >50 star repolar). Fonksiyonlar call-graph ile seçiliyor: repo-içi dependency'si, developer comment'i ve %100 line coverage sağlayan test'i olanlar. Üretilen fonksiyon dosyadaki yerine konuyor, projenin kendi pytest/mvn/go test'leri Docker'da koşuyor; metrik Pass@k.
Findings:
- Context'siz en iyi model Claude-3.5-Sonnet ortalama 8.6% Pass@1; in-file context ile 32.5%.
- Reasoning modeller (DeepSeek-R1, o3-mini) in-file context ile en iyi, ama hâlâ <%40.
- RAG (BM25/embedding) in-file context'ten kötü; RepoCoder Java/Go'da daha iyi (ortalama 18.1%).
- LLM-voting annotation'a göre hataların >%68'i "What" (gereksinimi anlamama), "How" değil.
Relevant Limitations:
- Hata analizi 5 LLM'in oylamasıyla yapılıyor; ground truth koda göre What/How etiketi — LLM-in-the-measurement.
- Sadece 22 proje; tek fonksiyon doldurma, repo üretimi değil.
Key Takeaway:
- Proje testlerini function-level coverage ile eşlemek, repo-context-gen için temiz bir oracle; darboğaz spesifikasyonun anlaşılması.

### PaperBench — PaperBench: Evaluating AI's Ability to Replicate AI Research (preprint, 2025) [arxiv:2504.01848]
Core benchmark: agent'a bir ICML 2024 paper'ı (+ yazarlardan addendum) veriliyor, sıfırdan tüm deneyleri çalıştıran bir repo + `reproduce.sh` üretmesi isteniyor. Orijinal kod blacklist'te.
20 Spotlight/Oral paper, 12 konu; her paper için yazarla birlikte haftalarca geliştirilmiş hiyerarşik rubric, toplam 8,316 leaf (Code Development / Execution / Result Match). Submission temiz bir VM'de (A10 GPU) yeniden çalıştırılıyor, sonra o3-mini tabanlı SimpleJudge her leaf'i binary puanlıyor; skor ağırlıklı ortalama "Replication Score". JudgeEval ile judge doğrulanıyor (o3-mini F1 0.83, ~$66/paper). Hafif varyant: PaperBench Code-Dev (sadece kod rubric'i).
Findings:
- BasicAgent ile Claude-3.5-Sonnet 21.0%, o1 13.2%, diğerleri <10%.
- IterativeAgent (erken bitirmeyi yasaklayan) o1'i 24.4%'e çıkarıyor, Claude'u 16.1%'e düşürüyor — scaffold hassasiyeti büyük.
- 3-paper subset'te ML PhD'ler 48 saatte 41.4%, o1 26.6%.
- Code-Dev'de o1 43.4%, ama full benchmark ile korelasyonu zayıf (r=0.48).
Relevant Limitations:
- Ölçüm tamamen LLM-judge; judge sadece top-10 dosyayı görüyor, F1 0.83 → skorlar gürültülü.
- Rubric leaf'leri paper'ın implementasyon detaylarına bağlı; farklı ama geçerli tasarımlar Code Development node'larında kaybedebilir.
- Sadece 20 paper, tek domain (ML, Python); maliyet çok yüksek (12 saat GPU run + judge).
Key Takeaway:
- Paper→repo için yazar-onaylı hiyerarşik rubric + temiz ortamda yeniden çalıştırma, kısmi ilerlemeyi ölçmenin güçlü bir şablonu; ama oracle executable değil, LLM verdict'i.

### RepoST — RepoST: Scalable Repository-Level Coding Environment Construction with Sandbox Testing (preprint, 2025) [arxiv:2503.07358]
Contextual benchmark + training-data + method: repo-level function generation için otomatik executable environment inşası. Tüm repoyu build etmek yerine hedef fonksiyon ve local dependency'leri ayrı bir script'e "sandbox"lanıyor, test'ler LLM ile üretiliyor.
Pipeline: repo/fonksiyon seçimi → sandboxing → GPT-4o ile test üretimi → iteratif hata düzeltme + branch coverage artırma → AST/execution/LLM tabanlı functionality-equivalence ve test-correctness kontrolü. RepoST-Train: 7,415 fonksiyon/824 repo; RepoST-Eval: 296 fonksiyon/99 repo; ortalama 8.2 test, %100 branch coverage (eval). Python. Model, orijinal repo context'i ile fonksiyonu üretiyor; Pass@1.
Findings:
- 12 model içinde en iyi GPT-4o 39.53 Pass@1; en iyi open-source (DS-R1-Qwen-32B) 5.07 geride.
- RepoST-Train ile rejection-sampling fine-tuning Qwen2.5-Coder'ı HumanEval'de +5.5, RepoEval'de +3.5 Pass@1 iyileştiriyor.
- Human study: GPT-4o equivalence check'i geçen 13/20'nin hepsi insanla uyumlu; öğrenciler örneklerin %81.5'ini çözebiliyor.
Relevant Limitations:
- Test'ler ve kalite kontrol aynı LLM ailesinden (GPT-4o); sandbox sonrası fonksiyonun orijinaliyle eşdeğerliği LLM'e emanet.
- Sadece Python, sadece "oracle" context; agent setting'i yok.
Key Takeaway:
- Tam repo build yerine function-level sandbox, execution feedback'i ölçeklemenin ucuz yolu — ama integration davranışı kaybolur.

### WebGen-Agent — WebGen-Agent: Enhancing Interactive Website Generation with Multi-Level Feedback and Step-Level Reinforcement Learning (preprint, 2025) [arxiv:2509.22644]
Core method + training çalışması: NL talimatından boş codebase ile başlayıp multi-file web sitesi üreten agent; execution, screenshot (VLM) ve GUI-agent testing feedback'i ile iteratif iyileştirme, backtracking ve select-best.
Her adım: codebase edit → dependency install + servis başlatma → Qwen2.5-VL-32B screenshot açıklaması/puanı → GUI-agent testi ve puanı. Step-GRPO: her adımın screenshot + GUI skorları step-level reward olarak kullanılıyor; ~700 DeepSeek-V3 trajectory ile SFT warm-start, 500 WebGen-Instruct talimatı ile GRPO. Değerlendirme WebGen-Bench (101 talimat, 647 GUI-agent test case; accuracy + GPT-4o appearance score).
Findings:
- Claude-3.5-Sonnet: Bolt.diy'de 26.4% → WebGen-Agent'ta 51.9% accuracy, appearance 3.0 → 3.9.
- En iyi: Qwen3-Coder-480B 58.2%, appearance 4.3.
- Qwen2.5-Coder-7B: 12.4% → SFT 38.9% → Step-GRPO 45.4%.
- Ablation: GUI-agent feedback en büyük accuracy katkısı (+3.3), screenshot appearance'ı 3.0→3.6.
Relevant Limitations:
- Hem feedback/reward hem de benchmark ölçümü VLM/GUI-agent tabanlı (Qwen2.5-VL-32B); aynı model reward'da ve evaluation'da → reward hacking / circularity riski.
- Baseline'ların değerleri WebGen-Bench paper'ından alınmış, harness farklı.
- Tek benchmark, 101 task; backend/DB derinliği sınırlı.
Key Takeaway:
- App üretiminde GUI-level E2E feedback hem inference hem RL reward olarak işe yarıyor; ama oracle'ın kendisi LLM, executable değil.

### Devonix — Devonix: A Hierarchical Multi-Agent and Neuro-Symbolic Orchestration Framework for Autonomous Web Application Synthesis (ICCMC 2026, 2026) [doi:10.1109/iccmc69250.2026.11624731]
Core method (sadece abstract okundu, full text yok): non-technical kullanıcının NL gereksiniminden modüler HTML/CSS/JS web uygulaması üreten hiyerarşik multi-agent framework.
Hierarchical Intent Modeling ile gereksinim doğrulanabilir subtask şemalarına ayrılıyor; LLM synthesis engine kod üretiyor; Smart Code Regeneration yapısal/mantıksal hataları onarıyor; Automated QA Validation sözdizimi ve "runtime simulation" kontrolü yapıyor. 50 stratified web app görevi üzerinde prompt-based ve manuel baseline'larla karşılaştırma.
Findings:
- Architectural accuracy 96.8%, structural integrity 94.2%, functional error'da %63 azalma, ortalama deployment latency 2.1 s (p < 0.001).
Relevant Limitations:
- Metrik tanımları abstract'ta yok; "architectural accuracy" neye göre (referans mimari mi?) belirsiz — reference coupling riski.
- Fonksiyonel doğruluk için executable test/oracle belirtilmemiş; 50 task, kaynak ve kontaminasyon bilgisi yok.
- Sadece front-end stack (HTML/CSS/JS).
Key Takeaway:
- Structured subtask şemaları hand-off için umut verici, ama değerlendirme full text olmadan doğrulanamıyor; düşük ağırlıkla raporlanmalı.

### Flutter-ChatGPT — Empirical evaluation of automated code generation for mobile applications by AI tools (IEEE C3 2023, 2023) [doi:10.1109/c358072.2023.10436306]
Core empirical çalışma (sadece abstract, full text yok): ChatGPT-3.5 ile Flutter framework'ünde sıfırdan bir mobil uygulama iteratif prompt'larla üretiliyor, süreç her adımda değerlendiriliyor.
Tek uygulama/case study; değerlendirme dört gösterge: code quality, solution quality, response time ve insan-yazımı kodla karşılaştırma. Dil Dart. Otomatik test veya benchmark kullanılmadığı anlaşılıyor.
Findings:
- Belirli bir karmaşıklık seviyesine kadar, giderek detaylanan prompt'larla ChatGPT çalışır kod üretebiliyor; bu kod daha karmaşık mantık için temel olabilir.
- Sayısal sonuç abstract'ta raporlanmamış.
Relevant Limitations:
- Tek app, tek model (GPT-3.5), human-in-the-loop prompt iterasyonu → otonom üretim ölçülmüyor.
- Değerlendirme büyük olasılıkla subjektif/manuel; replikasyon zor.
Key Takeaway:
- Erken (2023) nl-to-app örneği; mobil domain ve Dart kapsaması açısından değerli ama kanıt gücü düşük.
