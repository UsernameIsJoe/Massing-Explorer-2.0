"""Score Pilot 01b: concept embeddings, proxies and an optional LLM baseline
against the user's blind labels.

Usage (from pilots/p01b-concept):
    python scripts/score_p01b.py labels/user_labels.json [--llm labels/llm_labels.json]

Only decisive labels (option_1/option_2) are scored. An item whose repeat
disagrees with it is excluded as unstable. Repeats are never double counted.
"""
import collections
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_p01b import load, sdist, tfidf  # noqa: E402

VARIANTS = ["concept", "concept_intent", "struct"]
KINDS = ["cross_run", "disagree", "control"]


def resolve(t, a):
    return {"option_1": t["shown_order"][0], "option_2": t["shown_order"][1]}.get(a)


def labels_of(p):
    raw = json.loads(Path(p).read_text(encoding="utf-8"))
    return {k: (v.get("answer") if isinstance(v, dict) else v) for k, v in raw.items()}


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def main(argv):
    lab = labels_of(argv[0])
    llm = labels_of(argv[argv.index("--llm") + 1]) if "--llm" in argv else None
    sealed = json.loads((HERE / "data/triplets_SEALED.json").read_text(encoding="utf-8"))["triplets"]
    by = {t["triplet_id"]: t for t in sealed}
    originals = [t for t in sealed if "repeat_of" not in t]

    consistency = [{"item": t["repeat_of"], "repeat": t["triplet_id"],
                    "first": resolve(by[t["repeat_of"]], lab.get(t["repeat_of"])), "second": resolve(t, lab.get(t["triplet_id"]))}
                   for t in sealed if "repeat_of" in t]
    for c in consistency:
        c["consistent"] = c["first"] == c["second"]
    unstable = {c["item"] for c in consistency if not c["consistent"]}
    truth = {t["triplet_id"]: (None if t["triplet_id"] in unstable else resolve(t, lab.get(t["triplet_id"]))) for t in originals}
    decisive = [t for t in originals if truth[t["triplet_id"]]]

    cases = load()
    cos = tfidf({k: v["case"]["concept"] for k, v in cases.items()})
    preds = {
        "proxy:structure": {t["triplet_id"]: min(t["options"], key=lambda o: sdist(cases[t["anchor"]], cases[o])) for t in originals},
        "proxy:concept_wording": {t["triplet_id"]: max(t["options"], key=lambda o: cos(t["anchor"], o)) for t in originals},
    }
    if llm:
        preds["llm_baseline"] = {t["triplet_id"]: resolve(t, llm.get(t["triplet_id"])) for t in originals}
    for run in sorted((HERE / "runs").glob("*/embeddings.jsonl")):
        vec = {json.loads(l)["text_id"]: json.loads(l)["vector"] for l in open(run, encoding="utf-8")}
        for v in VARIANTS:
            preds[f"{run.parent.name}:{v}"] = {
                t["triplet_id"]: max(t["options"], key=lambda o: cosine(vec[f"{t['anchor']}::{v}"], vec[f"{o}::{v}"]))
                for t in originals}

    table = {}
    for name, p in preds.items():
        row = {}
        for k in KINDS + ["ALL"]:
            sel = [t for t in decisive if (k == "ALL" or t["kind"] == k) and p.get(t["triplet_id"])]
            if sel:
                ok = sum(p[t["triplet_id"]] == truth[t["triplet_id"]] for t in sel)
                row[k] = {"agree": ok, "n": len(sel)}
        table[name] = row
    per_item = {t["triplet_id"]: {"kind": t["kind"], "anchor": t["anchor"], "truth": truth[t["triplet_id"]],
                                  **{n: p.get(t["triplet_id"]) for n, p in preds.items()}} for t in originals}
    out = {"protocol": "p01b-v1", "label_distribution": dict(collections.Counter(lab.get(t["triplet_id"], "missing") for t in originals)),
           "excluded_unstable": sorted(unstable), "consistency": consistency, "decisive": len(decisive),
           "agreement": table, "per_item": per_item}
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results/scores.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"labels {out['label_distribution']}  decisive {len(decisive)}  consistency "
          f"{sum(c['consistent'] for c in consistency)}/{len(consistency)}  excluded {sorted(unstable)}")
    print(f"{'predictor':40}" + "".join(f"{k:>12}" for k in KINDS + ["ALL"]))
    for name, row in table.items():
        print(f"{name:40}" + "".join(f"{(str(row[k]['agree']) + '/' + str(row[k]['n'])) if k in row else '-':>12}" for k in KINDS + ["ALL"]))


if __name__ == "__main__":
    main(sys.argv[1:])
