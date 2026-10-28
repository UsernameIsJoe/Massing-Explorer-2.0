"""Assemble labeling/labeling_page.html from the template, the blind labeling set
and the diagram specs. No content is generated here; it only embeds data files.

Usage (from pilots/p01-representation):
    python scripts/build_labeling_page.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def embed(path):
    data = json.loads((HERE / path).read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def main():
    t = (HERE / "labeling" / "labeling_page.template.html").read_text(encoding="utf-8")
    for key, path in (("__DATA__", "data/labeling_set.json"), ("__DIAGRAMS__", "data/diagram_data.json")):
        if t.count(key) != 1:
            raise SystemExit(f"template must contain {key} exactly once")
        t = t.replace(key, embed(path))
    (HERE / "labeling" / "labeling_page.html").write_text(t, encoding="utf-8", newline="\n")
    print("wrote labeling/labeling_page.html")


if __name__ == "__main__":
    main()
