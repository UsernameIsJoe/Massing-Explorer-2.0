"""Assemble the Pilot 01b labeling pages (v1.1) for both passes.

Pass A (concept): labeling/labeling_page_concept.html
Pass B (full):    labeling/labeling_page.html (same file as v1, so its link is kept)

Usage (from pilots/p01b-concept):
    python scripts/build_labeling_page.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEXT = {
    "concept": ("ME2 Concept Pass", "Pilot 01b · Pass A · Concepts only",
                "Each scheme is shown only by its <strong>concept</strong>. Pick the option whose concept describes the <strong>closer organizing idea</strong> to the anchor's concept. Judge the idea, not the wording. Use \"Can't judge\" whenever the text alone is not enough."),
    "full": ("ME2 Whole Scheme Pass", "Pilot 01b · Pass B · Whole scheme",
             "Pick the option that is <strong>more like the same strategy</strong> as the anchor, judging the whole scheme: diagram, concept, intent, key moves and trade-off. Ignore wording, brief compliance and which design is better. Use \"About equal\" only when you truly cannot separate them."),
}


def embed(path):
    return json.dumps(json.loads((HERE / path).read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")


def main():
    tpl = (HERE / "labeling" / "labeling_page.template.html").read_text(encoding="utf-8")
    for mode, out in (("concept", "labeling_page_concept.html"), ("full", "labeling_page.html")):
        title, h1, sub = TEXT[mode]
        t = tpl
        for key, val in (("__TITLE__", title), ("__H1__", h1), ("__SUB__", sub), ("__MODE__", json.dumps(mode)),
                         ("__DATA__", embed(f"data/labeling_set_{mode}.json")), ("__DIAGRAMS__", embed("data/diagram_data.json")),
                         ("__PROBES__", embed("data/probe_review.json"))):
            if t.count(key) != 1:
                raise SystemExit(f"template must contain {key} exactly once")
            t = t.replace(key, val)
        (HERE / "labeling" / out).write_text(t, encoding="utf-8", newline="\n")
        print("wrote labeling/" + out)


if __name__ == "__main__":
    main()
