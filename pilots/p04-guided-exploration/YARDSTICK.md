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
