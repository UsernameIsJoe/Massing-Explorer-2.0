"""Joint map v0. Definitions: map/README.md.

Usage (from repo root):  python map/build_map.py
Writes map/v0/map_v0.json
"""
import collections
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

REPO = Path(__file__).resolve().parents[1]
P4 = REPO / "pilots/p04-guided-exploration"
P6 = REPO / "pilots/p06-intent-view"
sys.path.insert(0, str(P4 / "scripts"))
import score_p04 as s  # noqa: E402
import expand  # noqa: E402
from directions import cell  # noqa: E402

ENC = "qwen3-embedding:4b"
CHECK_ENCODERS = ["mxbai-embed-large", "nomic-embed-text", "bge-m3"]
K_RANGE = range(3, 13)
TRAITS = {"links": None, "sped": "D02", "height": None, "admin": "D08", "arts": "D03", "media": "D05"}
FIX_SHARE, FIX_MIN_N = 0.80, 4
ROLE_WORDS = {"L": "learning mass", "C": "commons", "X": "third mass"}


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


def best_k(X):
    sil = {k: float(silhouette_score(X, cluster(X, k), metric="cosine")) for k in K_RANGE}
    return max(sil, key=sil.get), sil


def roles(st):
    own = st["own"]
    L, C = own["D01"], own["D04"]
    X = next(m for m in set(own.values()) if m not in (L, C))
    return {L: "L", C: "C", X: "X"}


def traits(st):
    c = cell(st)
    r = roles(st)
    t = {"links": "+".join(c[0]) or "none", "height": c[2]}
    for name, d in TRAITS.items():
        if d:
            t[name] = r[st["own"][d]]
    return t


def pool_states():
    pool = json.loads((REPO / "pilots/p03-expansion/data/pool.json").read_text(encoding="utf-8"))
    out = []
    for m in pool["inside_members"] + [x for g in pool["groups"] for x in g["members"]]:
        st = m["state"]
        out.append({"own": st["own"], "floors": st["floors"], "links": {tuple(k.split("-")): v for k, v in st["links"].items()}})
    return out


def main():
    E4, E6 = load(P4 / "scoring/local/embeddings.jsonl"), load(P6 / "local/embeddings.jsonl")
    key = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))
    e_of = key["archive_ids"]
    arch_cases = s.archive()
    cases = s.load_cases()
    scores = json.loads((P4 / "results/scores.json").read_text(encoding="utf-8"))["per_case"]

    items = []
    for a in sorted(e_of):
        c = arch_cases[a]
        items.append({"id": e_of[a], "source": "seed", "batch": "archive_v2", "name": c["name"], "concept": c["concept"],
                      "intent": c["intent"], "state": expand.state_of(c), "tid": f"archive:{a}", "intent_tid": ("E6", f"archive:{a}::intent")})
    for q in sorted(cases):
        c = cases[q]["case"]
        sc = scores[q]
        items.append({"id": q, "source": f"pilot4_{sc['arm']}", "batch": "cases_v3.1", "name": c["name"], "concept": c["concept"],
                      "intent": c["intent"], "state": s.state(c), "tid": f"case:{q}", "intent_tid": ("E4", f"case:{q}::intent"),
                      "validity": sc["validity"], "consistency_v3text": sc.get("agreement_v3text")})

    def vecs(enc, view):
        out = []
        for it in items:
            if view == "intent":
                src, tid = it["intent_tid"]
                out.append((E6 if src == "E6" else E4)[enc][tid])
            else:
                out.append(E4[enc][f"{it['tid']}::{view}"])
        return np.array(out)

    batches = np.array([it["batch"] for it in items])

    def centred(M):
        M = M.copy()
        for b in set(batches):
            M[batches == b] -= M[batches == b].mean(0)
        return norm(M)

    def combined(enc):
        return np.hstack([centred(vecs(enc, "concept")), centred(vecs(enc, "intent"))]) / np.sqrt(2)

    X = combined(ENC)
    k, sil = best_k(X)
    lab = cluster(X, k)
    Cc, Ci = centred(vecs(ENC, "concept")), centred(vecs(ENC, "intent"))
    Sc, Si = Cc @ Cc.T, Ci @ Ci.T

    # Order neighbourhoods by size, label N1..Nk
    order = [c for c, _ in collections.Counter(lab).most_common()]
    name_of = {c: f"N{i + 1}" for i, c in enumerate(order)}
    for it, l in zip(items, lab):
        it["neighbourhood"] = name_of[l]
        it["cell"] = cell(it["state"])
        it["traits"] = traits(it["state"])

    # Checks
    refs = {}
    for nm, p in (("idea_families", REPO / "pilots/p05-neighbourhood-address/reference/families_claude_v1.json"),
                  ("purpose_families", P6 / "reference/purpose_families_claude_v1.json")):
        f = {e: fam for fam, v in json.loads(p.read_text(encoding="utf-8"))["families"].items() for e in v["members"]}
        refs[nm] = f
    seeds = [i for i, it in enumerate(items) if it["source"] == "seed"]
    checks = {"archive_ari": {nm: round(float(adjusted_rand_score([lab[i] for i in seeds], [f[items[i]["id"]] for i in seeds])), 3)
                              for nm, f in refs.items()}}
    mix = {}
    for c in order:
        mem = [items[i] for i in range(len(items)) if lab[i] == c]
        mix[name_of[c]] = {"seeds": sum(m["source"] == "seed" for m in mem), "cases": sum(m["source"] != "seed" for m in mem)}
    checks["batch_mixing"] = mix
    checks["neighbourhoods_mixing_both_batches"] = sum(v["seeds"] > 0 and v["cases"] > 0 for v in mix.values())
    # Without centring, for contrast
    Xr = np.hstack([norm(vecs(ENC, "concept")), norm(vecs(ENC, "intent"))]) / np.sqrt(2)
    kr, _ = best_k(Xr)
    labr = cluster(Xr, kr)
    checks["uncentred_contrast"] = {"k": int(kr), "neighbourhoods_mixing_both_batches": int(sum(
        any(items[i]["source"] == "seed" for i in range(len(items)) if labr[i] == c) and
        any(items[i]["source"] != "seed" for i in range(len(items)) if labr[i] == c) for c in set(labr)))}
    checks["encoder_agreement_ari"] = {}
    for enc in CHECK_ENCODERS:
        Xe = combined(enc)
        checks["encoder_agreement_ari"][enc] = round(float(adjusted_rand_score(lab, cluster(Xe, best_k(Xe)[0]))), 3)
    Xj = centred(vecs(ENC, "idea"))
    checks["joint_vector_agreement_ari"] = round(float(adjusted_rand_score(lab, cluster(Xj, best_k(Xj)[0]))), 3)

    # Co-location: neighbourhood x cell
    pool = pool_states()
    pool_cells = collections.Counter(cell(st) for st in pool)
    texted_cells = collections.Counter(it["cell"] for it in items)
    coloc = collections.defaultdict(lambda: collections.Counter())
    for it in items:
        coloc[it["neighbourhood"]][json.dumps(it["cell"])] += 1

    # Footprints
    footprints = {}
    for nb in [name_of[c] for c in order]:
        mem = [it for it in items if it["neighbourhood"] == nb]
        fp = {}
        for t in ("links", "sped", "height", "admin", "arts", "media"):
            cnt = collections.Counter(m["traits"][t] for m in mem)
            val, n = cnt.most_common(1)[0]
            share = n / len(mem)
            status = "too few" if len(mem) < FIX_MIN_N else ("fixed" if share >= FIX_SHARE else "free")
            fp[t] = {"status": status, "modal": val, "share": round(share, 2), "values": dict(cnt)}
        footprints[nb] = {"n": len(mem), "traits": fp, "cells": len({json.dumps(m["cell"]) for m in mem})}

    # Gaps
    cell_nbs = collections.defaultdict(set)
    for it in items:
        cell_nbs[it["cell"]].add(it["neighbourhood"])
    gaps = {
        "cells_with_valid_structures_no_texted_idea": sorted([[list(c[0]), c[1], c[2], pool_cells[c]] for c in pool_cells if c not in texted_cells],
                                                             key=lambda x: -x[3]),
        "cells_reached_by_one_neighbourhood_only": sorted([[list(c[0]), c[1], c[2], sorted(v)[0], texted_cells[c]] for c, v in cell_nbs.items() if len(v) == 1],
                                                          key=lambda x: -x[4]),
        "neighbourhoods_in_one_cell_only": [nb for nb, f in footprints.items() if f["cells"] == 1],
        "n_cells_total": 72, "n_cells_with_valid_pool_structures": len(pool_cells), "n_cells_texted": len(texted_cells),
    }

    # Pairs: same idea / different purpose and the reverse
    iu = np.triu_indices(len(items), 1)
    c90, imed = np.percentile(Sc[iu], 90), np.median(Si[iu])
    i90, cmed = np.percentile(Si[iu], 90), np.median(Sc[iu])
    pairs = {"same_idea_different_purpose": [], "same_purpose_different_idea": []}
    for a, b in zip(*iu):
        if Sc[a, b] >= c90 and Si[a, b] <= imed:
            pairs["same_idea_different_purpose"].append([items[a]["id"], items[b]["id"], round(float(Sc[a, b] - Si[a, b]), 3)])
        if Si[a, b] >= i90 and Sc[a, b] <= cmed:
            pairs["same_purpose_different_idea"].append([items[a]["id"], items[b]["id"], round(float(Si[a, b] - Sc[a, b]), 3)])
    for v in pairs.values():
        v.sort(key=lambda x: -x[2])

    # Pilot 4 re-read through the map
    seed_nbs = {it["neighbourhood"] for it in items if it["source"] == "seed"}
    seed_cells = {it["cell"] for it in items if it["source"] == "seed"}
    p4 = {}
    for arm in "UASJ":
        mem = [it for it in items if it["source"] == f"pilot4_{arm}"]
        p4[arm] = {"n": len(mem), "neighbourhoods_reached": len({m["neighbourhood"] for m in mem}),
                   "cases_in_neighbourhoods_without_seeds": sum(m["neighbourhood"] not in seed_nbs for m in mem),
                   "new_cells_vs_seeds": len({m["cell"] for m in mem} - seed_cells),
                   "valid": sum(m["validity"] == "valid" for m in mem),
                   "mean_consistency_v3text": round(float(np.mean([m["consistency_v3text"]["all"] if isinstance(m["consistency_v3text"], dict) else m["consistency_v3text"] for m in mem])), 2)}

    out = {"version": "v0", "date": "2026-11-03", "encoder": ENC, "k": int(k), "silhouette": sil,
           "checks": checks, "footprints": footprints, "colocation": {k_: dict(v) for k_, v in coloc.items()},
           "gaps": gaps, "pairs": pairs, "pilot4_reread": p4,
           "items": [{k_: (list(v) if k_ == "cell" else v) for k_, v in it.items() if k_ not in ("state", "tid", "intent_tid")} for it in items]}
    dest = REPO / "map/v0/map_v0.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=lambda o: list(o) if isinstance(o, tuple) else str(o)), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
