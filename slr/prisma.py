"""Print PRISMA 2020 flow counts from the search logs, records.csv and screening.csv."""
import csv
from collections import Counter
from pathlib import Path

from merge import load_raw

DATA = Path(__file__).parent / "data"

raw = Counter(r["source"] for r in load_raw())

records = list(csv.DictReader(open(DATA / "records.csv")))
screen = list(csv.DictReader(open(DATA / "screening.csv")))
n_raw = sum(int(r["n_raw"]) for r in records)

print("IDENTIFICATION")
for src, n in sorted(raw.items()):
    if n:
        print(f"  {src:10} {n}")
print(f"  total records identified: {n_raw}")
print(f"  duplicates removed:       {n_raw - len(records)}")
print("SCREENING (title)")
print(f"  records screened:         {len(screen)}")
print(f"  excluded:                 {Counter(r['title_reason'] for r in screen if r['title_decision'] == 'exclude')}")
abs_ = [r for r in screen if r["title_decision"] == "abstract"]
print("SCREENING (abstract)")
print(f"  records screened:         {len(abs_)}")
print(f"  excluded:                 {Counter(r['abs_reason'] for r in abs_ if r['abs_decision'] == 'exclude')}")
print(f"  to full text:             include={sum(r['abs_decision'] == 'include' for r in abs_)} "
      f"unsure={sum(r['abs_decision'] == 'unsure' for r in abs_)}")
if "ft_decision" in screen[0]:
    ft = [r for r in screen if r.get("ft_decision")]
    print("ELIGIBILITY (full text)")
    print(f"  assessed: {len(ft)}  excluded: {Counter(r['ft_reason'] for r in ft if r['ft_decision'] == 'exclude')}")
    print(f"  INCLUDED: {sum(r['ft_decision'] == 'include' for r in ft)}")
