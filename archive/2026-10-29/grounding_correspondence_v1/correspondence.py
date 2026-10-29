"""Grounding step 2a: which axes does semantic distance track? (15 seeds, runs 01-03)

Semantic distance: cosine distance of bge-m3 embeddings (Pilot 01b runs; config p01-enc-v1).
Axis distance per axis (axes-v1): share of differing bits for program_organization and
vertical_organization, 0/1 for topology, absolute difference for scalars.
Spearman correlation over the 105 seed pairs. Pairs share seeds, so p-values are optimistic.

Usage (from repo root):
    python grounding/correspondence.py
"""
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parent.parent
AXES = ["program_organization", "distribution_balance", "topology", "mean_height", "height_articulation", "vertical_organization"]


def main():
    E = {}
    for line in (REPO / "pilots/p01b-concept/runs/bge-m3/embeddings.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        E[r["text_id"]] = np.array(r["vector"])
    A = json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/axes/axes_v1.json").read_text(encoding="utf-8"))["cases"]
    pairs = list(itertools.combinations(sorted(A), 2))

    def sem(a, b, v):
        x, y = E[f"{a}::{v}"], E[f"{b}::{v}"]
        return 1 - float(x @ y / np.linalg.norm(x) / np.linalg.norm(y))

    def ax(a, b, name):
        p, q = A[a][name]["value"], A[b][name]["value"]
        if isinstance(p, dict):
            return sum(p[k] != q[k] for k in p) / len(p)
        if isinstance(p, str):
            return float(p != q)
        return abs(p - q)

    out = {}
    for v in ("concept", "concept_intent"):
        s = [sem(a, b, v) for a, b in pairs]
        for name in AXES:
            r, p = spearmanr(s, [ax(a, b, name) for a, b in pairs])
            out[f"{v}|{name}"] = {"rho": round(float(r), 3), "p": round(float(p), 4)}
            print(f"{v:15} {name:22} rho {r:+.3f}  p {p:.4f}")
    (REPO / "grounding/correspondence_v1.json").write_text(json.dumps({"pairs": len(pairs), "encoder": "bge-m3", "results": out}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
