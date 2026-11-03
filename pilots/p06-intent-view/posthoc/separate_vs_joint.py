"""Pilot 6 post hoc (2026-11-03, after the declared results; architect asked): concept and intent embedded SEPARATELY,
then used together. The two centred, normalised vectors are concatenated and scaled by 1/sqrt(2), so cosine similarity
is the equal-weight mean of the concept and intent similarities. Same neighbourhood method and measures as score_p06.py.
Usage (from repo root): python pilots/p06-intent-view/posthoc/separate_vs_joint.py"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
import score_p06 as m  # noqa: E402

def main():
    E4, E6 = m.load(m.P4 / "scoring/local/embeddings.jsonl"), m.load(HERE / "local/embeddings.jsonl")
    key = json.loads((m.P4 / "data/prompt_key_SEALED.json").read_text())
    e_of = key["archive_ids"]; arch = sorted(e_of)
    rw = json.loads((m.REPO / "pilots/p01c-robustness/data/rewrite_key_SEALED.json").read_text()); ids = sorted(rw)
    refs = {}
    for name, p in (("idea_families", m.REPO / "pilots/p05-neighbourhood-address/reference/families_claude_v1.json"),
                    ("purpose_families", HERE / "reference/purpose_families_claude_v1.json")):
        f = {e: fam for fam, v in json.loads(p.read_text())["families"].items() for e in v["members"]}
        refs[name] = [f[e_of[a]] for a in arch]
    arch_cases = m.s.archive()
    D = m.struct_dist([m.expand.state_of(arch_cases[a]) for a in arch])
    rng = np.random.default_rng(m.SEED)
    out = {}
    for enc in m.ENCODERS:
        A = {"concept": np.array([E4[enc][f"archive:{a}::concept"] for a in arch]),
             "intent": np.array([E6[enc][f"archive:{a}::intent"] for a in arch])}
        W = {"concept": np.array([E4[enc][f"p01c:{p}::rewrite"] for p in ids]),
             "intent": np.array([E6[enc][f"p06:{p}::intent_rewrite"] for p in ids])}
        As = np.hstack([m.prep(A["concept"], "centred"), m.prep(A["intent"], "centred")]) / np.sqrt(2)
        Ws = np.hstack([m.prep(W["concept"], "centred"), m.prep(W["intent"], "centred")]) / np.sqrt(2)
        k = m.best_k(As); lab = m.cluster(As, k); home = dict(zip(arch, lab))
        wl = m.assign(Ws, As, lab)
        stay = int(sum(wl[i] == home[rw[p]] for i, p in enumerate(ids)))
        q2 = {r: dict(zip(("ari", "p", "pass"), m.ari_test(lab, refs[r], rng))) for r in refs}
        rho, p = m.mantel(1 - As @ As.T, D, rng)
        out[enc] = {"k": int(k), "Q1": stay, "Q2": q2, "Q3_rho": rho, "Q3_p": p,
                    "largest_share": round(float(np.bincount(lab).max() / 15), 2),
                    "neighbourhoods": {str(c): sorted(e_of[a] for a in arch if home[a] == c) for c in sorted(set(lab))}}
    (HERE / "posthoc/separate_vs_joint.json").write_text(json.dumps(out, indent=1))
    for e, r in out.items():
        print(e[:6], r["k"], r["Q1"], {x: (y["ari"], y["pass"]) for x, y in r["Q2"].items()}, r["Q3_rho"], r["largest_share"])
    print(out["qwen3-embedding:4b"]["neighbourhoods"])

if __name__ == "__main__":
    main()
