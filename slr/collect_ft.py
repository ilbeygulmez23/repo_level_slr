"""Collect full-text decisions and notes from data/ft_batches into screening.csv, corpus.csv and corpus_notes.md."""
import csv
import glob
import re
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
EXTRA = ["task", "contribution", "languages", "evaluation", "venue"]

ft = {}
for path in sorted(glob.glob(str(DATA / "ft_batches" / "batch*_ft.csv"))):
    for r in csv.DictReader(open(path)):
        ft[r["key"]] = r

# reviewer-1 adjudications override agent decisions: | key | paper | agent | final | rationale |
flags = {}
for line in open(DATA / "ft_batches" / "adjudication.md"):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 5 or cells[0] not in ft:
        continue
    final = cells[3].replace("*", "").lower()
    d = ft[cells[0]]
    if final.startswith("exclude"):
        d["ft_decision"], d["ft_reason"] = "exclude", (re.findall(r"ec\d+", final) or [""])[0].upper()
    elif final.startswith("include"):
        d["ft_decision"], d["ft_reason"] = "include", ""
        d["tier"] = "core" if "core" in final else "contextual"
    flags[cells[0]] = ";".join(f for f in ("peripheral", "low qa") if f in final)

rows = list(csv.DictReader(open(DATA / "screening.csv")))
for s in rows:
    d = ft.get(s["key"])
    if d:
        s["ft_decision"], s["ft_reason"] = d["ft_decision"], d["ft_reason"]
        if d["ft_decision"] == "include":
            s["tier"] = d["tier"]
with open(DATA / "screening.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

recs = {r["key"]: r for r in csv.DictReader(open(DATA / "records.csv"))}
corpus = [s for s in rows if s["ft_decision"] == "include"]
with open(DATA / "corpus.csv", "w", newline="") as f:
    fields = ["key", "title", "year", "venue_record", "doi", "arxiv_id", "tier", "flags"] + EXTRA + ["ft_note"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for s in sorted(corpus, key=lambda s: (s["tier"], recs[s["key"]]["year"], s["title"])):
        r, d = recs[s["key"]], ft[s["key"]]
        w.writerow({"key": s["key"], "title": r["title"], "year": r["year"], "venue_record": r["venue"],
                    "doi": r["doi"], "arxiv_id": r["arxiv_id"], "tier": s["tier"], "flags": flags.get(s["key"], ""),
                    **{k: d.get(k, "") for k in EXTRA}, "ft_note": d.get("note", "")})

# notes: keep only entries of included papers, grouped by tier/task
notes = {}
for path in sorted(glob.glob(str(DATA / "ft_batches" / "batch*_notes.md"))):
    for block in re.split(r"\n(?=### )", open(path).read()):
        m = re.search(r"\[((?:arxiv|doi|title):[^\]]+)\]", block.split("\n", 1)[0])
        if m and m.group(1) in ft and ft[m.group(1)]["ft_decision"] == "include":
            notes[m.group(1)] = block.strip()
out = ["# Paper notes — final corpus\n\nAuto-collected from full-text review; grouped by tier and task.\n"]
for tier in ("core", "contextual"):
    for task in sorted({ft[k].get("task", "") for k in notes if ft[k]["tier"] == tier}):
        out.append(f"\n## {tier} / {task}\n")
        out += [notes[k] + "\n" for k in notes if ft[k]["tier"] == tier and ft[k].get("task", "") == task]
(HERE / "corpus_notes.md").write_text("\n".join(out))
missing = [s["title"][:60] for s in corpus if s["key"] not in notes]
print(f"assessed={len(ft)} included={len(corpus)} notes={len(notes)} missing_notes={len(missing)}")
for t in missing:
    print("  no note:", t)
