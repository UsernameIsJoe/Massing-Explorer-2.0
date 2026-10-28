"""Render Pilot 01 descriptions from the 15 frozen seed-scope case records.

Deterministic: no LLM, no added meaning. Every output sentence is either
rendered from structured fields (department/mass/floor/link) or copied
verbatim from the record's own text fields, and each text carries source keys.

Usage:
    python render_descriptions.py <all_15_cases.json> <output_dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

TEMPLATE_VERSION = "p01-desc-v1"

DEPT = {
    "D01": "core academic",
    "D02": "special education",
    "D03": "art and music",
    "D04": "physical education (gym)",
    "D05": "media center",
    "D06": "dining and food service",
    "D07": "medical",
    "D08": "administration and guidance",
    "D09": "custodial and maintenance",
}

COLLECTION_PREFIX = {"parents_05": "05", "additions_A": "A", "additions_B": "B"}

# Aspect keyword lists select whole source sentences verbatim; they never rewrite.
ASPECTS = {
    "inclusion": {
        "depts": ["D01", "D02"],
        "keywords": ["special education", "inclusion", "inclusive", "grade-level", "peers", "classmates"],
    },
    "civic_access": {
        "depts": ["D08", "D07", "D04", "D06"],
        "keywords": ["after-hours", "after hours", "entry", "front", "community", "event", "civic",
                     "supervision", "door", "visitors"],
    },
    "service": {
        "depts": ["D09", "D06"],
        "keywords": ["custodial", "kitchen", "receiving", "service"],
    },
}


def floors(fl):
    fl = sorted(fl)
    if len(fl) == 1:
        return f"floor {fl[0]}"
    if fl == list(range(fl[0], fl[-1] + 1)):
        return f"floors {fl[0]}-{fl[-1]}"
    return "floors " + ", ".join(map(str, fl))


def mass_roles(case):
    """Neutral, content-derived mass names (mass IDs are arbitrary per case)."""
    owner = {d["department_id"]: d["mass_ids"][0] for d in case["departments"]}
    roles = {owner["D01"]: "the classroom mass", owner["D04"]: "the commons mass"}
    if owner["D06"] != owner["D04"]:
        raise ValueError(f"{case['case_id']}: gym and dining in different masses")
    if len(roles) != 2:
        raise ValueError(f"{case['case_id']}: classrooms share the commons mass")
    for m in case["masses"]:
        roles.setdefault(m["mass_id"], "the third mass")
    if len(case["masses"]) != 3:
        raise ValueError(f"{case['case_id']}: expected 3 masses")
    return roles, owner


def structure_sentences(case, depts=None):
    roles, owner = mass_roles(case)
    order = ["the classroom mass", "the commons mass", "the third mass"]
    by_mass = {}
    for d in case["departments"]:
        if depts and d["department_id"] not in depts:
            continue
        by_mass.setdefault(roles[d["mass_ids"][0]], []).append(
            f"{DEPT[d['department_id']]} on {floors(d['occupied_floors'])}")
    out = []
    for r in order:
        if r in by_mass:
            out.append(f"{r[0].upper() + r[1:]} holds " + "; ".join(by_mass[r]) + ".")
    links = []
    for c in case["connections"]:
        a, b = sorted([roles[c["mass_a"]], roles[c["mass_b"]]], key=order.index)
        links.append((a, b, c["direct_link"]))
    if depts is None:
        linked = [f"{a} and {b}" for a, b, ok in links if ok]
        unlinked = [f"{a} and {b}" for a, b, ok in links if not ok]
        if linked:
            out.append("Direct links join " + "; ".join(linked) + ".")
        if unlinked:
            out.append("There is no direct link between " + "; ".join(unlinked) + ".")
    else:
        # Aspect view: links touching masses that hold the aspect's departments.
        involved = set(by_mass)
        rel = [(a, b, ok) for a, b, ok in links if a in involved or b in involved]
        for a, b, ok in rel:
            out.append(f"{a[0].upper() + a[1:]} and {b} are {'directly linked' if ok else 'not directly linked'}.")
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def source_sentences(case):
    """(field, sentence) pairs from the record's own text, verbatim."""
    out = [("organizing_principle", s) for s in sentences(case["organizing_principle"])]
    out += [("main_tradeoff", s) for s in sentences(case["main_tradeoff"])]
    for i, n in enumerate(case["unresolved_notes"]):
        out += [(f"unresolved_notes[{i}]", s) for s in sentences(n)]
    return out


def render(rec):
    case = rec["case"]
    cid = f"{COLLECTION_PREFIX[rec['collection']]}-{case['case_id']}"
    struct = structure_sentences(case)
    intent = sentences(case["organizing_principle"]) + sentences(case["main_tradeoff"])
    full = ([case["name"] + "."] + sentences(case["organizing_principle"]) + struct
            + sentences(case["main_tradeoff"])
            + ["Unresolved: " + " ".join(case["unresolved_notes"])])
    items = [
        ("struct", struct, ["departments", "connections"]),
        ("intent", intent, ["organizing_principle", "main_tradeoff"]),
        ("full", full, ["name", "organizing_principle", "departments", "connections",
                        "main_tradeoff", "unresolved_notes"]),
    ]
    src = source_sentences(case)
    for asp, spec in ASPECTS.items():
        picked = [(f, s) for f, s in src if any(k in s.lower() for k in spec["keywords"])]
        text = structure_sentences(case, spec["depts"]) + [s for _, s in picked]
        items.append((f"aspect_{asp}", text,
                      ["departments", "connections"] + sorted({f for f, _ in picked})))
    rows = []
    for variant, sents, keys in items:
        text = " ".join(sents)
        rows.append({
            "text_id": f"{cid}::{variant}",
            "case_id": cid,
            "collection": rec["collection"],
            "variant": variant,
            "template_version": TEMPLATE_VERSION,
            "source_fields": keys,
            "text": text,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })
    return rows


def main(src, outdir):
    src, outdir = Path(src), Path(outdir)
    data = json.loads(src.read_text(encoding="utf-8"))
    rows = [r for rec in data["records"] for r in render(rec)]
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "descriptions.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {
        "template_version": TEMPLATE_VERSION,
        "source_file": src.name,
        "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "texts": len(rows),
        "cases": len(data["records"]),
        "variants": sorted({r["variant"] for r in rows}),
    }
    (outdir / "descriptions_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
