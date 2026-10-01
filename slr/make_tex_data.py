"""Generate LaTeX data for the survey from the SLR data: numbers.tex (macros), corpus_table.tex, corpus.bib.

Usage: python make_tex_data.py  -> ../survey/generated/
"""
import csv
import re
from collections import Counter
from pathlib import Path

from merge import load_raw

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE.parent / "survey" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

records = {r["key"]: r for r in csv.DictReader(open(DATA / "records.csv"))}
screen = list(csv.DictReader(open(DATA / "screening.csv")))
corpus = list(csv.DictReader(open(DATA / "corpus.csv")))
raw = Counter(r["source"] for r in load_raw())

# short names from the notes headings: "### Short — Title (...) [key]"
short = {}
for line in open(HERE / "corpus_notes.md"):
    m = re.match(r"### (.+?) — .*\[((?:arxiv|doi|title):[^\]]+)\]\s*$", line)
    if m:
        short[m.group(2)] = m.group(1).strip()


def bibkey(key):
    name = re.sub(r"[^A-Za-z0-9]", "", short.get(key, "") or records[key]["title"].split(":")[0])[:24]
    return f"{name}{records[key]['year']}"


def tex(s):
    return re.sub(r"([&%$#_{}])", r"\\\1", s or "").replace("~", r"\textasciitilde{}").replace("^", r"\^{}")


# ---------- numbers ----------
title_ex = Counter(s["title_reason"] for s in screen if s["title_decision"] == "exclude")
abs_ = [s for s in screen if s["title_decision"] == "abstract"]
abs_ex = Counter(s["abs_reason"] for s in abs_ if s["abs_decision"] == "exclude")
ft = [s for s in screen if s["ft_decision"]]
ft_ex = Counter(s["ft_reason"] for s in ft if s["ft_decision"] == "exclude")
db_sources = ("OpenAlex", "arXiv", "IEEE", "ACM")
n_db = sum(raw[s] for s in db_sources)
core = [c for c in corpus if c["tier"] == "core"]
ctx = [c for c in corpus if c["tier"] == "contextual"]
years = Counter(c["year"] for c in corpus)
peer = sum(1 for c in corpus if c["venue"] and c["venue"] != "preprint")
py = sum(1 for c in corpus if "python" in c["languages"].lower())
py_only = sum(1 for c in corpus if c["languages"].strip().lower() == "python")
ev = Counter(e for c in core for e in c["evaluation"].split(";") if e)
llm_meas = sum(1 for c in core if "llm-judge" in c["evaluation"])
task = Counter(c["task"] for c in core)
snow_inc = sum(1 for s in screen if s["ft_decision"] == "include" and "snowball" in s["note"])

macros = {
    "nRawDB": n_db, "nRawOpenAlex": raw["OpenAlex"], "nRawArXiv": raw["arXiv"], "nRawIEEE": raw["IEEE"],
    "nRawACM": raw["ACM"], "nRawSnowball": raw["Snowball"], "nRawTotal": sum(raw.values()),
    "nUnique": len(records), "nDuplicates": sum(raw.values()) - len(records),
    "nTitleScreened": len(screen), "nTitleExcluded": sum(title_ex.values()),
    "nAbsScreened": len(abs_), "nAbsExcluded": sum(abs_ex.values()),
    "nFullText": len(ft), "nFullTextExcluded": sum(ft_ex.values()),
    "nIncluded": len(corpus), "nCore": len(core), "nContextual": len(ctx), "nSnowballIncluded": snow_inc,
    "nPeerReviewed": peer, "nPreprint": len(corpus) - peer, "nPython": py, "nPythonOnly": py_only,
    "nCoreLLMJudge": llm_meas, "nCoreRefTests": ev["reference-unit-tests"], "nCoreDiffOracle": ev["differential-oracle"],
    "nCoreHuman": ev["human"], "nCoreSimilarity": ev["similarity"], "nCoreBDD": ev["bdd-e2e-tests"],
    "nCoreBuildRun": ev["build-run"], "nCoreNonfunctional": ev["nonfunctional"],
    "nFtNoText": sum(1 for s in ft if s["ft_reason"] == "EC8"),
    **{f"nYear{w}": years.get(y, 0) for y, w in (("2022", "TwentyTwo"), ("2023", "TwentyThree"), ("2024", "TwentyFour"), ("2025", "TwentyFive"), ("2026", "TwentySix"))},
    **{f"nTask{re.sub('[^A-Za-z]', '', t.title())}": n for t, n in task.items() if t},
}
reasons = {"title": title_ex, "abs": abs_ex, "ft": ft_ex}
lines = [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items()]
for stage, cnt in reasons.items():
    txt = ", ".join(f"{k}: {v}" for k, v in sorted(cnt.items()) if k)
    lines.append(f"\\newcommand{{\\reasons{stage.title()}}}{{{txt}}}")
(OUT / "numbers.tex").write_text("\n".join(lines) + "\n")

# ---------- bib ----------
bib = []
for c in corpus:
    r = records[c["key"]]
    authors = " and ".join(a.strip() for a in r["authors"].split(";") if a.strip()) or "Anonymous"
    fields = {"title": "{" + tex(r["title"]) + "}", "author": tex(authors), "year": r["year"]}
    if c["venue"] and c["venue"] != "preprint":
        fields["note"] = tex(c["venue"])
    if r["arxiv_id"]:
        fields["eprint"], fields["archivePrefix"] = r["arxiv_id"], "arXiv"
    if r["doi"] and not r["doi"].startswith("10.48550"):
        fields["doi"] = r["doi"]
    bib.append(f"@misc{{{bibkey(c['key'])},\n" + ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items()) + "\n}")
(OUT / "corpus.bib").write_text("\n\n".join(bib) + "\n")

# ---------- corpus table (appendix) ----------
rows = []
for c in sorted(corpus, key=lambda c: (c["tier"], c["task"], c["year"], short.get(c["key"], c["title"]))):
    name = tex(short.get(c["key"], c["title"][:40]))
    flags = r"\textsuperscript{p}" if "peripheral" in c["flags"] else ""
    flags += r"\textsuperscript{q}" if "low qa" in c["flags"] else ""
    rows.append(f"{name}{flags}~\\cite{{{bibkey(c['key'])}}} & {c['year']} & {c['tier']} & {tex(c['task'])} & "
                f"{tex(c['contribution'].replace(';', ', '))} & {tex(c['languages'].replace(';', ', '))[:30]} & "
                f"{tex(c['evaluation'].replace(';', ', '))} \\\\")
head = (r"{\scriptsize" "\n" r"\begin{longtable}{@{}p{2.8cm}lllp{1.9cm}p{1.5cm}p{2.9cm}@{}}" "\n"
        r"\caption{All included studies. Superscripts: p = peripheral, q = low evidence (Section~\ref{sec:method}).}\\" "\n"
        r"\toprule Study & Year & Tier & Task & Contribution & Languages & Evaluation \\ \midrule \endfirsthead" "\n"
        r"\toprule Study & Year & Tier & Task & Contribution & Languages & Evaluation \\ \midrule \endhead" "\n")
(OUT / "corpus_table.tex").write_text(head + "\n".join(rows) + "\n\\bottomrule\n\\end{longtable}\n}\n")

# key map for writing: short name -> bib key
with open(OUT / "keys.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["short", "bibkey", "tier", "task", "key"])
    for c in corpus:
        w.writerow([short.get(c["key"], ""), bibkey(c["key"]), c["tier"], c["task"], c["key"]])
dups = [k for k, n in Counter(bibkey(c["key"]) for c in corpus).items() if n > 1]
print(f"numbers={len(macros)} bib={len(bib)} rows={len(rows)} duplicate bibkeys={dups}")
