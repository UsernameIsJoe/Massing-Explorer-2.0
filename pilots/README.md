# Pilots: status

Read [docs/CORE_CONTRIBUTION.md](../docs/CORE_CONTRIBUTION.md) and [docs/PROJECT_REVIEW_2026-10-29.md](../docs/PROJECT_REVIEW_2026-10-29.md) first.

| Pilot | What it tested | Status |
|---|---|---|
| p01-representation | Embeddings as a **judge of similarity** on placement-style text, against the architect's triplets | **Evidence, historical role.** Still cited: structure beat every text embedding |
| p01b-concept | Concept embeddings as a judge, Pass A and Pass B | **Evidence, historical role.** Weak, complementary on 3 items |
| p01c-robustness | Paraphrase and edit robustness; LLM judges | **Evidence.** bge-m3 is paraphrase-robust; no encoder passes the edit test; the LLM judges lean on structure |
| p02-region | Membership rules from graded ratings | **Partly active.** `data/decision_weights.json` (the architect's weights) remains the user configuration of distance. The membership rules here are superseded |
| p04-guided-exploration | Whether embedding guidance improves LLM exploration (2 × 2: unguided, axis, semantic, joint); output format v3 | **Run 2026-10-29** ([FINDINGS](p04-guided-exploration/FINDINGS.md)): primary undecidable (the meaning yardstick failed calibration); format v3.1 carries structure (agreement 0.56 vs 0.22); J vs A structure novelty 5 vs 3, exploratory. Next: fix the meaning yardstick, re-score the same 40 cases |
| p03-expansion | Structural generator, expansion review, structure-only region | **Partly active.** `scripts/expand.py` (the generator, with hard rules) and `data/pool.json` are in use. The region file is a structure-only candidate, not the region |

The embedding role tested in p01–p01c (judge) is not the role it has in the current direction: a map for steering the LLM. That role is untested.
