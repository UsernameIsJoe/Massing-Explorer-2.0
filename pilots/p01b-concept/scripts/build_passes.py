"""Build the two labeling passes for Pilot 01b v1.1 from the locked triplets.

Pass A (concept): each scheme shown as its concept text only.
Pass B (full):    diagram, concept, intent, key moves, trade-off, structure line,
                  with commitments in a collapsed section. Unresolved notes omitted.
Items and presentation order are exactly those of data/triplets_SEALED.json.

Usage (from pilots/p01b-concept):
    python scripts/build_passes.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_p01b import compact, load  # noqa: E402

NAME = {"D01": "core academic", "D02": "special ed", "D03": "art & music", "D04": "gym", "D05": "media",
        "D06": "dining", "D07": "medical", "D08": "admin", "D09": "custodial"}


def ref(r):
    if r["type"] == "placement":
        f = r["floors"]
        return f"{NAME[r['department_id']]} · {r['mass_id']} · fl {f[0]}" + (f"–{f[-1]}" if len(f) > 1 else "")
    return f"{r['mass_a']}–{r['mass_b']} {'linked' if r['direct_link'] else 'not linked'}"


def main():
    cases = load()
    sealed = json.loads((HERE / "data/triplets_SEALED.json").read_text(encoding="utf-8"))
    by = {t["triplet_id"]: t for t in sealed["triplets"]}

    def concept_only(k):
        return {"text": cases[k]["case"]["concept"]}

    def full(k):
        c = cases[k]["case"]
        roles = {m["mass_id"]: m["role"] for m in c["structure"]["masses"]}
        return {"text": c["concept"], "intent": c["intent"], "structure": compact(cases[k]),
                "masses": ", ".join(f"{m} = {r}" for m, r in roles.items()),
                "moves": [{"move": m["move"], "serves": m["serves"], "refs": [ref(r) for r in m["decisions"]]} for m in c["key_moves"]],
                "tradeoff": c["brief_response"]["main_tradeoff"],
                "commitments": {"core": [x["statement"] for x in c.get("commitments", {}).get("core", [])],
                                "flexible": c.get("commitments", {}).get("flexible", [])}}

    for mode, fn, q in (("concept", concept_only, "Which option's concept describes the closer organizing idea to the anchor's concept?"),
                        ("full", full, "Which option is the closer architectural strategy to the anchor?")):
        items = [{"item": n, "triplet_id": tid, "anchor": fn(by[tid]["anchor"]),
                  "option_1": fn(by[tid]["shown_order"][0]), "option_2": fn(by[tid]["shown_order"][1])}
                 for n, tid in enumerate(sealed["presentation_order"], 1)]
        (HERE / f"data/labeling_set_{mode}.json").write_text(
            json.dumps({"mode": mode, "question": q, "answers": ["option_1", "option_2", "about_equal", "cannot_judge"],
                        "items": items}, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"data/labeling_set_{mode}.json: {len(items)} items")


if __name__ == "__main__":
    main()
