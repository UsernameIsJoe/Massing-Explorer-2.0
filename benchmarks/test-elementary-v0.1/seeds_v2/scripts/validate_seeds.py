"""Check a v2.0 seed collection for internal coherence and brief rules.

Standard library only. Prints a report and writes <input>.validation.json.
ERROR = the record contradicts itself or a hard rule. WARN = likely problem to review.
A clean report is not a feasibility or quality certificate.

Usage:
    python validate_seeds.py <seeds.json> [--no-commitments]

--no-commitments ignores the optional commitments module entirely, as if it
were absent, so the module can be dropped without regenerating seeds.
"""
import itertools
import json
import re
import sys
from pathlib import Path

DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
NFA = {"D01": 14280, "D02": 5610, "D03": 3040, "D04": 6950, "D05": 2800,
       "D06": 6150, "D07": 730, "D08": 2510, "D09": 2200}
MIN_PORTION_SF = 753
PREFS = {"arts_ground_floor", "media_top_above_admin", "three_floors"}
WORDS = {"concept": (35, 70), "intent": (20, 40)}
TRADEOFF_WORDS = (15, 35)
# Department name fragments used to flag a concept that enumerates placements.
DEPT_TERMS = ["classroom", "academic", "special education", "sped", "art", "music", "gym",
              "physical education", "media", "library", "dining", "cafeteria", "kitchen",
              "medical", "nurse", "administration", "admin", "office", "guidance", "custodial",
              "maintenance"]
FLOOR_PATTERN = re.compile(r"\b(floor|level|storey|story)\s*[1-3]\b|\b(first|second|third)\s+(floor|level)\b", re.I)
BOILERPLATE = re.compile(r"double[- ]height|gym and dining together", re.I)


def words(s):
    return len(re.findall(r"\b[\w'-]+\b", s or ""))


def check_case(c, use_commitments):
    E, W = [], []
    s = c.get("structure") or {}
    masses = [m.get("mass_id") for m in s.get("masses", [])]
    mset = set(masses)
    if len(masses) != 3 or len(mset) != 3:
        E.append(f"expected three distinct masses, found {masses}")
    for m in s.get("masses", []):
        if not (m.get("role") or "").strip():
            E.append(f"mass {m.get('mass_id')} has no role")

    deps = {}
    for d in s.get("departments", []):
        if d.get("department_id") in deps:
            E.append(f"department {d['department_id']} listed twice")
        deps[d.get("department_id")] = d
    missing = [x for x in DEPTS if x not in deps]
    if missing:
        E.append(f"missing departments {missing}")

    owner, floors = {}, {}
    nulls = []
    for k, d in deps.items():
        mids, fl = d.get("mass_ids"), d.get("occupied_floors")
        if mids is None:
            nulls.append(f"{k} mass")
        elif len(mids) != 1:
            E.append(f"{k} assigned to {len(mids)} masses {mids}; each department must be in exactly one")
        elif mids[0] not in mset:
            E.append(f"{k} assigned to unknown mass {mids[0]}")
        else:
            owner[k] = mids[0]
        if fl is None:
            nulls.append(f"{k} floors")
        else:
            fl = sorted(fl)
            floors[k] = fl
            if not fl:
                E.append(f"{k} has no occupied floors")
            elif fl[0] < 1 or fl[-1] > 3:
                E.append(f"{k} floors {fl} outside 1-3")
            elif fl != list(range(fl[0], fl[-1] + 1)):
                E.append(f"{k} floors {fl} are not contiguous")
            elif len(fl) > 1 and NFA[k] < MIN_PORTION_SF * len(fl):
                E.append(f"{k} spans {len(fl)} floors but its {NFA[k]} SF cannot give {MIN_PORTION_SF} SF per floor")
    if nulls:
        W.append(f"unresolved values {nulls}; confirm each is explained in 'unresolved'")

    if "D08" in floors and 1 not in floors["D08"]:
        E.append("administration is not on the ground floor")
    if "D04" in owner and "D06" in owner and owner["D04"] != owner["D06"]:
        E.append("gym and dining are in different masses")

    links = {}
    for x in s.get("connections", []):
        pair = tuple(sorted((x.get("mass_a"), x.get("mass_b"))))
        if not set(pair) <= mset or pair[0] == pair[1]:
            E.append(f"connection {pair} names unknown or identical masses")
            continue
        if pair in links:
            E.append(f"connection {pair} listed twice")
        links[pair] = x.get("direct_link")
    for pair in itertools.combinations(sorted(mset), 2):
        if pair not in links:
            E.append(f"connection {pair} missing")
        elif links[pair] is None:
            W.append(f"connection {pair} unresolved; confirm it is explained in 'unresolved'")

    # Key moves must reference the structure exactly.
    moves = c.get("key_moves", [])
    ids = [m.get("move_id") for m in moves]
    if not 2 <= len(moves) <= 4:
        W.append(f"{len(moves)} key moves (expected 2-4)")
    if len(set(ids)) != len(ids):
        E.append(f"duplicate move ids {ids}")
    for m in moves:
        for r in m.get("decisions", []):
            if r.get("type") == "placement":
                k = r.get("department_id")
                if owner.get(k) != r.get("mass_id") or floors.get(k) != sorted(r.get("floors") or []):
                    E.append(f"{m.get('move_id')} claims {k} in {r.get('mass_id')} on {r.get('floors')}, "
                             f"structure has {owner.get(k)} on {floors.get(k)}")
            elif r.get("type") == "link":
                pair = tuple(sorted((r.get("mass_a"), r.get("mass_b"))))
                if links.get(pair) != r.get("direct_link"):
                    E.append(f"{m.get('move_id')} claims link {pair}={r.get('direct_link')}, structure has {links.get(pair)}")

    if use_commitments and "commitments" in c:
        cm = c["commitments"]
        for item in cm.get("core", []):
            bad = [p for p in item.get("protects", []) if p not in ids]
            if bad:
                E.append(f"core commitment protects unknown moves {bad}")
        if not 2 <= len(cm.get("core", [])) <= 4:
            W.append(f"{len(cm.get('core', []))} core commitments (expected 2-4)")
        if not 2 <= len(cm.get("flexible", [])) <= 4:
            W.append(f"{len(cm.get('flexible', []))} flexible items (expected 2-4)")
    elif use_commitments:
        W.append("commitments module absent")

    # Stated preferences given up must match what the structure implies.
    derived = set()
    if "D03" in floors and 1 not in floors["D03"]:
        derived.add("arts_ground_floor")
    if {"D05", "D08"} <= floors.keys() and {"D05", "D08"} <= owner.keys():
        same = owner["D05"] == owner["D08"]
        top = max(max(fl) for k, fl in floors.items() if owner.get(k) == owner["D05"]) if same else None
        if not (same and max(floors["D05"]) == top and min(floors["D05"]) > max(floors["D08"])):
            derived.add("media_top_above_admin")
    for mid in mset:
        top = 0
        for k, fl in floors.items():
            if owner.get(k) == mid:
                t = max(fl)
                if k in ("D04", "D06") and min(fl) == 1:
                    t = max(t, 2)
                top = max(top, t)
        if top < 3:
            derived.add("three_floors")
    stated = set((c.get("brief_response") or {}).get("preferences_given_up", []))
    if stated - PREFS:
        E.append(f"unknown preference ids {sorted(stated - PREFS)}")
    if stated != derived:
        W.append(f"preferences_given_up {sorted(stated)} differs from structure {sorted(derived)}")

    # Text fields: length, no enumeration, no shared boilerplate.
    for f, (lo, hi) in WORDS.items():
        n = words(c.get(f))
        if not lo <= n <= hi:
            W.append(f"{f} has {n} words (expected {lo}-{hi})")
    n = words((c.get("brief_response") or {}).get("main_tradeoff"))
    if not TRADEOFF_WORDS[0] <= n <= TRADEOFF_WORDS[1]:
        W.append(f"main_tradeoff has {n} words (expected {TRADEOFF_WORDS[0]}-{TRADEOFF_WORDS[1]})")
    concept = (c.get("concept") or "").lower()
    hits = sorted({t for t in DEPT_TERMS if re.search(r"\b" + re.escape(t), concept)})
    if len(hits) >= 5:
        W.append(f"concept names many departments {hits}; it may be enumerating placements")
    if FLOOR_PATTERN.search(c.get("concept") or ""):
        W.append("concept refers to specific floors; floor placement belongs in structure")
    if BOILERPLATE.search(c.get("concept") or ""):
        W.append("concept restates a requirement every scheme shares")
    if len(c.get("unresolved", [])) > 4:
        W.append("more than four unresolved items")
    return E, W, sorted(derived)


def main(argv):
    path = Path(argv[0])
    use_commitments = "--no-commitments" not in argv
    data = json.loads(path.read_text(encoding="utf-8"))
    report = {"file": path.name, "commitments_module": use_commitments, "cases": []}
    total_e = 0
    ids = [c.get("case_id") for c in data.get("cases", [])]
    if len(set(ids)) != len(ids):
        print(f"ERROR duplicate case ids {ids}")
        total_e += 1
    for c in data.get("cases", []):
        E, W, derived = check_case(c, use_commitments)
        total_e += len(E)
        report["cases"].append({"case_id": c.get("case_id"), "name": c.get("name"),
                                "errors": E, "warnings": W, "derived_preferences_given_up": derived})
        print(f"\n{c.get('case_id')}  {c.get('name')}  ({len(E)} errors, {len(W)} warnings)")
        for e in E:
            print(f"  ERROR {e}")
        for w in W:
            print(f"  WARN  {w}")
    out = path.with_suffix(".validation.json")
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"\n{len(ids)} cases, {total_e} errors. Report: {out.name}")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
