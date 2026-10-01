"""Merge raw search results from all sources and deduplicate -> data/records.csv

Inputs:
  data/raw/<source>_<family>.jsonl                automated sources (search.py)
  data/manual/<acm|ieee|scopus>_<family>.<csv|bib>  manual exports, e.g. ieee_F1.csv, acm_F2.bib
Dedup keys, in order: DOI (non-arXiv) -> arXiv ID -> normalised title.
"""
import csv
import glob
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def arxiv_from_doi(doi):
    m = re.match(r"10\.48550/arxiv\.(.+)", doi or "")
    return m.group(1) if m else ""


# ---------- manual export parsers ----------
CSV_COLS = {  # canonical field -> candidate column names (IEEE Xplore, Scopus, generic)
    "title": ["Document Title", "Title"],
    "abstract": ["Abstract"],
    "doi": ["DOI"],
    "date": ["Publication Year", "Year"],
    "venue": ["Publication Title", "Source title"],
    "authors": ["Authors", "Author full names"],
}


def read_csv_export(path):
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            yield {k: next((row[c] for c in cols if row.get(c)), "") for k, cols in CSV_COLS.items()}


def read_bib_export(path):
    text = Path(path).read_text(encoding="utf-8")
    for entry in re.split(r"\n@", text):
        field = lambda k: " ".join((re.search(rf"\b{k}\s*=\s*[{{\"](.*?)[}}\"],?\s*\n", entry, re.S | re.I)
                                   or [None, ""])[1].replace("{", "").replace("}", "").split())
        if field("title"):
            yield {"title": field("title"), "abstract": field("abstract"), "doi": field("doi"),
                   "date": field("year"), "venue": field("booktitle") or field("journal"),
                   "authors": field("author").replace(" and ", "; ")}


def load_raw():
    for path in sorted(glob.glob(str(DATA / "raw" / "*.jsonl"))):
        for line in open(path):
            yield json.loads(line)
    for path in sorted(glob.glob(str(DATA / "manual" / "*"))):
        if path.endswith("manual_log.csv"):
            continue
        stem = re.sub(r"_p\d+$", "", Path(path).stem)  # e.g. ieee_F1, acm_F2_p3 -> acm_F2
        source, family = stem.split("_", 1)
        reader = read_bib_export if path.endswith(".bib") else read_csv_export
        for r in reader(path):
            doi = r["doi"].lower().replace("https://doi.org/", "")
            yield {**r, "source": source.upper(), "family": family, "doi": doi,
                   "arxiv_id": arxiv_from_doi(doi), "source_id": doi or norm_title(r["title"])}


# ---------- dedup (union-find over shared keys) ----------
def dedup(raw):
    parent = list(range(len(raw)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, r in enumerate(raw):
        arx = r.get("arxiv_id") or arxiv_from_doi(r.get("doi"))
        keys = [("doi", r["doi"]) if r.get("doi") and not arxiv_from_doi(r["doi"]) else None,
                ("arxiv", arx) if arx else None,
                ("title", norm_title(r["title"])) if len(norm_title(r["title"])) > 15 else None]
        for k in filter(None, keys):
            if k in seen:
                parent[find(i)] = find(seen[k])
            else:
                seen[k] = i
    groups = {}
    for i in range(len(raw)):
        groups.setdefault(find(i), []).append(raw[i])
    return list(groups.values())


def canonical(group):
    # Prefer a peer-reviewed record (non-arXiv DOI) as canonical; keep the longest abstract.
    pub = [r for r in group if r.get("doi") and not arxiv_from_doi(r["doi"])]
    base = dict((pub or group)[0])
    base["abstract"] = max((r.get("abstract") or "" for r in group), key=len)
    base["arxiv_id"] = next((r["arxiv_id"] for r in group if r.get("arxiv_id")), "")
    base["year"] = min((r.get("date") or "9999")[:4] for r in group)
    base["sources"] = ";".join(sorted({r["source"] for r in group}))
    base["families"] = ";".join(sorted({r["family"] for r in group}))
    base["n_raw"] = len(group)
    return base


FIELDS = ["rid", "key", "title", "year", "venue", "doi", "arxiv_id", "authors", "sources", "families", "n_raw", "abstract"]

if __name__ == "__main__":
    raw = list(load_raw())
    groups = dedup(raw)
    recs = sorted((canonical(g) for g in groups), key=lambda r: (r["year"], norm_title(r["title"])))
    with open(DATA / "records.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for i, r in enumerate(recs, 1):
            key = r["arxiv_id"] and f"arxiv:{r['arxiv_id']}" or r["doi"] and f"doi:{r['doi']}" or f"title:{norm_title(r['title'])[:80]}"
            w.writerow({**r, "rid": f"R{i:04d}", "key": key})
    print("raw records per source:", dict(Counter(r["source"] for r in raw)))
    print(f"raw total={len(raw)}  unique after dedup={len(recs)}  duplicates removed={len(raw) - len(recs)}")
