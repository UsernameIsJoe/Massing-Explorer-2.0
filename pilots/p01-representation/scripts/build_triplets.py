"""Build the Pilot 01 triplet set and the blind labeling set.

Real-case triplets are selected deterministically where a structural distance
and a wording (TF-IDF) similarity on the intent text disagree about which option
is closer to the anchor. Agreement controls are where both agree by a wide margin.
Probe triplets come from data/probes.json. A few items are repeated with options
swapped to measure labeler consistency.

The selection proxies are only used to CHOOSE discriminating items. Neither is a
ground truth; the user's blind labels are.

Usage:
    python build_triplets.py <all_15_cases.json> <descriptions.jsonl> <probes.json> <output_dir>
"""
import collections
import hashlib
import itertools
import json
import math
import random
import re
import sys
from pathlib import Path

SEED = 20261028
N_REAL = 12
N_CONTROL = 3
DEPTS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
SHORT = {"D01": "academic", "D02": "SPED", "D03": "art/music", "D04": "gym", "D05": "media",
         "D06": "dining", "D07": "medical", "D08": "admin", "D09": "custodial"}
PREFIX = {"parents_05": "05", "additions_A": "A", "additions_B": "B"}


def load_cases(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for rec in data["records"]:
        c = rec["case"]
        cid = f"{PREFIX[rec['collection']]}-{c['case_id']}"
        own = {d["department_id"]: d["mass_ids"][0] for d in c["departments"]}
        fl = {d["department_id"]: sorted(d["occupied_floors"]) for d in c["departments"]}
        role = {own["D01"]: "C", own["D04"]: "G"}
        for m in c["masses"]:
            role.setdefault(m["mass_id"], "T")
        links = {tuple(sorted((role[x["mass_a"]], role[x["mass_b"]]))): x["direct_link"]
                 for x in c["connections"]}
        out[cid] = {"own": {d: role[m] for d, m in own.items()}, "floors": fl, "links": links}
    return out


def struct_distance(a, b):
    """Mean of grouping Hamming (36 co-location bits), floor-set Jaccard and link Hamming."""
    g = sum((a["own"][x] == a["own"][y]) != (b["own"][x] == b["own"][y])
            for x, y in itertools.combinations(DEPTS, 2)) / 36
    v = sum(1 - len(set(a["floors"][d]) & set(b["floors"][d])) / len(set(a["floors"][d]) | set(b["floors"][d]))
            for d in DEPTS) / 9
    l = sum(a["links"][k] != b["links"][k] for k in a["links"]) / 3
    return (g + v + l) / 3


def tfidf_cos(texts):
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


def compact(s):
    parts = []
    for role, name in (("C", "Classroom mass"), ("G", "Commons mass"), ("T", "Third mass")):
        items = []
        for d in DEPTS:
            if s["own"][d] == role:
                f = s["floors"][d]
                items.append(f"{SHORT[d]} {f[0]}" if len(f) == 1 else f"{SHORT[d]} {f[0]}-{f[-1]}")
        parts.append(f"{name}: " + ", ".join(items))
    names = {"C": "classroom", "G": "commons", "T": "third"}
    linked = [f"{names[a]}-{names[b]}" for (a, b), ok in sorted(s["links"].items()) if ok]
    parts.append("Direct links: " + ", ".join(linked))
    return " | ".join(parts)


def main(cases_path, desc_path, probes_path, outdir):
    cases = load_cases(cases_path)
    desc = [json.loads(l) for l in open(desc_path, encoding="utf-8")]
    intent = {r["case_id"]: r["text"] for r in desc if r["variant"] == "intent"}
    probes = json.loads(Path(probes_path).read_text(encoding="utf-8"))
    cos = tfidf_cos(intent)
    ids = sorted(cases)

    cands = []
    for a in ids:
        for x, y in itertools.combinations([i for i in ids if i != a], 2):
            ds = struct_distance(cases[a], cases[x]) - struct_distance(cases[a], cases[y])
            dl = cos(a, x) - cos(a, y)
            # ds < 0: x structurally closer. dl > 0: x lexically closer.
            if ds < 0 and dl < 0:
                cands.append(("disagree", min(-ds, -dl), a, x, y))
            elif ds > 0 and dl > 0:
                cands.append(("disagree", min(ds, dl), a, y, x))
            elif ds < 0 and dl > 0:
                cands.append(("agree", min(-ds, dl), a, x, y))
            elif ds > 0 and dl < 0:
                cands.append(("agree", min(ds, -dl), a, y, x))
    cands.sort(key=lambda t: (-t[1], t[2], t[3], t[4]))

    triplets, used = [], set()
    for kind, margin, a, sx, other in cands:
        if kind == "disagree" and a not in used and len([t for t in triplets if t["kind"] == "real_disagree"]) < N_REAL:
            used.add(a)
            triplets.append({"kind": "real_disagree", "anchor": a, "options": [sx, other],
                             "selection": {"struct_closer": sx, "lexical_closer": other, "margin": round(margin, 4)}})
    for kind, margin, a, both, other in cands:
        if kind == "agree" and a not in used and len([t for t in triplets if t["kind"] == "real_control"]) < N_CONTROL:
            used.add(a)
            triplets.append({"kind": "real_control", "anchor": a, "options": [both, other],
                             "selection": {"struct_and_lexical_closer": both, "margin": round(margin, 4)}})
    for p in probes["triplets"]:
        triplets.append({"kind": p["kind"], "anchor": p["anchor"], "options": list(p["options"]),
                         "construction_expectation": p["construction_expectation"]})

    rng = random.Random(SEED)
    for i, t in enumerate(triplets, 1):
        t["triplet_id"] = f"T{i:02d}"
        t["shown_order"] = rng.sample(t["options"], 2)
    # Repeats with swapped display order (consistency check).
    pick = [t for t in triplets if t["kind"] == "real_disagree"][:2] + [t for t in triplets if t["kind"] == "lexical_trap"][:1]
    for j, t in enumerate(pick, 1):
        r = dict(t)
        r["triplet_id"] = f"T{len(triplets) + 1:02d}"
        r["repeat_of"] = t["triplet_id"]
        r["shown_order"] = list(reversed(t["shown_order"]))
        triplets.append(r)

    order = [t["triplet_id"] for t in triplets]
    for _ in range(1000):
        rng.shuffle(order)
        pos = {tid: i for i, tid in enumerate(order)}
        if all(abs(pos[t["triplet_id"]] - pos[t["repeat_of"]]) >= 8 for t in triplets if "repeat_of" in t):
            break

    def show(ref, real):
        if ref in probes["texts"]:
            return {"text": probes["texts"][ref]}
        item = {"text": intent[ref]}
        if real:
            item["structure"] = compact(cases[ref])
        return item

    by_id = {t["triplet_id"]: t for t in triplets}
    blind = []
    for n, tid in enumerate(order, 1):
        t = by_id[tid]
        real = t["kind"].startswith("real")
        blind.append({
            "item": n,
            "triplet_id": tid,
            "anchor": show(t["anchor"], real),
            "option_1": show(t["shown_order"][0], real),
            "option_2": show(t["shown_order"][1], real),
        })

    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    full = {"seed": SEED, "presentation_order": order, "triplets": triplets}
    (out / "triplets_SEALED.json").write_text(json.dumps(full, indent=1), encoding="utf-8")
    blind_txt = json.dumps({"question": "Which option is the closer architectural strategy to the anchor?",
                            "answers": ["option_1", "option_2", "about_equal", "cannot_judge"],
                            "items": blind}, indent=1, ensure_ascii=False)
    (out / "labeling_set.json").write_text(blind_txt, encoding="utf-8")
    counts = collections.Counter(t["kind"] for t in triplets)
    print(json.dumps({"triplets": len(triplets), "by_kind": counts,
                      "labeling_set_sha256": hashlib.sha256(blind_txt.encode()).hexdigest()}, indent=1))
    for t in triplets:
        print(t["triplet_id"], t["kind"], t["anchor"], t["options"], t.get("repeat_of", ""))


if __name__ == "__main__":
    main(*sys.argv[1:5])
