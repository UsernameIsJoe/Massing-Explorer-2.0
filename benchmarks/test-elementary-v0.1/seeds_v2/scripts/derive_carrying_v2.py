"""Derive idea / important marks from the architect's round-1 ticks (carrying-v1.1) and
the architect's own stated rules, without a second survey.

Architect's rules:
  - round 1 mixed two things: program importance and fit to the intent (2026-10-28)
  - importance: core academic, special education, administration, gym, dining matter most;
    media and art mild; custodial almost not (decision weights, Pilot 2)
  - floors are kept as relations, not exact floors (2026-10-28)

Split of each round-1 tick:
  link tick                                   -> idea (links carry no importance weight)
  department named in the seed's concept      -> idea
  department not named, importance weight 1.0 -> important
  department not named, mild or low weight    -> idea (ticked despite low importance)

Usage (from seeds_v2):
    python scripts/derive_carrying_v2.py
"""
import json
import re
from pathlib import Path

from build_carrying_page import floor_relation

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]
W = json.loads((REPO / "pilots/p02-region/data/decision_weights.json").read_text(encoding="utf-8"))["department_mass_change"]
NAMED = {"D01": r"learning|classroom|academ|teaching", "D02": r"special", "D03": r"\barts?\b|making|music",
         "D04": r"commons|hall|athletic|gym|dining", "D05": r"library|media", "D07": r"care|nurse|health",
         "D08": r"office|civic|front|arrival", "D09": r"custod|service"}


def main():
    v1 = json.loads((HERE / "carrying/architect_carrying_v1.1.json").read_text(encoding="utf-8"))["answers"]
    cases = {f"R1-{c['case_id']}": c for c in json.loads((HERE / "cases/seeds.json").read_text(encoding="utf-8"))["cases"]}
    out = {}
    for sid, a in v1.items():
        c = cases[sid]
        s = c["structure"]
        own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
        floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]}

        def kind(d):
            if re.search(NAMED[d], c["concept"], re.I):
                return "idea"
            return "important" if W[d] >= 1.0 else "idea"
        out[sid] = {"mass": {d: kind(d) for d in a["mass"]},
                    "floors": {d: {"kind": kind(d), "relation": floor_relation(d, own, floors)} for d in a["floors"]},
                    "links": {l: "idea" for l in a["links"]}}
    doc = {"version": "carrying-v2-derived", "source": "derived from carrying-v1.1 by the architect's stated rules; no second survey",
           "rules": __doc__, "answers": out}
    (HERE / "carrying/carrying_v2_derived.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    for sid, a in out.items():
        idea = [f"{d} mass" for d, k in a["mass"].items() if k == "idea"] + [f"{d} {'+'.join(v['relation'])}" for d, v in a["floors"].items() if v["kind"] == "idea"] + list(a["links"])
        imp = [f"{d} mass" for d, k in a["mass"].items() if k == "important"] + [f"{d} {'+'.join(v['relation'])}" for d, v in a["floors"].items() if v["kind"] == "important"]
        print(sid, cases[sid]["name"], "\n  idea:", ", ".join(idea), "\n  important:", ", ".join(imp) or "-")


if __name__ == "__main__":
    main()
