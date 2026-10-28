"""Assemble review/review_page.html from the template, the blind review set and
the shared diagram code (taken from the Pilot 01 page so diagrams read the same).

Usage (from pilots/p02-region):
    python scripts/build_review_page.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = HERE.parent / "p01-representation/labeling/labeling_page.template.html"


def main():
    tpl = SRC.read_text(encoding="utf-8")
    tokens = re.search(r":root\{.*?\n\}\n@media \(prefers-color-scheme:dark\)\{.*?\}\}\n:root\[data-theme=\"dark\"\]\{.*?\}", tpl, re.S).group(0)
    kinds = re.search(r"const KIND = \{.*?\};\nconst ROLE = .*?;\n", tpl, re.S).group(0)
    diagram = re.search(r"function diagramSVG\(spec\)\{.*?\n\}\n", tpl, re.S).group(0)
    diagram = diagram.replace("return {role:m.role, blocks,", "return {role:m.role, label:m.label||ROLE[m.role], blocks,")
    diagram = diagram.replace('text-anchor="middle">${ROLE[c.role]}</text>', 'text-anchor="middle">${escx(c.label)}</text>')
    assert "escx(c.label)" in diagram
    data = json.dumps(json.loads((HERE / "data/expansion_review_set.json").read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")
    page = (HERE / "review/review_page.template.html").read_text(encoding="utf-8")
    page = page.replace("/*__TOKENS__*/", tokens).replace("/*__KINDS__*/", kinds).replace("/*__DIAGRAM__*/", diagram).replace("__DATA__", data)
    (HERE / "review/review_page.html").write_text(page, encoding="utf-8", newline="\n")
    print("wrote review/review_page.html")


if __name__ == "__main__":
    main()
