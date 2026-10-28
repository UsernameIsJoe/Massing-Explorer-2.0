"""Experiment 1 scoring: the per-axis grounding map.

Part A (no LLM calls): Mantel correspondence between semantic distance (4 encoders x
concept / concept+intent) and each axis distance, item permutation test (9,999 permutations).

Part B (needs responses.jsonl from run_extraction.py): for each question and model, the
modal answer across prompts and samples is compared with the code answer key.
  accuracy        share of items whose modal answer equals the code value
  kappa           Cohen's kappa of modal answers vs code values over the 15 items
  shuffled        mean accuracy when answers are scored against other items' code values
  majority        accuracy of always giving the most common code value (leave one out)
  not_stated      share of samples answering "not stated"
  stability       share of samples that agree with their item's modal answer
Axis class (text arm, both models): carried if kappa >= 0.6 and accuracy > shuffled,
partial if kappa 0.4-0.6, otherwise uncarried. The express arm is the ceiling.

Usage (from repo root):  python grounding/exp1/score.py [responses.jsonl]
"""
import collections
import itertools
import json
import random
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parents[2]
HERE = REPO / "grounding/exp1"
AXIS_OF = {"place": "program_organization", "link": "topology", "storeys": "heights", "level": "vertical_organization"}
NFA = {"D01": 14280, "D02": 5610, "D03": 3040, "D04": 6950, "D05": 2800, "D06": 6150, "D07": 730, "D08": 2510, "D09": 2200}


def mantel():
    A = json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/axes/axes_v1.json").read_text(encoding="utf-8"))["cases"]
    ids = sorted(A)
    n = len(ids)

    def axd(name):
        M = np.zeros((n, n))
        for i, j in itertools.combinations(range(n), 2):
            p, q = A[ids[i]][name]["value"], A[ids[j]][name]["value"]
            d = sum(p[k] != q[k] for k in p) / len(p) if isinstance(p, dict) else (float(p != q) if isinstance(p, str) else abs(p - q))
            M[i, j] = M[j, i] = d
        return M
    axes = {a: axd(a) for a in ["program_organization", "distribution_balance", "topology", "mean_height", "height_articulation", "vertical_organization"]}
    iu = np.triu_indices(n, 1)
    rng = random.Random(20261028)
    out = {}
    for enc in ["bge-m3", "mxbai-embed-large", "nomic-embed-text", "qwen3-embedding_0.6b"]:
        E = {}
        for line in (REPO / f"pilots/p01b-concept/runs/{enc}/embeddings.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            E[r["text_id"]] = np.array(r["vector"])
        for v in ("concept", "concept_intent"):
            X = np.array([E[f"{i}::{v}"] / np.linalg.norm(E[f"{i}::{v}"]) for i in ids])
            S = 1 - X @ X.T
            for a, M in axes.items():
                rho = spearmanr(S[iu], M[iu])[0]
                ge = 0
                for _ in range(9999):
                    p = list(range(n)); rng.shuffle(p)
                    if spearmanr(S[iu], M[np.ix_(p, p)][iu])[0] >= rho:
                        ge += 1
                out[f"{enc}|{v}|{a}"] = {"rho": round(float(rho), 3), "p_mantel": round((ge + 1) / 10000, 4)}
    return out


def kappa(pred, true):
    labels = sorted(set(pred) | set(true))
    n = len(true)
    po = sum(p == t for p, t in zip(pred, true)) / n
    pe = sum((pred.count(l) / n) * (true.count(l) / n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def balance(places):
    if any(v == "not stated" for v in places.values()):
        return None
    area = collections.Counter({"L": NFA["D01"], "C": NFA["D04"] + NFA["D06"]})
    for d, m in places.items():
        area[m] += NFA[d]
    area["X"] += 0
    return 1 - max(area.values()) / sum(NFA.values()) if area["X"] > 0 else None


def score_responses(path):
    items = {i["id"]: i for i in json.loads((HERE / "items.json").read_text(encoding="utf-8"))["items"]}
    ids = sorted(items)
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    res = {}
    for arm in ("text", "express"):
        for model in sorted({r["model"] for r in rows if r["arm"] == arm}):
            samples = collections.defaultdict(list)
            for r in rows:
                if r["arm"] == arm and r["model"] == model:
                    samples[r["item"]].append(r["output"])
            if len(samples) < len(ids):
                continue
            for q in items[ids[0]]["truth"]:
                true = [items[i]["truth"][q] for i in ids]
                allv = [[s.get(q, "not stated") for s in samples[i]] for i in ids]
                modal = [collections.Counter(v).most_common(1)[0][0] for v in allv]
                acc = sum(m == t for m, t in zip(modal, true)) / len(ids)
                shuf = np.mean([modal[i] == true[j] for i in range(len(ids)) for j in range(len(ids)) if i != j])
                maj = np.mean([collections.Counter(true[:i] + true[i + 1:]).most_common(1)[0][0] == true[i] for i in range(len(ids))])
                ns = np.mean([v.count("not stated") / len(v) for v in allv])
                stab = np.mean([v.count(m) / len(v) for v, m in zip(allv, modal)])
                res[f"{arm}|{model}|{q}"] = {"accuracy": round(acc, 3), "kappa": round(kappa(modal, true), 3), "shuffled": round(float(shuf), 3),
                                             "majority": round(float(maj), 3), "not_stated": round(float(ns), 3), "stability": round(float(stab), 3)}
            # derived: distribution balance from extracted placements
            errs = []
            for i in ids:
                mod = {}
                for q in items[i]["truth"]:
                    if q.startswith("place_"):
                        mod[q[6:]] = collections.Counter(s.get(q, "not stated") for s in samples[i]).most_common(1)[0][0]
                b_hat = balance(mod)
                b = balance({q[6:]: v for q, v in items[i]["truth"].items() if q.startswith("place_")})
                errs.append(None if b_hat is None else abs(b_hat - b))
            ok = [e for e in errs if e is not None]
            res[f"{arm}|{model}|derived_balance"] = {"mae": round(float(np.mean(ok)), 3) if ok else None, "recovered_items": len(ok)}
    # axis classes from the text arm
    classes = {}
    for prefix, axis in AXIS_OF.items():
        ks, wins = [], []
        for k, v in res.items():
            arm, model, q = k.split("|")
            if arm == "text" and q.startswith(prefix + "_"):
                ks.append(v["kappa"]); wins.append(v["accuracy"] > v["shuffled"])
        if ks:
            k = float(np.mean(ks))
            classes[axis] = {"mean_kappa": round(k, 3), "beats_shuffled": f"{sum(wins)}/{len(wins)}",
                             "class": "carried" if k >= 0.6 and sum(wins) > len(wins) / 2 else ("partial" if k >= 0.4 else "uncarried")}
    return res, classes


def main():
    out = {"mantel": mantel()}
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "responses.jsonl"
    if path.exists():
        out["questions"], out["grounding_map"] = score_responses(path)
    (HERE / "results.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out["mantel"].items():
        if k.split("|")[1] == "concept_intent":
            print(f"mantel {k:58} rho {v['rho']:+.3f} p {v['p_mantel']}")
    for axis, v in out.get("grounding_map", {}).items():
        print(f"grounding {axis:22} kappa {v['mean_kappa']:+.3f} beats shuffled {v['beats_shuffled']:>5}  {v['class']}")


if __name__ == "__main__":
    main()
