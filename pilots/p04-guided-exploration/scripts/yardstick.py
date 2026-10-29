"""Meaning-yardstick fix, as declared in YARDSTICK.md. Writes results/yardstick.json.

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/yardstick.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE / "scripts"))
import score_p04 as s  # noqa: E402

JUDGES = ["mxbai-embed-large", "nomic-embed-text", "qwen3-embedding:4b"]
CORRECTIONS = ["raw", "centred", "centred_pc1"]


def norm(M):
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def batches(E, enc, scores):
    key = json.loads((REPO / "pilots/p01c-robustness/data/rewrite_key_SEALED.json").read_text(encoding="utf-8"))
    origs = sorted(set(key.values()))
    arch = sorted(s.archive())
    cases = sorted(scores["per_case"])
    B = {"O": (origs, np.array([E[enc][f"p01c:{o}::original"] for o in origs])),
         "W": (sorted(key), np.array([E[enc][f"p01c:{p}::rewrite"] for p in sorted(key)])),
         "A": (arch, np.array([E[enc][f"archive:{a}::concept"] for a in arch])),
         "C": (cases, np.array([E[enc][f"case:{q}::concept"] for q in cases]))}
    return key, B


def correct(B, how):
    if how == "raw":
        return {k: (ids, norm(M)) for k, (ids, M) in B.items()}
    out = {k: (ids, norm(M - M.mean(0))) for k, (ids, M) in B.items()}
    if how == "centred_pc1":
        P = np.vstack([M for _, M in out.values()])
        pc = np.linalg.svd(P - P.mean(0), full_matrices=False)[2][0]
        out = {k: (ids, norm(M - np.outer(M @ pc, pc))) for k, (ids, M) in out.items()}
    return out


def evaluate(key, V):
    O_ids, O = V["O"]; W_ids, W = V["W"]; A_ids, A = V["A"]
    D_wo = 1 - W @ O.T
    own = np.array([D_wo[i, O_ids.index(key[p])] for i, p in enumerate(W_ids)])
    th = float(np.percentile(own, 95))
    own_nearest = int(sum(O_ids[int(np.argmin(D_wo[i]))] == key[p] for i, p in enumerate(W_ids)))
    D_aa = 1 - A @ A.T
    np.fill_diagonal(D_aa, 9)
    distinct = int(sum(D_aa.min(1) > th))
    return {"threshold": round(th, 4), "paraphrase_median": round(float(np.median(own)), 4),
            "seed_spacing_median": round(float(np.median(D_aa.min(1))), 4),
            "own_nearest": own_nearest, "seeds_distinct": distinct, "pass": own_nearest >= 12 and distinct >= 12}


def main():
    E = s.load_embeddings()
    scores = json.loads((HERE / "results/scores.json").read_text(encoding="utf-8"))
    table, chosen = {}, None
    for how in CORRECTIONS:
        for enc in JUDGES:
            key, B = batches(E, enc, scores)
            table[f"{how}|{enc}"] = evaluate(key, correct(B, how))
        passing = [enc for enc in JUDGES if table[f"{how}|{enc}"]["pass"]]
        if passing and chosen is None:
            chosen = (how, passing)
    out = {"table": table, "chosen": chosen}
    if chosen:
        how, judges = chosen
        P = scores["per_case"]
        new = {}
        for enc in judges:
            key, B = batches(E, enc, scores)
            V = correct(B, how)
            th = table[f"{how}|{enc}"]["threshold"]
            C_ids, C = V["C"]; _, A = V["A"]
            for i, q in enumerate(C_ids):
                prev = [j for j, p in enumerate(C_ids) if P[p]["arm"] == P[q]["arm"] and P[p]["order"] < P[q]["order"]]
                d = min([float((1 - A @ C[i]).min())] + [float(1 - C[j] @ C[i]) for j in prev])
                new.setdefault(q, []).append(d > th)
        summ = {}
        for arm in s.ARMS:
            qs = [q for q in P if P[q]["arm"] == arm]
            nm = [q for q in qs if all(new[q])]
            summ[arm] = {"new_meaning": len(nm),
                         "new_strategy": sum(P[q]["validity"] == "valid" and P[q]["new_structure"] for q in nm),
                         "new_strategy_incl_declared": sum(P[q]["validity"] in ("valid", "declared") and P[q]["new_structure"] for q in nm)}
        out["rescore"] = summ
        out["per_case_new_meaning"] = {q: all(v) for q, v in new.items()}
    (HERE / "results/yardstick.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in table.items():
        print(f"{k:32} {v}")
    print("chosen:", chosen)
    if chosen:
        for arm, v in out["rescore"].items():
            print(arm, v)


if __name__ == "__main__":
    main()
