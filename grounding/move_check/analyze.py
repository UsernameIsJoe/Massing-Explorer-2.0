"""Move check analysis: does key-move text track its referenced decisions better than
idea text (concept + intent) tracks the whole record?

For each encoder: Spearman correlation between text cosine distance and decision-signature
Jaccard distance, with an item-permutation (Mantel) test, 9,999 permutations.
  idea level  15 seeds, whole-record signatures
  move level  54 key moves, referenced-decision signatures (all pairs, and cross-seed pairs only)

Usage (from repo root):  python grounding/move_check/analyze.py
"""
import json
import random
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent


def jacc(a, b):
    A, B = {tuple(x) for x in a}, {tuple(x) for x in b}
    return 1 - len(A & B) / len(A | B)


def mantel(V, sigs, mask=None, n=9999, seed=20261029):
    k = len(sigs)
    X = V / np.linalg.norm(V, axis=1, keepdims=True)
    S = 1 - X @ X.T
    D = np.array([[jacc(sigs[i], sigs[j]) for j in range(k)] for i in range(k)])
    iu = np.triu_indices(k, 1)
    sel = np.ones(len(iu[0]), bool) if mask is None else mask[iu]
    rho = spearmanr(S[iu][sel], D[iu][sel])[0]
    rng = random.Random(seed)
    ge = 0
    for _ in range(n):
        p = list(range(k)); rng.shuffle(p)
        Dp = D[np.ix_(p, p)]
        if spearmanr(S[iu][sel], Dp[iu][sel])[0] >= rho:
            ge += 1
    return round(float(rho), 3), round((ge + 1) / (n + 1), 4)


def main():
    texts = {t["text_id"]: t for t in json.loads((HERE / "texts.json").read_text(encoding="utf-8"))}
    E = {}
    for line in (HERE / "embeddings.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        E.setdefault(r["encoder"], {})[r["text_id"]] = np.array(r["vector"])
    out = {}
    for enc, vecs in E.items():
        for kind in ("idea", "move"):
            ids = sorted(t for t in texts if texts[t]["kind"] == kind)
            V = np.array([vecs[i] for i in ids])
            sigs = [texts[i]["sig"] for i in ids]
            out[f"{enc}|{kind}"] = mantel(V, sigs, n=2999 if kind == "move" else 9999)
            if kind == "move":
                cases = [texts[i]["case"] for i in ids]
                mask = np.array([[cases[a] != cases[b] for b in range(len(ids))] for a in range(len(ids))])
                out[f"{enc}|move_cross_seed"] = mantel(V, sigs, mask=mask, n=2999)
    (HERE / "results.json").write_text(json.dumps({k: {"rho": v[0], "p": v[1]} for k, v in out.items()}, indent=1), encoding="utf-8")
    for k, (r, p) in out.items():
        print(f"{k:38} rho {r:+.3f}  p {p}")


if __name__ == "__main__":
    main()
