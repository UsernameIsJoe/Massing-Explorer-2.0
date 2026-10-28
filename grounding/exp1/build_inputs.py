"""Experiment 1 inputs: the 15 seeds' concept + intent text (key moves withheld) and the
code answer key for every question in the trait questionnaire.

Questionnaire (concrete traits, label-free; masses named by role):
  L = the mass with the core academic classrooms
  C = the mass with gym and dining (the commons)
  X = the remaining mass
  place_<dept>   which mass holds the department: L / C / X           (program organization, balance)
  link_LX/LC/CX  directly connected or not                            (topology)
  storeys_L/C/X  1 / 2 / 3, a double-height hall counts as 2          (mean height, articulation)
  level_<dept>   ground only / ground and upper / upper only          (vertical organization)
Every question also allows "not stated".

Usage (from repo root):  python grounding/exp1/build_inputs.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEEDS = REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases"
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
PLACED = {"D02": "special education", "D03": "art and music", "D05": "media center / library",
          "D07": "medical / nurse", "D08": "administration / front office", "D09": "custodial / maintenance"}
LEVELED = {"D01": "core academic classrooms", **PLACED}


def truth(structure):
    own = {d["department_id"]: d["mass_ids"][0] for d in structure["departments"]}
    floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in structure["departments"]}
    L, C = own["D01"], own["D04"]
    X = next(m["mass_id"] for m in structure["masses"] if m["mass_id"] not in (L, C))
    role = {L: "L", C: "C", X: "X"}
    links = {"".join(sorted((role[c["mass_a"]], role[c["mass_b"]]))): c["direct_link"] for c in structure["connections"]}

    def height(m):
        return max(max(max(floors[d]), 2 if d in ("D04", "D06") and floors[d] == [1] else 0) for d in own if own[d] == m)

    def level(f):
        return "ground only" if f == [1] else ("ground and upper" if 1 in f else "upper only")
    ans = {f"place_{d}": role[own[d]] for d in PLACED}
    ans.update({"link_LX": "linked" if links["LX"] else "not linked", "link_LC": "linked" if links["CL"] else "not linked",
                "link_CX": "linked" if links["CX"] else "not linked"})
    ans.update({f"storeys_{role[m]}": str(height(m)) for m in (L, C, X)})
    ans.update({f"level_{d}": level(floors[d]) for d in LEVELED})
    return ans


def record_in_words(structure):
    """The full record as plain sentences, for the expressibility arm (writer input)."""
    a = truth(structure)
    names = {"L": "the learning mass (core academic classrooms)", "C": "the commons mass (gym and dining, double height)", "X": "the third mass"}
    lines = [f"{PLACED[d].capitalize()} is in {names[a['place_' + d]]}." for d in PLACED]
    lines += [f"{names[p[0]].capitalize()} and {names[p[1]]} are {a['link_' + p]}." for p in ("LX", "LC", "CX")]
    lines += [f"{names[r].capitalize()} has {a['storeys_' + r]} storeys." for r in "LCX"]
    lines += [f"{LEVELED[d].capitalize()}: {a['level_' + d]}." for d in LEVELED]
    return " ".join(lines)


def main():
    items = []
    for run, f in RUNS:
        for c in json.loads((SEEDS / f).read_text(encoding="utf-8"))["cases"]:
            items.append({"id": f"{run}-{c['case_id']}", "text": f"{c['concept']} {c['intent']}",
                          "truth": truth(c["structure"]), "record_words": record_in_words(c["structure"])})
    out = {"questions": {"place": PLACED, "level": LEVELED}, "items": items}
    (REPO / "grounding/exp1/items.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(items), "items;", len(items[0]["truth"]), "questions each")


if __name__ == "__main__":
    main()
