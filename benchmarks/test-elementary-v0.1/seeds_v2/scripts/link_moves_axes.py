"""Task 3: link each seed's intention -> key moves -> decisions -> nine-axis components.

Rules (axes-v1):
  program_organization  a move fixes the same-mass bit of every pair of departments it
                        places (1 if placed in the same mass, 0 if in different masses).
                        Pairs with departments the move does not name are not fixed by it.
  vertical_organization a placement fixes that department's floors.
  topology              a link decision fixes that pair's link.
  mean_height,          a placement contributes when the department reaches its mass's
  height_articulation   program height (it sets the top of that mass).
  distribution_balance  a placement contributes the department's area to its mass.
  loading, geometric_character, mass_count: no key-move decision reaches them.

Also reports how much of each seed the moves lock, which is the first test of the
semantic-lock proposal (lock what the key moves point to, vary the rest).

Usage (from seeds_v2):
    python scripts/link_moves_axes.py
"""
import json
from itertools import combinations
from pathlib import Path

from extract_axes import DEPTS, RUNS, roles

HERE = Path(__file__).resolve().parent.parent


def link_case(case):
    s = case["structure"]
    own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
    floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]}
    role = roles(own)

    def top(m):
        t = 0
        for d in DEPTS:
            if own[d] == m:
                t = max(t, max(floors[d]), 2 if d in ("D04", "D06") and floors[d] == [1] else 0)
        return t

    moves, all_pairs, all_depts, all_links = [], set(), set(), set()
    for k in case["key_moves"]:
        placed = {x["department_id"]: x["mass_id"] for x in k["decisions"] if x["type"] == "placement"}
        links = ["".join(sorted((role[x["mass_a"]], role[x["mass_b"]]))) + ("+" if x["direct_link"] else "-")
                 for x in k["decisions"] if x["type"] == "link"]
        pairs = {f"{a}-{b}": int(placed[a] == placed[b]) for a, b in combinations(sorted(placed), 2)}
        axes = {}
        if pairs:
            axes["program_organization"] = pairs
        if placed:
            axes["vertical_organization"] = {d: floors[d] for d in placed}
            axes["distribution_balance"] = sorted(placed)
            tops = sorted(d for d, m in placed.items() if max(floors[d]) == top(m) or (d in ("D04", "D06") and top(m) == 2))
            if tops:
                axes["mean_height / height_articulation"] = tops
        if links:
            axes["topology"] = links
        moves.append({"move_id": k["move_id"], "move": k["move"], "serves": k["serves"], "axes": axes})
        all_pairs |= set(pairs)
        all_depts |= set(placed)
        all_links |= {l[:2] for l in links}
    return {
        "intent": case["intent"], "moves": moves,
        "locked": {"departments_placed": len(all_depts), "of_departments": 9,
                   "pair_bits_fixed": len(all_pairs), "of_pair_bits": 36,
                   "links_fixed": len(all_links), "of_links": 3,
                   "departments_not_named": sorted(set(DEPTS) - all_depts)},
    }


def main():
    out = {"extraction": "axes-v1", "cases": {}}
    for run, f in RUNS:
        for c in json.loads((HERE / f).read_text(encoding="utf-8"))["cases"]:
            out["cases"][f"{run}-{c['case_id']}"] = link_case(c)
    (HERE / "axes/move_axis_links_v1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out["cases"].items():
        L = v["locked"]
        print(k, f"depts {L['departments_placed']}/9  pairs {L['pair_bits_fixed']}/36  links {L['links_fixed']}/3  free: {','.join(L['departments_not_named']) or '-'}")


if __name__ == "__main__":
    main()
