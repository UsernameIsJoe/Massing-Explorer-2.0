"""Score encoders (and an optional LLM baseline) against the user's blind labels.

Usage (from pilots/p01-representation):
    python scripts/score_triplets.py labels/user_labels.json [--llm labels/llm_labels.json]

Labels file: {"T01": {"answer": "option_1"|"option_2"|"about_equal"|"cannot_judge"}, ...}
keyed by triplet_id, as exported from the labeling page.

Reads data/triplets_SEALED.json and every runs/<encoder>/embeddings.jsonl.
Writes results/scores.json and prints a summary table.
Only decisive user labels (option_1/option_2) are scored; repeats are used only
for the labeler-consistency check, never double counted.
"""
import collections
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_triplets import load_cases, struct_distance, tfidf_cos  # noqa: E402

CASES = HERE.parent.parent / "benchmarks/test-elementary-v0.1/seed_scope_cases_2026-10-27/cases/all_15_cases.json"
VARIANTS = ["struct", "intent", "full", "aspect_inclusion", "aspect_civic_access", "aspect_service"]
REAL = {"real_disagree", "real_control"}


def resolve(t, answer):
    if answer == "option_1":
        return t["shown_order"][0]
    if answer == "option_2":
        return t["shown_order"][1]
    return None


def load_labels(p):
    raw = json.loads(Path(p).read_text(encoding="utf-8"))
    return {k: (v.get("answer") if isinstance(v, dict) else v) for k, v in raw.items()}


def cosine(a, b):
    num = sum(x * y for x, y in zip(a, b))
    return num / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def ref_id(ref, variant, probes):
    return f"{ref}::probe" if ref in probes else f"{ref}::{variant}"


def main(argv):
    labels = load_labels(argv[0])
    llm = load_labels(argv[argv.index("--llm") + 1]) if "--llm" in argv else None
    sealed = json.loads((HERE / "data" / "triplets_SEALED.json").read_text(encoding="utf-8"))
    probes = json.loads((HERE / "data" / "probes.json").read_text(encoding="utf-8"))["texts"]
    trip = {t["triplet_id"]: t for t in sealed["triplets"]}
    originals = [t for t in sealed["triplets"] if "repeat_of" not in t]

    # Labeler consistency on repeated items.
    consistency = []
    for t in sealed["triplets"]:
        if "repeat_of" in t:
            a, b = resolve(trip[t["repeat_of"]], labels.get(t["repeat_of"])), resolve(t, labels.get(t["triplet_id"]))
            consistency.append({"item": t["repeat_of"], "repeat": t["triplet_id"], "first": a, "second": b,
                                "consistent": a == b})

    truth = {t["triplet_id"]: resolve(t, labels.get(t["triplet_id"])) for t in originals}
    decisive = [t for t in originals if truth[t["triplet_id"]]]
    label_dist = collections.Counter(labels.get(t["triplet_id"], "missing") for t in originals)

    predictors = {}
    # Reference proxies (real triplets only).
    cases = load_cases(CASES)
    desc = [json.loads(l) for l in open(HERE / "data" / "descriptions.jsonl", encoding="utf-8")]
    cos_lex = tfidf_cos({r["case_id"]: r["text"] for r in desc if r["variant"] == "intent"})

    def proxy(fn):
        return {t["triplet_id"]: min(t["options"], key=lambda o: fn(t["anchor"], o))
                for t in originals if t["kind"] in REAL}
    predictors["proxy:structure"] = proxy(lambda a, o: struct_distance(cases[a], cases[o]))
    predictors["proxy:wording_tfidf"] = proxy(lambda a, o: -cos_lex(a, o))
    predictors["construction_expectation"] = {t["triplet_id"]: t["construction_expectation"]
                                              for t in originals if "construction_expectation" in t}
    if llm:
        predictors["llm_baseline"] = {t["triplet_id"]: resolve(t, llm.get(t["triplet_id"])) for t in originals}

    for run in sorted((HERE / "runs").glob("*/embeddings.jsonl")):
        vec = {}
        for line in open(run, encoding="utf-8"):
            r = json.loads(line)
            vec[r["text_id"]] = r["vector"]
        enc = run.parent.name
        for v in VARIANTS:
            pred = {}
            for t in originals:
                # Probe texts are intent-style, so probe triplets compare against case intent text only.
                if t["kind"] not in REAL and v != "intent":
                    continue
                a = vec[ref_id(t["anchor"], v, probes)]
                s = {o: cosine(a, vec[ref_id(o, v, probes)]) for o in t["options"]}
                pred[t["triplet_id"]] = max(s, key=s.get)
            predictors[f"{enc}:{v}"] = pred

    kinds = sorted({t["kind"] for t in originals})
    table = {}
    for name, pred in predictors.items():
        row = {}
        for k in kinds + ["ALL_REAL", "ALL"]:
            sel = [t for t in decisive if (k == "ALL" or (k == "ALL_REAL" and t["kind"] in REAL) or t["kind"] == k)
                   and pred.get(t["triplet_id"])]
            if sel:
                ok = sum(pred[t["triplet_id"]] == truth[t["triplet_id"]] for t in sel)
                row[k] = {"agree": ok, "n": len(sel), "rate": round(ok / len(sel), 3)}
        table[name] = row

    out = {"labels_file": str(argv[0]), "label_distribution": dict(label_dist),
           "decisive": len(decisive), "consistency": consistency, "agreement": table}
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "scores.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    cols = ["ALL_REAL", "paraphrase", "lexical_trap", "generic", "intent_vs_wording", "ALL"]
    print(f"labels: {dict(label_dist)}  decisive: {len(decisive)}  "
          f"consistency: {sum(c['consistent'] for c in consistency)}/{len(consistency)}")
    print(f"{'predictor':42}" + "".join(f"{c:>18}" for c in cols))
    for name, row in table.items():
        cells = [f"{row[c]['agree']}/{row[c]['n']}" if c in row else "-" for c in cols]
        print(f"{name:42}" + "".join(f"{x:>18}" for x in cells))


if __name__ == "__main__":
    main(sys.argv[1:])
