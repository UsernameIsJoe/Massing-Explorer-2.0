"""Region v1: joint membership rule (Task 4), applied to unseen and seen strategies.

Rule
  A valid strategy is in the region if it keeps every idea mark of at least one seed.
  That seed's family is the strategy's idea. Idea marks (carrying-v2-derived):
    mass   idea-marked departments keep their together/apart relations to each other
    floor  idea-marked departments keep their floor relation (ground / above ground, and
           top of mass where the seed has it; reaching the top where the seed does not is allowed)
    link   idea-marked links between the C, T and G masses keep their state
  Within the region, two strategies count as different strategies when the weighted
  change between them is >= 1.0 (the architect's decision weights). Important marks are
  covered by those weights; they never decide membership.
  A strategy that keeps no seed's idea is outside the region. It enters only as a
  provisional expansion, by the architect's review (Pilot 3 add / maybe).
  Embeddings are not used for membership. The nine axes are computed for every member
  as grounding and coverage.

Usage (from repo root):
    python region/membership_v1.py
"""
import collections
import itertools
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEEDS2 = REPO / "benchmarks/test-elementary-v0.1/seeds_v2"
sys.path.insert(0, str(SEEDS2 / "scripts"))
sys.path.insert(0, str(REPO / "pilots/p03-expansion/scripts"))
from build_carrying_page import floor_relation  # noqa: E402
from extract_axes import DEPTS, RUNS  # noqa: E402
import expand  # noqa: E402  (valid(), change(), state_of())

UNITS = ["D01", "D02", "D03", "D04", "D05", "D07", "D08", "D09"]


def roles(own):
    c, g = own["D01"], own["D04"]
    t = next(m for m in set(own.values()) if m not in (c, g))
    return {c: "C", g: "G", t: "T"}


def role_links(own, links):
    r = roles(own)
    return {"".join(sorted((r[a], r[b]))): v for (a, b), v in links.items()}


def make_lock(st, marks):
    own, floors = st["own"], st["floors"]
    idea_mass = sorted(d for d, k in marks["mass"].items() if k == "idea")
    return {"pairs": {(a, b): own[a] == own[b] for a, b in itertools.combinations(idea_mass, 2)},
            "floors": {d: v["relation"] for d, v in marks["floors"].items() if v["kind"] == "idea"},
            "links": {k: v for k, v in role_links(own, st["links"]).items() if marks["links"].get(k) == "idea"}}


def keeps(lock, st, check_floors=True):
    own = st["own"]
    if any((own[a] == own[b]) != v for (a, b), v in lock["pairs"].items()):
        return False
    if check_floors and any(not set(rel) <= set(floor_relation(d, own, st["floors"])) for d, rel in lock["floors"].items()):
        return False
    rl = role_links(own, st["links"])
    return all(rl[k] == v for k, v in lock["links"].items())


def family(locks, st):
    return [sid for sid, lk in locks.items() if keeps(lk, st)]


def pool_state(m):
    st = m["state"]
    return {"own": st["own"], "floors": st["floors"], "slots": st["slots"],
            "links": {tuple(k.split("-")): v for k, v in st["links"].items()}, "hub_links": []}


def organizations():
    seen, out = set(), []
    for assign in itertools.product(range(3), repeat=len(UNITS)):
        if len(set(assign)) < 3:
            continue
        g = frozenset(frozenset(u for u, a in zip(UNITS, assign) if a == k) for k in range(3))
        if g in seen:
            continue
        seen.add(g)
        gl = sorted(g, key=sorted)
        if any(x == frozenset({"D09"}) for x in gl):
            continue
        own = {u: f"M{i}" for i, x in enumerate(gl) for u in x}
        if own["D01"] == own["D04"]:
            continue
        own["D06"] = own["D04"]
        for bits in itertools.product([True, False], repeat=3):
            out.append({"own": own, "links": dict(zip([("M0", "M1"), ("M0", "M2"), ("M1", "M2")], bits))})
    return out


def main():
    marks = json.loads((SEEDS2 / "carrying/carrying_v2_derived.json").read_text(encoding="utf-8"))["answers"]
    cases = {}
    for run, f in RUNS:
        for c in json.loads((SEEDS2 / f).read_text(encoding="utf-8"))["cases"]:
            cases[f"{run}-{c['case_id']}"] = c
    seed_st = {sid: expand.state_of(cases[sid]) for sid in marks}
    locks = {sid: make_lock(seed_st[sid], marks[sid]) for sid in marks}

    # 1. organization level (floors free)
    orgs = organizations()
    org_fam = [[sid for sid, lk in locks.items() if keeps(lk, o, check_floors=False)] for o in orgs]
    org_count = {sid: sum(sid in f for f in org_fam) for sid in locks}
    org_union = sum(bool(f) for f in org_fam)
    org_overlap = sum(len(f) > 1 for f in org_fam)

    # 2. the 15 seeds
    seeds_family = {k: family(locks, expand.state_of(c)) for k, c in cases.items()}

    # 3. Pilot 3 pool (unseen strategies) and its reviewed expansions
    pool = json.loads((REPO / "pilots/p03-expansion/data/pool.json").read_text(encoding="utf-8"))
    members = pool["inside_members"] + [m for g in pool["groups"] for m in g["members"]]
    group_of = {m["key"]: g["group"] for g in pool["groups"] for m in g["members"]}
    sealed = json.loads((REPO / "pilots/p03-expansion/data/expansion_SEALED.json").read_text(encoding="utf-8"))["items"]
    decided = {it["group"]: json.loads((REPO / "pilots/p03-expansion/labels/user_expansion.json").read_text(encoding="utf-8"))[it["expansion_id"]]["answer"] for it in sealed}
    rows, fam_count, distinct = [], collections.Counter(), collections.Counter()
    for m in members:
        st = pool_state(m)
        fam = family(locks, st)
        for sid in fam:
            fam_count[sid] += 1
            if expand.change(seed_st[sid], st)[0] >= 1.0:
                distinct[sid] += 1
        rev = decided.get(group_of.get(m["key"]))
        status = "member" if fam else {"add": "expansion_added", "maybe": "expansion_maybe", "skip": "rejected"}.get(rev, "outside")
        rows.append({"key": m["key"], "families": fam, "status": status, "state": m["state"]})
    tally = collections.Counter(r["status"] for r in rows)
    agree = collections.Counter((r["status"], decided.get(group_of.get(r["key"]))) for r in rows if group_of.get(r["key"]) in decided)

    out = {"version": "region-v1", "date": "2026-10-28", "rule": __doc__, "marks": "carrying-v2-derived",
           "organizations": {"total": len(orgs), "in_region": org_union, "in_two_or_more_families": org_overlap, "per_family": org_count},
           "seeds": seeds_family, "pool": {"total": len(rows), "tally": dict(tally), "per_family": dict(fam_count),
                                            "distinct_strategies_per_family": dict(distinct)},
           "pilot3_review_vs_rule": {f"{s}|{d}": n for (s, d), n in agree.items()},
           "members": rows}
    (REPO / "region/region_v1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    print(f"organizations: {len(orgs)}; in region {org_union} ({100*org_union/len(orgs):.1f}%); in 2+ families {org_overlap}")
    for sid in locks:
        others = [k for k in seeds_family if sid in seeds_family[k] and k != sid]
        print(f"  {sid} {cases[sid]['name'][:36]:36} orgs {org_count[sid]:4}  pool {fam_count[sid]:4} (distinct strategies {distinct[sid]:3})  other seeds in family: {', '.join(others) or '-'}")
    print("seeds outside every family:", [k for k, f in seeds_family.items() if not f])
    print("pool:", dict(tally))
    print("Pilot 3 reviewed groups vs rule (status|your answer: count):", {f"{s}|{d}": n for (s, d), n in sorted(agree.items())})


if __name__ == "__main__":
    main()
