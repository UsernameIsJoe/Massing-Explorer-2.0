"""Pilot 4 scoring, step 1 (container): build the inputs for the local run, blind to arm.

Writes scoring/local/ (copied to the architect's PC; standard library only):
  texts.json   every text to embed, with three encoders (mxbai, nomic: measurement; bge-m3: manipulation check)
                 archive  15 seeds: idea (concept + intent), concept
                 cases    40 replies: idea, concept, intent, each move (move + serves), each unresolved item
                 p01c     Pilot 01c originals and rewrites, re-embedded in the same run for the paraphrase threshold
  items.json   extraction items for the text-record agreement check (llama3.1:8b, as in Experiment 1)
                 v3text   concept + section_intent + program_stance (what format v3 adds for extraction)
                 idea     concept + intent (the Experiment 1 text, for comparison)
Cases get random IDs Q01-Q40 here; the map back to reply/case is data/blind_map.json. The arm key
(data/prompt_key_SEALED.json) is not read by this step.

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/build_scoring.py
"""
import hashlib
import json
import random
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
sys.path.insert(0, str(REPO / "grounding/exp1"))
import validate_v3  # noqa: E402
from build_inputs import LEVELED, PLACED, truth  # noqa: E402

SEED = 20261030
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
OUT = HERE / "scoring/local"


def normalized(structure):
    """Gym and dining written [1, 2] count as [1] (the double height spans floors 1-2)."""
    s = json.loads(json.dumps(structure))
    for d in s["departments"]:
        if d["department_id"] in ("D04", "D06") and d["occupied_floors"] == [1, 2]:
            d["occupied_floors"] = [1]
    return s


def load_replies():
    cases = []
    for n in range(1, 9):
        d = validate_v3.parse((HERE / f"replies/clean/R{n}.json").read_text(encoding="utf-8"))
        val = json.loads((HERE / f"replies/clean/R{n}.validation.json").read_text(encoding="utf-8"))
        vmap = {v["case_id"]: v for v in val["cases"]}
        for c in d["cases"]:
            cases.append({"reply": f"R{n}", "case_id": c["case_id"], "case": c, "validation": vmap[c["case_id"]]})
    return cases


def main():
    cases = load_replies()
    assert len(cases) == 40, len(cases)
    ids = [f"Q{i + 1:02d}" for i in range(40)]
    rng = random.Random(SEED)
    rng.shuffle(ids)
    blind = {q: {"reply": c["reply"], "case_id": c["case_id"]} for q, c in zip(ids, cases)}

    texts = []
    add = lambda tid, t: texts.append({"text_id": tid, "text": t})
    for run, f in RUNS:
        for c in json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases" / f).read_text(encoding="utf-8"))["cases"]:
            k = f"{run}-{c['case_id']}"
            add(f"archive:{k}::idea", f"{c['concept']} {c['intent']}")
            add(f"archive:{k}::concept", c["concept"])
    items = []
    for q, c in sorted(zip(ids, cases)):
        x = c["case"]
        add(f"case:{q}::idea", f"{x['concept']} {x['intent']}")
        add(f"case:{q}::concept", x["concept"])
        add(f"case:{q}::intent", x["intent"])
        for m in x["key_moves"]:
            add(f"case:{q}::move::{m['move_id']}", f"{m['move']}. {m['serves']}")
        for i, u in enumerate(x["unresolved"], 1):
            add(f"case:{q}::unresolved::{i}", u)
        t = truth(normalized(x["structure"]))
        items.append({"id": f"{q}::v3text", "text": f"{x['concept']} {x['section_intent']} {x['program_stance']}", "truth": t})
        items.append({"id": f"{q}::idea", "text": f"{x['concept']} {x['intent']}", "truth": t})
    for line in (REPO / "pilots/p01c-robustness/data/descriptions.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["text_id"].endswith(("::original", "::rewrite")):
            add(f"p01c:{r['text_id']}", r["text"])

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "texts.json").write_text(json.dumps(texts, indent=0, ensure_ascii=False), encoding="utf-8")
    (OUT / "items.json").write_text(json.dumps({"questions": {"place": PLACED, "level": LEVELED}, "items": items}, indent=0, ensure_ascii=False), encoding="utf-8")
    (HERE / "data/blind_map.json").write_text(json.dumps(blind, indent=1), encoding="utf-8")
    h = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT / "texts.json", OUT / "items.json")}
    (HERE / "data/scoring_inputs_lock.json").write_text(json.dumps(h, indent=1), encoding="utf-8")
    print(f"{len(texts)} texts, {len(items)} extraction items -> {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
