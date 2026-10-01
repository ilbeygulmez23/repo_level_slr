# Manuel database araması (ACM DL, IEEE Xplore, Scopus)

Toplam 3 database × 3 query ailesi (F1, F2, F3) = 9 arama. Kurumsal erişim (üniversite ağı veya VPN) gerekiyor. Tahmini süre 30–45 dakika.

**Query'ler:** [queries_rendered.md](queries_rendered.md). Her ailede ilgili database başlığının altındaki string'i olduğu gibi kopyalayın, hiç değiştirmeyin.

**Dosyaların yeri:** `slr/data/manual/`. Dosya adları `<db>_<aile>` biçiminde olmalı, örneğin `ieee_F1.csv`, `scopus_F2.csv`, `acm_F3.bib`. Aynı arama birden fazla dosyaya export edildiyse sonuna `_p1`, `_p2` ekleyin (`acm_F1_p1.bib`, `acm_F1_p2.bib`).

**Log:** Her arama için `slr/data/manual/manual_log.csv` dosyasına bir satır ekleyin:
```
db,family,run_date,hits,notes
ieee,F1,2026-10-02,123,
```
`hits`, database'in ekranda gösterdiği toplam sonuç sayısıdır. Bu sayı PRISMA diyagramına girecek.

---

## IEEE Xplore
1. Advanced Search → **Command Search** sekmesi. String'i yapıştırın.
2. Sonuç sayfasında soldan **Year** filtresini 2022–2026 yapın.
3. **Export → Search Results → CSV** (tüm sonuçlar) → `ieee_F1.csv`.
4. Hata alırsanız (örneğin "too many terms"), ne yazdığını bana iletin, string'i bölerim.

## Scopus
1. Advanced document search. String'i yapıştırın; yıl filtresi string'in içinde zaten var.
2. **Export → CSV**. "Citation information" ve **"Abstract & keywords"** seçili olsun.
3. `scopus_F1.csv`.

## ACM Digital Library
1. Advanced Search → **Edit Search** (search query kutusu). String'i yapıştırın.
2. Publication date: 01/2022 – 09/2026.
3. Sayfa başına 50 sonuç gösterin → **Select All** → **Export Citations → BibTeX** → indirin. Bunu her sayfa için tekrarlayın (`acm_F1_p1.bib`, `acm_F1_p2.bib`, …).
4. Syntax hatası alırsanız veya sonuç sayısı şüpheli derecede düşük ya da yüksekse ekran görüntüsünü bana iletin.

---

Bitince `python3 merge.py` komutunu çalıştırın (ya da bana haber verin). Tüm kaynaklar birleşip tekilleştirilecek.
