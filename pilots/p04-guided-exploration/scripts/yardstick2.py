"""Yardstick attempt 2 (YARDSTICK.md): same test on llama-restated concepts. Writes results/yardstick2.json.

Usage (from repo root):  python pilots/p04-guided-exploration/scripts/yardstick2.py
"""
import collections
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
import score_p04 as s  # noqa: E402
import yardstick as y  # noqa: E402


def main():
    E = collections.defaultdict(dict)
    for line in (HERE / "scoring/normalize/embeddings_norm.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        E[r["encoder"]][r["text_id"]] = s.unit(r["vector"])
    scores = json.loads((HERE / "results/scores.json").read_text(encoding="utf-8"))
    table, chosen = {}, None
    for how in ["raw", "centred"]:
        for enc in y.JUDGES:
            key, B = y.batches(E, enc, scores)
            table[f"{how}|{enc}"] = y.evaluate(key, y.correct(B, how))
        passing = [e for e in y.JUDGES if table[f"{how}|{e}"]["pass"]]
        if passing and chosen is None:
            chosen = (how, passing)
    out = {"table": table, "chosen": chosen}
    if chosen:
        how, judges = chosen
        P = scores["per_case"]
        new = {}
        for enc in judges:
            key, B = y.batches(E, enc, scores)
            V = y.correct(B, how)
            th = table[f"{how}|{enc}"]["threshold"]
            C_ids, C = V["C"]; _, A = V["A"]
            for i, q in enumerate(C_ids):
                prev = [j for j, p in enumerate(C_ids) if P[p]["arm"] == P[q]["arm"] and P[p]["order"] < P[q]["order"]]
                d = min([float((1 - A @ C[i]).min())] + [float(1 - C[j] @ C[i]) for j in prev])
                new.setdefault(q, []).append(d > th)
        out["rescore"] = {arm: {"new_meaning": sum(all(new[q]) for q in P if P[q]["arm"] == arm),
                                "new_strategy": sum(all(new[q]) and P[q]["validity"] == "valid" and P[q]["new_structure"] for q in P if P[q]["arm"] == arm),
                                "new_strategy_incl_declared": sum(all(new[q]) and P[q]["validity"] in ("valid", "declared") and P[q]["new_structure"] for q in P if P[q]["arm"] == arm)}
                          for arm in s.ARMS}
    (HERE / "results/yardstick2.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in table.items():
        print(f"{k:28} {v}")
    print("chosen:", chosen)
    for arm, v in out.get("rescore", {}).items():
        print(arm, v)


if __name__ == "__main__":
    main()
