# Pilot 3 — Expansion: which new strategies enter the region?

Status: **locked 2026-10-28** before any answer.

## Question

The region (Pilot 2) holds each seed's variations: candidates whose weighted change from the seed is below one defining change. Pilot 3 asks which candidates **outside every region** are worth adding as new strategies, so the space grows beyond what the LLM proposed. Admission follows the Step 02–03 plan: an explainable, brief-relevant, meaningfully different possibility; superiority and dimensional feasibility are not required.

## Materials

- Generator (`scripts/expand.py`): two widened edits from each run-01 seed, now including moving core academic and moving gym with dining together; label-free weighted change using the architect's weights (`pilots/p02-region/data/decision_weights.json`), minimum over mass matchings.
- Result: 1,068 valid candidates; 638 inside a seed region; **430 outside every region** (the expansion pool); only 28 of the 430 are within one defining change of a seed from runs 02–03, so about 400 are organizations the generating LLM did not offer in three runs. The pool forms **65 distinct defining-move groups**.
- Review set (`scripts/build_review.py`, `data/expansion_review_set.json`): 20 representatives, 4 per seed, one per group, groups taken largest first with distinct defining departments per seed; each representative is the cleanest member of its group.

## Check (human, about 5 minutes)

Page `review/review_page.html`, record `expansion`. For each new strategy: seed (diagram, concept), the defining change in bold with any other changes, the brief preferences the new strategy gives up, and its diagram. Answer **Add / Maybe / Skip**: is this a brief-relevant strategy worth exploring?

## Outcome

- **Add** and **Maybe** representatives enter region v1 as provisional expansions, each with its group (all members inherit the decision, since they share the same defining move from the same seed), the reason recorded, and Maybe flagged.
- **Skip** groups are recorded as rejected directions with their defining move, so later search does not rediscover them silently.
- Added strategies are then described by an outside model (ChatGPT, temporary chat), concept-level, so every member of the region has a concept like the seeds.
- Summary statistics: share added by defining department and by seed.

## Limits

One reviewer; 20 of 65 groups reviewed; group membership assumes that the same defining move from the same seed means the same decision; feasibility untested.
