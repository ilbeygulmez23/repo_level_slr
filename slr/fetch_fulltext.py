import os
"""Download full texts for full-text eligibility -> data/fulltext/<safe key>.txt, log in data/fulltext/log.csv

Source order: own arXiv ID -> arXiv ID of a duplicate preprint (dup_of) -> OpenAlex open-access PDF by DOI.
Sequential with pauses to respect arXiv rate limits. Re-running skips already downloaded texts.
"""
import csv
import io
import time
from pathlib import Path

import requests
from pypdf import PdfReader

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = DATA / "fulltext"
UA = {"User-Agent": "SLR full-text retrieval (mailto:" + os.environ.get("OPENALEX_MAILTO", "") + ")"}


def safe(key):
    return key.replace(":", "_").replace("/", "_")


def pdf_text(content):
    reader = PdfReader(io.BytesIO(content))
    return "\n".join((p.extract_text() or "") for p in reader.pages)


def openalex_pdf_url(doi):
    js = requests.get(f"https://api.openalex.org/works/doi:{doi}",
                      params={"mailto": os.environ.get("OPENALEX_MAILTO", "")}, timeout=60).json()
    locs = [js.get("best_oa_location") or {}] + (js.get("locations") or [])
    return next((l["pdf_url"] for l in locs if l and l.get("pdf_url")), "")


def fetch(url):
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=120)
            if r.status_code == 200 and r.content[:4] == b"%PDF":
                return r.content
            if r.status_code == 429:
                time.sleep(60 * (attempt + 1))
                continue
            return None
        except requests.RequestException:
            time.sleep(10)
    return None


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    recs = {r["key"]: r for r in csv.DictReader(open(DATA / "records.csv"))}
    screen = list(csv.DictReader(open(DATA / "screening.csv")))
    preprint_of = {r["dup_of"]: recs[r["key"]]["arxiv_id"] for r in screen if r.get("dup_of")}
    matches = OUT / "arxiv_matches.csv"  # title-matched preprints (find_arxiv.py)
    if matches.exists():
        preprint_of.update({m["key"]: m["arxiv_id"] for m in csv.DictReader(open(matches))})
    todo = [r for r in screen if r["abs_decision"] in ("include", "unsure") and r.get("ft_reason") != "EC7"]
    log = []
    for s in todo:
        rid, rec = s["key"], recs[s["key"]]
        out = OUT / f"{safe(rid)}.txt"
        if out.exists():
            log.append({"key": rid, "status": "ok", "source": "cached"})
            continue
        arx = rec["arxiv_id"] or preprint_of.get(rid, "")
        url = f"https://arxiv.org/pdf/{arx}" if arx else (openalex_pdf_url(rec["doi"]) if rec["doi"] else "")
        content = fetch(url) if url else None
        if content:
            try:
                out.write_text(pdf_text(content), encoding="utf-8", errors="replace")
                status = "ok"
            except Exception as e:  # malformed PDF
                status = f"parse-error: {e.__class__.__name__}"
        else:
            status = "no-open-full-text"
        log.append({"key": rid, "status": status, "source": url})
        print(rid, status, url, flush=True)
        time.sleep(4 if "arxiv.org" in url else 1)
    with open(OUT / "log.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["key", "status", "source"])
        w.writeheader()
        w.writerows(log)
