"""Pilot 3: find expansion candidates, structures that make at least one defining
change away from every seed, and group them into distinct moves for review.

Representation is label-free: masses are slots; a department "changes mass" when no
matching of the candidate's masses to the seed's keeps it in place. Weighted change
uses the architect's weights (pilots/p02-region/data/decision_weights.json), taking
the minimum over the six mass matchings. Gym and dining move together and count once.

Widened edits (two at most, from each run-01 seed):
  move     core academic, special education, art and music, media, medical,
           administration or custodial to another mass, floors kept
  commons  move gym and dining together to another mass
  shift    one floor up or down (not gym or dining)
  link     flip one direct link
Hard rules as in Pilot 2, plus core academic and gym never share a mass (the brief's
three-mass reading keeps them distinct in every seed).

Usage (from pilots/p03-expansion):
    python scripts/expand.py
"""
import collections
import copy
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
SEEDS = REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases"
W = json.loads((REPO / "pilots/p02-region/data/decision_weights.json").read_text(encoding="utf-8"))
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
NFA = {"D01": 14280, "D02": 5610, "D03": 3040, "D04": 6950, "D05": 2800, "D06": 6150, "D07": 730, "D08": 2510, "D09": 2200}
MOVABLE = ["D01", "D02", "D03", "D05", "D07", "D08", "D09"]
TH = W["different_strategy_threshold"]
RUN_FILES = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]


def state_of(case):
    s = case["structure"]
    st = {"own": {d["department_id"]: d["mass_ids"][0] for d in s["departments"]},
          "floors": {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]},
          "links": {}, "slots": sorted(m["mass_id"] for m in s["masses"])}
    for c in s["connections"]:
        st["links"][tuple(sorted((c["mass_a"], c["mass_b"])))] = c["direct_link"]
    hub = "heart" in case["concept"].lower()
    st["hub_links"] = [p for p, ok in st["links"].items() if hub and ok and st["own"]["D04"] in p]
    return st


def valid(st):
    if 1 not in st["floors"]["D08"] or st["own"]["D04"] != st["own"]["D06"] or st["own"]["D01"] == st["own"]["D04"]:
        return False
    for d, f in st["floors"].items():
        if not f or f[0] < 1 or f[-1] > 3 or f != list(range(f[0], f[-1] + 1)):
            return False
        if len(f) > 1 and NFA[d] < 753 * len(f):
            return False
    for m in st["slots"]:
        occ = set()
        for d in DEPTS:
            if st["own"][d] == m:
                occ |= set(st["floors"][d])
                if d in ("D04", "D06") and st["floors"][d] == [1]:
                    occ.add(2)
        if not occ or sorted(occ) != list(range(1, max(occ) + 1)):
            return False
    return True


def canon(st):
    best = None
    for perm in itertools.permutations(st["slots"]):
        mp = dict(zip(st["slots"], "abc"))
        mp = {s: "abc"[perm.index(s)] for s in st["slots"]}
        own = tuple(mp[st["own"][d]] for d in DEPTS)
        fl = tuple(tuple(st["floors"][d]) for d in DEPTS)
        lk = tuple(sorted((tuple(sorted((mp[a], mp[b]))), ok) for (a, b), ok in st["links"].items()))
        k = json.dumps([own, fl, lk])
        best = k if best is None or k < best else best
    return best


def neighbours(st):
    for d in MOVABLE:
        for m in st["slots"]:
            if m != st["own"][d]:
                v = copy.deepcopy(st); v["own"][d] = m
                yield v, ("move", d, m)
    for m in st["slots"]:
        if m != st["own"]["D04"]:
            v = copy.deepcopy(st); v["own"]["D04"] = v["own"]["D06"] = m
            yield v, ("commons", "D04", m)
    for d in MOVABLE:
        for step in (-1, 1):
            v = copy.deepcopy(st); v["floors"][d] = [x + step for x in st["floors"][d]]
            yield v, ("shift", d, step)
    for p in st["links"]:
        v = copy.deepcopy(st); v["links"][p] = not st["links"][p]
        yield v, ("link", p, v["links"][p])


def change(seed, cand):
    """Minimum weighted change over matchings of cand slots to seed slots, with the itemised defining changes."""
    best = None
    w = W["department_mass_change"]
    for perm in itertools.permutations(seed["slots"]):
        mp = dict(zip(cand["slots"], perm))
        total, defining = 0.0, []
        for d in DEPTS:
            if d == "D06":
                continue
            moved = mp[cand["own"][d]] != seed["own"][d]
            if moved:
                total += w[d]
                if w[d] >= TH:
                    defining.append(("moves", d, seed["own"][d], mp[cand["own"][d]]))
            elif cand["floors"][d] != seed["floors"][d]:
                total += w[d] * W["floor_only_change_factor"]
        for (a, b), ok in cand["links"].items():
            sp = tuple(sorted((mp[a], mp[b])))
            if seed["links"][sp] != ok:
                if sp in seed["hub_links"]:
                    total += W["hub_link_change"]; defining.append(("hub_link", sp, ok))
                else:
                    total += W["link_change"]
        if best is None or total < best[0]:
            best = (round(total, 3), defining, mp)
    return best


def main():
    cases = {}
    for run, f in RUN_FILES:
        for c in json.loads((SEEDS / f).read_text(encoding="utf-8"))["cases"]:
            cases[f"{run}-{c['case_id']}"] = c
    seeds = {k: state_of(cases[k]) for k in cases if k.startswith("R1-")}
    others = {k: state_of(cases[k]) for k in cases if not k.startswith("R1-")}
    seed_keys = {canon(s) for s in seeds.values()}

    pool = {}
    for sid, s in seeds.items():
        for v1, e1 in neighbours(s):
            if valid(v1) and canon(v1) not in seed_keys:
                pool.setdefault(canon(v1), (v1, sid, [e1]))
            for v2, e2 in neighbours(v1):
                if valid(v2) and canon(v2) not in seed_keys:
                    pool.setdefault(canon(v2), (v2, sid, [e1, e2]))

    rows = []
    for k, (st, origin, edits) in pool.items():
        ch = {sid: change(seeds[sid], st) for sid in seeds}
        near = min(ch, key=lambda s: (ch[s][0], s))
        oth = {o: change(others[o], st)[0] for o in others}
        on = min(oth, key=oth.get)
        rows.append({"key": k, "state": st, "nearest_seed": near, "weighted_change": ch[near][0],
                     "defining": ch[near][1], "matching": ch[near][2], "inside": ch[near][0] < TH,
                     "nearest_other_run_seed": on, "change_to_other_run_seed": oth[on],
                     "edits": len(edits)})
    inside = [r for r in rows if r["inside"]]
    outside = [r for r in rows if not r["inside"]]
    proposed_elsewhere = [r for r in outside if r["change_to_other_run_seed"] < TH]

    def sig(r):
        parts = []
        for d in r["defining"]:
            if d[0] == "moves":
                parts.append(f"{d[1]}:{d[2]}->{d[3]}")
            else:
                parts.append(f"hub:{'-'.join(d[1])}:{'on' if d[2] else 'off'}")
        return r["nearest_seed"] + "|" + ",".join(sorted(parts))
    groups = collections.defaultdict(list)
    for r in outside:
        groups[sig(r)].append(r)
    reps = []
    for g, members in groups.items():
        rep = min(members, key=lambda r: (r["weighted_change"], r["edits"], r["key"]))
        reps.append({"group": g, "size": len(members), "rep": rep})

    out = HERE / "data"
    out.mkdir(exist_ok=True)
    ser = lambda r: {k: (v if k != "state" else {"own": v["own"], "floors": v["floors"],
                                                 "links": {"-".join(p): ok for p, ok in v["links"].items()}, "slots": v["slots"]})
                     for k, v in r.items() if k not in ("matching",)} | {"matching": r["matching"]}
    (out / "pool.json").write_text(json.dumps({"inside": len(inside), "outside": len(outside),
                                               "groups": [{"group": g["group"], "size": g["size"], "rep": ser(g["rep"])} for g in sorted(reps, key=lambda g: (-g["size"], g["group"]))]},
                                              indent=1), encoding="utf-8")
    print(f"valid candidates within two widened edits: {len(rows)}")
    print(f"  inside a seed region: {len(inside)} | outside every region (expansion pool): {len(outside)}")
    print(f"  of the expansion pool, already proposed by the LLM in runs 02-03 (within one defining change): {len(proposed_elsewhere)}")
    print(f"  distinct defining-move groups: {len(groups)}")
    by_type = collections.Counter()
    for g in groups:
        for p in g.split("|")[1].split(","):
            by_type[p.split(":")[0]] += 1
    print("  defining moves by department across groups:", dict(by_type))
    print("  largest groups:", [(g["group"], g["size"]) for g in sorted(reps, key=lambda g: -g["size"])[:8]])


if __name__ == "__main__":
    main()
