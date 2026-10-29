"""Pilot 4 scoring, step 2 (container): score the 40 cases, then unblind by arm.

Fixed before any local output was seen (see SCORING.md). Inputs:
  scoring/local/embeddings.jsonl, scoring/local/extraction.jsonl   (from the local run)
  replies/clean/R*.json + R*.validation.json, data/blind_map.json
  data/prompt_key_SEALED.json (read only in unblind(), after every per-case measure is computed)

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/score_p04.py
"""
import collections
import json
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
sys.path.insert(0, str(REPO / "pilots/p03-expansion/scripts"))
import expand  # noqa: E402
import validate_v3  # noqa: E402
from build_scoring import RUNS, normalized  # noqa: E402
from directions import cell  # noqa: E402

LOCAL = HERE / "scoring/local"
MEASURE = ["mxbai-embed-large", "nomic-embed-text"]
STEER = "bge-m3"
PCTL = 95
TH = expand.TH  # 1.0, the architect's "different strategy" bar
ARMS = ["U", "A", "S", "J"]
# A hard-rule error, and the words that count as naming it in `unresolved` (audited in the output).
DECLARE = [(re.compile(r"does not stand from the ground"),
            re.compile(r"intermediate|second[- ]floor|floor 2|level 2|unoccupied|empty|vacant|between ground|middle (floor|level)", re.I))]
GROUPS = {"place_D02": "special_education", "place": "placement", "link": "links", "storeys": "heights", "level": "vertical"}


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def dist(a, b):
    return float(max(0.0, 1 - a @ b))


def load_embeddings():
    E = collections.defaultdict(dict)
    for line in (LOCAL / "embeddings.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        E[r["encoder"]][r["text_id"]] = unit(r["vector"])
    return E


def thresholds(E):
    """95th percentile of original-to-rewrite distances, Pilot 01c, re-embedded in this run."""
    key = json.loads((REPO / "pilots/p01c-robustness/data/rewrite_key_SEALED.json").read_text(encoding="utf-8"))
    out = {}
    for enc in E:
        d = [dist(E[enc][f"p01c:{p}::rewrite"], E[enc][f"p01c:{c}::original"]) for p, c in key.items()]
        out[enc] = {"threshold": round(float(np.percentile(d, PCTL)), 4), "median": round(float(np.median(d)), 4), "n": len(d)}
    return out


def load_cases():
    blind = json.loads((HERE / "data/blind_map.json").read_text(encoding="utf-8"))
    by_reply = {}
    for n in range(1, 9):
        d = validate_v3.parse((HERE / f"replies/clean/R{n}.json").read_text(encoding="utf-8"))
        v = json.loads((HERE / f"replies/clean/R{n}.validation.json").read_text(encoding="utf-8"))
        vm = {x["case_id"]: x for x in v["cases"]}
        for c in d["cases"]:
            by_reply[(f"R{n}", c["case_id"])] = (c, vm[c["case_id"]])
    return {q: {"q": q, **b, "case": by_reply[(b["reply"], b["case_id"])][0], "validation": by_reply[(b["reply"], b["case_id"])][1]}
            for q, b in blind.items()}


def validity(c):
    v = c["validation"]
    if v["valid"]:
        return "valid", []
    audit, declared = [], True
    for err in v["errors"]:
        hit = None
        for rule, words in DECLARE:
            if rule.search(err):
                hit = next((u for u in c["case"]["unresolved"] if words.search(u)), None)
        audit.append({"error": err, "declared_by": hit})
        declared &= hit is not None
    return ("declared" if declared else "undeclared"), audit


def state(case):
    c = dict(case)
    c["structure"] = normalized(case["structure"])
    return expand.state_of(c)


def archive():
    out = {}
    for run, f in RUNS:
        for c in json.loads((REPO / "benchmarks/test-elementary-v0.1/seeds_v2/cases" / f).read_text(encoding="utf-8"))["cases"]:
            out[f"{run}-{c['case_id']}"] = c
    return out


def agreement():
    """Modal answer of 3 samples per question vs the code record."""
    items = {i["id"]: i for i in json.loads((LOCAL / "items.json").read_text(encoding="utf-8"))["items"]}
    samples = collections.defaultdict(list)
    for line in (LOCAL / "extraction.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        samples[r["item"]].append(r["output"])
    res = {}
    for iid, it in items.items():
        q, view = iid.split("::")
        row = {}
        for k, t in it["truth"].items():
            vals = [s.get(k, "not stated") for s in samples[iid]]
            row[k] = {"modal": sorted(collections.Counter(vals).items(), key=lambda x: (-x[1], x[0]))[0][0] if vals else "not stated", "true": t}
        res.setdefault(q, {})[view] = row
    return res


def group_of(k):
    return GROUPS["place_D02"] if k == "place_D02" else GROUPS[k.split("_")[0]]


def per_case(cases, E, TH_E, arch, arch_states, AG):
    """Everything that does not need the arm."""
    out = {}
    for q, c in cases.items():
        cat, audit = validity(c)
        st = state(c["case"])
        ch = {k: expand.change(s, st)[0] for k, s in arch_states.items()}
        near_struct = min(ch, key=lambda k: (ch[k], k))
        r = {"q": q, "reply": c["reply"], "case_id": c["case_id"], "name": c["case"]["name"], "validity": cat, "declaration_audit": audit,
             "cell": [list(x) if isinstance(x, tuple) else x for x in cell(st)], "struct_change_to_archive": ch[near_struct],
             "struct_nearest_archive": near_struct, "meaning": {}}
        for enc in MEASURE + [STEER]:
            for view in ("idea", "concept"):
                dv = {k: dist(E[enc][f"case:{q}::{view}"], E[enc][f"archive:{k}::{view}"]) for k in arch}
                nk = min(dv, key=dv.get)
                r["meaning"][f"{enc}|{view}"] = {"nearest_archive": nk, "dist": round(dv[nk], 4), "all": {k: round(x, 4) for k, x in dv.items()}}
        if q in AG:
            for view, row in AG[q].items():
                acc = np.mean([x["modal"] == x["true"] for x in row.values()])
                grp = collections.defaultdict(list)
                for k, x in row.items():
                    grp[group_of(k)].append(x["modal"] == x["true"])
                r[f"agreement_{view}"] = {"all": round(float(acc), 3), **{g: round(float(np.mean(v)), 3) for g, v in grp.items()}}
        out[q] = r
    return out


def parse_direction(text, eid_to_seed):
    es = [eid_to_seed[e] for e in re.findall(r"\bE\d{2}\b", text)]
    if text.startswith("An idea unlike"):
        return {"type": "away", "seeds": es}
    if text.startswith("An idea that combines"):
        return {"type": "bridge", "intent_of": es[0], "organization_of": es[1]}
    if text.startswith("A different idea in the spirit"):
        return {"type": "develop", "seed": es[0]}
    return {"type": "gap"}


def unblind(P, cases, E, TH_E, arch_states):
    key = json.loads((HERE / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))
    dirs = json.loads((HERE / "data/directions.json").read_text(encoding="utf-8"))
    eid_to_seed = {e: s for s, e in key["archive_ids"].items()}
    meta = {}
    for i, p in enumerate(key["prompts"], 1):
        meta[f"R{i}"] = p
    for q, r in P.items():
        p = meta[r["reply"]]
        r["arm"], r["chat"] = p["arm"], p["chat"]
        k = int(r["case_id"][1:]) - 1
        r["order"] = (p["chat"] - 1) * 5 + k
        if p["arm"] in ("A", "J"):
            g = dirs["A"][(p["chat"] - 1) * 5 + k]["gap"]
            tgt = [sorted(g[0]), g[1], g[2]]
            got = [sorted(r["cell"][0]), r["cell"][1], r["cell"][2]]
            r["steer"] = {"target_cell": tgt, "hit": tgt == got, "links_hit": tgt[0] == got[0], "sped_hit": tgt[1] == got[1], "height_hit": tgt[2] == got[2]}
        elif p["arm"] == "S":
            d = parse_direction(p["directions"][k], eid_to_seed)
            dv = r["meaning"][f"{STEER}|idea"]["all"]
            rank = sorted(dv, key=lambda s: (dv[s], s))
            if d["type"] == "away":
                hit = rank[0] not in d["seeds"]
            elif d["type"] == "bridge":
                hit = d["intent_of"] in rank[:5] and d["organization_of"] in rank[:5]
            else:
                hit = d["seed"] in rank[:3] and dv[d["seed"]] > TH_E[STEER]["threshold"]
            r["steer"] = {"direction": d, "hit": bool(hit), "nearest5": rank[:5]}
    # novelty against archive and earlier same-arm cases
    by_arm = collections.defaultdict(list)
    for q, r in P.items():
        by_arm[r["arm"]].append(q)
    for arm, qs in by_arm.items():
        qs.sort(key=lambda q: P[q]["order"])
        for i, q in enumerate(qs):
            r, prev = P[q], qs[:i]
            st = state(cases[q]["case"])
            sc_prev = min([expand.change(state(cases[p]["case"]), st)[0] for p in prev], default=None)
            r["struct_change_to_prev"] = sc_prev
            r["new_structure"] = r["struct_change_to_archive"] >= TH and (sc_prev is None or sc_prev >= TH)
            r["new_structure_vs_archive_only"] = r["struct_change_to_archive"] >= TH
            for view in ("idea", "concept"):
                ok, ok_arch = True, True
                for enc in MEASURE:
                    da = r["meaning"][f"{enc}|{view}"]["dist"]
                    dp = min([dist(E[enc][f"case:{q}::{view}"], E[enc][f"case:{p}::{view}"]) for p in prev], default=9.0)
                    r["meaning"][f"{enc}|{view}"]["dist_prev"] = None if not prev else round(dp, 4)
                    ok &= min(da, dp) > TH_E[enc]["threshold"]
                    ok_arch &= da > TH_E[enc]["threshold"]
                r[f"new_meaning_{view}"] = bool(ok)
                r[f"new_meaning_{view}_vs_archive_only"] = bool(ok_arch)
            r["new_strategy"] = r["validity"] == "valid" and r["new_meaning_idea"] and r["new_structure"]
            r["new_strategy_incl_declared"] = r["validity"] in ("valid", "declared") and r["new_meaning_idea"] and r["new_structure"]
            r["new_strategy_concept_view"] = r["validity"] == "valid" and r["new_meaning_concept"] and r["new_structure"]
            r["new_strategy_vs_archive_only"] = r["validity"] == "valid" and r["new_meaning_idea_vs_archive_only"] and r["new_structure_vs_archive_only"]
    return by_arm


def view_diversity(E, P, by_arm):
    """Within-arm spread of each embedded view (analysis only)."""
    out = {}
    for arm, qs in by_arm.items():
        for enc in MEASURE:
            for view in ("idea", "concept", "intent", "move", "unresolved"):
                ids = {q: [t for t in E[enc] if t.startswith(f"case:{q}::{view}")] for q in qs}
                nn = []
                for q in qs:
                    for t in ids[q]:
                        others = [dist(E[enc][t], E[enc][u]) for p in qs if p != q for u in ids[p]]
                        if others:
                            nn.append(min(others))
                out[f"{arm}|{enc}|{view}"] = round(float(np.mean(nn)), 4) if nn else None
    return out


def summarize(P, by_arm, arch_cells):
    S = {}
    for arm in ARMS:
        rs = [P[q] for q in by_arm.get(arm, [])]
        if not rs:
            continue
        s = {"n": len(rs)}
        for k in ("new_strategy", "new_strategy_incl_declared", "new_strategy_concept_view", "new_strategy_vs_archive_only",
                  "new_structure", "new_meaning_idea", "new_meaning_concept"):
            s[k] = sum(bool(r[k]) for r in rs)
        s["validity"] = dict(collections.Counter(r["validity"] for r in rs))
        for view in ("v3text", "idea"):
            vals = [r[f"agreement_{view}"] for r in rs if f"agreement_{view}" in r]
            if vals:
                s[f"agreement_{view}"] = {g: round(float(np.mean([v[g] for v in vals if g in v])), 3) for g in vals[0]}
        st = [r["steer"]["hit"] for r in rs if "steer" in r]
        s["steer_hits"] = f"{sum(st)}/{len(st)}" if st else None
        cells = {json.dumps(r["cell"]) for r in rs if r["validity"] == "valid"}
        s["new_cells_reached"] = len([c for c in cells if c not in arch_cells])
        S[arm] = s
    return S


def decide(S):
    if not all(a in S for a in ARMS):
        return "incomplete"
    J, A, U, Sx = S["J"], S["A"], S["U"], S["S"]
    val = lambda s: s["validity"].get("valid", 0)
    agr = lambda s: s.get("agreement_v3text", {}).get("all", 0)
    lines = []
    if J["new_strategy"] - A["new_strategy"] >= 2 and val(A) - val(J) <= 1 and agr(A) - agr(J) <= 0.10:
        lines.append("PROMISING: J beats A by >= 2 new strategies with validity and agreement held")
    elif abs(J["new_strategy"] - A["new_strategy"]) <= 1 and J["new_strategy"] > U["new_strategy"] and A["new_strategy"] > U["new_strategy"]:
        lines.append("J ~ A, both beat U: embedding adds nothing detectable on top of axes; S vs U: "
                     + ("S > U (semantic helps alone, overlaps axes)" if Sx["new_strategy"] > U["new_strategy"] else "S ~ U (leans to fallback)"))
    else:
        lines.append(f"No pre-registered pattern matched exactly (J {J['new_strategy']}, A {A['new_strategy']}, S {Sx['new_strategy']}, U {U['new_strategy']})")
    if any(val(U) - val(S[a]) >= 2 for a in ("A", "S", "J")):
        lines.append("GUARDRAIL: a guided arm loses >= 2 cases on validity vs U")
    if any(agr(U) - agr(S[a]) > 0.20 for a in ("A", "S", "J")):
        lines.append("GUARDRAIL: a guided arm loses > 0.20 mean agreement vs U")
    return lines


def main():
    E = load_embeddings()
    TH_E = thresholds(E)
    cases = load_cases()
    arch = archive()
    arch_states = {k: expand.state_of(c) for k, c in arch.items()}
    arch_cells = {json.dumps([list(x) if isinstance(x, tuple) else x for x in cell(s)]) for s in arch_states.values()}
    AG = agreement() if (LOCAL / "extraction.jsonl").exists() else {}
    P = per_case(cases, E, TH_E, arch, arch_states, AG)          # blind
    by_arm = unblind(P, cases, E, TH_E, arch_states)            # arm key read here
    S = summarize(P, by_arm, arch_cells)
    out = {"thresholds": TH_E, "summary": S, "decision": decide(S), "view_diversity": view_diversity(E, P, by_arm),
           "declaration_audit": {q: r["declaration_audit"] for q, r in P.items() if r["declaration_audit"]},
           "per_case": P}
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results/scores.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("thresholds:", {k: v["threshold"] for k, v in TH_E.items()})
    for arm, s in S.items():
        print(arm, {k: v for k, v in s.items() if k != "agreement_idea"})
    for line in out["decision"]:
        print(line)


if __name__ == "__main__":
    main()
