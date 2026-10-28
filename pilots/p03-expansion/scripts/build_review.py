"""Pick expansion representatives and build the Add / Maybe / Skip review set.

Selection (deterministic): for each run-01 seed, its defining-move groups are taken
largest first, skipping a group whose defining departments were already covered for
that seed, up to 4 per seed. Groups with no single defining move (several smaller
changes adding up) are skipped. One representative per group: the cleanest member
(smallest weighted change, then fewest edits).

Usage (from pilots/p03-expansion):
    python scripts/build_review.py
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
SEEDS = REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases/seeds.json"
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
NAME = {"D01": "core academic", "D02": "special education", "D03": "art and music", "D04": "gym and dining",
        "D05": "media center", "D06": "dining", "D07": "medical", "D08": "administration", "D09": "custodial"}
PER_SEED = 4
SEED = 20261031


def fl(f):
    return f"floor {f[0]}" if len(f) == 1 else f"floors {f[0]}-{f[-1]}"


def derived_prefs(st):
    own, floors = st["own"], st["floors"]
    out = []
    if 1 not in floors["D03"]:
        out.append("art and music leave the ground floor")
    top = max(max(f) for d, f in floors.items() if own[d] == own["D05"])
    if not (own["D05"] == own["D08"] and max(floors["D05"]) == top and min(floors["D05"]) > max(floors["D08"])):
        out.append("media is not above administration")
    for m in st["slots"]:
        t = 0
        for d, f in floors.items():
            if own[d] == m:
                t = max(t, max(f), 2 if d in ("D04", "D06") and f == [1] else 0)
        if t < 3:
            out.append("not every mass reaches three floors")
            break
    return out


def roles_and_spec(st, labels_by_slot):
    c, g = st["own"]["D01"], st["own"]["D04"]
    t = next(m for m in st["slots"] if m not in (c, g))
    order = [(c, "C"), (t, "T"), (g, "G")]
    masses = [{"role": r, "label": labels_by_slot.get(m, m),
               "departments": [{"dept": d, "floors": st["floors"][d]} for d in DEPTS if st["own"][d] == m]} for m, r in order]
    rmap = {m: r for m, r in order}
    links = ["".join(sorted((rmap[a], rmap[b]))) for (a, b), ok in st["links"].items() if ok]
    return {"masses": masses, "links": links}


def main():
    seeds = {f"R1-{c['case_id']}": c for c in json.loads(SEEDS.read_text(encoding="utf-8"))["cases"]}
    pool = json.loads((HERE / "data/pool.json").read_text(encoding="utf-8"))
    picked = []
    for sid in sorted(seeds):
        covered, n = set(), 0
        for g in pool["groups"]:
            seed_of, moves = g["group"].split("|")
            if seed_of != sid or not moves:
                continue
            depts = {m.split(":")[0] for m in moves.split(",")}
            if depts <= covered:
                continue
            covered |= depts
            picked.append(g)
            n += 1
            if n == PER_SEED:
                break
    items = []
    for g in picked:
        rep = g["rep"]
        sid = rep["nearest_seed"]
        seed = seeds[sid]
        s_struct = seed["structure"]
        labels = {m["mass_id"]: m["role"] for m in s_struct["masses"]}
        cand = rep["state"]
        cand["links"] = {tuple(k.split("-")): v for k, v in cand["links"].items()}
        mp = rep["matching"]  # candidate slot -> seed slot
        cand_labels = {cs: labels[ss] for cs, ss in mp.items()}
        sst = {"own": {d["department_id"]: d["mass_ids"][0] for d in s_struct["departments"]},
               "floors": {d["department_id"]: sorted(d["occupied_floors"]) for d in s_struct["departments"]},
               "links": {tuple(sorted((c["mass_a"], c["mass_b"]))): c["direct_link"] for c in s_struct["connections"]},
               "slots": sorted(labels)}
        changes, defining = [], []
        for d in DEPTS:
            if d == "D06":
                continue
            a, b = sst["own"][d], mp[cand["own"][d]]
            if a != b:
                txt = f"{NAME[d]} moves from the {labels[a]} to the {labels[b]}"
                (defining if d in ("D01", "D02", "D04", "D08") else changes).append(txt)
            elif sst["floors"][d] != cand["floors"][d]:
                changes.append(f"{NAME[d]} moves from {fl(sst['floors'][d])} to {fl(cand['floors'][d])} in the {labels[a]}")
        for (a, b), ok in cand["links"].items():
            sa, sb = sorted((mp[a], mp[b]))
            if sst["links"][(sa, sb)] != ok:
                hub = "heart" in seed["concept"].lower() and sst["links"][(sa, sb)] and sst["own"]["D04"] in (sa, sb)
                (defining if hub else changes).append(f"the {labels[sa]} and the {labels[sb]} {'become directly linked' if ok else 'lose their direct link'}")
        items.append({"expansion_id": f"X{len(items) + 1:02d}", "group": g["group"], "group_size": g["size"], "seed": sid,
                      "seed_name": seed["name"], "seed_concept": seed["concept"],
                      "seed_diagram": roles_and_spec(sst, labels), "cand_diagram": roles_and_spec(cand, cand_labels),
                      "defining_changes": defining, "other_changes": changes,
                      "brief_preferences_given_up": derived_prefs(cand),
                      "weighted_change": rep["weighted_change"],
                      "proposed_elsewhere_by_llm": rep["change_to_other_run_seed"] < 1.0,
                      "state": {"own": cand["own"], "floors": cand["floors"], "links": {"-".join(p): v for p, v in cand["links"].items()}, "slots": cand["slots"]}})
    random.Random(SEED).shuffle(items)
    for i, it in enumerate(items, 1):
        it["item"] = i
    (HERE / "data/expansion_SEALED.json").write_text(json.dumps({"items": items}, indent=1, ensure_ascii=False), encoding="utf-8")
    blind = [{k: it[k] for k in ("item", "expansion_id", "seed_name", "seed_concept", "seed_diagram", "cand_diagram",
                                 "defining_changes", "other_changes", "brief_preferences_given_up")} for it in items]
    (HERE / "data/expansion_review_set.json").write_text(json.dumps({"items": blind}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(items), "representatives")
    for it in sorted(items, key=lambda x: x["seed"]):
        print(it["seed"], it["group_size"], "|", "; ".join(it["defining_changes"]) or "-", "|", "; ".join(it["other_changes"])[:80])


if __name__ == "__main__":
    main()
