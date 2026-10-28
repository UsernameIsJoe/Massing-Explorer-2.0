"""Build the seed coherence review page (seeds v2.0).

Reuses the Pilot 01 diagram code and colour tokens so diagrams read the same way.
Masses are shown in a fixed order (classroom mass, other mass, commons mass) and
titled with each seed's own role label.

Usage (from the repo root):
    python benchmarks/test-elementary-v0.1/seeds_v2/scripts/build_review_page.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V2 = ROOT / "benchmarks/test-elementary-v0.1/seeds_v2"
LABEL_TPL = ROOT / "pilots/p01-representation/labeling/labeling_page.template.html"
NOTES = V2 / "review" / "claude_notes.json"


def diagram_spec(case):
    s = case["structure"]
    owner = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
    roles = {owner["D01"]: "C", owner["D04"]: "G"}
    for m in s["masses"]:
        roles.setdefault(m["mass_id"], "T")
    label = {m["mass_id"]: m["role"] for m in s["masses"]}
    masses = []
    for r in ("C", "T", "G"):
        mid = next(k for k, v in roles.items() if v == r)
        masses.append({"role": r, "label": f"{mid} · {label[mid]}",
                       "departments": [{"dept": d["department_id"], "floors": d["occupied_floors"]}
                                       for d in s["departments"] if d["mass_ids"][0] == mid]})
    links = []
    for c in s["connections"]:
        if c["direct_link"]:
            links.append("".join(sorted((roles[c["mass_a"]], roles[c["mass_b"]]))))
    return {"masses": masses, "links": links}


def main():
    tpl = LABEL_TPL.read_text(encoding="utf-8")
    tokens = re.search(r":root\{.*?\n\}\n@media \(prefers-color-scheme:dark\)\{.*?\}\}\n:root\[data-theme=\"dark\"\]\{.*?\}", tpl, re.S).group(0)
    kinds = re.search(r"const KIND = \{.*?\};\nconst ROLE = .*?;\n", tpl, re.S).group(0)
    diagram = re.search(r"function diagramSVG\(spec\)\{.*?\n\}\n", tpl, re.S).group(0)
    diagram = diagram.replace("return {role:m.role, blocks,", "return {role:m.role, label:m.label||ROLE[m.role], blocks,")
    diagram = diagram.replace('<text class="mt" x="${x+CW/2}" y="${base+16}" text-anchor="middle">${ROLE[c.role]}</text>',
                              '<text class="mt" x="${x+CW/2}" y="${base+16}" text-anchor="middle">${escx(c.label)}</text>')
    assert "escx(c.label)" in diagram and "label:m.label" in diagram

    data = json.loads((V2 / "cases" / "seeds.json").read_text(encoding="utf-8"))
    report = json.loads((V2 / "cases" / "seeds.validation.json").read_text(encoding="utf-8"))
    notes = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}
    cases = []
    for c in data["cases"]:
        r = next(x for x in report["cases"] if x["case_id"] == c["case_id"])
        cases.append({"case": c, "diagram": diagram_spec(c), "checks": {"errors": r["errors"], "warnings": r["warnings"]},
                      "claude_notes": notes.get(c["case_id"], [])})
    payload = json.dumps({"cases": cases, "collection_differences": data["collection_differences"]},
                         ensure_ascii=False).replace("</", "<\\/")
    page = (V2 / "review" / "review_page.template.html").read_text(encoding="utf-8")
    page = page.replace("/*__TOKENS__*/", tokens).replace("/*__KINDS__*/", kinds).replace("/*__DIAGRAM__*/", diagram).replace("__SEEDS__", payload)
    (V2 / "review" / "review_page.html").write_text(page, encoding="utf-8", newline="\n")
    print("wrote review/review_page.html")


if __name__ == "__main__":
    main()
