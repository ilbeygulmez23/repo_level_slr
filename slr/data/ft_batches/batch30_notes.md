### Co-Learning — Experiential Co-Learning of Software-Developing Agents (ACL 2024, 2023) [doi:10.18653/v1/2024.acl-long.305]
Method: ChatDev üzerine, instructor ve assistant agent'ların geçmiş trajectory'lerinden "shortcut" deneyimleri çıkarıp yeni görevlerde kullandığı experiential co-learning framework'ü (arXiv 2312.17025 full text).
Değerlendirme SRDD (1,200 NL yazılım gereksinimi, 5 kategori) test split'i üzerinde, ChatDev'in metrikleriyle: Completeness (placeholder'sız kod oranı), Executability (çalışma), Consistency (requirement–kod embedding benzerliği) ve bunların çarpımı Quality; baseline GPT-Engineer, MetaGPT, ChatDev.
Findings:
- Quality 0.7304 vs ChatDev 0.4267, MetaGPT 0.1439, GPT-Engineer 0.1363; Executability 0.965 vs 0.880.
- Süre ChatDev'e göre daha kısa (122.8 s vs 148.2 s).
Relevant Limitations:
- Fonksiyonel doğruluk ölçülmüyor: executability çalışıp çökmemek, consistency embedding benzerliği (ChatDev ile aynı zayıflık); metrikler aynı grubun kendi tanımları.
- Artefact'lar küçük (ChatDev ölçeğinde birkaç dosya); bağımsız benchmark'ta doğrulama yok.
Key Takeaway:
- Deneyim/hafıza tabanlı iyileşme ChatDev metriklerinde büyük görünüyor; bağımsız, test-tabanlı oracle altında (E2EDev) bu çizgideki framework'lerin avantajı kaybolduğu için dikkatle yorumlanmalı.
