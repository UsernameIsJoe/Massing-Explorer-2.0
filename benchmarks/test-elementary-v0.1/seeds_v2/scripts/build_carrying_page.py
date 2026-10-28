"""Build carrying/page.html: the architect ticks, for each R1 seed, the decisions its
idea cannot lose (input to the Task 4 semantic-lock rule).

Usage (from seeds_v2):
    python scripts/build_carrying_page.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]
SRC = REPO / "pilots/p01-representation/labeling/labeling_page.template.html"
NAME = {"D01": "Core academic", "D02": "Special education", "D03": "Art and music", "D04": "Gym and dining",
        "D05": "Media center", "D07": "Medical", "D08": "Administration", "D09": "Custodial"}
ITEMS = ["D01", "D02", "D03", "D04", "D05", "D07", "D08", "D09"]
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]


def fl(f):
    return f"floor {f[0]}" if len(f) == 1 else f"floors {f[0]}–{f[-1]}"


def mass_height(m, own, floors):
    """Program height of a mass: top occupied floor; gym and dining on floor 1 count as 2."""
    return max(max(max(floors[d]), 2 if d in ("D04", "D06") and floors[d] == [1] else 0)
               for d in DEPTS if own[d] == m)


def floor_relation(d, own, floors):
    """Relations kept by a floor lock (carrying-v2): on the ground floor or above it,
    plus at the top of its mass when it reaches the top."""
    f = floors[d]
    rel = ["ground"] if 1 in f else ["above_ground"]
    if max(f) == mass_height(own[d], own, floors) and not (d in ("D04", "D06") and f == [1]):
        rel.append("top")
    return rel


REL_TEXT = {"ground": "on the ground floor", "above_ground": "above the ground floor", "top": "at the top of its mass"}


def seed_item(c, relations=False):
    s = c["structure"]
    own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
    floors = {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]}
    label = {m["mass_id"]: m["role"] for m in s["masses"]}
    cm, gm = own["D01"], own["D04"]
    tm = next(m for m in label if m not in (cm, gm))
    order = [(cm, "C"), (tm, "T"), (gm, "G")]
    rmap = dict(order)
    diagram = {"masses": [{"role": r, "label": label[m], "departments": [{"dept": d, "floors": floors[d]} for d in DEPTS if own[d] == m]} for m, r in order],
               "links": ["".join(sorted((rmap[x["mass_a"]], rmap[x["mass_b"]]))) for x in s["connections"] if x["direct_link"]]}
    mass, flo = [], []
    for d in ITEMS:
        mates = [NAME[o] for o in ITEMS if o != d and own[o] == own[d]]
        mass.append({"id": d, "text": f"{NAME[d]} in the {label[own[d]]}" + (f" (with {', '.join(m.lower() for m in mates)})" if mates else " (alone)")})
        if relations:
            rel = floor_relation(d, own, floors)
            flo.append({"id": d, "relation": rel, "text": f"{NAME[d]} " + " and ".join(REL_TEXT[r] for r in rel) + f" (now {fl(floors[d])})"})
        else:
            flo.append({"id": d, "text": f"{NAME[d]} on {fl(floors[d])}" + (" (double height)" if d == "D04" and floors[d] == [1] else "")})
    links = []
    for x in s["connections"]:
        a, b = label[x["mass_a"]], label[x["mass_b"]]
        pid = "".join(sorted((rmap[x["mass_a"]], rmap[x["mass_b"]])))
        links.append({"id": pid, "text": f"The {a} and the {b} are {'directly linked' if x['direct_link'] else 'not linked'}"})
    return {"seed_id": f"R1-{c['case_id']}", "name": c["name"], "concept": c["concept"], "intent": c["intent"],
            "moves": [{"move": k["move"], "serves": k["serves"]} for k in c["key_moves"]],
            "diagram": diagram, "mass": mass, "floors": flo, "links": links}


def main(version="v2"):
    """v1: exact floors, one tick (page.html). v2: floor relations, idea / important (page2.html)."""
    v2 = version == "v2"
    cases = json.loads((HERE / "cases/seeds.json").read_text(encoding="utf-8"))["cases"]
    data = {"seeds": [seed_item(c, relations=v2) for c in cases]}
    (HERE / ("carrying/carrying_set_v2.json" if v2 else "carrying/carrying_set.json")).write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    tpl = SRC.read_text(encoding="utf-8")
    tokens = re.search(r":root\{.*?\n\}\n@media \(prefers-color-scheme:dark\)\{.*?\}\}\n:root\[data-theme=\"dark\"\]\{.*?\}", tpl, re.S).group(0)
    kinds = re.search(r"const KIND = \{.*?\};\nconst ROLE = .*?;\n", tpl, re.S).group(0)
    diagram = re.search(r"function diagramSVG\(spec\)\{.*?\n\}\n", tpl, re.S).group(0)
    diagram = diagram.replace("return {role:m.role, blocks,", "return {role:m.role, label:m.label||ROLE[m.role], blocks,")
    diagram = diagram.replace('text-anchor="middle">${ROLE[c.role]}</text>', 'text-anchor="middle">${escx(c.label)}</text>')
    assert "escx(c.label)" in diagram
    page = (HERE / ("carrying/page2.template.html" if v2 else "carrying/page.template.html")).read_text(encoding="utf-8")
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = page.replace("/*__TOKENS__*/", tokens).replace("/*__KINDS__*/", kinds).replace("/*__DIAGRAM__*/", diagram).replace("__DATA__", js)
    out = "carrying/page2.html" if v2 else "carrying/page.html"
    (HERE / out).write_text(page, encoding="utf-8", newline="\n")
    print("wrote", out)


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "v2")
