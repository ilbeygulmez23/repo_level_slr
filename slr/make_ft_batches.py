"""Create full-text eligibility batches for candidates not yet assigned.

Usage: python make_ft_batches.py [--all] [--size 12]
Without --all only candidates whose full text is already downloaded are batched;
with --all the rest are batched too (text_file empty = no open full text).
Assignments are tracked in data/ft_batches/assigned.txt so each paper is batched once.
"""
import argparse
import csv
from pathlib import Path

from fetch_fulltext import safe

DATA = Path(__file__).parent / "data"
OUT = DATA / "ft_batches"

ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true")
ap.add_argument("--size", type=int, default=12)
args = ap.parse_args()

assigned_file = OUT / "assigned.txt"
assigned = set(assigned_file.read_text().split()) if assigned_file.exists() else set()
cands = [s for s in csv.DictReader(open(DATA / "screening.csv"))
         if s["abs_decision"] in ("include", "unsure") and s["ft_reason"] != "EC7" and s["key"] not in assigned]
rows = []
for s in cands:
    txt = DATA / "fulltext" / f"{safe(s['key'])}.txt"
    if txt.exists() or args.all:
        rows.append({"key": s["key"], "title": s["title"], "abs_decision": s["abs_decision"], "tier": s["tier"],
                     "note": s["note"], "text_file": str(txt) if txt.exists() else ""})

start = len(list(OUT.glob("batch*.csv"))) - len(list(OUT.glob("batch*_ft.csv"))) + 1
for i in range(0, len(rows), args.size):
    n = start + i // args.size
    with open(OUT / f"batch{n}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows[i:i + args.size])
    print(f"batch{n}: {len(rows[i:i + args.size])}")
with open(assigned_file, "a") as f:
    f.writelines(r["key"] + "\n" for r in rows)
