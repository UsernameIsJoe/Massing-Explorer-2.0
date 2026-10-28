"""Pilot 2: generate unseen strategy candidates around the five seeds and test
two membership rules for the region.

Representation: role-labeled structure (classroom mass C, commons mass G, third
mass T), each department's mass and floors, and the three direct links.

Candidates: every distinct structure reachable from a seed by one or two edits,
filtered by hard rules. Edits:
  move   a department other than core academic, gym or dining to another mass, floors kept
  shift  a department other than gym or dining up or down one floor, staying within 1-3
  link   flip one direct link

Membership rules compared:
  radius  inside if structure distance to the nearest seed <= 0.10, the distance at
          which Pilot 01b found independently written versions of the same idea
  lock    inside a seed's family if it keeps every structural decision referenced by
          the key moves that the seed's core commitments protect (implementation lock)

Usage (from pilots/p02-region):
    python scripts/region.py
"""
import collections
import copy
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "pilots/p01b-concept/scripts"))
from build_p01b import DEPTS, load, sdist  # noqa: E402

NFA = {"D01": 14280, "D02": 5610, "D03": 3040, "D04": 6950, "D05": 2800, "D06": 6150, "D07": 730, "D08": 2510, "D09": 2200}
MOVABLE = ["D02", "D03", "D05", "D07", "D08", "D09"]
SHIFTABLE = ["D01", "D02", "D03", "D05", "D07", "D08", "D09"]
PAIRS = [("C", "G"), ("C", "T"), ("G", "T")]
RADIUS = 0.10
SEED_IDS = [f"R1-S0{i}" for i in range(1, 6)]


def key(s):
    return json.dumps([[s["own"][d], s["floors"][d]] for d in DEPTS] + [s["links"][p] for p in PAIRS])


def valid(s):
    """Hard rules from MODEL_INPUT v0.2 that the representation can check."""
    if 1 not in s["floors"]["D08"]:
        return False
    for d, f in s["floors"].items():
        if not f or f[0] < 1 or f[-1] > 3 or f != list(range(f[0], f[-1] + 1)):
            return False
        if len(f) > 1 and NFA[d] < 753 * len(f):
            return False
    if s["own"]["D04"] != s["own"]["D06"]:
        return False
    for m in "CGT":
        occ = set()
        for d in DEPTS:
            if s["own"][d] == m:
                occ |= set(s["floors"][d])
                if d in ("D04", "D06") and s["floors"][d] == [1]:
                    occ.add(2)  # double-height volume
        if not occ or sorted(occ) != list(range(1, max(occ) + 1)):
            return False  # every mass non-empty and stacked from the ground without gaps
    return True


def neighbours(s):
    for d in MOVABLE:
        for m in "CGT":
            if m != s["own"][d]:
                v = copy.deepcopy(s); v["own"][d] = m
                yield v, f"move {d} {s['own'][d]}->{m}"
    for d in SHIFTABLE:
        for step in (-1, 1):
            f = [x + step for x in s["floors"][d]]
            v = copy.deepcopy(s); v["floors"][d] = f
            yield v, f"shift {d} {'up' if step > 0 else 'down'}"
    for p in PAIRS:
        v = copy.deepcopy(s); v["links"][p] = not s["links"][p]
        yield v, f"link {p[0]}-{p[1]} {'on' if v['links'][p] else 'off'}"


def locks(seed_case, s):
    """Structural decisions a seed's core commitments protect, in role terms."""
    c = seed_case
    own = {d["department_id"]: d["mass_ids"][0] for d in c["structure"]["departments"]}
    role = {own["D01"]: "C", own["D04"]: "G"}
    for m in c["structure"]["masses"]:
        role.setdefault(m["mass_id"], "T")
    protected = {p for item in c.get("commitments", {}).get("core", []) for p in item["protects"]}
    out = []
    for mv in c["key_moves"]:
        if mv["move_id"] not in protected:
            continue
        for r in mv["decisions"]:
            if r["type"] == "placement":
                out.append(("placement", r["department_id"], role[r["mass_id"]], tuple(sorted(r["floors"]))))
            else:
                out.append(("link", tuple(sorted((role[r["mass_a"]], role[r["mass_b"]]))), r["direct_link"]))
    return out


def keeps(s, lock):
    if lock[0] == "placement":
        _, d, m, f = lock
        return s["own"][d] == m and tuple(s["floors"][d]) == f
    _, p, ok = lock
    return s["links"][tuple(p)] == ok


def main():
    cases = load()
    seeds = {i: cases[i] for i in SEED_IDS}
    seed_keys = {key(s) for s in seeds.values()}
    cand = {}
    for sid, s in seeds.items():
        for v1, e1 in neighbours(s):
            if valid(v1) and key(v1) not in seed_keys:
                cand.setdefault(key(v1), {"s": v1, "paths": []})["paths"].append((sid, [e1]))
            for v2, e2 in neighbours(v1):
                if valid(v2) and key(v2) not in seed_keys:
                    cand.setdefault(key(v2), {"s": v2, "paths": []})["paths"].append((sid, [e1, e2]))
    lockset = {sid: locks(seeds[sid]["case"], seeds[sid]) for sid in seeds}
    for sid, ls in lockset.items():
        assert all(keeps(seeds[sid], l) for l in ls), f"{sid} fails its own locks"

    rows = []
    for k, c in cand.items():
        s = c["s"]
        d = {sid: sdist(s, seeds[sid]) for sid in seeds}
        near = min(d, key=d.get)
        fam = [sid for sid in seeds if all(keeps(s, l) for l in lockset[sid])]
        edits = min(len(p[1]) for p in c["paths"] if p[0] == near) if any(p[0] == near for p in c["paths"]) else None
        rows.append({"key": k, "nearest_seed": near, "nearest_distance": round(d[near], 4), "edits_from_nearest": edits,
                     "radius_in": d[near] <= RADIUS, "lock_families": fam, "lock_in": bool(fam),
                     "structure": {"own": s["own"], "floors": s["floors"], "links": {"-".join(p): s["links"][p] for p in PAIRS}}})
    rows.sort(key=lambda r: (r["nearest_seed"], r["nearest_distance"], r["key"]))
    for i, r in enumerate(rows, 1):
        r["candidate_id"] = f"K{i:04d}"

    (HERE / "data").mkdir(exist_ok=True)
    (HERE / "data/candidates.json").write_text(json.dumps({"radius": RADIUS, "seeds": SEED_IDS,
                                                           "locks": {k: [list(map(str, l)) for l in v] for k, v in lockset.items()},
                                                           "candidates": rows}, indent=1), encoding="utf-8")
    both = sum(r["radius_in"] and r["lock_in"] for r in rows)
    ro = sum(r["radius_in"] and not r["lock_in"] for r in rows)
    lo = sum(r["lock_in"] and not r["radius_in"] for r in rows)
    none_ = sum(not r["radius_in"] and not r["lock_in"] for r in rows)
    print(f"valid candidates within two edits: {len(rows)}")
    print(f"  inside by both rules: {both} | radius only: {ro} | lock only: {lo} | neither: {none_}")
    print("  per seed (nearest):", dict(collections.Counter(r["nearest_seed"] for r in rows)))
    print("  locks per seed:", {k: len(v) for k, v in lockset.items()})
    print("  multi-family by lock:", sum(len(r["lock_families"]) > 1 for r in rows))
    dist = sorted(r["nearest_distance"] for r in rows)
    print("  nearest-seed distance: min", dist[0], "median", dist[len(dist) // 2], "max", dist[-1])


if __name__ == "__main__":
    main()
