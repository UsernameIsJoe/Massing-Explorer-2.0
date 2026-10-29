# Pilot 4 findings: embedding-guided exploration

Date: 2026-10-29.
- Plan: [PLAN.md](PLAN.md). Scoring rules, fixed before scoring: [SCORING.md](SCORING.md).
- Scores: `results/scores.json`. Replies: `replies/clean/R1–R8` (format v3.1).
- Generator: ChatGPT temporary chats, medium effort, 8 chats × 5 cases.

## In one line

The pre-registered decision **cannot be made**: the meaning yardstick failed its own calibration, so "new strategy" is 0 in every arm. Three other things are clear:
- format v3.1 makes the structure readable from text;
- axis steering lands where it is aimed;
- the joint arm leads axis-only on structural novelty by the pre-set margin (5 vs 3). That last result is exploratory and on 10 cases per arm.

## 1. Primary measure: not decidable

| Arm | New strategy (primary) | Incl. declared | Concept view | Secondary judge (qwen3 4b) |
|---|---:|---:|---:|---:|
| U unguided | 0 | 0 | 0 | 0 |
| A axis gaps | 0 | 0 | 0 | 0 |
| S semantic | 0 | 0 | 0 | 0 |
| J joint | 0 | 0 | 0 | 0 |

The cause is the yardstick, not the arms. In every encoder, rewording a concept moves it farther than switching to a different accepted strategy does:

| Encoder | Rewrite → own original (median) | Threshold (95th pct) | Archive seed → nearest other seed (median) | Seeds that would count as "new" vs each other | Rewrite nearest its own original |
|---|---:|---:|---:|---:|---:|
| mxbai | 0.183 | 0.203 | 0.137 | 2/15 | 8/15 |
| nomic | 0.131 | 0.161 | 0.090 | 0/15 | 7/15 |
| qwen3-embedding 4b | 0.277 | 0.343 | 0.187 | 0/15 | 11/15 |
| bge-m3 (steering; check only) | 0.239 | 0.289 | 0.159 | 0/15 | 10/15 |

Rewrites still tend to sit *nearest* their own original: qwen3 4b manages 11/15, the best judge here, and Pilot 01c's bar is 12. Yet they sit *far* from it in absolute terms. So distance carries a large offset for writer, style and format, and meaning is mostly in the *ranking*.

The new cases come from a different writer and format than the archive. Their distance to the archive (qwen3 median 0.275) is about the paraphrase offset (0.277). An absolute "paraphrase threshold" therefore cannot separate a new idea from a restyled old one.

**Reading:** this pilot neither supports nor refutes embedding steering. It shows that whole-concept embedding distance, judged against a fixed threshold, is not a usable novelty judge across writers or formats. This fits Pilot 01c, where the encoders were weak on paraphrase, and the move check, where the meaning signal was largely lexical.

## 2. Exploratory results (not the decision rule)

| Arm | New in structure (≥ 1.0 from archive and earlier same-arm) | Mean change to nearest seed | Steering hit | New axis cells reached | Valid / declared |
|---|---:|---:|---:|---:|---:|
| U | 3 | 1.08 | – | 4 | 10 / 0 |
| A | 3 | 1.31 | 10/10 | 10 | 10 / 0 |
| S | 5 | 0.95 | 3/10 | 4 | 8 / 2 |
| J | 5 | 1.23 | 9/10 | 10 | 10 / 0 |

- **Axis steering works as a manipulation.** A and J land in the target gap 10/10 and 9/10. J does so while also being told which ideas to avoid.
- **Semantic-only steering is weak as a manipulation:** 3/10 by the bge-m3 check. Its two rule breaks (empty middle floors, both declared) trip the pre-set validity guardrail for S.
- **J vs A on structure: 5 vs 3**, which equals the pre-set margin of 2. A coarse gap can be reached with a small weighted change, which is why A hits 10/10 gaps but only 3 new structures; J's semantic context seems to push the arrangement farther. With 10 cases per arm, this is a signal to test at scale, not an effect.
- **Meaning spread within an arm** (nearest other case, idea view) is similar across arms. J > A under all three judges (mxbai 0.109 vs 0.095; nomic 0.083 vs 0.066; qwen3 0.233 vs 0.222), and U is about as spread as J. All 40 cases share one writer and format, so this within-pilot comparison has no style offset, but the differences are small.

## 3. Format v3.1: the text now carries the structure

Text–record agreement uses the llama3.1:8b extractor, the modal answer of 3 samples, and the same 40 cases read two ways:

| Trait group | concept + section_intent + program_stance | concept + intent (Experiment 1 text) |
|---|---:|---:|
| All 19 questions | **0.56** | 0.22 |
| Special education placement | **0.85** | 0.18 |
| Storeys per mass | **0.84** | 0.35 |
| Floors per department | **0.52** | 0.18 |
| Links | 0.67 | 0.55 |
| Other placements | 0.34 | 0.03 |

- This is a within-case comparison, so the gain is the format's, not the cases'.
- Special education and storeys, which Experiment 1 found expressible but not carried, are now carried.
- Placement of the smaller departments (art, media, medical, custodial, administration) remains weak, because the 20–40-word fields name only academic, special education, administration and the commons.
- Agreement by arm (v3text): U 0.62, A 0.49, S 0.54, J 0.61. J is not worse than A, so the agreement guardrail holds.

## What this means for the project

1. **The grounding half of the core contribution works on the axes we tested.** Text that states the section and program stance can be read back onto the axes. This is the "structured record anchors every proposal" side.
2. **The steering half is still untested.** The embedding was never shown to fail. The pilot showed that the judge was miscalibrated.
3. **The blind check is not needed now.** It could only veto a win, and there is no primary win to veto.

## Next steps (proposed, not started)

1. **Fix the meaning yardstick before any further steering pilot.** Candidate judges, to be checked on data already in hand, so the architect's time is not needed:
   - *rank-based:* is a case's nearest neighbour an archive case or a same-batch case, relative to paraphrases;
   - *style-matched calibration:* paraphrase thresholds built from cases of the same writer and format;
   - *meaning at the level of moves,* which tracked decisions best in the move check.

   The fix succeeds if the archive's 15 seeds count as distinct from each other and their rewrites do not.
2. **Then re-score these same 40 cases with the fixed yardstick.** Generating new cases is not needed for that.
3. If J still leads A, scale up as PLAN.md says: more chats and a second model.
