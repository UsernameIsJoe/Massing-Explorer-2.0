# Pilot 01c — Robustness checks with known answers and an outside judge

Status: **locked 2026-10-28** before any response or embedding.

## Why

Pilot 01b rested on 11 decisive judgments by one labeler, whose own repeats disagreed once per pass. 01c adds evidence that does not depend on that labeler: two tests whose answers are fixed by construction, and an outside model as a judge, calibrated against the labeler before it may be used at scale.

All outside-model steps use **ChatGPT in fresh chats**, a different model family from the Claude model that generated the seeds. Prompts are in `prompts/`, built by `scripts/build_p01c.py`.

## Test 1 — Paraphrase invariance (fidelity, no rater)

ChatGPT rewrites the 15 v2.0 concepts under opaque, shuffled IDs, keeping the idea and avoiding the original's distinctive words. Each rewrite is embedded and compared with the 15 originals.

- **Hit:** the most similar original is its own source, or a structural twin of it (structure distance ≤ 0.10; the pool contains near-repeats across runs).
- **Reference:** TF-IDF wording similarity on the same texts. If the rewrites succeed in avoiding the original words, wording should do poorly.
- **Pass:** an encoder scores ≥ 12/15 (80%) own-or-twin hits. Chance is about 1–2 of 15.

## Test 2 — Edit sensitivity (no rater)

Code makes 30 variants of the five run-01 seeds: two each with 1, 2 and 3 edits (move a department other than core academic, gym or dining to another mass; or flip one link). ChatGPT writes a concept for all 35 structures (bases included) under shuffled IDs and neutral mass letters, without knowing which are related.

- **Measure:** for each base, Spearman correlation between edit count and embedding distance from the base's concept; and whether level-3 variants are on average farther than level-1.
- **Pass:** mean Spearman ≥ 0.5 and level 3 farther than level 1 for ≥ 4 of 5 bases.

This tests whether concept embeddings move with real structural change when the same writer describes both, not whether edits are architecturally meaningful.

## Test 3 — Outside judge calibration

The 16 Pilot 01b Pass B items are sent to two separate fresh ChatGPT chats.

- **Measures:** agreement with the labeler's decisive, stable Pass B labels (11); agreement between the two runs.
- **Qualifies as a panel judge** if it agrees with the labeler on ≥ 9/11 and with itself on ≥ 13/16 decisive-in-both items. Only a qualified judge may label a larger item set in a follow-up, which would remove the dependence on 11 items.
- Reference: the Claude baseline agreed with the labeler on 8/11.

## Reading

- Tests 1 and 2 pass: embeddings read concepts faithfully; any weakness in Pilot 01b lies in what concepts capture, not in the encoders.
- Test 1 fails: encoders follow wording; concept embeddings are not a sound basis, whatever Pilot 01b suggested.
- Test 3: decides whether a scaled-up judged set is possible without more human labeling.

## Limits

One outside model; edits are generic code operations, not designed alternatives; the rewrite instruction cannot guarantee that meaning was kept (spot-checked by the labeler); concept wording rules differ slightly between the seeds' generator and the describer.
