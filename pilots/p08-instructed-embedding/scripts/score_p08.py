"""Pilot 8 scoring: instructed qwen3 embeddings. Implements PROTOCOL.md. Written before the local embeddings arrived.

Usage (from repo root):  python pilots/p08-instructed-embedding/scripts/score_p08.py
"""
import json
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
P4 = REPO / "pilots/p04-guided-exploration"
ENC = "qwen3-embedding:4b"
N_PERM, SEED = 10_000, 20261103


def norm(M):
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def cluster(X, k):
    return AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average").fit_predict(X)


def best_k(X, ks):
    sil = {k: float(silhouette_score(X, cluster(X, k), metric="cosine")) for k in ks}
    return max(sil, key=sil.get)


def main():
    E = {}
    for line in open(HERE / "local/embeddings.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["encoder"] == ENC:
            E[r["text_id"]] = np.array(r["vector"], dtype=float)
    e_of = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))["archive_ids"]
    arch = sorted(e_of)
    sc = json.loads((P4 / "results/scores.json").read_text(encoding="utf-8"))["per_case"]
    qs = sorted(sc)
    twins = {q: sc[q]["struct_nearest_archive"] for q in qs if sc[q]["struct_change_to_archive"] < 1.0}
    fam = {e: f for f, v in json.loads((REPO / "pilots/p05-neighbourhood-address/reference/families_claude_v1.json")
                                       .read_text(encoding="utf-8"))["families"].items() for e in v["members"]}

    def comb(prefix, ids):
        return np.hstack([norm(np.array([E[f"{prefix}:{i}::concept"] for i in ids])),
                          norm(np.array([E[f"{prefix}:{i}::intent"] for i in ids]))]) / np.sqrt(2)

    Cs = comb("case", qs)
    out = {"encoder": ENC, "n_twins": len(twins)}
    for name, prefix in (("original", "orig"), ("reexpressed", "p07")):
        S = comb(prefix, arch)
        T = sum(int(np.argmax(S @ Cs[qs.index(q)]) == arch.index(a)) for q, a in twins.items())
        X = np.vstack([S, Cs])
        M = X @ X.T
        np.fill_diagonal(M, -9)
        nn_seed = int(sum(np.argmax(M[len(arch) + j]) < len(arch) for j in range(len(qs))))
        kb = best_k(X, range(3, 13))
        is_seed = [1] * len(arch) + [0] * len(qs)
        res = {"T_twins_nearest_seed_is_twin": T, "C2a_cases_with_seed_nearest": nn_seed,
               "C2b_ari_clusters_batch": round(float(adjusted_rand_score(cluster(X, kb), is_seed)), 3), "C2b_k": int(kb),
               "per_twin": {q: {"twin": e_of[a], "nearest_seed": e_of[arch[int(np.argmax(S @ Cs[qs.index(q)]))]]} for q, a in twins.items()}}
        if name == "original":
            k1 = best_k(S, range(3, 9))
            lab = cluster(S, k1)
            ref = [fam[e_of[a]] for a in arch]
            ari = float(adjusted_rand_score(lab, ref))
            rng = np.random.default_rng(SEED)
            p = (sum(adjusted_rand_score(lab, rng.permutation(ref)) >= ari for _ in range(N_PERM)) + 1) / (N_PERM + 1)
            res["C1"] = {"k": int(k1), "ari_idea_families": round(ari, 3), "perm_p": round(p, 4), "pass": ari >= 0.40 and p < 0.05,
                         "neighbourhoods": {str(c): sorted(e_of[a] for a, l in zip(arch, lab) if l == c) for c in sorted(set(lab))}}
        out[name] = res
    T, c1 = out["original"]["T_twins_nearest_seed_is_twin"], out["original"]["C1"]["pass"]
    out["pass"] = T >= 9 and c1
    out["reading"] = ("C1 fails: do not use the instruction" if not c1 else
                      "pass: instructed embeddings for map v0.1" if T >= 9 else
                      "helps but not enough: canonical describer, embedded with the instruction" if T >= 5 else
                      "no change: canonical describer")
    dest = HERE / "results/scores_p08.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
