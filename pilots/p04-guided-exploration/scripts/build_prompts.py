"""Build the 8 Pilot 4 prompts (4 arms x 2 chats) from one template; only the direction block
differs. Run order is shuffled with a fixed seed; prompt files are named by run order (P1-P8),
so the arm is not visible to the person running them. The key is sealed in data/.

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/build_prompts.py
"""
import hashlib
import json
import random
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
SEED = 20261029
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
ATTACH = ["MODEL_INPUT.md", "ROOM_PROGRAM.csv", "CASE_FORMAT_v3.md", "case.schema.v3.json"]

COMMON_HEAD = """[Strategy generation v3.1. Each attachment listed below is embedded verbatim after this instruction, between BEGIN/END ATTACHMENT markers; treat each embedded block as that attachment.]

Attachments: MODEL_INPUT.md, ROOM_PROGRAM.csv, CASE_FORMAT_v3.md, case.schema.v3.json.

Use only these supplied inputs and this instruction. Do not browse, run code or request external tools.

You are proposing new architectural strategies for the supplied elementary school brief. Each strategy starts from an organizing idea; develop the idea first, then make the program, floor and connection decisions that implement it.

## Existing cases

These strategies already exist. Their names and concepts are listed so that you know what has been proposed.

{archive}

## Your task

{task}

## Rules for every case

- The hard rules in CASE_FORMAT_v3.md apply without exception. If a direction cannot be met without breaking a hard rule, keep the hard rule, follow the direction as far as possible, and say so in `direction_response` and `unresolved`.
- Coherence matters more than novelty. Within each case, every field must describe the same scheme. Before returning, check every case and fix it if any item fails:
  1. Every key move's decisions match the structure exactly.
  2. The concept does not state a relationship the structure contradicts.
  3. `section_intent` matches the structure's floors: which masses rise, and what sits at grade and at the top.
  4. `program_stance` matches where core academic, special education, administration and the commons actually sit.
  5. The intent follows from the concept and is not a generic benefit any scheme could claim.
  6. `preferences_given_up` matches what the structure does.
  7. The concept does not list departments by mass or floor.
  8. Every mass is occupied from the ground up, with no empty floor between occupied floors; gym and dining are written as floor [1].
  9. No null values anywhere in `structure`.
- Stay at strategy level: no dimensions, areas by mass, geometry or scores. Preserve the given program. Do not invent site geometry or access.

Return only one JSON object conforming to CASE_FORMAT_v3.md and case.schema.v3.json, with case IDs C01 to C05."""

TASK = {
    "U": "Propose exactly 5 new strategies. Each must differ from all the existing cases and from the other four, in its organizing idea and in the consequential commitments that follow from it, not only in names, wording or renumbered masses. In `direction_response`, say in one sentence how the case differs from the existing cases.",
    "guided": "Propose exactly 5 new strategies, one per direction below, in order: C01 answers direction 1, C02 direction 2, and so on. {kind} Each case must also differ from all the existing cases, not only in names or wording.\n\n{dirs}",
    "A": "Each direction describes where a strategy's organization should end up, not the idea itself. Find a meaningful architectural idea that leads there; the arrangement must follow from the idea, not be forced to fit.",
    "S": "Each direction points to a region of ideas. Interpret it architecturally and propose a coherent strategy.",
    "J": "Each direction describes where a strategy's organization should end up, together with existing ideas to stay clear of and one whose intent you may borrow. Find a meaningful architectural idea that leads there; the arrangement must follow from the idea, not be forced to fit.",
}


def main():
    cases = {}
    for run, f in RUNS:
        for c in json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases" / f).read_text(encoding="utf-8"))["cases"]:
            cases[f"{run}-{c['case_id']}"] = c
    rng = random.Random(SEED)
    order = sorted(cases)
    rng.shuffle(order)
    eid = {k: f"E{i + 1:02d}" for i, k in enumerate(order)}
    ref = lambda k: f"{eid[k]} \"{cases[k]['name']}\""
    archive = "\n".join(f"- {eid[k]} \"{cases[k]['name']}\": {cases[k]['concept']}" for k in order)

    d = json.loads((HERE / "data/directions.json").read_text(encoding="utf-8"))
    A = [g["words"] for g in d["A"]]
    S = []
    for s in d["S"]:
        if s["type"] == "away":
            S.append(("away", f"An idea unlike all of these existing cases: {', '.join(ref(k) for k in s['seeds'])}. It must not be a variation of any of them."))
        elif s["type"] == "bridge":
            S.append(("bridge", f"An idea that combines the intent of {ref(s['intent_of'])} with the organization of {ref(s['organization_of'])}, reinterpreted as a new strategy rather than a mix of the two."))
        else:
            S.append(("develop", f"A different idea in the spirit of {ref(s['seed'])}; not a variation of it."))
    by = {t: [x for x in S if x[0] == t] for t in ("away", "bridge", "develop")}
    S_order = [by["away"][0], by["bridge"][0], by["develop"][0], by["away"][1], by["bridge"][1],
               by["away"][2], by["develop"][1], by["away"][3], by["bridge"][2], by["develop"][2]]
    S_txt = [x[1] for x in S_order]
    J_txt = [f"An organization that ends up with {j['words']}. Existing cases closest in meaning: {ref(j['do_not_rephrase'][0])} and {ref(j['do_not_rephrase'][1])}; do not rephrase them. You may borrow the intent of {ref(j['may_borrow_intent_of'])}." for j in d["J"]]
    A_txt = [f"An organization that ends up with {w}." for w in A]

    attach = "\n\n".join(f"===== BEGIN ATTACHMENT: {n} =====\n{(HERE / 'generation_inputs' / n).read_text(encoding='utf-8').strip()}\n===== END ATTACHMENT: {n} =====" for n in ATTACH)
    prompts = []
    for arm in ("U", "A", "S", "J"):
        for chat in (1, 2):
            if arm == "U":
                task, dirs = TASK["U"], None
            else:
                dirs = {"A": A_txt, "S": S_txt, "J": J_txt}[arm][(chat - 1) * 5: chat * 5]
                task = TASK["guided"].format(kind=TASK[arm], dirs="\n".join(f"{i + 1}. {t}" for i, t in enumerate(dirs)))
            text = COMMON_HEAD.format(archive=archive, task=task) + "\n\n" + attach + "\n"
            prompts.append({"arm": arm, "chat": chat, "directions": dirs, "text": text})
    rng.shuffle(prompts)
    key = {"seed": SEED, "archive_ids": eid, "prompts": []}
    for i, p in enumerate(prompts, 1):
        name = f"P{i}.txt"
        (HERE / "prompts" / name).write_text(p["text"], encoding="utf-8")
        key["prompts"].append({"file": name, "arm": p["arm"], "chat": p["chat"], "directions": p["directions"],
                               "sha256": hashlib.sha256(p["text"].encode("utf-8")).hexdigest(), "words": len(p["text"].split())})
    (HERE / "data/prompt_key_SEALED.json").write_text(json.dumps(key, indent=1, ensure_ascii=False), encoding="utf-8")
    for p in key["prompts"]:
        print(p["file"], p["words"], "words")


if __name__ == "__main__":
    main()
