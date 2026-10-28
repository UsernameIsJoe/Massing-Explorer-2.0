"""Nine-axis records for seed v2 cases (extraction rules axes-v1, docs/AXIS_RECORDS_SPEC.md).

Deterministic and label-free: values do not depend on mass ids or their order.
Axes that need geometry are recorded as unknown, never defaulted.

Usage (from seeds_v2):
    python scripts/extract_axes.py
"""
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
VERSION = "axes-v1"
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
NFA = {"D01": 14280, "D02": 5610, "D03": 3040, "D04": 6950, "D05": 2800, "D06": 6150, "D07": 730, "D08": 2510, "D09": 2200}
RUNS = [("R1", "cases/seeds.json"), ("R2", "cases/run02_seeds.json"), ("R3", "cases/run03_seeds.json")]
UNKNOWN = {"value": None, "status": "unknown", "reason": "needs geometry; recorded at realization"}


def roles(own):
    c, g = own["D01"], own["D04"]
    t = next(m for m in set(own.values()) | set() if m not in (c, g)) if len(set(own.values())) == 3 else None
    return {c: "C", g: "G", t: "T"}


def axes_of(structure):
    own = {d["department_id"]: d["mass_ids"][0] for d in structure["departments"]}
    floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in structure["departments"]}
    masses = [m["mass_id"] for m in structure["masses"]]
    role = roles(own)

    # program organization: same-mass bit for every department pair
    po = {f"{a}-{b}": int(own[a] == own[b]) for a, b in combinations(DEPTS, 2)}

    # distribution balance: 1 - largest mass share of program area
    area = {m: sum(NFA[d] for d in DEPTS if own[d] == m) for m in masses}
    balance = round(1 - max(area.values()) / sum(area.values()), 4)

    # topology (redefined, architect 2026-10-28): link pattern between C, T, G masses
    links = sorted("".join(sorted((role[c["mass_a"]], role[c["mass_b"]]))) for c in structure["connections"] if c["direct_link"])
    n = len(links)
    if n == 3:
        shape = "all linked"
    elif n == 2:
        hub = next(r for r in "CGT" if all(r in p for p in links))
        shape = f"chain through {hub}"
    elif n == 1:
        shape = f"single link {links[0]}"
    else:
        shape = "detached"

    # program height of each mass: top occupied floor; gym/dining on floor 1 is double height
    def height(m):
        top = 0
        for d in DEPTS:
            if own[d] == m:
                top = max(top, max(floors[d]), 2 if d in ("D04", "D06") and floors[d] == [1] else 0)
        return top
    h = {role[m]: height(m) for m in masses}
    hs = list(h.values())

    return {
        "extraction": VERSION,
        "program_organization": {"value": po, "status": "derived"},
        "mass_count": {"value": len(masses), "status": "derived", "note": "fixed at 3 by the brief; does not separate cases"},
        "distribution_balance": {"value": balance, "status": "derived", "detail": {role[m]: area[m] for m in masses}},
        "topology": {"value": shape, "status": "derived", "detail": links},
        "loading": UNKNOWN,
        "mean_height": {"value": round(sum(hs) / len(hs), 4), "status": "derived", "detail": h,
                        "note": "program height (top occupied floor), not built height"},
        "height_articulation": {"value": max(hs) - min(hs), "status": "derived"},
        "vertical_organization": {"value": {d: floors[d] for d in DEPTS}, "status": "derived"},
        "geometric_character": dict(UNKNOWN, note="includes the bar arrangement (legacy topology meaning)"),
    }


def main():
    out = {"extraction": VERSION, "spec": "docs/AXIS_RECORDS_SPEC.md", "cases": {}}
    for run, f in RUNS:
        for c in json.loads((HERE / f).read_text(encoding="utf-8"))["cases"]:
            out["cases"][f"{run}-{c['case_id']}"] = axes_of(c["structure"])
    (HERE / "axes").mkdir(exist_ok=True)
    (HERE / "axes/axes_v1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, a in out["cases"].items():
        print(k, a["distribution_balance"]["value"], "|", a["topology"]["value"], "|",
              a["mean_height"]["detail"], a["mean_height"]["value"], a["height_articulation"]["value"])


if __name__ == "__main__":
    main()
