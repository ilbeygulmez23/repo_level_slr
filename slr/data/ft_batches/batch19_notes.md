### RepoMasterEval — RepoMasterEval: Evaluating Code Completion via Real-World Repositories (ASE 2025, 2025) [doi:10.1109/ase63991.2025.00304]
Benchmark çalışması (+ 10 model üzerinde empirical değerlendirme): real-world repo'lardan, test suite'i olan dosyalarda bir code snippet mask'lenip modelden tamamlaması isteniyor. Not: open full text bulunamadı; bu not yalnızca abstract'a (ve citing paper'lardaki özet tablolara) dayanıyor.
Input: mask'lenmiş dosya + repo context (NL açıklama yok, fonksiyon ortası/blok seviyesi completion); output: eksik snippet. Değerlendirme repo'nun kendi test'leriyle; test kalitesi mutation testing ile ölçülüp düşük mutation score'lu suite'lere manuel test ekleniyor. Citing paper'lara göre 6 repo, 2 dil (muhtemelen Python ve TypeScript — doğrulanmalı).
Findings:
- Test augmentation benchmark doğruluğu için kritik (abstract'ta sayı yok).
- 10 SOTA model arasında real-world senaryoda varyans raporlanıyor; endüstriyel deployment'ta skorun pratik model performansıyla yüksek korelasyonlu olduğu iddia ediliyor.
Relevant Limitations:
- Ölçek küçük (citing tabloya göre 6 repo); contamination riski yüksek (public repo'lar).
- Ground-truth snippet ve mevcut test'lere bağlı white-box setup; ama execution-based olduğu için similarity'den daha az reference-coupled.
- Somut sayılar full text olmadan çıkarılamadı.
Key Takeaway:
- Mutation testing ile test yeterliliğini ölçüp güçlendirmek, repo-context benchmark'larında false positive'leri azaltmanın ucuz bir yolu.
