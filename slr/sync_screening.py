"""After re-running merge.py: re-attach existing screening rows to records.csv and list unscreened records.

Existing decisions are matched by key, falling back to normalised title (a key can change when a
new source adds an arXiv ID to a record). Unscreened records are written to data/new_records.csv.
"""
import csv
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())[:60]

recs = list(csv.DictReader(open(DATA / "records.csv")))
by_key = {r["key"]: r for r in recs}
by_title = {norm(r["title"]): r for r in recs}

rows, seen = [], set()
for s in csv.DictReader(open(DATA / "screening.csv")):
    r = by_key.get(s["key"]) or by_title.get(norm(s["title"]))
    if not r or r["key"] in seen:  # merged into another record that already has a decision
        print("dropped (merged):", s["title"][:70])
        continue
    s["key"], s["rid"] = r["key"], r["rid"]
    seen.add(r["key"])
    rows.append(s)
with open(DATA / "screening.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

new = [r for r in recs if r["key"] not in seen]
with open(DATA / "new_records.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["rid", "key", "year", "sources", "venue", "title", "abstract"], extrasaction="ignore")
    w.writeheader()
    w.writerows(new)
print(f"records={len(recs)} screened={len(seen)} new={len(new)} -> data/new_records.csv")
