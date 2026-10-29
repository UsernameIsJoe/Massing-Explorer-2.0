# Fixing the meaning yardstick (declared before computing, 2026-10-29)

**Problem** ([FINDINGS.md](FINDINGS.md) §1): in raw embedding distance, rewording a concept moves it farther than switching to another accepted strategy does. The offset tracks the writer and format, so a fixed paraphrase threshold cannot separate new ideas from restyled ones.

**Data.** Only data already embedded in this run is used.
- **O:** the Pilot 01c originals (15 concepts).
- **W:** their ChatGPT rewrites (15).
- **A:** the archive concepts (15 seeds, format v2).
- **C:** the 40 Pilot 4 case concepts.

The concept view is used throughout, because the calibration texts are concepts.

**Candidate corrections, tried in this fixed order:**
1. **Raw:** cosine distance as before.
2. **Batch-centred:** subtract each batch's mean vector (O, W, A, C separately), renormalise, then take the cosine distance. This removes a shared writer or format offset, but also any shift every case in a batch shares; that loss is accepted as conservative.
3. **Batch-centred plus top component removed:** as 2, then remove the first principal component of the pooled centred vectors.

**Judges:** mxbai, nomic and qwen3-embedding:4b. bge-m3 steered the arms, so it is never a judge.

**Threshold:** for each judge and correction, the 95th percentile of the 15 W-to-own-O distances, as before.

**Pass criteria** (both must hold):
- (a) **Paraphrase:** at least 12 of 15 rewrites have their own original as the nearest O, the Pilot 01c bar.
- (b) **Distinct seeds:** at least 12 of 15 archive seeds lie farther than the threshold from their nearest other seed. That is, accepted different strategies count as new relative to each other.

**Choice:** the first correction in the order above at which at least one judge passes. Every judge that passes at that correction is used, and a case counts as new in meaning only if every passing judge says so. If nothing passes, the yardstick stays unfixed and the 40 cases are not re-scored on meaning.

**Re-score.** New in meaning means farther than the threshold from every archive seed and every earlier same-arm case, under the chosen correction. New in structure, validity and the primary definition are unchanged from SCORING.md.

## Result (computed after the declaration above; `scripts/yardstick.py`, `results/yardstick.json`)

**No correction passes, under any judge.** The yardstick stays unfixed and the 40 cases are **not** re-scored on meaning.

| Correction | Judge | Rewrite nearest own original (bar 12) | Seeds distinct from each other (bar 12) | Paraphrase median | Seed spacing median |
|---|---|---:|---:|---:|---:|
| raw | mxbai | 8 | 1 | 0.183 | 0.169 |
| raw | nomic | 7 | 0 | 0.131 | 0.094 |
| raw | qwen3 4b | 11 | 0 | 0.277 | 0.246 |
| centred | mxbai | **12** | 4 | 0.691 | 0.761 |
| centred | nomic | 9 | 2 | 0.785 | 0.723 |
| centred | qwen3 4b | 11 | 2 | 0.709 | 0.695 |
| centred + PC1 | mxbai | 10 | 2 | 0.731 | 0.836 |
| centred + PC1 | nomic | 9 | 0 | 0.803 | 0.823 |
| centred + PC1 | qwen3 4b | 8 | 2 | 0.800 | 0.784 |

**Reading.** Removing the writer/format offset makes the *ranking* usable: centred mxbai passes the paraphrase test. But the *gap* never opens. Even after correction, a rewording moves a concept about as far as switching to a different accepted strategy does. On this corpus, whole-concept embeddings resolve meaning neighbourhoods, not individual strategies. This is a limit of the semantic representation's resolution, not of the threshold rule.

## Attempt 2: style-normalised restatement (declared before running, 2026-10-29)

**Idea:** remove the writer by having one writer restate everything.
- llama3.1:8b restates each of the 85 concept texts (O, W, A, C) in one fixed three-sentence plain template, at temperature 0 with a fixed seed: `scoring/normalize/run_normalize.py`.
- The restatements are then embedded with the same three judges.

**Corrections, in order:** raw distance on the restatements, then batch-centred.
**Thresholds, pass criteria and choice rule:** identical to attempt 1.
**Possible outcomes:**
- If a judge passes, the 40 cases are re-scored on meaning with it.
- If none passes, whole-concept embeddings are taken to resolve neighbourhoods only, and the axes judge novelty.

Restating can also blur real differences, making seeds look alike; criterion (b) tests exactly that.
