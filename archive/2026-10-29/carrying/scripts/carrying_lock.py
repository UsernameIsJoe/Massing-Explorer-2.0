"""Semantic lock from the architect's carrying decisions (carrying-v1.1), and what it admits.

Lock rule (stated on the page the architect answered):
  mass    ticked departments keep their same-mass / different-mass relations to each other
  floors  ticked departments keep their floors
  links   ticked links between the C, T and G masses keep their state
Everything unticked is free. Gym and dining move together (hard rule).

Measurements (input to Task 4, not a membership decision):
  1. organization space: of all valid groupings x link patterns, the share each lock admits
     (floors not enumerated)
  2. which of the 15 seeds (runs 01-03) each lock admits, floors included
  3. the Pilot 3 pool: how many strategies each lock admits

Usage (from seeds_v2):
    python scripts/carrying_lock.py
"""
import itertools
import json
from pathlib import Path

from extract_axes import DEPTS, RUNS

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]
UNITS = ["D01", "D02", "D03", "D04", "D05", "D07", "D08", "D09"]  # D06 follows D04


def state_from_case(c):
    s = c["structure"]
    own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
    floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]}
    links = {tuple(sorted((x["mass_a"], x["mass_b"]))): x["direct_link"] for x in s["connections"]}
    return own, floors, links


def role_links(own, links):
    c, g = own["D01"], own["D04"]
    masses = set(own.values())
    t = next(m for m in masses if m not in (c, g))
    r = {c: "C", g: "G", t: "T"}
    return {"".join(sorted((r[a], r[b]))): v for (a, b), v in links.items()}


def make_lock(own, floors, links, ans):
    mass = sorted(ans["mass"])
    return {"pairs": {(a, b): own[a] == own[b] for a, b in itertools.combinations(mass, 2)},
            "floors": {d: floors[d] for d in ans["floors"]},
            "links": {k: v for k, v in role_links(own, links).items() if k in ans["links"]}}


def admits(lock, own, floors, links, check_floors=True):
    if any((own[a] == own[b]) != v for (a, b), v in lock["pairs"].items()):
        return False
    if check_floors and any(floors[d] != f for d, f in lock["floors"].items()):
        return False
    rl = role_links(own, links)
    return all(rl[k] == v for k, v in lock["links"].items())


def organizations():
    """All groupings of the 8 units into 3 non-empty unlabeled masses, D01 apart from D04,
    custodial not alone, each with every link pattern."""
    seen = set()
    for assign in itertools.product(range(3), repeat=len(UNITS)):
        if len(set(assign)) < 3:
            continue
        groups = frozenset(frozenset(u for u, a in zip(UNITS, assign) if a == k) for k in range(3))
        if groups in seen:
            continue
        seen.add(groups)
    out = []
    for groups in seen:
        gl = sorted(groups, key=sorted)
        if any(g == frozenset({"D09"}) for g in gl):
            continue
        own = {u: f"M{i}" for i, g in enumerate(gl) for u in g}
        if own["D01"] == own["D04"]:
            continue
        own["D06"] = own["D04"]
        pairs = [("M0", "M1"), ("M0", "M2"), ("M1", "M2")]
        for bits in itertools.product([True, False], repeat=3):
            out.append((own, dict(zip(pairs, bits))))
    return out


def main():
    ans = json.loads((HERE / "carrying/architect_carrying_v1.1.json").read_text(encoding="utf-8"))["answers"]
    cases = {}
    for run, f in RUNS:
        for c in json.loads((HERE / f).read_text(encoding="utf-8"))["cases"]:
            cases[f"{run}-{c['case_id']}"] = (c["name"], state_from_case(c))
    locks = {sid: make_lock(*cases[sid][1], ans[sid]) for sid in ans}

    orgs = organizations()
    report = {"organizations_total": len(orgs), "locks": {}}
    print(f"organization space (groupings x link patterns, floors free): {len(orgs)}")
    for sid, lk in locks.items():
        n = sum(admits(lk, own, None, links, check_floors=False) for own, links in orgs)
        hits = [k for k, (_, st) in cases.items() if admits(lk, *st)]
        hits_nofloor = [k for k, (_, st) in cases.items() if admits(lk, *st, check_floors=False)]
        report["locks"][sid] = {"organizations_admitted": n, "share": round(n / len(orgs), 4),
                                "seeds_admitted": hits, "seeds_admitted_ignoring_floors": hits_nofloor}
        print(f"{sid} {cases[sid][0][:34]:34} admits {n:5} ({100*n/len(orgs):4.1f}%)  seeds: {', '.join(h for h in hits if h != sid) or '-'}"
              f"   ignoring floors: {', '.join(h for h in hits_nofloor if h != sid) or '-'}")

    pool = json.loads((REPO / "pilots/p03-expansion/data/pool.json").read_text(encoding="utf-8"))
    members = pool["inside_members"] + [m for g in pool["groups"] for m in g["members"]]
    print(f"Pilot 3 pool: {len(members)} strategies")
    for sid, lk in locks.items():
        n = 0
        for m in members:
            st = m["state"]
            links = {tuple(k.split("-")): v for k, v in st["links"].items()}
            n += admits(lk, st["own"], st["floors"], links)
        report["locks"][sid]["pilot3_pool_admitted"] = n
        print(f"  {sid} admits {n}")
    (HERE / "carrying/lock_measurements_v1.1.json").write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
