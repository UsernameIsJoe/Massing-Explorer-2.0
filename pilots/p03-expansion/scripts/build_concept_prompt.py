"""Build the prompt asking an outside model (ChatGPT, temporary chat) to write a
concept for each added or maybe expansion representative.

Usage (from pilots/p03-expansion):
    python scripts/build_concept_prompt.py
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
NAME = {"D01": "core academic", "D02": "special education", "D03": "art and music", "D04": "physical education (gym)",
        "D05": "media center", "D06": "dining and food service", "D07": "medical", "D08": "administration and guidance",
        "D09": "custodial and maintenance"}
DEPTS = list(NAME)


def describe(st, letters):
    lines = []
    for m in st["slots"]:
        items = []
        for d in DEPTS:
            if st["own"][d] == m:
                f = st["floors"][d]
                items.append(f"{NAME[d]} (floor {f[0]})" if len(f) == 1 else f"{NAME[d]} (floors {f[0]}-{f[-1]})")
        lines.append(f"Mass {letters[m]}: " + "; ".join(items))
    for p, ok in sorted(st["links"].items()):
        a, b = p.split("-")
        lines.append(f"Mass {letters[a]} and Mass {letters[b]}: {'directly linked' if ok else 'not directly linked'}")
    return "\n".join(lines)


def main():
    sealed = json.loads((HERE / "data/expansion_SEALED.json").read_text(encoding="utf-8"))["items"]
    dec = {k: v["answer"] for k, v in json.loads((HERE / "labels/user_expansion.json").read_text(encoding="utf-8")).items()}
    keep = [it for it in sealed if dec[it["expansion_id"]] in ("add", "maybe")]
    rng = random.Random(20261101)
    rng.shuffle(keep)
    blocks, key = [], {}
    for i, it in enumerate(keep, 1):
        nid = f"N{i:02d}"
        key[nid] = it["expansion_id"]
        letters = dict(zip(it["state"]["slots"], rng.sample("ABC", 3)))
        blocks.append(f"{nid}\n{describe(it['state'], letters)}")
    (HERE / "prompts").mkdir(exist_ok=True)
    (HERE / "prompts/DESCRIBE_EXPANSIONS.txt").write_text(f"""You are an architect. Below are {len(keep)} strategy-level arrangements for the same three-mass elementary school. Each lists which departments sit in which mass (Mass A, B and C are arbitrary labels), on which floors (ground = 1), and which masses are directly linked. Gym and dining always share a double-height volume.

For each arrangement, write its concept: the organizing spatial idea a designer would sketch first.

Rules:
- 35-70 words.
- Describe the roles the parts play and how they relate (for example a civic front, a learning wing, a shared heart, a support house, detached pavilions; centralized, linear, clustered, stacked, layered).
- Name at most THREE departments or program groups, and only where they carry the idea. Do not list what is in each mass or on each floor.
- Do not restate requirements every scheme shares (for example that gym and dining are together and double height).
- Do not argue benefits or quality. Call the media center the media center.
- Describe each arrangement on its own; do not compare or refer to other IDs.

Return JSON only, in exactly this shape, one entry per ID:
{{"N01": "concept", "N02": "concept"}}

""" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    (HERE / "data/concept_key_SEALED.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print(len(keep), "arrangements in prompts/DESCRIBE_EXPANSIONS.txt")


if __name__ == "__main__":
    main()
