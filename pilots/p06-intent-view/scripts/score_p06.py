"""Pilot 6 scoring: concept vs intent vs idea as the map's meaning coordinate. Implements PROTOCOL.md.

Written before the local embeddings arrived.
Inputs: pilots/p04-guided-exploration/scoring/local/embeddings.jsonl (concept, idea, cases, concept rewrites)
        pilots/p06-intent-view/local/embeddings.jsonl (archive intents, intent rewrites, idea rewrites)
Usage (from repo root):  python pilots/p06-intent-view/scripts/score_p06.py
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
P4 = REPO / "pilots/p04-guided-exploration"
sys.path.insert(0, str(P4 / "scripts"))
import score_p04 as s  # noqa: E402
import expand  # noqa: E402  (path set by score_p04)

ENCODERS = ["qwen3-embedding:4b", "mxbai-embed-large", "nomic-embed-text", "bge-m3"]
PRIMARY = "qwen3-embedding:4b"
VIEWS = ["concept", "intent", "idea"]
CORRECTIONS = ["centred", "raw"]          # centred primary
K_RANGE = range(3, 9)
N_PERM, N_MANTEL, SEED = 10_000, 9_999, 20261103


def load(path):
    E = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        E.setdefault(r["encoder"], {})[r["text_id"]] = np.array(r["vector"], dtype=float)
    return E


def norm(M):
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def prep(M, how):
    return norm(M) if how == "raw" else norm(M - M.mean(0))


def cluster(A, k):
    return AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average").fit_predict(A)


def best_k(A):
    sil = {k: float(silhouette_score(A, cluster(A, k), metric="cosine")) for k in K_RANGE}
    return max(sil, key=sil.get)


def assign(X, A, lab):
    ids = sorted(set(lab))
    cents = norm(np.array([A[lab == c].mean(0) for c in ids]))
    return np.array(ids)[np.argmax(X @ cents.T, axis=1)]


def ari_test(lab, ref, rng):
    obs = float(adjusted_rand_score(lab, ref))
    ref = np.array(ref)
    hits = sum(adjusted_rand_score(lab, rng.permutation(ref)) >= obs for _ in range(N_PERM))
    p = (hits + 1) / (N_PERM + 1)
    return round(obs, 3), round(p, 4), obs >= 0.40 and p < 0.05


def condensed(D):
    i, j = np.triu_indices(len(D), 1)
    return D[i, j]


def mantel(Dx, Dy, rng):
    obs = spearmanr(condensed(Dx), condensed(Dy))[0]
    n, hits = len(Dx), 0
    for _ in range(N_MANTEL):
        p = rng.permutation(n)
        hits += spearmanr(condensed(Dx[np.ix_(p, p)]), condensed(Dy))[0] >= obs
    return round(float(obs), 3), round((hits + 1) / (N_MANTEL + 1), 4)


def struct_dist(states):
    n = len(states)
    D = np.zeros((n, n))
    for a, b in itertools.combinations(range(n), 2):
        D[a, b] = D[b, a] = (expand.change(states[a], states[b])[0] + expand.change(states[b], states[a])[0]) / 2
    return D


def main():
    E4 = load(P4 / "scoring/local/embeddings.jsonl")
    E6 = load(HERE / "local/embeddings.jsonl")
    key = json.loads((P4 / "data/prompt_key_SEALED.json").read_text(encoding="utf-8"))
    e_of = key["archive_ids"]
    arch = sorted(e_of)
    rw = json.loads((REPO / "pilots/p01c-robustness/data/rewrite_key_SEALED.json").read_text(encoding="utf-8"))
    rw_ids = sorted(rw)
    idea_ref = json.loads((REPO / "pilots/p05-neighbourhood-address/reference/families_claude_v1.json").read_text(encoding="utf-8"))
    purp_ref = json.loads((HERE / "reference/purpose_families_claude_v1.json").read_text(encoding="utf-8"))
    refs = {}
    for name, r in (("idea_families", idea_ref), ("purpose_families", purp_ref)):
        f = {e: fam for fam, v in r["families"].items() for e in v["members"]}
        refs[name] = [f[e_of[a]] for a in arch]
    view_refs = {"concept": ["idea_families"], "intent": ["purpose_families"], "idea": ["idea_families", "purpose_families"]}

    arch_cases = s.archive()
    cases = s.load_cases()
    qs = sorted(cases)
    D_arch = struct_dist([expand.state_of(arch_cases[a]) for a in arch])
    D_case = struct_dist([s.state(cases[q]["case"]) for q in qs])

    def vec(enc, view, batch):
        if batch == "A":
            if view == "intent":
                return np.array([E6[enc][f"archive:{a}::intent"] for a in arch])
            return np.array([E4[enc][f"archive:{a}::{view}"] for a in arch])
        if batch == "W":
            if view == "concept":
                return np.array([E4[enc][f"p01c:{p}::rewrite"] for p in rw_ids])
            return np.array([E6[enc][f"p06:{p}::{view}_rewrite"] for p in rw_ids])
        return np.array([E4[enc][f"case:{q}::{view}"] for q in qs])

    rng = np.random.default_rng(SEED)
    out = {"primary_encoder": PRIMARY, "primary_correction": "centred", "results": {}, "concept_vs_intent": {}}
    labels = {}
    for how in CORRECTIONS:
        for enc in ENCODERS:
            for view in VIEWS:
                A, W, C = (prep(vec(enc, view, b), how) for b in "AWC")
                k = best_k(A)
                lab = cluster(A, k)
                home = dict(zip(arch, lab))
                wl = assign(W, A, lab)
                stay = int(sum(wl[i] == home[rw[p]] for i, p in enumerate(rw_ids)))
                largest = float(np.bincount(lab).max() / len(lab))
                collapsed = k == 3 and largest >= 0.60
                q2 = {r: dict(zip(("ari", "p", "pass"), ari_test(lab, refs[r], rng))) for r in refs}  # both refs reported; gate uses the view's own
                own_ref = view_refs[view][0] if view != "idea" else max(view_refs[view], key=lambda r: q2[r]["ari"])
                cos_A = 1 - A @ A.T
                cos_C = 1 - C @ C.T
                rA, pA = mantel(cos_A, D_arch, rng)
                rC, pC = mantel(cos_C, D_case, rng)
                labels[(how, enc, view)] = (lab, cluster(C, best_k(C)))
                out["results"].setdefault(how, {}).setdefault(enc, {})[view] = {
                    "k": int(k),
                    "neighbourhoods": {str(c): sorted(e_of[a] for a in arch if home[a] == c) for c in sorted(set(lab))},
                    "Q1_rewrites_stay_home": stay, "Q1_pass": stay >= 12,
                    "Q2": q2, "Q2_pass": q2[own_ref]["pass"],
                    "Q3_mantel_archive": {"rho": rA, "p": pA}, "Q3_mantel_cases": {"rho": rC, "p": pC},
                    "Q4_largest_share": round(largest, 2), "Q4_collapsed": collapsed,
                    "qualifies": stay >= 12 and q2[own_ref]["pass"] and not collapsed,
                }
            la_c, lc_c = labels[(how, enc, "concept")]
            la_i, lc_i = labels[(how, enc, "intent")]
            out["concept_vs_intent"].setdefault(how, {})[enc] = {
                "Q5_ari_archive": round(float(adjusted_rand_score(la_c, la_i)), 3),
                "Q5_ari_cases": round(float(adjusted_rand_score(lc_c, lc_i)), 3)}

    # Readings, as fixed in PROTOCOL.md: must hold in the primary encoder and at least one other (centred).
    R = out["results"]["centred"]
    Q5 = out["concept_vs_intent"]["centred"]

    def holds(pred):
        return pred(PRIMARY) and any(pred(e) for e in ENCODERS if e != PRIMARY)

    q = lambda e, v: R[e][v]["qualifies"]  # noqa: E731
    rho = lambda e, v: R[e][v]["Q3_mantel_archive"]["rho"]  # noqa: E731
    readings = []
    if holds(lambda e: q(e, "intent") and rho(e, "intent") < rho(e, "concept")):
        readings.append("intent qualifies and is less tied to the axes than concept: intent as main coordinate")
    if holds(lambda e: q(e, "intent") and q(e, "concept") and Q5[e]["Q5_ari_archive"] < 0.5):
        readings.append("both qualify and disagree: two addresses (purpose and idea)")
    if holds(lambda e: q(e, "intent") and q(e, "concept") and Q5[e]["Q5_ari_archive"] >= 0.5):
        readings.append("both qualify and largely agree: use the one with lower Q3 rho; tie goes to intent")
    if holds(lambda e: not q(e, "intent")):
        readings.append("intent fails or collapses: concept stays the coordinate; intent as wording only")
    best_single = lambda e: max(R[e]["concept"]["Q2"]["idea_families"]["ari"], R[e]["intent"]["Q2"]["purpose_families"]["ari"])  # noqa: E731
    if holds(lambda e: q(e, "idea") and max(R[e]["idea"]["Q2"][r]["ari"] for r in R[e]["idea"]["Q2"]) > best_single(e)
             and rho(e, "idea") <= min(rho(e, "concept"), rho(e, "intent"))):
        readings.append("idea qualifies and beats both singles: one combined coordinate")
    out["readings"] = readings or ["no pre-set reading holds in the primary encoder plus one other"]

    dest = HERE / "results/scores_p06.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
