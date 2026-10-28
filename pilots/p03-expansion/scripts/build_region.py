"""Assemble region v1 from the seeds, their inside variations and the expansion
groups, using the architect's Pilot 3 decisions.

Status of each expansion group:
  added / maybe / rejected     decided by the architect on the group's representative
  needs_review                 its reviewed representative broke the custodial rule added
                               afterwards, so the decision no longer applies to the group
  inferred_add                 unreviewed; its defining move is special education or core
                               academic, the moves the architect added (9 of 10 reviewed)
  inferred_maybe               unreviewed; administration only (reviewed 5 of 5 maybe)
  unreviewed                   any other unreviewed group

Usage (from pilots/p03-expansion):
    python scripts/build_region.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def main():
    pool = json.loads((HERE / "data/pool.json").read_text(encoding="utf-8"))
    sealed = {it["expansion_id"]: it for it in json.loads((HERE / "data/expansion_SEALED.json").read_text(encoding="utf-8"))["items"]}
    decisions = {k: v["answer"] for k, v in json.loads((HERE / "labels/user_expansion.json").read_text(encoding="utf-8")).items()}
    reviewed = {}
    for eid, it in sealed.items():
        st = it["state"]
        masses = collections.defaultdict(list)
        for d, m in st["own"].items():
            masses[m].append(d)
        invalid = any(v == ["D09"] for v in masses.values())
        reviewed[it["group"]] = {"expansion_id": eid, "answer": decisions[eid], "rep_now_invalid": invalid}

    groups = []
    for g in pool["groups"]:
        sig = g["group"]
        moves = sig.split("|")[1]
        depts = {m.split(":")[0] for m in moves.split(",")} if moves else set()
        r = reviewed.get(sig)
        if r and r["rep_now_invalid"]:
            status = "needs_review"
        elif r:
            status = {"add": "added", "maybe": "maybe", "skip": "rejected"}[r["answer"]]
        elif depts & {"D01", "D02"}:
            status = "inferred_add"
        elif depts == {"D08"}:
            status = "inferred_maybe"
        else:
            status = "unreviewed"
        groups.append({"group": sig, "seed": sig.split("|")[0], "defining_moves": moves or "several smaller changes",
                       "status": status, "reviewed_as": r["expansion_id"] if r else None,
                       "size": g["size"], "members": [m["key"] for m in g["members"]], "representative": g["rep"]["key"]})
    region = {
        "version": "region-candidate-structural",
        "date": "2026-10-28",
        "membership": "weighted change from the nearest seed < 1.0 (architect's weights, pilots/p02-region/data/decision_weights.json)",
        "hard_rules": "MODEL_INPUT v0.2 representable rules + core academic and gym in different masses + custodial not a mass of its own",
        "seeds": ["R1-S01", "R1-S02", "R1-S03", "R1-S04", "R1-S05"],
        "inside_variations": len(pool["inside_members"]),
        "expansion_groups": groups,
    }
    (HERE / "region").mkdir(exist_ok=True)
    (HERE / "region/region_candidate_structural.json").write_text(json.dumps(region, indent=1), encoding="utf-8")
    tally = collections.Counter()
    for g in groups:
        tally[g["status"]] += g["size"]
    gcount = collections.Counter(g["status"] for g in groups)
    print("region v1: 5 seeds +", region["inside_variations"], "inside variations")
    for s in ("added", "maybe", "inferred_add", "inferred_maybe", "needs_review", "unreviewed", "rejected"):
        print(f"  {s:15} groups {gcount[s]:3}  structures {tally[s]:4}")


if __name__ == "__main__":
    main()
