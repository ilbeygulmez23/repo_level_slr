import os
"""Backward + forward snowballing (Wohlin) over OpenAlex for the included studies.

Usage: python snowball.py <round>   e.g. python snowball.py 1
Seeds: studies with ft_decision == include in data/screening.csv (round 1), or the inclusions of
the previous round (later rounds). Candidates not already in records.csv are written to
data/snowball_r<round>.csv for screening.
"""
import csv
import re
import sys
import time
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data"
API = "https://api.openalex.org/works"
MAIL = {"mailto": os.environ.get("OPENALEX_MAILTO", "")}
D0, D1 = "2022-01-01", "2026-09-30"
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())[:60]


def openalex_id(rec):
    ref = f"doi:{rec['doi']}" if rec["doi"] else (f"doi:10.48550/arxiv.{rec['arxiv_id']}" if rec["arxiv_id"] else "")
    if not ref:
        return ""
    r = requests.get(f"{API}/{ref}", params={**MAIL, "select": "id,referenced_works"}, timeout=60)
    return r.json() if r.status_code == 200 else ""


def works(filter_):
    out, cursor = [], "*"
    while cursor:
        js = requests.get(API, params={**MAIL, "filter": filter_, "per-page": 200, "cursor": cursor,
                                       "select": "id,doi,title,publication_date,abstract_inverted_index,primary_location"},
                          timeout=90).json()
        out += js.get("results", [])
        cursor = js.get("meta", {}).get("next_cursor")
    return out


def abstract(inv):
    pos = {p: w for w, ps in (inv or {}).items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


if __name__ == "__main__":
    rnd = int(sys.argv[1])
    recs = {r["key"]: r for r in csv.DictReader(open(DATA / "records.csv"))}
    known = {norm(r["title"]) for r in recs.values()}
    if rnd == 1:
        seeds = [recs[s["key"]] for s in csv.DictReader(open(DATA / "screening.csv")) if s.get("ft_decision") == "include"]
    else:  # seeds = studies included since the previous round (data/snowball_seeds_r<rnd>.txt)
        seeds = [recs[k] for k in open(DATA / f"snowball_seeds_r{rnd}.txt").read().split() if k in recs]
    cands = {}
    for s in seeds:
        w = openalex_id(s)
        if not w:
            print("not in OpenAlex:", s["title"][:70])
            continue
        wid = w["id"].rsplit("/", 1)[-1]
        refs = [x.rsplit("/", 1)[-1] for x in w.get("referenced_works", [])]
        found = []
        for i in range(0, len(refs), 50):  # backward
            found += works(f"openalex:{'|'.join(refs[i:i + 50])},from_publication_date:{D0}")
        found += works(f"cites:{wid},from_publication_date:{D0},to_publication_date:{D1}")  # forward
        for f in found:
            t = norm(f.get("title"))
            if t and t not in known:
                c = cands.setdefault(t, {"title": f["title"], "doi": (f.get("doi") or "").replace("https://doi.org/", ""),
                                         "date": f.get("publication_date"), "abstract": abstract(f.get("abstract_inverted_index")),
                                         "venue": ((f.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
                                         "found_via": set()})
                c["found_via"].add(s["title"][:40])
        time.sleep(0.2)
    with open(DATA / f"snowball_r{rnd}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["title", "doi", "date", "venue", "n_seeds", "found_via", "abstract",
                                           "decision", "reason", "ft_decision", "note"])
        w.writeheader()
        for c in sorted(cands.values(), key=lambda c: -len(c["found_via"])):
            w.writerow({**c, "n_seeds": len(c["found_via"]), "found_via": " | ".join(sorted(c["found_via"]))[:300]})
    print(f"round {rnd}: seeds={len(seeds)} new candidates={len(cands)}")
