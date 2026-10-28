"""Build data/probe_review.json for the probe check (protocol p01-v1.2).

Probes are not blind-labeled. The labeler reviews each probe's construction:
the intended answer and the reason it was built that way. Only probes the
labeler agrees with are used to score encoders. Repeats of probes are skipped.

Usage (from pilots/p01-representation):
    python scripts/build_probe_review.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

REASONS = {
    ("paraphrase", None): "Same organization and intentions as the anchor, in different words. The other option is a different real scheme.",
    ("lexical_trap", "05-S01"): "Reuses the anchor's words but makes the commons, not the civic hub, the mass every route passes through.",
    ("lexical_trap", "05-S04"): "Reuses the anchor's words but attaches the pavilions, reversing the detached-campus idea and its trade-off.",
    ("lexical_trap", "A-E04"): "Reuses the anchor's words but puts special education at grade beside classrooms and moves the arts up, reversing the anchor's main trade-off.",
    ("lexical_trap", "B-E05"): "Reuses the anchor's words but moves media out of the learning bar to sit above administration, the opposite of the anchor's library-heart move.",
    ("generic", None): "The generic text commits to no strategy, so the real scheme is closer.",
    ("intent_vs_wording", "P-INC-ANCHOR"): "Same intention (special education among grade-level classrooms) on a different floor. The other uses similar words but separates special education into a support wing.",
    ("intent_vs_wording", "P-CIV-ANCHOR"): "Same intention (community use while classrooms stay closed off) by a different arrangement. The other uses similar words but loses that separation.",
    ("intent_vs_wording", "P-SRV-ANCHOR"): "Same intention (service reaches the kitchen without crossing students) by a service yard. The other uses similar words but routes service across the student link.",
}


def main():
    sealed = json.loads((HERE / "data" / "triplets_SEALED.json").read_text(encoding="utf-8"))
    blind = {i["triplet_id"]: i for i in json.loads((HERE / "data" / "labeling_set.json").read_text(encoding="utf-8"))["items"]}
    rows = []
    for t in sealed["triplets"]:
        if t["kind"].startswith("real") or "repeat_of" in t:
            continue
        reason = REASONS.get((t["kind"], t["anchor"])) or REASONS[(t["kind"], None)]
        b = blind[t["triplet_id"]]
        rows.append({
            "triplet_id": t["triplet_id"],
            "kind": t["kind"],
            "anchor": b["anchor"]["text"],
            "option_1": b["option_1"]["text"],
            "option_2": b["option_2"]["text"],
            "intended": "option_1" if t["shown_order"][0] == t["construction_expectation"] else "option_2",
            "reason": reason,
        })
    (HERE / "data" / "probe_review.json").write_text(json.dumps({"items": rows}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} probes -> data/probe_review.json")


if __name__ == "__main__":
    main()
