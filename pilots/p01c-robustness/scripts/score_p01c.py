"""Score Pilot 01c robustness tests.

Usage (from pilots/p01c-robustness):
    python scripts/score_p01c.py build-texts   # after responses/1 and 2 exist: writes data/descriptions.jsonl for embedding
    python scripts/score_p01c.py score         # after runs/ exist (and responses/3a, 3b for the judge test)

Responses expected (saved exactly as returned by ChatGPT):
    responses/1_rewrite.json     {"P01": "...", ...}
    responses/2_describe.json    {"V01": "...", ...}
    responses/3a_judge.json, responses/3b_judge.json   {"C01": {"answer": ...}, ...}
"""
import hashlib
import itertools
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "pilots/p01b-concept/scripts"))
from build_p01b import load, sdist, tfidf  # noqa: E402

TWIN = 0.10


def rj(p):
    return json.loads((HERE / p).read_text(encoding="utf-8"))


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def build_texts():
    cases = load()
    key, variants = rj("data/rewrite_key_SEALED.json"), rj("data/variants_SEALED.json")
    rew, des = rj("responses/1_rewrite.json"), rj("responses/2_describe.json")
    assert set(rew) == set(key), "rewrite IDs do not match"
    assert set(des) == set(variants), "describe IDs do not match"
    rows = [(f"{cid}::original", cases[cid]["case"]["concept"]) for cid in sorted(cases)]
    rows += [(f"{pid}::rewrite", rew[pid]) for pid in sorted(rew)]
    rows += [(f"{vid}::described", des[vid]) for vid in sorted(des)]
    with open(HERE / "data/descriptions.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for tid, text in rows:
            f.write(json.dumps({"text_id": tid, "text": text, "sha256": hashlib.sha256(text.encode()).hexdigest()}, ensure_ascii=False) + "\n")
    (HERE / "data/probes.json").write_text(json.dumps({"texts": {}}), encoding="utf-8")
    print(f"{len(rows)} texts -> data/descriptions.jsonl")


def score():
    cases = load()
    key, variants = rj("data/rewrite_key_SEALED.json"), rj("data/variants_SEALED.json")
    rew = rj("responses/1_rewrite.json")
    twins = {a: {b for b in cases if b != a and sdist(cases[a], cases[b]) <= TWIN} for a in cases}
    out = {"paraphrase": {}, "edits": {}, "judge": {}}

    # Wording baseline for the paraphrase test: TF-IDF over originals + rewrites.
    texts = {f"{c}::original": cases[c]["case"]["concept"] for c in cases}
    texts.update({f"{p}::rewrite": rew[p] for p in rew})
    lex = tfidf(texts)
    encs = {"tfidf_wording": None}
    for run in sorted((HERE / "runs").glob("*/embeddings.jsonl")):
        encs[run.parent.name] = {json.loads(l)["text_id"]: json.loads(l)["vector"] for l in open(run, encoding="utf-8")}

    for name, vec in encs.items():
        own = twin_ok = 0
        for pid, cid in key.items():
            sim = (lambda o: lex(f"{pid}::rewrite", f"{o}::original")) if vec is None else \
                  (lambda o: cosine(vec[f"{pid}::rewrite"], vec[f"{o}::original"]))
            top = max(cases, key=sim)
            own += top == cid
            twin_ok += top == cid or top in twins[cid]
        out["paraphrase"][name] = {"own_top1": own, "own_or_twin_top1": twin_ok, "n": len(key)}

    # Edit test: distance from each base's described concept to its variants', by edit count.
    by_base = {}
    for vid, e in variants.items():
        by_base.setdefault(e["base"], []).append((vid, e["level"]))
    for name, vec in encs.items():
        if vec is None:
            continue
        rhos, wins = [], 0
        for base, vs in by_base.items():
            b = next(v for v, lvl in vs if lvl == 0)
            pts = [(lvl, 1 - cosine(vec[f"{b}::described"], vec[f"{v}::described"])) for v, lvl in vs if lvl > 0]
            rhos.append(spearman([p[0] for p in pts], [p[1] for p in pts]))
            d1 = statistics.mean(d for l, d in pts if l == 1)
            d3 = statistics.mean(d for l, d in pts if l == 3)
            wins += d3 > d1
        out["edits"][name] = {"mean_spearman": round(statistics.mean(rhos), 3), "per_base": [round(r, 3) for r in rhos],
                              "bases_level3_farther_than_level1": wins, "bases": len(by_base)}

    # Judge test: agreement with the labeler (Pass B, decisive and stable) and between the two runs.
    p01b = REPO / "pilots/p01b-concept"
    scores_b = json.loads((p01b / "results/scores_user_labels_full.json").read_text(encoding="utf-8"))
    truth = {k: v["truth"] for k, v in scores_b["per_item"].items() if v["truth"]}
    sealed = {t["triplet_id"]: t for t in json.loads((p01b / "data/triplets_SEALED.json").read_text(encoding="utf-8"))["triplets"]}
    res = lambda t, a: {"option_1": t["shown_order"][0], "option_2": t["shown_order"][1]}.get(a)
    runs = {}
    for tag in ("3a_judge", "3b_judge", "3c_judge"):
        p = HERE / f"responses/{tag}.json"
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            runs[tag] = {k: res(sealed[k], (v.get("answer") if isinstance(v, dict) else v)) for k, v in raw.items()}
            ok = [k for k in truth if runs[tag].get(k)]
            out["judge"][tag] = {"agree_with_labeler": sum(runs[tag][k] == truth[k] for k in ok), "decisive_overlap": len(ok)}
    if len(runs) == 2:
        a, b = runs["3a_judge"], runs["3b_judge"]
        both = [k for k in sealed if a.get(k) and b.get(k)]
        out["judge"]["run_to_run"] = {"agree": sum(a[k] == b[k] for k in both), "decisive_both": len(both)}

    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results/scores.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    {"build-texts": build_texts, "score": score}[sys.argv[1]]()
