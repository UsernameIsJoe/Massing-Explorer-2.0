"""Pilot 5: is a meaning neighbourhood a reliable address? Implements PROTOCOL.md.

Usage (from repo root):
    python pilots/p05-neighbourhood-address/scripts/neighbourhoods.py [reference.json]
Writes results/neighbourhoods_<reference version>.json
"""
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
P4 = REPO / "pilots/p04-guided-exploration"
ENCODERS = ["mxbai-embed-large", "nomic-embed-text", "qwen3-embedding:4b", "bge-m3"]
PREVIEW_ENCODERS = ENCODERS[:3]
CORRECTIONS = ["raw", "centred"]
K_RANGE = range(3, 9)
N_PERM, SEED = 10_000, 20261103


def load():
    E = {}
    for line in open(P4 / "scoring/local/embeddings.jsonl", encoding="utf-8"):
        r = json.loads(line)
        E.setdefault(r["encoder"], {})[r["text_id"]] = np.array(r["vector"], dtype=float)
    return E


def norm(M):
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def prep(M, how):
    return norm(M) if how == "raw" else norm(M - M.mean(0))


def cluster(A, k):
    return AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average").fit_predict(A)


def best_k(A):
    s = {k: float(silhouette_score(A, cluster(A, k), metric="cosine")) for k in K_RANGE}
    return max(s, key=s.get), s


def assign(X, A, labels):
    cents = norm(np.array([A[labels == c].mean(0) for c in sorted(set(labels))]))
    return np.array(sorted(set(labels)))[np.argmax(X @ cents.T, axis=1)]


def perm_p(labels, ref, obs, rng):
    ref = np.array(ref)
    hits = sum(adjusted_rand_score(labels, rng.permutation(ref)) >= obs for _ in range(N_PERM))
    return (hits + 1) / (N_PERM + 1)


def main(ref_path):
    ref = json.loads(Path(ref_path).read_text(encoding="utf-8"))
    key = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))
    e_of = key["archive_ids"]                                   # archive id -> E id
    arch = sorted(e_of)
    fam_of_e = {e: f for f, v in ref["families"].items() for e in v["members"]}
    ref_labels = [fam_of_e[e_of[a]] for a in arch]
    rw = json.loads((REPO / "pilots/p01c-robustness/data/rewrite_key_SEALED.json").read_text(encoding="utf-8"))
    rw_ids = sorted(rw)
    scores = json.loads((P4 / "results/scores.json").read_text(encoding="utf-8"))["per_case"]
    cases = sorted(scores)
    E = load()
    rng = np.random.default_rng(SEED)

    out = {"reference": ref["version"], "n_reference_families": len(ref["families"]), "encoders": {}}
    labels_at = {}
    for how in CORRECTIONS:
        for enc in ENCODERS:
            A = prep(np.array([E[enc][f"archive:{a}::concept"] for a in arch]), how)
            W = prep(np.array([E[enc][f"p01c:{p}::rewrite"] for p in rw_ids]), how)
            C = prep(np.array([E[enc][f"case:{q}::concept"] for q in cases]), how)
            k, sil = best_k(A)
            res = {"silhouette": sil}
            for kname, kk in (("silhouette_k", k), ("k_eq_families", len(ref["families"]))):
                lab = cluster(A, kk)
                home = {a: int(l) for a, l in zip(arch, lab)}
                wl = assign(W, A, lab)
                stay = sum(int(wl[i]) == home[rw[p]] for i, p in enumerate(rw_ids))
                ari = float(adjusted_rand_score(lab, ref_labels))
                p = perm_p(lab, ref_labels, ari, rng)
                res[kname] = {
                    "k": int(kk),
                    "neighbourhoods": {str(c): sorted(e_of[a] for a in arch if home[a] == c) for c in sorted(set(lab))},
                    "paraphrase_stays_home": stay, "c1_pass": stay >= 12,
                    "ari_vs_reference": round(ari, 3), "perm_p": round(p, 4), "c2_pass": ari >= 0.40 and p < 0.05,
                }
                res[kname]["pass"] = res[kname]["c1_pass"] and res[kname]["c2_pass"]
                labels_at[(how, enc, kname)] = (lab, assign(C, A, lab))
            out["encoders"].setdefault(how, {})[enc] = res

    chosen = next((h for h in CORRECTIONS if any(out["encoders"][h][e]["silhouette_k"]["pass"] for e in ENCODERS)), None)
    out["chosen_correction"] = chosen
    out["passing_encoders"] = [e for e in ENCODERS if chosen and out["encoders"][chosen][e]["silhouette_k"]["pass"]]

    # Criterion 3: encoder agreement
    out["encoder_agreement"] = {
        how: {f"{a} | {b}": round(float(adjusted_rand_score(labels_at[(how, a, "silhouette_k")][0], labels_at[(how, b, "silhouette_k")][0])), 3)
              for a, b in itertools.combinations(ENCODERS, 2)} for how in CORRECTIONS}

    # Criterion 4: preview of J vs A (no decision)
    out["preview_J_vs_A"] = preview(chosen or "raw", chosen is not None, key, e_of, arch, cases, scores, labels_at)
    # Post-hoc sensitivity (added after the declared result was seen): the same preview under centring
    out["preview_J_vs_A_posthoc_centred"] = preview("centred", None, key, e_of, arch, cases, scores, labels_at)

    dest = HERE / f"results/neighbourhoods_{ref['version']}.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(dest)


def preview(how, reliable, key, e_of, arch, cases, scores, labels_at):
    prompts = {f"R{i}": p for i, p in enumerate(key["prompts"], 1)}
    eid_to_arch = {e: a for a, e in e_of.items()}
    prev = {"correction": how, "reliable": reliable, "encoders": {}}
    for enc in PREVIEW_ENCODERS:
        lab, cl = labels_at[(how, enc, "silhouette_k")]
        home = {a: int(l) for a, l in zip(arch, lab)}
        case_nb = {q: int(l) for q, l in zip(cases, cl)}
        largest = Counter(lab).most_common(1)[0][0]
        per_arm = {}
        for q in cases:
            per_arm.setdefault(scores[q]["arm"], []).append(case_nb[q])
        gaps = {}
        for q in cases:
            r, arm = scores[q], scores[q]["arm"]
            if arm not in ("A", "J"):
                continue
            idx = (r["chat"] - 1) * 5 + int(r["case_id"][1:]) - 1
            gaps.setdefault(idx, {})[arm] = q
        avoid_hits = {"A": 0, "J": 0}
        detail = []
        for idx, d in sorted(gaps.items()):
            jq = d["J"]
            jp = prompts[scores[jq]["reply"]]
            text = jp["directions"][int(scores[jq]["case_id"][1:]) - 1]
            avoid = re.findall(r"(E\d\d) \"[^\"]+\"", text.split("do not rephrase")[0].split("closest in meaning:")[1])
            avoid_nb = {home[eid_to_arch[e]] for e in avoid}
            row = {"gap": idx, "avoid": avoid}
            for arm in ("A", "J"):
                hit = case_nb[d[arm]] in avoid_nb
                avoid_hits[arm] += hit
                row[arm] = {"case": d[arm], "neighbourhood": case_nb[d[arm]], "in_avoid_neighbourhood": hit}
            detail.append(row)
        prev["encoders"][enc] = {
            "landed_in_avoided_neighbourhood": avoid_hits,
            "distinct_neighbourhoods_per_arm": {a: len(set(v)) for a, v in sorted(per_arm.items())},
            "share_in_largest_archive_neighbourhood": {a: round(v.count(largest) / len(v), 2) for a, v in sorted(per_arm.items())},
            "per_gap": detail,
        }
    return prev


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "reference/families_claude_v1.json")
