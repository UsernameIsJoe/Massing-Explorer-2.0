"""Pilot 7 scoring: shared writer and format. Implements PROTOCOL.md. Written before the local embeddings arrived.

Usage (from repo root):  python pilots/p07-shared-format/scripts/score_p07.py
"""
import json
import re
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
P4, P5, P6 = (REPO / f"pilots/{p}" for p in ("p04-guided-exploration", "p05-neighbourhood-address", "p06-intent-view"))
ENCODERS = ["qwen3-embedding:4b", "mxbai-embed-large", "nomic-embed-text", "bge-m3"]
PRIMARY = ENCODERS[0]
N_PERM, SEED = 10_000, 20261103
KEYWORDS = {"F1_commons_heart": r"\bheart\b|\bhub\b|central (commons|hall)", "F2_civic_hinge_chain": r"\bhinge\b|gateway",
            "F3_linked_cluster_around_court": r"courtyard|\bcourt\b|\bring\b|\bloop\b", "F4_detached_campus": r"free-?standing|detached|pavilion|campus"}


def load(path):
    E = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        E.setdefault(r["encoder"], {})[r["text_id"]] = np.array(r["vector"], dtype=float)
    return E


def norm(M):
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def cluster(X, k):
    return AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average").fit_predict(X)


def best_k(X, ks):
    sil = {k: float(silhouette_score(X, cluster(X, k), metric="cosine")) for k in ks}
    return max(sil, key=sil.get)


def combined(C, I):
    return np.hstack([norm(C), norm(I)]) / np.sqrt(2)


def main():
    E4, E7 = load(P4 / "scoring/local/embeddings.jsonl"), load(HERE / "local/embeddings.jsonl")
    e_of = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))["archive_ids"]
    arch = sorted(e_of)
    qs = sorted(json.loads((P4 / "results/scores.json").read_text(encoding="utf-8"))["per_case"])
    case_text = {t["text_id"]: t["text"] for t in json.loads((P4 / "scoring/local/texts.json").read_text(encoding="utf-8"))}
    fam = {e: f for f, v in json.loads((P5 / "reference/families_claude_v1.json").read_text(encoding="utf-8"))["families"].items() for e in v["members"]}
    pur = {e: f for f, v in json.loads((P6 / "reference/purpose_families_claude_v1.json").read_text(encoding="utf-8"))["families"].items() for e in v["members"]}
    ref_i, ref_p = [fam[e_of[a]] for a in arch], [pur[e_of[a]] for a in arch]
    rng = np.random.default_rng(SEED)
    out = {"encoders": {}}
    for enc in ENCODERS:
        S7 = combined(np.array([E7[enc][f"p07:{a}::concept"] for a in arch]), np.array([E7[enc][f"p07:{a}::intent"] for a in arch]))
        Cs = combined(np.array([E4[enc][f"case:{q}::concept"] for q in qs]), np.array([E4[enc][f"case:{q}::intent"] for q in qs]))
        # C1: families preserved, re-expressed seeds alone
        k1 = best_k(S7, range(3, 9))
        lab = cluster(S7, k1)
        ari = float(adjusted_rand_score(lab, ref_i))
        p = (sum(adjusted_rand_score(lab, rng.permutation(ref_i)) >= ari for _ in range(N_PERM)) + 1) / (N_PERM + 1)
        c1 = {"k": int(k1), "ari_idea_families": round(ari, 3), "perm_p": round(p, 4), "pass": ari >= 0.40 and p < 0.05,
              "ari_purpose_families": round(float(adjusted_rand_score(lab, ref_p)), 3),
              "neighbourhoods": {str(c): sorted(e_of[a] for a, l in zip(arch, lab) if l == c) for c in sorted(set(lab))}}
        # C2: gap closed, uncentred pool of 15 re-expressed seeds + 40 cases
        X = np.vstack([S7, Cs])
        is_seed = np.array([True] * len(arch) + [False] * len(qs))
        S = X @ X.T
        np.fill_diagonal(S, -9)
        nn_seed = int(sum(is_seed[np.argmax(S[i])] for i in np.where(~is_seed)[0]))
        k2 = best_k(X, range(3, 13))
        ari_b = float(adjusted_rand_score(cluster(X, k2), is_seed))
        c2 = {"cases_with_seed_nearest": nn_seed, "a_pass": nn_seed >= 8, "k": int(k2), "ari_clusters_batch": round(ari_b, 3),
              "b_pass": ari_b <= 0.10}
        c2["pass"] = c2["a_pass"] and c2["b_pass"]
        # Reported: keyword lean (cases using a family's own words, against that family's re-expressed centroid)
        lean = {}
        for f, rx in KEYWORDS.items():
            cent = norm(S7[[i for i, a in enumerate(arch) if fam[e_of[a]] == f]].mean(0, keepdims=True))[0]
            others = [g for g in KEYWORDS if g != f]
            txt = [case_text[f"case:{q}::concept"] for q in qs]
            hit = [j for j, t in enumerate(txt) if re.search(rx, t, re.I) and not any(re.search(KEYWORDS[g], t, re.I) for g in others)]
            miss = [j for j, t in enumerate(txt) if not re.search(rx, t, re.I)]
            if hit:
                lean[f] = {"n": len(hit), "hit_mean": round(float(np.mean(Cs[hit] @ cent)), 3), "rest_mean": round(float(np.mean(Cs[miss] @ cent)), 3)}
        # Reported: each re-expressed seed's nearest original seed (cross-format)
        O = combined(np.array([E4[enc][f"archive:{a}::concept"] for a in arch]),
                     np.array([E6[enc][f"archive:{a}::intent"] for a in arch]))
        home = int(sum(np.argmax(S7[i] @ O.T) == i for i in range(len(arch))))
        out["encoders"][enc] = {"C1": c1, "C2": c2, "keyword_lean": lean, "reexpressed_nearest_own_original": home}
    holds = lambda c: out["encoders"][PRIMARY][c]["pass"] and any(out["encoders"][e][c]["pass"] for e in ENCODERS[1:])  # noqa: E731
    out["C1_pass"], out["C2_pass"] = holds("C1"), holds("C2")
    out["reading"] = ("one writer and format makes the address work: build map v0.1" if out["C1_pass"] and out["C2_pass"] else
                      "re-expression washes out the families" if not out["C1_pass"] else
                      "families preserved but the gap is not format alone: rethink before any map")
    dest = HERE / "results/scores_p07.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(dest)


E6 = load(P6 / "local/embeddings.jsonl")

if __name__ == "__main__":
    main()
