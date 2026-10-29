"""Pilot 4 directions: deterministic, code-generated (see PLAN.md).

  A  10 axis gaps: coarse cells (link pattern x special education's mass x height profile)
     unoccupied by the 15 archive seeds but containing valid structures in the Pilot 3 pool
  S  10 semantic directions from bge-m3 idea embeddings (concept + intent) of the archive:
     4 away (one per largest cluster), 3 bridge (farthest pairs), 3 develop (thinnest clusters)
  J  A's 10 gaps, each with semantic context: the 2 archive concepts nearest in meaning to the
     gap's structurally nearest seed (not to be rephrased) and the archive concept farthest in
     meaning from it (intent may be borrowed)

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/directions.py
"""
import collections
import itertools
import json
import random
import sys
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.metrics import silhouette_score

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pilots/p03-expansion/scripts"))
import expand  # noqa: E402

SEED = 20261029
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
ROLE_WORDS = {"L": "the learning mass (core academic)", "C": "the commons (gym and dining)", "X": "the third mass"}


def cell(st):
    own, fl = st["own"], st["floors"]
    L, C = own["D01"], own["D04"]
    X = next(m for m in set(own.values()) if m not in (L, C))
    r = {L: "L", C: "C", X: "X"}
    links = tuple(sorted("".join(sorted(r[a] + r[b])) for (a, b), v in st["links"].items() if v))

    def h(m):
        return max(max(max(fl[d]), 2 if d in ("D04", "D06") and fl[d] == [1] else 0) for d in own if own[d] == m)
    hs = sorted(h(m) for m in (L, C, X))
    hp = "all3" if hs == [3, 3, 3] else ("low" if sum(hs) <= 6 else "mixed")
    return (links, r[own["D02"]], hp)


def gap_words(c):
    links, sped, hp = c
    pairs = {"CL": ("the learning mass", "the commons"), "LX": ("the learning mass", "the third mass"), "CX": ("the commons", "the third mass")}
    if not links:
        lw = "no built connections between the three masses"
    elif len(links) == 3:
        lw = "all three masses directly connected to each other"
    elif len(links) == 2:
        hub = next(r for r in "LCX" if all(r in p for p in links))
        lw = f"masses connected in a chain through {ROLE_WORDS[hub]}"
    else:
        a, b = pairs["".join(sorted(links[0]))]
        lw = f"only {a} and {b} directly connected"
    sw = {"L": "special education shares the learning mass", "C": "special education sits with the commons", "X": "special education is in the third mass"}[sped]
    hw = {"all3": "all three masses rise to three storeys", "mixed": "the masses differ in height", "low": "most masses stay low (one or two storeys)"}[hp]
    return f"{lw}; {sw}; {hw}"


def cell_dist(a, b):
    la, lb = set(a[0]), set(b[0])
    return len(la ^ lb) + (a[1] != b[1]) + (a[2] != b[2])


def main():
    cases, states = {}, {}
    for run, f in RUNS:
        for c in json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases" / f).read_text(encoding="utf-8"))["cases"]:
            k = f"{run}-{c['case_id']}"
            cases[k], states[k] = c, expand.state_of(c)
    ids = sorted(cases)
    occ = {cell(states[k]) for k in ids}
    pool = json.loads((REPO / "pilots/p03-expansion/data/pool.json").read_text(encoding="utf-8"))
    members = pool["inside_members"] + [m for g in pool["groups"] for m in g["members"]]
    pc = collections.Counter()
    for m in members:
        st = m["state"]
        pc[cell({"own": st["own"], "floors": st["floors"], "links": {tuple(k.split("-")): v for k, v in st["links"].items()}})] += 1
    gaps_all = sorted((c for c in pc if c not in occ), key=lambda c: (c[0], c[1], c[2]))
    rng = random.Random(SEED)
    by_pattern = collections.defaultdict(list)
    for c in gaps_all:
        by_pattern[c[0]].append(c)
    for v in by_pattern.values():
        rng.shuffle(v)
    patterns = sorted(by_pattern)
    rng.shuffle(patterns)
    gaps = []
    while len(gaps) < 10:
        for p in patterns:
            if by_pattern[p] and len(gaps) < 10:
                gaps.append(by_pattern[p].pop())

    # semantic map: bge-m3 idea embeddings (concept + intent), Pilot 01b run, config p01-enc-v1
    E = {}
    for line in (REPO / "pilots/p01b-concept/runs/bge-m3/embeddings.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["text_id"].endswith("::concept_intent"):
            E[r["text_id"].split("::")[0]] = np.array(r["vector"])
    X = np.array([E[k] / np.linalg.norm(E[k]) for k in ids])
    D = np.clip(1 - X @ X.T, 0, None)
    np.fill_diagonal(D, 0)
    Z = linkage(squareform(D, checks=False), "average")
    best = max(range(3, 7), key=lambda k: silhouette_score(D, fcluster(Z, k, "maxclust"), metric="precomputed"))
    lab = fcluster(Z, best, "maxclust")
    clusters = collections.defaultdict(list)
    for k, l in zip(ids, lab):
        clusters[int(l)].append(k)
    size_order = sorted(clusters.values(), key=lambda v: (-len(v), v))
    away = [{"type": "away", "seeds": v} for v in size_order[:4]]
    pairs = sorted(itertools.combinations(range(len(ids)), 2), key=lambda p: -D[p])
    used, bridge = set(), []
    for i, j in pairs:
        if i in used or j in used:
            continue
        bridge.append({"type": "bridge", "intent_of": ids[i], "organization_of": ids[j]})
        used |= {i, j}
        if len(bridge) == 3:
            break
    thin = sorted(clusters.values(), key=lambda v: (len(v), v))
    develop, k = [], 0
    while len(develop) < 3:
        v = thin[k % len(thin)]
        pick = v[(k // len(thin)) % len(v)]
        if all(pick != d["seed"] for d in develop):
            develop.append({"type": "develop", "seed": pick})
        k += 1
    S = away + bridge + develop

    J = []
    for g in gaps:
        near = min(ids, key=lambda k: (cell_dist(cell(states[k]), g), k))
        i = ids.index(near)
        order = np.argsort(D[i])
        J.append({"gap": list(map(list, [g[0]])) + [g[1], g[2]], "words": gap_words(g), "structural_nearest": near,
                  "do_not_rephrase": [ids[o] for o in order[:2]], "may_borrow_intent_of": ids[int(np.argmax(D[i]))]})
    out = {"seed": SEED, "occupied_cells": len(occ), "candidate_gaps": len(gaps_all), "silhouette_k": best,
           "clusters": {str(k): v for k, v in clusters.items()},
           "A": [{"gap": [list(g[0]), g[1], g[2]], "words": gap_words(g)} for g in gaps], "S": S, "J": J}
    (HERE / "data/directions.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells occupied {len(occ)}, candidate gaps {len(gaps_all)}, clusters k={best}: {[len(v) for v in size_order]}")
    for a in out["A"]:
        print("A:", a["words"])
    for s in S:
        print("S:", s)


if __name__ == "__main__":
    main()
