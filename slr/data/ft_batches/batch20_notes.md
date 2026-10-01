### AgileCoder — AgileCoder: Dynamic Collaborative Agents for Software Development based on Agile Methodology (FORGE 2025, 2025) [doi:10.1109/forge66646.2025.00026]
Method çalışması: ChatDev/MetaGPT'nin waterfall akışı yerine Agile/Scrum rollerini (Product Manager, Scrum Master, Developer, Senior Developer, Tester) sprint'ler halinde çalıştıran multi-agent framework; küçük bir ProjectDev benchmark'ı da öneriyor.
Input: NL yazılım isteği (ör. "Create a snake game") → PM backlog çıkarıyor, her sprint planning → development → testing → review; output çok dosyalı çalıştırılabilir Python kod tabanı. Dynamic Code Graph Generator (static analysis ile Code Dependency Graph) context retrieval ve test sırası için kullanılıyor. Değerlendirme: HumanEval/MBPP pass@1 + ProjectDev (14 task: mini-game, image processing, data visualization); ProjectDev'de insan değerlendiriciler programı çalıştırıp requirement listesine göre karşılanan oran ("executability") hesaplıyor; her task 3 run, GPT-3.5-Turbo backbone.
Findings:
- ProjectDev executability: AgileCoder 57.79 vs ChatDev 32.79, MetaGPT 7.73; #Errors 0 vs 6/32.
- Maliyet yüksek: 36,818 token, $0.44, 444 s (ChatDev 7,440 token, $0.12); ortalama 1.64 sprint.
- CDG ablation: graph olmadan executability 57.50 → 23.38.
- HumanEval 70.53 / MBPP 80.92 pass@1 (GPT-3.5), MetaGPT'ye göre +7.71 / +6.19.
Relevant Limitations:
- ProjectDev yalnızca 14 task, tek dil (Python), tek backbone; istatistiksel güç yok.
- Değerlendirme tamamen manuel ve requirement listesi yazarlar tarafından hazırlanmış; kriterler öznel, inter-rater agreement raporlanmamış.
- Ana başlık sonuçları HumanEval/MBPP gibi isolated benchmark'lara dayanıyor; repo-level iddia için zayıf kanıt.
- Hand-off'lar büyük ölçüde free-form NL (backlog, review); CDG tek structured artefakt.
Key Takeaway:
- Iteratif/incremental süreç ve structured code graph, waterfall multi-agent sistemlere göre çalıştırılabilirliği artırıyor; ama ölçüm altyapısı (küçük, manuel) survey'de "early-stage evidence" olarak konumlanmalı.

### EvoGit — EvoGit: Decentralized Code Evolution via Git-Based Multi-Agent Collaboration (preprint, 2025) [arxiv:2506.02049]
Method çalışması: merkezi orkestratör, mesajlaşma veya shared memory olmadan, Git version graph'ı (phylogenetic DAG) koordinasyon ortamı olarak kullanan evolutionary multi-agent geliştirme framework'ü.
İnsan PM üst seviye hedefi ve seed scaffold'u veriyor; 16 bağımsız agent 120 iterasyon boyunca rastgele seçilen dosyadan ≤128 satırlık bölgeye mutation veya iki branch arasında crossover uyguluyor. Her yeni versiyon parent'ına karşı compiler/linter/type-checker/test çıktılarıyla ve bir LLM-judge'ın binary kararıyla kabul/ret ediliyor ("no worse than parent" partial order). İnsan her 10 (Task 1) / 20 (Task 2) iterasyonda frontier'dan bir versiyon seçip kısa feedback veriyor. Görevler: (1) Next.js scaffold'dan araştırma projesi tanıtım web sitesi, (2) bin-packing solver'ı LLM ile evrimleştiren meta-level Python pipeline.
Findings:
- Her iki görevde de çalışan, modüler artefaktlar üretildiği ve repo'ların public olduğu raporlanıyor.
- Task 2'de input validation, logging, exception handling gibi özellikler talimatsız ortaya çıkmış (kalitatif gözlem).
- Nicel metrik, baseline veya tekrar sayısı yok.
Relevant Limitations:
- Değerlendirme yalnızca yazarların kalitatif incelemesi; "evaluation protocol" insan müdahalesini sınırlıyor ama başarıyı ölçmüyor.
- İnsan seçimleri (frontier'dan preferred version) sonucu ciddi yönlendiriyor; autonomy katkısı ayrıştırılamıyor.
- Kabul kararı LLM-judge'a dayalı; ölçüm ile üretim aynı model ailesinde.
- İki görev, tek run; model, maliyet ve token raporu sınırlı.
Key Takeaway:
- Git lineage'ı structured, denetlenebilir bir koordinasyon artefaktı olarak kullanmak ilginç bir tasarım; ama survey'de kanıt düzeyi "demonstration" olarak işaretlenmeli.

### LAIL — Large Language Model-Aware In-Context Learning for Code Generation (TOSEM 2025, 2025) [doi:10.1145/3715908]
Method çalışması (peripheral): ICL demonstration seçimi için LLM'in kendisini etiketleyici olarak kullanan model-aware retriever. Not: open full text bulunamadı; not abstract'a dayanıyor.
LLM, aday örnekleri bir requirement için positive/negative olarak etiketliyor; bu etiketlerle contrastive bir retriever eğitiliyor ve inference'ta seçilen örnekler prompt'a ekleniyor. Ana değerlendirme function-level (MBJP, MBPP, MBCPP; CodeGen-Multi-16B, CodeLlama-34B, Text-davinci-003), ayrıca repository-level DevEval üzerinde Pass@1/3/5 (CodeLlama-7B) ve human evaluation.
Findings:
- DevEval'de SOTA ICL baseline'larına göre Pass@1/3/5'te +10.04 / +8.12 / +4.63 puan (CodeLlama-7B).
- Function-level'da MBJP/MBPP/MBCPP Pass@1'de +1.2–11.6 puan kazanç; retriever LLM'ler ve dataset'ler arası transfer ediliyor.
Relevant Limitations:
- Repo-level kısmı tek model (CodeLlama-7B) ve tek benchmark; mutlak skorlar abstract'ta yok.
- DevEval'in repo context'i nasıl verildiği (retrieval mı, sadece ICL örneği mi) abstract'tan anlaşılmıyor.
Key Takeaway:
- Demonstration seçiminin repo-level görevlerde function-level'dan daha büyük fark yaratabileceğine dair bir sinyal; full text ile doğrulanmalı.

### NL2Repo-Bench — NL2Repo-Bench: Towards Long-Horizon Repository Generation Evaluation of Coding Agents (preprint, 2025) [arxiv:2512.12730]
Benchmark + empirical çalışma: agent'a tek bir NL requirements dokümanı ve boş workspace veriliyor; kurulabilir (installable) bir Python kütüphanesini sıfırdan üretmesi isteniyor.
104 task, GitHub'daki gerçek Python kütüphanelerinden (300–120k LOC, ≥10 star, son 3 yıl, tüm testleri geçen) seçiliyor. Annotator'lar repoyu reverse-engineering ile ortalama ~18.8k token'lık spec'e çeviriyor (Project Description, Supports/dizin yapısı ve bağımlılıklar, API Usage Guide, Implementation Nodes); AST tabanlı coverage kontrolü, uzman review ve SOTA agent'larla pilot run ile spec rafine ediliyor. Değerlendirme: Docker'da upstream pytest suite'i; skor ortalama test pass rate + tam geçiş (Pass@1 count). Zorluk: Easy 26 / Medium 46 / Hard 32; 9 kategori. Agent: çoğunlukla OpenHands-CodeAct, ayrıca Cursor-CLI ve Claude Code; 10 model.
Findings:
- En iyi: Claude-Sonnet-4.5 + Claude Code %40.2; tüm modeller <%40.5, yarısı <%20. 104 repo'dan en iyi model tek run'da sadece ~5'ini tam geçiyor.
- GPT-5 %21.7: erken durup kullanıcı girdisi bekliyor, <100 turn.
- Aynı model farklı framework'lerde <%1 fark → benchmark model-centric.
- Zorlukla monoton düşüş (Claude-Sonnet-4.5: Easy 55.3 → Hard 21.4); ML ve networking kategorileri en zor.
Relevant Limitations:
- Spec, referans repodan reverse-engineer ediliyor ve upstream white-box testlerini geçecek kadar API imzalarını dayatıyor → alternatif tasarımlar cezalandırılır; görev pratikte "spec'ten API-uyumlu reconstruction".
- Sadece Python; public repo'lar → contamination riski (recency filtresi sınırlı koruma).
- Dizin yapısı ve bağımlılıklar spec'te verildiği için "architectural design" iddiası kısmen zayıf.
Key Takeaway:
- Upstream test suite'i oracle yapan, scaffold'suz NL→repo formülasyonu şu an alandaki en temiz execution-based kurulumlardan biri; ama spec–test coupling'i survey'de açıkça tartışılmalı.

### What Makes ICL Examples Effective — What Makes In-Context Examples Effective for Code Generation? (ISSTA 2026, 2026) [arxiv:2508.06414]
Empirical çalışma (peripheral): ICL code example'larının hangi özelliklerinin (solution insight, context bilgisi, identifier naming, formatting) code generation'ı etkilediğini kontrollü deneylerle inceliyor.
İki benchmark: LiveCodeBench LeetCode (362 soru, Python+Java) ve repository-level DevEval (1,427 task, Python). DevEval için repodaki fonksiyon/sınıflar retrieval DB; BM25 ve 3 embedding retriever, mutation operatörleri (identifier obfuscation vb.), naming style varyantları. Modeller: GPT-4o-mini, Qwen2.5-7B/32B, DeepSeek-Coder-V2-Lite; metrik Pass@1 (test execution), istatistiksel testler.
Findings:
- DevEval'de repo-retrieved ICL güçlü etki: Qwen-32B zero-shot 15.21 → gist-large 36.79; LeetCode'da benzer soru/çözüm eklemek anlamlı fayda sağlamıyor.
- Namespace bilgisi eklemek tüm modellerde DevEval'i artırıyor (ör. Qwen-32B BM25 26.70 → 30.34).
- Identifier obfuscation (FVE) DevEval'de GPT-4o-mini 37.91 → 25.58.
Relevant Limitations:
- Tek repo-level benchmark, sadece Python; küçük/orta modeller.
- Ground-truth'u testleri geçemeyen ~400 DevEval task çıkarılmış; seçim etkisi raporlanmamış.
Key Takeaway:
- Repo-context generation'da "hangi context" sorusunda identifier/namespace bilgisi örnek mantığından daha belirleyici.

### RealDevWorld — You Don't Know Until You Click: Automated GUI Testing for Production-Ready Software Evaluation (preprint, 2025) [arxiv:2508.14104]
Benchmark + evaluation method: sıfırdan üretilen interaktif uygulamaları (web/app) GUI üzerinden tıklayarak değerlendiren RealDevWorld; RealDevBench (194 task) ve AppEvalPilot (agent-as-a-judge) bileşenleri.
Task = requirements açıklaması + yapılandırılmış feature listesi + bazı task'larda multimodal materyal (görsel, ses, tablo). Requirement'lar SRDD ve Upwork/Freelancer'dan; feature listeleri Claude-3.5-Sonnet ile GitHub projelerinin dokümantasyonundan genişletilmiş. Domain: Display %50, Analysis %18.6, Game %17, Data %14.4. AppEvalPilot feature'lardan test case üretip web/OS seviyesinde etkileşimle çalıştırıyor, Pass/Fail/Uncertain sınıflıyor. Validasyon: 49 Lovable-üretimi proje, 3 QA uzmanı ile human ground truth.
Findings:
- AppEvalPilot test case accuracy 0.92, feature-level korelasyon 0.85 (Browser-Use 0.58, WebVoyager 0.43); app başına 9 dk, Browser-Use'a göre %77 daha ucuz.
- 54 test task'ta agent sistemleri (MGX BoN-3 0.78, Lovable 0.74) düz LLM'lerden (%0.29–0.53) belirgin iyi; ortalama ~+0.27.
- Statik code quality ve visual skorlar runtime kalitesiyle uyumsuz.
Relevant Limitations:
- Ölçüm tamamen LLM-driven: feature listesi Claude ile üretilmiş, test case'ler ve verdict Claude-tabanlı agent'tan; üretici modellerle aynı aile (Claude-3.7) → self-preference riski.
- Human validation sadece Lovable çıktıları üzerinde; diğer sistemlere genelleme varsayılıyor.
- Deployment için LLM-generated komutlar kullanılıyor; deploy hatası ile fonksiyonel hata karışabilir. Model çıktılarının çok dosyalı olup olmadığı sisteme göre değişiyor (LLM'ler tek script).
- Değerlendirme sadece 54 task üzerinde, tek run.
Key Takeaway:
- GUI-tabanlı agent-as-judge, referans implementasyona bağlı olmadığı için alternatif tasarımları cezalandırmıyor; ama oracle güvenilirliği test üreten LLM'e taşınıyor — structured/executable feature spec'leri (BDD) bu boşluğu kapatabilir.
