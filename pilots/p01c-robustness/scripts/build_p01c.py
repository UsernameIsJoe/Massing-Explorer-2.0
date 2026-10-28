"""Build Pilot 01c robustness tasks for an outside model (ChatGPT, fresh chats).

Deterministic. Writes:
  prompts/1_REWRITE.txt   rewrite the 15 v2.0 concepts in different words (opaque IDs, shuffled)
  prompts/2_DESCRIBE.txt  write a concept for 35 anonymous structures: 5 run-01 bases + 30 edited variants
  prompts/3_JUDGE.txt     rate the 16 Pilot 01b Pass B items (send to two separate fresh chats)
  data/rewrite_key_SEALED.json   opaque ID -> case ID
  data/variants_SEALED.json      opaque ID -> base, edit count, edits, structure

Edits on a base structure (strategy level, no dimensions):
  move  one department (not core academic, gym or dining) to another mass, keeping its floors
  link  flip one mass-to-mass direct link
A variant at level k has k distinct edits. Two variants per level 1, 2, 3 for each base.

Usage (from pilots/p01c-robustness):
    python scripts/build_p01c.py
"""
import copy
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
SEEDS = REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases"
P01B = REPO / "pilots/p01b-concept/data/labeling_set_full.json"
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
SEED = 20261029
NAME = {"D01": "core academic", "D02": "special education", "D03": "art and music", "D04": "physical education (gym)",
        "D05": "media center", "D06": "dining and food service", "D07": "medical", "D08": "administration and guidance",
        "D09": "custodial and maintenance"}
MOVABLE = ["D02", "D03", "D05", "D07", "D08", "D09"]

CONCEPT_RULES = """Concept rules (same as the original seed format):
- 35-70 words describing the organizing spatial idea a designer would sketch first: the roles the parts play and how they relate (centralized, linear, clustered, stacked, layered, detached and so on).
- You may name program groups when they carry the idea. Do not list departments by mass or floor.
- Do not restate requirements every scheme shares (for example that gym and dining are together and double height).
- Do not argue benefits or quality.
- Call the media center the media center."""


def structure_of(case):
    s = case["structure"]
    return {"departments": {d["department_id"]: {"mass": d["mass_ids"][0], "floors": d["occupied_floors"]} for d in s["departments"]},
            "links": {"-".join(sorted((c["mass_a"], c["mass_b"]))): c["direct_link"] for c in s["connections"]},
            "masses": [m["mass_id"] for m in s["masses"]]}


def describe(st, letters):
    lines = []
    for m in st["masses"]:
        items = [f"{NAME[d]} (floor{'s' if len(v['floors']) > 1 else ''} {'-'.join(map(str, [v['floors'][0], v['floors'][-1]])) if len(v['floors']) > 1 else v['floors'][0]})"
                 for d, v in sorted(st["departments"].items()) if v["mass"] == m]
        lines.append(f"Mass {letters[m]}: " + "; ".join(items))
    for pair, ok in sorted(st["links"].items()):
        a, b = pair.split("-")
        lines.append(f"Mass {letters[a]} and Mass {letters[b]}: {'directly linked' if ok else 'not directly linked'}")
    return "\n".join(lines)


def edit(st, k, rng):
    for _ in range(500):
        v = copy.deepcopy(st)
        ops, used = [], set()
        for _ in range(k):
            if rng.random() < 0.6:
                d = rng.choice([x for x in MOVABLE if x not in used])
                src = v["departments"][d]["mass"]
                others = [m for m in v["masses"] if m != src]
                dst = rng.choice(others)
                v["departments"][d]["mass"] = dst
                used.add(d)
                ops.append({"op": "move", "department": d, "from": src, "to": dst})
            else:
                pair = rng.choice([p for p in v["links"] if p not in used])
                v["links"][pair] = not v["links"][pair]
                used.add(pair)
                ops.append({"op": "link", "pair": pair, "now": v["links"][pair]})
        nonempty = all(any(x["mass"] == m for x in v["departments"].values()) for m in v["masses"])
        if nonempty and v != st:
            return v, ops
    raise RuntimeError("could not build a valid variant")


def main():
    rng = random.Random(SEED)
    cases = {}
    for run, f in RUNS:
        for c in json.loads((SEEDS / f).read_text(encoding="utf-8"))["cases"]:
            cases[f"{run}-{c['case_id']}"] = c
    (HERE / "prompts").mkdir(exist_ok=True)
    (HERE / "data").mkdir(exist_ok=True)

    # 1. Rewrite
    ids = sorted(cases)
    rng.shuffle(ids)
    key = {f"P{i:02d}": cid for i, cid in enumerate(ids, 1)}
    body = "\n".join(f"{pid}: {cases[cid]['concept']}" for pid, cid in key.items())
    (HERE / "prompts/1_REWRITE.txt").write_text(f"""You are an architect. Below are 15 short concept statements for different strategies for the same three-mass elementary school. Rewrite each one so that it describes exactly the same organizing idea, the same roles and the same relationships between the parts, but in completely different words.

Rules:
- Keep the meaning. Do not add, remove or change any relationship, role or placement the original implies.
- Avoid the original's distinctive words and phrases (for example, if it says "hinge", "heart", "bar", "loop", "pavilion" or "crown", find other ways to say it). Ordinary words like "school", "the" or "and" are fine.
- 35-70 words each.
- Judge each one on its own; do not compare them.

Return JSON only, in exactly this shape, one entry per ID:
{{"P01": "rewritten concept", "P02": "rewritten concept"}}

{body}
""", encoding="utf-8")
    (HERE / "data/rewrite_key_SEALED.json").write_text(json.dumps(key, indent=1), encoding="utf-8")

    # 2. Describe
    entries = []
    for cid in [f"R1-S0{i}" for i in range(1, 6)]:
        base = structure_of(cases[cid])
        entries.append({"base": cid, "level": 0, "edits": [], "structure": base})
        for k in (1, 2, 3):
            seen = []
            while len(seen) < 2:
                v, ops = edit(base, k, rng)
                if v not in seen:
                    seen.append(v)
                    entries.append({"base": cid, "level": k, "edits": ops, "structure": v})
    rng.shuffle(entries)
    blocks, sealed = [], {}
    for i, e in enumerate(entries, 1):
        vid = f"V{i:02d}"
        letters = dict(zip(e["structure"]["masses"], rng.sample("ABC", 3)))
        e["letters"] = letters
        sealed[vid] = e
        blocks.append(f"{vid}\n{describe(e['structure'], letters)}")
    (HERE / "prompts/2_DESCRIBE.txt").write_text(f"""You are an architect. Below are 35 strategy-level arrangements for the same three-mass elementary school. Each lists which departments sit in which mass (Mass A, B and C are arbitrary labels), on which floors (ground = 1), and which masses are directly linked. Gym and dining always share a double-height volume.

For each arrangement, write the concept: the organizing idea it expresses.

{CONCEPT_RULES}
- Describe each arrangement on its own; do not compare arrangements or refer to other IDs.

Return JSON only, in exactly this shape, one entry per ID:
{{"V01": "concept", "V02": "concept"}}

""" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    (HERE / "data/variants_SEALED.json").write_text(json.dumps(sealed, indent=1), encoding="utf-8")

    # 3. Judge
    items = json.loads(P01B.read_text(encoding="utf-8"))
    (HERE / "prompts/3_JUDGE.txt").write_text("""You are an experienced school architect. The JSON below contains 16 items. Each has an anchor scheme and two option schemes for a three-mass elementary school on one brief. Each scheme has a concept, an intent, key moves with the structural decisions they consist of, a trade-off, commitments, and a structure line listing which departments sit in which mass, on which floors, and which masses are directly linked.

For each item, judge which option is the closer architectural strategy to the anchor, judging the whole scheme: program organization, relationships between parts, and strategic intentions. Do not judge by wording overlap or writing style. Judge each item independently.

Return JSON only, in exactly this shape, one entry per item, keyed by triplet_id:
{"C01": {"answer": "option_1"}, "C05": {"answer": "about_equal"}}
Allowed answers: option_1, option_2, about_equal, cannot_judge. Include all 16 triplet_ids. No explanations.

""" + json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    for f in ("1_REWRITE.txt", "2_DESCRIBE.txt", "3_JUDGE.txt"):
        t = (HERE / "prompts" / f).read_text(encoding="utf-8")
        print(f, len(t.split()), "words")
    print("variants by level:", {k: sum(1 for e in entries if e["level"] == k) for k in range(4)})


if __name__ == "__main__":
    main()
