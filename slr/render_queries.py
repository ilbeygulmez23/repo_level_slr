"""Render the database-agnostic query families in queries.json into each database's syntax.

Usage: python render_queries.py  -> writes queries_rendered.md
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
Q = json.loads((HERE / "queries.json").read_text())


def _or(terms, fmt):
    return "(" + " OR ".join(fmt(t) for t in terms) + ")"


def arxiv(family):
    blocks = [_or(Q["blocks"][b], lambda t: f'ti:"{t}" OR abs:"{t}"') for b in Q["families"][family]]
    return " AND ".join(blocks)


def arxiv_parts(family):
    """The arXiv API rejects long queries (HTTP 503), so the first block is split into one
    sub-query per term; the union of the sub-queries equals arxiv(family)."""
    first, *rest = Q["families"][family]
    tail = " AND ".join(_or(Q["blocks"][b], lambda t: f'ti:"{t}" OR abs:"{t}"') for b in rest)
    return [f'(ti:"{t}" OR abs:"{t}") AND {tail}' for t in Q["blocks"][first]]


def openalex(family):
    return " AND ".join(_or(Q["blocks"][b], lambda t: f'"{t}"') for b in Q["families"][family])


def scopus(family):
    inner = " AND ".join(_or(Q["blocks"][b], lambda t: f'"{t}"') for b in Q["families"][family])
    y0, y1 = int(Q["window"]["from"][:4]), int(Q["window"]["to"][:4])
    return f"TITLE-ABS-KEY({inner}) AND PUBYEAR > {y0 - 1} AND PUBYEAR < {y1 + 1}"


def ieee(family):
    return " AND ".join(_or(Q["blocks"][b], lambda t: f'"All Metadata":"{t}"') for b in Q["families"][family])


def acm(family):
    # Title OR Abstract per block (AllField would also match full text).
    blocks = []
    for b in Q["families"][family]:
        terms = _or(Q["blocks"][b], lambda t: f'"{t}"')
        blocks.append(f"(Title:{terms} OR Abstract:{terms})")
    return " AND ".join(blocks)


RENDERERS = {"arXiv": arxiv, "OpenAlex": openalex, "Scopus": scopus, "IEEE Xplore": ieee, "ACM DL": acm}

if __name__ == "__main__":
    out = [f"# Rendered search strings\n\nWindow: {Q['window']['from']} to {Q['window']['to']}. "
           "Generated from queries.json; do not edit by hand.\n"]
    for fam in Q["families"]:
        out.append(f"\n## {fam}\n")
        for db, fn in RENDERERS.items():
            out.append(f"\n### {db}\n\n```\n{fn(fam)}\n```\n")
    (HERE / "queries_rendered.md").write_text("".join(out))
    print("wrote queries_rendered.md")
