"""Build Pilot 01b inputs from the 15 v2.0 seeds (three generation runs).

Deterministic, no LLM, and nothing here looks at embeddings. Writes:
  data/descriptions.jsonl   concept, concept_intent and struct texts per case
  data/probes.json          empty (the shared runner expects the file)
  data/triplets_SEALED.json selection data; never shown during labeling
  data/labeling_set.json    blind items: diagram key, concept, intent
  data/diagram_data.json    diagram specs keyed by structure line

Triplet rule (fixed before any embedding is computed):
  cross_run   anchor + its nearest structural twin from another run (distance <= 0.10)
              versus the most concept-wording-similar case that is NOT a twin.
              Tests whether independently written versions of one idea stay close.
  disagree    structure distance and concept wording (TF-IDF) disagree on the closer option;
              one per anchor, largest margin first.
  control     both agree by a wide margin.
  repeat      two items shown again with options swapped (labeler consistency).

Usage (from pilots/p01b-concept):
    python scripts/build_p01b.py
"""
import collections
import hashlib
import itertools
import json
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SEEDS = HERE.parent.parent / "benchmarks/test-elementary-v0.1/seeds_v2/cases"
RUNS = [("R1", "seeds.json"), ("R2", "run02_seeds.json"), ("R3", "run03_seeds.json")]
SEED = 20261028
N_CROSS, N_DISAGREE, N_CONTROL, N_REPEAT = 5, 8, 2, 2
TWIN = 0.10
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
SHORT = {"D01": "academic", "D02": "SPED", "D03": "art/music", "D04": "gym", "D05": "media",
         "D06": "dining", "D07": "medical", "D08": "admin", "D09": "custodial"}
LONG = {"D01": "core academic", "D02": "special education", "D03": "art and music",
        "D04": "physical education (gym)", "D05": "media center", "D06": "dining and food service",
        "D07": "medical", "D08": "administration and guidance", "D09": "custodial and maintenance"}
ROLE_NAME = {"C": "the classroom mass", "G": "the commons mass", "T": "the third mass"}


def load():
    cases = {}
    for run, f in RUNS:
        for c in json.loads((SEEDS / f).read_text(encoding="utf-8"))["cases"]:
            s = c["structure"]
            own = {d["department_id"]: d["mass_ids"][0] for d in s["departments"]}
            role = {own["D01"]: "C", own["D04"]: "G"}
            for m in s["masses"]:
                role.setdefault(m["mass_id"], "T")
            cases[f"{run}-{c['case_id']}"] = {
                "case": c,
                "own": {d: role[m] for d, m in own.items()},
                "floors": {d["department_id"]: sorted(d["occupied_floors"]) for d in s["departments"]},
                "links": {tuple(sorted((role[x["mass_a"]], role[x["mass_b"]]))): x["direct_link"] for x in s["connections"]},
            }
    return cases


def sdist(a, b):
    g = sum((a["own"][x] == a["own"][y]) != (b["own"][x] == b["own"][y]) for x, y in itertools.combinations(DEPTS, 2)) / 36
    v = sum(1 - len(set(a["floors"][d]) & set(b["floors"][d])) / len(set(a["floors"][d]) | set(b["floors"][d])) for d in DEPTS) / 9
    l = sum(a["links"][k] != b["links"][k] for k in a["links"]) / 3
    return (g + v + l) / 3


def tfidf(texts):
    tok = lambda s: re.findall(r"[a-z]+", s.lower())
    df = collections.Counter(w for t in texts.values() for w in set(tok(t)))
    n = len(texts)
    vec = {k: {w: c * math.log(n / df[w]) for w, c in collections.Counter(tok(t)).items()} for k, t in texts.items()}

    def cos(a, b):
        va, vb = vec[a], vec[b]
        num = sum(va[w] * vb.get(w, 0) for w in va)
        den = math.sqrt(sum(x * x for x in va.values()) * sum(x * x for x in vb.values()))
        return num / den if den else 0.0
    return cos


def struct_text(s):
    out = []
    for r in "CGT":
        items = [f"{LONG[d]} on {fl(s['floors'][d])}" for d in DEPTS if s["own"][d] == r]
        if items:
            name = ROLE_NAME[r]
            out.append(f"{name[0].upper() + name[1:]} holds " + "; ".join(items) + ".")
    order = ["C", "G", "T"]
    pairs = sorted(s["links"].items(), key=lambda kv: (order.index(kv[0][0]), order.index(kv[0][1])))
    yes = [f"{ROLE_NAME[a]} and {ROLE_NAME[b]}" for (a, b), ok in pairs if ok]
    no = [f"{ROLE_NAME[a]} and {ROLE_NAME[b]}" for (a, b), ok in pairs if not ok]
    if yes:
        out.append("Direct links join " + "; ".join(yes) + ".")
    if no:
        out.append("There is no direct link between " + "; ".join(no) + ".")
    return " ".join(out)


def fl(f):
    return f"floor {f[0]}" if len(f) == 1 else f"floors {f[0]}-{f[-1]}"


def compact(s):
    parts = []
    for r, name in (("C", "Classroom mass"), ("G", "Commons mass"), ("T", "Third mass")):
        items = [f"{SHORT[d]} {s['floors'][d][0]}" if len(s["floors"][d]) == 1 else f"{SHORT[d]} {s['floors'][d][0]}-{s['floors'][d][-1]}"
                 for d in DEPTS if s["own"][d] == r]
        parts.append(f"{name}: " + ", ".join(items))
    nm = {"C": "classroom", "G": "commons", "T": "third"}
    parts.append("Direct links: " + (", ".join(f"{nm[a]}-{nm[b]}" for (a, b), ok in sorted(s["links"].items()) if ok) or "none"))
    return " | ".join(parts)


def diagram(s):
    return {"masses": [{"role": r, "departments": [{"dept": d, "floors": s["floors"][d]} for d in DEPTS if s["own"][d] == r]}
                       for r in ("C", "T", "G")],
            "links": [a + b for (a, b), ok in sorted(s["links"].items()) if ok]}


def main():
    cases = load()
    ids = sorted(cases)
    concept = {k: cases[k]["case"]["concept"] for k in ids}
    cos = tfidf(concept)
    D = {(a, b): sdist(cases[a], cases[b]) for a in ids for b in ids}

    triplets, used_anchor = [], set()
    # cross_run: anchor + cross-run twin vs most wording-similar non-twin.
    cands = []
    for a in ids:
        twins = [b for b in ids if b != a and b[:2] != a[:2] and D[a, b] <= TWIN]
        if not twins:
            continue
        t = min(twins, key=lambda b: (D[a, b], b))
        near = [b for b in ids if b != a and D[a, b] > TWIN]
        lex = max(near, key=lambda b: (cos(a, b), b))
        cands.append((D[a, t], a, t, lex))
    pair_seen = set()
    for _, a, t, lex in sorted(cands):
        if len([x for x in triplets if x["kind"] == "cross_run"]) >= N_CROSS:
            break
        key = frozenset((a, t))
        if key in pair_seen:
            continue
        pair_seen.add(key)
        used_anchor.add(a)
        triplets.append({"kind": "cross_run", "anchor": a, "options": [t, lex],
                         "selection": {"twin": t, "twin_distance": round(D[a, t], 4),
                                       "wording_closer_non_twin": lex, "wording_cos": round(cos(a, lex), 4)}})

    dis, agr = [], []
    for a in ids:
        for x, y in itertools.combinations([i for i in ids if i != a], 2):
            ds, dl = D[a, x] - D[a, y], cos(a, x) - cos(a, y)
            if ds < 0 and dl < 0:
                dis.append((min(-ds, -dl), a, x, y))
            elif ds > 0 and dl > 0:
                dis.append((min(ds, dl), a, y, x))
            elif ds < 0 and dl > 0:
                agr.append((min(-ds, dl), a, x, y))
            elif ds > 0 and dl < 0:
                agr.append((min(ds, -dl), a, y, x))
    for m, a, sx, lx in sorted(dis, key=lambda t: (-t[0], t[1:])):
        if len([x for x in triplets if x["kind"] == "disagree"]) >= N_DISAGREE:
            break
        if a in used_anchor:
            continue
        used_anchor.add(a)
        triplets.append({"kind": "disagree", "anchor": a, "options": [sx, lx],
                         "selection": {"struct_closer": sx, "wording_closer": lx, "margin": round(m, 4)}})
    for m, a, both, other in sorted(agr, key=lambda t: (-t[0], t[1:])):
        if len([x for x in triplets if x["kind"] == "control"]) >= N_CONTROL:
            break
        if a in used_anchor:
            continue
        used_anchor.add(a)
        triplets.append({"kind": "control", "anchor": a, "options": [both, other],
                         "selection": {"struct_and_wording_closer": both, "margin": round(m, 4)}})

    rng = random.Random(SEED)
    for i, t in enumerate(triplets, 1):
        t["triplet_id"] = f"C{i:02d}"
        t["shown_order"] = rng.sample(t["options"], 2)
    picks = [t for t in triplets if t["kind"] == "disagree"][:1] + [t for t in triplets if t["kind"] == "cross_run"][:1]
    for t in picks[:N_REPEAT]:
        r = dict(t, triplet_id=f"C{len(triplets) + 1:02d}", repeat_of=t["triplet_id"], shown_order=list(reversed(t["shown_order"])))
        triplets.append(r)
    order = [t["triplet_id"] for t in triplets]
    for _ in range(1000):
        rng.shuffle(order)
        pos = {k: i for i, k in enumerate(order)}
        if all(abs(pos[t["triplet_id"]] - pos[t["repeat_of"]]) >= 7 for t in triplets if "repeat_of" in t):
            break

    def show(k):
        c = cases[k]["case"]
        return {"text": c["concept"], "intent": c["intent"], "structure": compact(cases[k])}

    by = {t["triplet_id"]: t for t in triplets}
    items = [{"item": n, "triplet_id": tid, "anchor": show(by[tid]["anchor"]),
              "option_1": show(by[tid]["shown_order"][0]), "option_2": show(by[tid]["shown_order"][1])}
             for n, tid in enumerate(order, 1)]

    out = HERE / "data"
    out.mkdir(exist_ok=True)
    rows = []
    for k in ids:
        c = cases[k]["case"]
        for variant, text in (("concept", c["concept"]), ("concept_intent", c["concept"] + " " + c["intent"]),
                              ("struct", struct_text(cases[k]))):
            rows.append({"text_id": f"{k}::{variant}", "case_id": k, "variant": variant, "text": text,
                         "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
    with open(out / "descriptions.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / "probes.json").write_text(json.dumps({"note": "Pilot 01b has no probes.", "texts": {}}, indent=1), encoding="utf-8")
    (out / "triplets_SEALED.json").write_text(json.dumps({"seed": SEED, "presentation_order": order, "triplets": triplets}, indent=1), encoding="utf-8")
    blind = json.dumps({"question": "Which option is the closer architectural strategy to the anchor?",
                        "answers": ["option_1", "option_2", "about_equal", "cannot_judge"], "items": items},
                       indent=1, ensure_ascii=False)
    (out / "labeling_set.json").write_text(blind, encoding="utf-8")
    (out / "diagram_data.json").write_text(json.dumps({compact(cases[k]): diagram(cases[k]) for k in ids}, indent=1), encoding="utf-8")
    print(json.dumps({"cases": len(ids), "texts": len(rows), "triplets": len(triplets),
                      "by_kind": collections.Counter(t["kind"] for t in triplets)}, indent=1))
    for t in triplets:
        print(t["triplet_id"], t["kind"].ljust(9), t["anchor"], t["options"], t.get("repeat_of", ""), t.get("selection", ""))


if __name__ == "__main__":
    main()
