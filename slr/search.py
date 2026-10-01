import os
"""Run the query families against the open sources (arXiv, OpenAlex) and store raw records.

Usage:
  python search.py --count     # only report hit counts per source x family (pilot)
  python search.py             # fetch all records -> data/raw/<source>_<family>.jsonl, data/search_log.csv
"""
import argparse
import csv
import json
import time
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import requests

from render_queries import Q, arxiv, arxiv_parts, openalex

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw"
MAILTO = os.environ.get("OPENALEX_MAILTO", "")  # OpenAlex polite pool
ATOM = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/"}
D0, D1 = Q["window"]["from"], Q["window"]["to"]


def _get(url, **params):
    for attempt in range(6):
        try:
            r = requests.get(url, params=params, timeout=90)
        except requests.RequestException:
            time.sleep(10)
            continue
        if r.status_code == 200:
            return r
        time.sleep(30 * (attempt + 1))  # arXiv 429s need long back-off
    r.raise_for_status()


# ---------- arXiv ----------
def arxiv_search(family, count_only=False):
    """Union of per-term sub-queries (see render_queries.arxiv_parts); hits = unique records."""
    recs, sub_hits = {}, 0
    for part in arxiv_parts(family):
        _, total, part_recs = _arxiv_query(part, count_only)
        sub_hits += total
        print(f"  arXiv sub-query hits={total}: {part[:60]}", flush=True)
        recs.update((r["arxiv_id"], r) for r in part_recs)
        time.sleep(10)
    return arxiv(family), (sub_hits if count_only else len(recs)), list(recs.values())


def _arxiv_query(q, count_only=False):
    q = f"({q}) AND submittedDate:[{D0.replace('-', '')}0000 TO {D1.replace('-', '')}2359]"
    recs, start, total = [], 0, None
    while total is None or start < total:
        root = ET.fromstring(_get("https://export.arxiv.org/api/query", search_query=q,
                                  start=start, max_results=200).text)
        total = int(root.find("os:totalResults", ATOM).text)
        if count_only:
            return q, total, []
        entries = root.findall("a:entry", ATOM)
        if not entries:
            break
        for e in entries:
            aid = e.find("a:id", ATOM).text.split("/abs/")[-1].rsplit("v", 1)[0]
            doi = e.find("{http://arxiv.org/schemas/atom}doi")
            recs.append({
                "source": "arXiv", "source_id": aid, "arxiv_id": aid,
                "doi": doi.text.lower() if doi is not None else "",
                "title": " ".join(e.find("a:title", ATOM).text.split()),
                "abstract": " ".join(e.find("a:summary", ATOM).text.split()),
                "date": e.find("a:published", ATOM).text[:10],
                "venue": "arXiv",
                "authors": "; ".join(a.find("a:name", ATOM).text for a in e.findall("a:author", ATOM)),
            })
        start += len(entries)
        time.sleep(10)  # arXiv API etiquette (429s at 3 s)
    return q, total, recs


# ---------- OpenAlex ----------
def _abstract(inv):
    if not inv:
        return ""
    pos = {p: w for w, ps in inv.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


def openalex_search(family, count_only=False):
    q = openalex(family)
    flt = f"title_and_abstract.search:{q},from_publication_date:{D0},to_publication_date:{D1}"
    recs, cursor, total = [], "*", None
    while cursor:
        js = _get("https://api.openalex.org/works", filter=flt, cursor=cursor,
                  **{"per-page": 200, "mailto": MAILTO}).json()
        total = js["meta"]["count"]
        if count_only:
            return q, total, []
        for w in js["results"]:
            ids = w.get("ids", {})
            loc = w.get("primary_location") or {}
            src = loc.get("source") or {}
            arx = next((l.get("landing_page_url", "") for l in w.get("locations", [])
                        if "arxiv.org" in (l.get("landing_page_url") or "")), "")
            recs.append({
                "source": "OpenAlex", "source_id": w["id"].rsplit("/", 1)[-1],
                "arxiv_id": arx.rstrip("/").split("/abs/")[-1].rsplit("v", 1)[0] if "/abs/" in arx else "",
                "doi": (ids.get("doi") or "").replace("https://doi.org/", "").lower(),
                "title": w.get("title") or "",
                "abstract": _abstract(w.get("abstract_inverted_index")),
                "date": w.get("publication_date") or "",
                "venue": src.get("display_name") or "",
                "authors": "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])),
            })
        cursor = js["meta"].get("next_cursor")
    return q, total, recs


SOURCES = {"arXiv": arxiv_search, "OpenAlex": openalex_search}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--source", choices=list(SOURCES), help="run one source only")
    args = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    log = []
    for src, fn in SOURCES.items():
        if args.source and src != args.source:
            continue
        for fam in Q["families"]:
            q, total, recs = fn(fam, count_only=args.count)
            print(f"{src:9} {fam:28} hits={total} fetched={len(recs)}")
            if not args.count:
                with open(RAW / f"{src}_{fam}.jsonl", "w") as f:
                    for r in recs:
                        f.write(json.dumps({**r, "family": fam}) + "\n")
                log.append({"source": src, "family": fam, "run_date": str(date.today()),
                            "hits": total, "fetched": len(recs), "query": q})
    if log:
        with open(HERE / "data" / "search_log.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=log[0].keys())
            w.writeheader()
            w.writerows(log)
