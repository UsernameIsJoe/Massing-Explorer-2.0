"""Pilot 9 scoring: canonical describer. Implements PROTOCOL.md. Written before any description or embedding exists.

Usage (from repo root):  python pilots/p09-canonical-describer/scripts/score_p09.py
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
P4 = REPO / "pilots/p04-guided-exploration"
sys.path.insert(0, str(P4 / "scripts"))
import score_p04 as s  # noqa: E402
import expand  # noqa: E402

ENCODERS = ["qwen3-embedding:4b", "mxbai-embed-large", "nomic-embed-text", "bge-m3"]
PRIMARY = ENCODERS[0]
N_PERM, N_MANTEL, SEED = 10_000, 9_999, 20261103


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
        E.setdefault(r["encoder"], {})[r["text_id"]] = np.array(r["vector"], dtype=float)
    key = json.loads((HERE / "data/item_key_SEALED.json").read_text(encoding="utf-8"))
    src_to_x = {v["source"]: x for x, v in key.items()}
    e_of = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))["archive_ids"]
    arch = sorted(e_of)
    sc = json.loads((P4 / "results/scores.json").read_text(encoding="utf-8"))["per_case"]
    qs = sorted(sc)
    twins = {q: sc[q]["struct_nearest_archive"] for q in qs if sc[q]["struct_change_to_archive"] < 1.0}
    fam = {e: f for f, v in json.loads((REPO / "pilots/p05-neighbourhood-address/reference/families_claude_v1.json")
                                       .read_text(encoding="utf-8"))["families"].items() for e in v["members"]}
    ref = [fam[e_of[a]] for a in arch]
    arch_cases, cases = s.archive(), s.load_cases()
    states = [expand.state_of(arch_cases[a]) for a in arch] + [s.state(cases[q]["case"]) for q in qs]
    n = len(states)
    D = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        D[i, j] = D[j, i] = (expand.change(states[i], states[j])[0] + expand.change(states[j], states[i])[0]) / 2
    iu = np.triu_indices(n, 1)
    rng = np.random.default_rng(SEED)
    out = {"encoders": {}}
    for enc in ENCODERS:
        def comb(ids):
            xs = [src_to_x[i] for i in ids]
            return np.hstack([norm(np.array([E[enc][f"{x}::concept"] for x in xs])),
                              norm(np.array([E[enc][f"{x}::intent"] for x in xs]))]) / np.sqrt(2)
        S, C = comb(arch), comb(qs)
        T = sum(int(np.argmax(S @ C[qs.index(q)]) == arch.index(a)) for q, a in twins.items())
        Tf = sum(fam[e_of[arch[int(np.argmax(S @ C[qs.index(q)]))]]] == fam[e_of[a]] for q, a in twins.items())
        k1 = best_k(S, range(3, 9))
        lab = cluster(S, k1)
        ari = float(adjusted_rand_score(lab, ref))
        p = (sum(adjusted_rand_score(lab, rng.permutation(ref)) >= ari for _ in range(N_PERM)) + 1) / (N_PERM + 1)
        X = np.vstack([S, C])
        M = X @ X.T
        np.fill_diagonal(M, -9)
        nn_seed = int(sum(np.argmax(M[len(arch) + j]) < len(arch) for j in range(len(qs))))
        kb = best_k(X, range(3, 13))
        ari_b = float(adjusted_rand_score(cluster(X, kb), [1] * len(arch) + [0] * len(qs)))
        cos = 1 - X @ X.T
        obs = spearmanr(cos[iu], D[iu])[0]
        hits = 0
        for _ in range(N_MANTEL):
            pr = rng.permutation(n)
            hits += spearmanr(cos[np.ix_(pr, pr)][iu], D[iu])[0] >= obs
        out["encoders"][enc] = {
            "T_twins_nearest_seed_is_twin": T, "T_pass": T >= 9, "T_fam": int(Tf),
            "C1": {"k": int(k1), "ari_idea_families": round(ari, 3), "perm_p": round(p, 4), "pass": ari >= 0.40 and p < 0.05,
                   "neighbourhoods": {str(c): sorted(e_of[a] for a, l in zip(arch, lab) if l == c) for c in sorted(set(lab))}},
            "C2a_cases_with_seed_nearest": nn_seed, "C2b_ari_clusters_batch": round(ari_b, 3), "C2b_k": int(kb),
            "Q3_mantel_all55": {"rho": round(float(obs), 3), "p": round((hits + 1) / (N_MANTEL + 1), 4)},
            "per_twin": {q: {"twin": e_of[a], "nearest_seed": e_of[arch[int(np.argmax(S @ C[qs.index(q)]))]]} for q, a in twins.items()},
        }
    R = out["encoders"]
    holds = lambda f: f(R[PRIMARY]) and any(f(R[e]) for e in ENCODERS[1:])  # noqa: E731
    T_ok, C1_ok = holds(lambda r: r["T_pass"]), holds(lambda r: r["C1"]["pass"])
    T5 = holds(lambda r: r["T_twins_nearest_seed_is_twin"] >= 5)
    out["T_pass"], out["C1_pass"] = T_ok, C1_ok
    out["reading"] = ("C1 fails: the describer flattens ideas; revise it" if not C1_ok else
                      "pass: describer becomes a method step; build map v0.1" if T_ok else
                      "partial (T 5-8): family level only; test the questionnaire for strategy level" if T5 else
                      "T < 5: questionnaire representation as the meaning side")
    dest = HERE / "results/scores_p09.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
