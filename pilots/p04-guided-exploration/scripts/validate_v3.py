"""Validate a format v3 reply (OUTPUT_FORMAT_v3.md). Reuses the v2 checks (without the
commitments module) and adds the v3 rules. Invalid cases are reported, never repaired.

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/validate_v3.py <reply.json or .txt>
Writes <reply>.validation.json next to the input.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "benchmarks/test-elementary-v0.1/seeds_v2/scripts"))
from validate_seeds import check_case, words  # noqa: E402

V3_WORDS = {"section_intent": (20, 40), "program_stance": (20, 40)}


def parse(text):
    t = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    return json.loads(t)


def check_v3(c):
    E, W, derived = check_case(c, use_commitments=False)
    for f, (lo, hi) in V3_WORDS.items():
        n = words(c.get(f))
        if n == 0:
            E.append(f"{f} missing")
        elif not lo <= n <= hi:
            W.append(f"{f} has {n} words (expected {lo}-{hi})")
    if not (c.get("direction_response") or "").strip():
        E.append("direction_response missing")
    if "commitments" in c:
        W.append("commitments module present (removed in v3)")
    s = c.get("structure") or {}
    owner = {d.get("department_id"): (d.get("mass_ids") or [None])[0] for d in s.get("departments", [])}
    floors = {d.get("department_id"): sorted(d.get("occupied_floors") or []) for d in s.get("departments", [])}
    if owner.get("D01") and owner.get("D01") == owner.get("D04"):
        E.append("core academic and gym/dining share a mass")
    for m in s.get("masses", []):
        mid = m.get("mass_id")
        held = [d for d, o in owner.items() if o == mid]
        if not held:
            E.append(f"mass {mid} holds no department")
            continue
        if held == ["D09"]:
            E.append(f"mass {mid} holds only custodial")
        occ = set()
        for d in held:
            occ |= set(floors.get(d) or [])
            if d in ("D04", "D06") and floors.get(d) == [1]:
                occ.add(2)
        if occ and sorted(occ) != list(range(1, max(occ) + 1)):
            E.append(f"mass {mid} does not stand from the ground: occupied floors {sorted(occ)}")
    return E, W, derived


def main(path):
    p = Path(path)
    report = {"file": p.name, "parse_error": None, "collection_errors": [], "cases": []}
    try:
        data = parse(p.read_text(encoding="utf-8"))
    except Exception as e:
        report["parse_error"] = str(e)
        data = {}
    if data:
        try:
            import jsonschema
            schema = json.loads((Path(__file__).resolve().parents[1] / "generation_inputs/case.schema.v3.json").read_text(encoding="utf-8"))
            for err in jsonschema.Draft202012Validator(schema).iter_errors(data):
                report["collection_errors"].append(f"schema: {err.message[:160]} at {list(err.absolute_path)}")
        except ImportError:
            report["collection_errors"].append("schema not checked (jsonschema not installed)")
        if data.get("format") != "v3":
            report["collection_errors"].append("format is not 'v3'")
        cases = data.get("cases") or []
        if len(cases) != 5:
            report["collection_errors"].append(f"{len(cases)} cases (expected 5)")
        ids = [c.get("case_id") for c in cases]
        if ids != [f"C0{i}" for i in range(1, len(cases) + 1)]:
            report["collection_errors"].append(f"case ids {ids} (expected C01..)")
        for c in cases:
            E, W, derived = check_v3(c)
            report["cases"].append({"case_id": c.get("case_id"), "name": c.get("name"), "valid": not E,
                                    "errors": E, "warnings": W, "derived_preferences_given_up": derived})
    p.with_suffix(".validation.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}))
    for c in report["cases"]:
        print(c["case_id"], "VALID" if c["valid"] else "INVALID", "|", "; ".join(c["errors"] + c["warnings"])[:200])


if __name__ == "__main__":
    main(sys.argv[1])
