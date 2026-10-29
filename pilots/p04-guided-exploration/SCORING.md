# Pilot 4 scoring: fixed before any scoring output was seen

Written 2026-10-29, after all 8 replies were in and validated, and before the local run. This file adds the operational details that [PLAN.md](PLAN.md) left open; where the two differ, PLAN.md's decision rules stand.

## Pipeline

1. `scripts/build_scoring.py` (container). Gives the 40 cases random IDs (Q01–Q40, `data/blind_map.json`) and writes `scoring/local/texts.json` and `items.json`, hashed in `data/scoring_inputs_lock.json`. It does not read the arm key.
2. `scoring/local/RUN_P04_SCORING.bat` (architect's PC; no new downloads). Embeds every text with mxbai, nomic and bge-m3, then runs the llama3.1:8b extractor.
3. `scripts/score_p04.py` (container). Computes every per-case measure first, then reads `data/prompt_key_SEALED.json` to group by arm. Writes `results/scores.json`.

## Definitions

- **Gym/dining written `[1, 2]`** counts as `[1]` before any structural measure.
- **Validity**, from `replies/clean/R*.validation.json`:
  - *valid:* no errors.
  - *declared:* every error is named in `unresolved`.
  - *undeclared:* anything else.

  For the empty-intermediate-floor error, "named" means an `unresolved` item that mentions an intermediate, second or middle floor or level, an empty, unoccupied or vacant floor, or "between ground". Every match is listed in `declaration_audit`.
- **New in meaning** (primary view: idea = concept + intent). The cosine distance to the nearest archive idea and to every earlier same-arm case must exceed the encoder's threshold, under both mxbai and nomic.
  - The threshold is the 95th percentile of the 15 original-to-rewrite distances from Pilot 01c, re-embedded in this same run.
  - Same-arm order is chat 1 C01–C05, then chat 2.
  - Note: the Pilot 01c texts are concepts only, not concept + intent. So the concept-only view is reported as a sensitivity that matches the calibration exactly.
- **New in structure.** The weighted change (`expand.change`, the architect's weights) to the nearest archive seed and to every earlier same-arm case is ≥ 1.0.
- **New strategy (primary)** = valid AND new in meaning (idea view) AND new in structure.
  - *Secondary:* including declared violations.
  - *Sensitivities:* concept view; novelty against the archive only.
- **Text–record agreement.**
  - The extractor is llama3.1:8b with Experiment 1's first prompt and questionnaire: 3 samples at temperature 0.7, scored by modal answer against the code record (19 questions).
  - Two texts are scored. *v3text* is concept + section_intent + program_stance, the guardrail and the format-v3 check. *idea* is concept + intent, the Experiment 1 text, for comparison.
  - Per case, agreement is the share of questions correct, reported overall and by group: special education placement, placements, links, heights, vertical.
  - The guardrail compares arm means. PLAN.md's "within 1 case" is read as J's mean agreement no more than 0.10 below A's, since one of ten cases fully losing agreement moves the mean by 0.10.
- **Steerability** (diagnostic).
  - *A and J:* does the coarse cell (link pattern × special education's mass × height profile) equal the target gap? Each component is reported too.
  - *S,* by bge-m3 idea distances to the archive:
    - away: the nearest archive case is not one of the listed cases;
    - bridge: both named cases are among the 5 nearest;
    - develop: the named case is among the 3 nearest but farther than bge-m3's paraphrase threshold.
- **Coverage** (diagnostic). Distinct coarse cells reached by valid cases that no archive seed occupies.
- **Views.**
  - Idea, concept, intent, each move (move + serves) and each unresolved item are embedded for every case.
  - The within-arm nearest-neighbour distance per view is analysis only; it plays no part in the decision rule.

## Secondary judge (added 2026-10-29, before the local run)

qwen3-embedding:4b is embedded alongside the others. It is reported as a secondary judge only and never changes the primary measure. Its own paraphrase test (own original nearest, out of 15, against Pilot 01c's bar of 12) comes from the same run. Two sensitivities use it: the new-strategy count with it as the only meaning judge, and with all three judges required.

## Not changed

The arms, decision rule, the bge-m3 exclusion from outcome measures, and the blind-check rules in PLAN.md.
