"""Attach outside-model concepts to region v1 and check them against the prompt rules.

Usage (from pilots/p03-expansion):
    python scripts/attach_concepts.py responses/raw/describe_expansions_chatgpt.txt
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TERMS = {"core academic": r"core academic|academic|learning block|instruction|teaching",
         "special education": r"special(ized)? (learning|instruction|education)",
         "art and music": r"creative|arts?\b|music",
         "gym/dining": r"communal|shared[- ]activity|dining|gym",
         "media center": r"media center",
         "administration": r"administrat|institutional|civic",
         "medical": r"\bcare\b|medical|health",
         "custodial": r"service|support|custodial"}


def main(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    key = json.loads((HERE / "data/concept_key_SEALED.json").read_text(encoding="utf-8"))
    sealed = {it["expansion_id"]: it for it in json.loads((HERE / "data/expansion_SEALED.json").read_text(encoding="utf-8"))["items"]}
    region_p = HERE / "region/region_v1.json"
    region = json.loads(region_p.read_text(encoding="utf-8"))
    by_group = {g["group"]: g for g in region["expansion_groups"]}
    out, checks = {}, []
    for nid, eid in key.items():
        text = raw[nid].strip()
        words = len(text.split())
        named = [t for t, rx in TERMS.items() if re.search(rx, text, re.I)]
        g = sealed[eid]["group"]
        out[eid] = {"concept": text, "prompt_id": nid, "group": g}
        by_group[g]["concept"] = text
        by_group[g]["concept_source"] = "ChatGPT temporary chat, prompts/DESCRIBE_EXPANSIONS.txt"
        checks.append({"expansion_id": eid, "words": words, "program_groups_named": len(named), "named": named})
    (HERE / "responses/describe_expansions.json").write_text(json.dumps({"concepts": out, "checks": checks}, indent=1), encoding="utf-8")
    region_p.write_text(json.dumps(region, indent=1), encoding="utf-8")
    for c in checks:
        print(c["expansion_id"], c["words"], c["program_groups_named"], ",".join(c["named"]))
    print("in 35-70 words:", sum(35 <= c["words"] <= 70 for c in checks), "/", len(checks))
    print("<= 3 program groups:", sum(c["program_groups_named"] <= 3 for c in checks), "/", len(checks))


if __name__ == "__main__":
    main(sys.argv[1])
