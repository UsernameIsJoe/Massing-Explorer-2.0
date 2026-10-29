"""Move check inputs: key-move texts and case-level idea texts for the 15 seeds, each with a
label-free decision signature.

Signature items:
  placement  (department, mass role L/C/X, level class)   L = core academic's mass, C = gym's mass
  link       (role pair, linked / not linked)
Case signature = all placements and links of the record; move signature = the decisions it references.

Usage (from repo root):  python grounding/move_check/build_texts.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]


def level(f):
    return "ground only" if f == [1] else ("ground and upper" if 1 in f else "upper only")


def main():
    texts = []
    for run, f in RUNS:
        for c in json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases" / f).read_text(encoding="utf-8"))["cases"]:
            s = c["structure"]
            own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
            fl = {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]}
            L, C = own["D01"], own["D04"]
            role = {m["mass_id"]: ("L" if m["mass_id"] == L else "C" if m["mass_id"] == C else "X") for m in s["masses"]}
            pl = lambda d: ["P", d, role[own[d]], level(fl[d])]
            lk = lambda a, b, v: ["K", "".join(sorted(role[a] + role[b])), "linked" if v else "not linked"]
            case_sig = [pl(d) for d in sorted(own)] + [lk(x["mass_a"], x["mass_b"], x["direct_link"]) for x in s["connections"]]
            cid = f"{run}-{c['case_id']}"
            texts.append({"text_id": f"{cid}::idea", "case": cid, "kind": "idea", "text": f"{c['concept']} {c['intent']}", "sig": case_sig})
            for k in c["key_moves"]:
                sig = [pl(x["department_id"]) if x["type"] == "placement" else lk(x["mass_a"], x["mass_b"], x["direct_link"]) for x in k["decisions"]]
                texts.append({"text_id": f"{cid}::{k['move_id']}", "case": cid, "kind": "move", "text": f"{k['move']}: {k['serves']}", "sig": sig})
    (Path(__file__).parent / "texts.json").write_text(json.dumps(texts, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(texts), "texts:", sum(t["kind"] == "move" for t in texts), "moves,", sum(t["kind"] == "idea" for t in texts), "ideas")


if __name__ == "__main__":
    main()
