# Pilot 2 — Which membership rule defines the region?

Status: **locked 2026-10-28** before any answer; **revision p02-v1.1** (graded rating) made before any answer was saved.

## Question

Step 03 needs a region around the seeds that contains unseen strategies. Pilots 01–01c established that the explicit structure (grouping, floors, links) is the primary basis for similarity. Pilot 2 asks: **which structural membership rule separates "still this seed's strategy" from "a different strategy" the way an architect does?** Candidates outside the region but brief-valid are the material for provisional expansion later.

## Materials

- Seeds: the five run-01 v2.0 seeds (`R1-S01`…`R1-S05`).
- Candidates (`data/candidates.json`, `scripts/region.py`): every distinct structure within two edits of a seed that passes the representable hard rules (admin on floor 1; gym with dining; floors 1–3, contiguous; ≥753 SF per floor portion; every mass non-empty and stacked from the ground). Edits: move a department (not core academic, gym, dining) to another mass; shift a department one floor; flip a link. **962 candidates.**

## Rules compared

| Rule | Inside if | Admits |
|---|---|---:|
| Strict lock | keeps every decision referenced by moves the seed's core commitments protect | 18 |
| Tolerant lock | breaks at most one such decision | 295 |
| Radius | structure distance to the nearest seed ≤ 0.10 (the cross-run "same idea" level from Pilot 01b) | 669 |

Finding before any answer: the generating LLM's core commitments protect 3–4 of 3–4 key moves in every seed, locking 9–12 of the 12 structural decisions. As generated, the commitments module does not discriminate, so the lock rules are close to "nothing may change".

## Light check (human, about 8 minutes)

26 items (`data/review_set.json`, page `review/review_page.html`, record `membership`): 24 candidates sampled 4 per stratum, plus 2 repeats. Each shows the nearest seed (diagram, concept), the changes in plain words, and the candidate's diagram. Answer (v1.1, at the labeler's request): a **1–5 rating of how different the candidate's strategy is** from the seed's: 1 practically the same scheme, 2 same strategy with a small variation, 3 borderline, 4 different strategy, 5 very different; or can't tell.

| Stratum | Edits from nearest seed | Locked decisions broken | Radius |
|---|---|---|---|
| A | 1 | 0 | in |
| B | 1 | 1 | in |
| C | 2 | 1 | mostly in |
| D | 2 | 2 | in |
| E | 2 | 2 | out |
| F | reached from another seed | 3+ | mixed |

Bar given to the labeler (on the page): "same strategy" means the same organizing idea, a version one would present as "Option 1b", not identical; "different strategy" means the change alters what the scheme is about, a new option. Added 2026-10-28 before any answer was saved.

## Scoring

- **Binary agreement:** ratings 1–2 count as same, 4–5 as different; 3 and can't tell are excluded. Each rule predicts same for candidates it admits. An item whose repeat lands on the other side (same vs different) is dropped. Reported per stratum.
- **Graded agreement:** Spearman correlation between the rating and each rule's continuous score (structure distance for radius; number of locked decisions broken for the lock rules). Shows which measure rises the way the labeler's sense of difference does, and where on it a threshold should sit.
- **Borderline share:** how many ratings are 3, by stratum, as a direct reading of where the boundary is fuzzy.

Optionally, the same 26 items go to the qualified ChatGPT judge; it is structure-biased, which here is not a defect because the rules are structural, but it is reported separately and never replaces the labeler.

## Gate

- The rule with the highest binary agreement becomes the Pilot 3 membership rule, **if** it agrees on ≥ 75% of decisive items. Ties go to the rule with the higher graded correlation, then to the stricter rule.
- If the best continuous measure correlates with the ratings (Spearman ≥ 0.5) but the fixed thresholds misplace the boundary, the threshold is re-set from the ratings and confirmed on a fresh sample.
- If no rule reaches 75%, the answers are used to fit a better rule (for example, which kinds of edit change the strategy), and that rule must be confirmed on a fresh sample before use.
- Concept similarity (bge-m3) is not used here; it enters only if Pilot 3 needs a tie-breaker among structural rules.

## Limits

One labeler, 24 items, generic code edits rather than designed alternatives, and a distance threshold borrowed from Pilot 01b.
