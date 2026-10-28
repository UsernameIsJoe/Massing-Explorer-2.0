"""Build the Pilot 2 membership check: a stratified sample of candidates, each shown
beside its nearest seed with the changes in plain words. One question per item:
is the candidate the same strategy as the seed, or a different one?

Strata (4 each, deterministic): edits from nearest seed x locked decisions broken
  A 1 edit, 0 broken      B 1 edit, 1 broken      C 2 edits, 1 broken
  D 2 edits, 2 broken, radius in      E 2 edits, 2 broken, radius out
  F farther (reached from another seed), 3+ broken
plus 2 repeats for consistency.

Usage (from pilots/p02-region):
    python scripts/build_review.py
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / "pilots/p01b-concept/scripts"))
from region import SEED_IDS, keeps, locks  # noqa: E402
from build_p01b import DEPTS, load  # noqa: E402

SEED = 20261030
NAME = {"D01": "core academic", "D02": "special education", "D03": "art and music", "D04": "gym", "D05": "media center",
        "D06": "dining", "D07": "medical", "D08": "administration", "D09": "custodial"}
PAIRS = [("C", "G"), ("C", "T"), ("G", "T")]


def to_state(r):
    st = r["structure"]
    return {"own": st["own"], "floors": st["floors"], "links": {tuple(k.split("-")): v for k, v in st["links"].items()}}


def role_labels(case):
    own = {d["department_id"]: d["mass_ids"][0] for d in case["structure"]["departments"]}
    role = {own["D01"]: "C", own["D04"]: "G"}
    for m in case["structure"]["masses"]:
        role.setdefault(m["mass_id"], "T")
    return {role[m["mass_id"]]: m["role"] for m in case["structure"]["masses"]}


def fl(f):
    return f"floor {f[0]}" if len(f) == 1 else f"floors {f[0]}-{f[-1]}"


def changes(seed, cand, labels):
    out = []
    for d in DEPTS:
        a, b = (seed["own"][d], seed["floors"][d]), (cand["own"][d], cand["floors"][d])
        if a[0] != b[0] and a[1] != b[1]:
            out.append(f"{NAME[d]} moves from the {labels[a[0]]} to the {labels[b[0]]}, {fl(a[1])} to {fl(b[1])}")
        elif a[0] != b[0]:
            out.append(f"{NAME[d]} moves from the {labels[a[0]]} to the {labels[b[0]]}")
        elif a[1] != b[1]:
            out.append(f"{NAME[d]} moves from {fl(a[1])} to {fl(b[1])} in the {labels[a[0]]}")
    for p in PAIRS:
        if seed["links"][p] != cand["links"][p]:
            out.append(f"the {labels[p[0]]} and the {labels[p[1]]} {'become directly linked' if cand['links'][p] else 'lose their direct link'}")
    return out


def spec(state, labels):
    return {"masses": [{"role": r, "label": labels[r],
                        "departments": [{"dept": d, "floors": state["floors"][d]} for d in DEPTS if state["own"][d] == r]}
                       for r in ("C", "T", "G")],
            "links": ["".join(sorted(p)) for p in PAIRS if state["links"][p]]}


def main():
    cases = load()
    data = json.loads((HERE / "data/candidates.json").read_text(encoding="utf-8"))
    L = {s: locks(cases[s]["case"], cases[s]) for s in SEED_IDS}
    for r in data["candidates"]:
        r["broken"] = sum(not keeps(to_state(r), l) for l in L[r["nearest_seed"]])
    strata = {
        "A": lambda r: r["edits_from_nearest"] == 1 and r["broken"] == 0,
        "B": lambda r: r["edits_from_nearest"] == 1 and r["broken"] == 1,
        "C": lambda r: r["edits_from_nearest"] == 2 and r["broken"] == 1,
        "D": lambda r: r["edits_from_nearest"] == 2 and r["broken"] == 2 and r["radius_in"],
        "E": lambda r: r["edits_from_nearest"] == 2 and r["broken"] == 2 and not r["radius_in"],
        "F": lambda r: r["edits_from_nearest"] is None and r["broken"] >= 3,
    }
    rng = random.Random(SEED)
    picked = []
    for name, f in strata.items():
        pool = [r for r in data["candidates"] if f(r)]
        for r in rng.sample(pool, min(4, len(pool))):
            picked.append((name, r))
    items = []
    for name, r in picked:
        s = r["nearest_seed"]
        labels = role_labels(cases[s]["case"])
        items.append({"candidate_id": r["candidate_id"], "stratum": name, "seed": s,
                      "seed_name": cases[s]["case"]["name"], "seed_concept": cases[s]["case"]["concept"],
                      "seed_diagram": spec(cases[s], labels), "cand_diagram": spec(to_state(r), labels),
                      "changes": changes(cases[s], to_state(r), labels),
                      "nearest_distance": r["nearest_distance"], "broken": r["broken"], "radius_in": r["radius_in"]})
    rng.shuffle(items)
    reps = [dict(it, candidate_id=it["candidate_id"] + "-R", repeat_of=it["candidate_id"]) for it in rng.sample(items, 2)]
    for rep in reps:
        items.insert(rng.randrange(len(items) // 2, len(items) + 1), rep)
    for i, it in enumerate(items, 1):
        it["item"] = i
    sealed = {"seed": SEED, "items": items}
    (HERE / "data/review_SEALED.json").write_text(json.dumps(sealed, indent=1, ensure_ascii=False), encoding="utf-8")
    blind = [{k: it[k] for k in ("item", "candidate_id", "seed_name", "seed_concept", "seed_diagram", "cand_diagram", "changes")} for it in items]
    (HERE / "data/review_set.json").write_text(json.dumps({"items": blind}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(items), "items;", {k: sum(1 for it in items if it["stratum"] == k and "repeat_of" not in it) for k in strata})
    for it in items[:3]:
        print(it["item"], it["seed"], it["changes"])


if __name__ == "__main__":
    main()
