"""For full-text candidates without open full text, look up an arXiv preprint by exact title.
Writes data/fulltext/arxiv_matches.csv (key, arxiv_id, arxiv_title); fetch_fulltext.py then uses it."""
import csv, re, time, difflib, xml.etree.ElementTree as ET
import requests
from pathlib import Path
from fetch_fulltext import safe
DATA = Path(__file__).parent / "data"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
out = []
for s in csv.DictReader(open(DATA / "screening.csv")):
    if s["abs_decision"] not in ("include", "unsure") or s["ft_reason"] == "EC7":
        continue
    if (DATA / "fulltext" / f"{safe(s['key'])}.txt").exists():
        continue
    words = " AND ".join(f"ti:{w}" for w in norm(s["title"]).split()[:8] if len(w) > 3)
    try:
        root = ET.fromstring(requests.get("https://export.arxiv.org/api/query",
                             params={"search_query": words, "max_results": 5}, timeout=60).text)
    except Exception:
        time.sleep(10); continue
    best = max(((difflib.SequenceMatcher(None, norm(s["title"]), norm(e.find("a:title", ATOM).text)).ratio(),
                 e.find("a:id", ATOM).text.split("/abs/")[-1].rsplit("v", 1)[0], " ".join(e.find("a:title", ATOM).text.split()))
                for e in root.findall("a:entry", ATOM)), default=(0, "", ""))
    if best[0] > 0.9:
        out.append({"key": s["key"], "arxiv_id": best[1], "arxiv_title": best[2]})
        print(s["title"][:60], "->", best[1], flush=True)
    time.sleep(4)
with open(DATA / "fulltext" / "arxiv_matches.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["key", "arxiv_id", "arxiv_title"]); w.writeheader(); w.writerows(out)
print("matched", len(out))
