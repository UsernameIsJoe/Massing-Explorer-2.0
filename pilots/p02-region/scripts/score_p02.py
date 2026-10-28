"""Score Pilot 2 membership ratings against the three rules.

Usage (from pilots/p02-region):
    python scripts/score_p02.py labels/user_ratings.json
"""
import collections
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def spearman(x, y):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]:
                j += 1
            for k in range(i, j + 1):
                r[o[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y); mx, my = statistics.mean(rx), statistics.mean(ry)
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / den if den else 0.0


def main(path):
    ratings = {k: v["answer"] for k, v in json.loads(Path(path).read_text(encoding="utf-8")).items()}
    items = json.loads((HERE / "data/review_SEALED.json").read_text(encoding="utf-8"))["items"]
    orig = [it for it in items if "repeat_of" not in it]
    side = lambda r: "same" if r in ("1", "2") else "different" if r in ("4", "5") else None
    reps = [(it["repeat_of"], ratings.get(it["repeat_of"]), ratings.get(it["candidate_id"])) for it in items if "repeat_of" in it]
    unstable = {a for a, r1, r2 in reps if side(r1) and side(r2) and side(r1) != side(r2)}

    rules = {
        "strict_lock": lambda it: it["broken"] == 0,
        "tolerant_lock": lambda it: it["broken"] <= 1,
        "radius_0.10": lambda it: it["radius_in"],
    }
    dec = [it for it in orig if side(ratings.get(it["candidate_id"])) and it["candidate_id"] not in unstable]
    out = {"ratings": dict(collections.Counter(ratings.get(it["candidate_id"], "missing") for it in orig)),
           "repeats": reps, "unstable": sorted(unstable), "decisive": len(dec), "binary": {}, "per_stratum": {}}
    for name, f in rules.items():
        ok = sum((f(it) and side(ratings[it["candidate_id"]]) == "same") or (not f(it) and side(ratings[it["candidate_id"]]) == "different") for it in dec)
        out["binary"][name] = {"agree": ok, "n": len(dec)}
    num = [it for it in orig if ratings.get(it["candidate_id"]) in ("1", "2", "3", "4", "5")]
    rv = [int(ratings[it["candidate_id"]]) for it in num]
    out["spearman"] = {"structure_distance": round(spearman([it["nearest_distance"] for it in num], rv), 3),
                       "locked_decisions_broken": round(spearman([it["broken"] for it in num], rv), 3)}
    for s in "ABCDEF":
        rs = [ratings.get(it["candidate_id"]) for it in orig if it["stratum"] == s]
        nums = [int(r) for r in rs if r in ("1", "2", "3", "4", "5")]
        out["per_stratum"][s] = {"ratings": rs, "mean": round(statistics.mean(nums), 2) if nums else None}
    # Post-hoc: the radius threshold that would best separate 1-2 from 4-5 (reported, not adopted).
    best = None
    for t in sorted({it["nearest_distance"] for it in dec}):
        ok = sum((it["nearest_distance"] <= t) == (side(ratings[it["candidate_id"]]) == "same") for it in dec)
        if best is None or ok > best[1]:
            best = (t, ok)
    out["posthoc_best_radius"] = {"threshold": best[0], "agree": best[1], "n": len(dec)} if best else None
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results/scores.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
