"""Build non-dimensional diagram specs for the labeling page (protocol p01-v1.1).

Each spec is derived only from the structured record: which departments sit in
which mass, on which floors, and which masses are directly linked. Specs are keyed
by the compact structure line already shown on the page, so a diagram can only
show what that line states. No dimensions, positions or site relationships.

Usage:
    python build_diagram_data.py <all_15_cases.json> <output_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_triplets import DEPTS, compact, load_cases  # noqa: E402


def spec(s):
    masses = []
    for role in ("C", "T", "G"):
        depts = [{"dept": d, "floors": s["floors"][d]} for d in DEPTS if s["own"][d] == role]
        masses.append({"role": role, "departments": depts})
    links = [f"{a}{b}" for (a, b), ok in sorted(s["links"].items()) if ok]
    return {"masses": masses, "links": links}


def main(cases_path, outdir):
    cases = load_cases(cases_path)
    out = {compact(s): spec(s) for s in cases.values()}
    if len(out) != len(cases):
        raise SystemExit("two cases share a structure line; diagrams would be ambiguous")
    p = Path(outdir) / "diagram_data.json"
    p.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(out)} diagram specs -> {p}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
