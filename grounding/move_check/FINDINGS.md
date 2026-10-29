# Move check: does key-move text track its decisions better than idea text tracks the whole record?

Date: 2026-10-29. Inputs: `texts.json` (54 key moves and 15 idea texts from the seeds of runs 01–03). Embeddings: four local encoders (config p01-enc-v1). Analysis: `analyze.py`, Mantel item-permutation test. Results: `results.json`.

| Text | nomic | mxbai | bge-m3 | qwen3 | TF-IDF wording (control) |
|---|---:|---:|---:|---:|---:|
| Idea (concept + intent) vs whole record | 0.10 (p 0.23) | 0.10 (p 0.27) | **0.37** (p 0.0002) | 0.07 (p 0.27) | 0.30 (p 0.003) |
| Key move vs its decisions | **0.37** | **0.37** | **0.37** | **0.45** | 0.33 (p 0.001) |
| Key move, pairs across seeds only | 0.39 | 0.39 | 0.39 | 0.47 | – |

Values are Spearman ρ between text distance and decision-signature distance. All move-level p ≤ 0.0003, the floor for 2,999 permutations.

## Reading

- **Moves ground more consistently than ideas.** All four encoders track a move's decisions; only bge-m3 tracks the idea text against the whole record. The effect holds across seeds, so it is not just moves from the same seed resembling each other.
- **Much of it is wording.** Plain word overlap reaches ρ 0.33 on moves, because move text names the programs it places ("holds the office, care and library"). The encoders add little above that, except qwen3 (0.45).
- **The idea text carries structure mostly through words too.** TF-IDF wording (0.30) beats three of the four encoders on idea text; only bge-m3 matches it. So the meaning signal in idea text, beyond shared vocabulary, is weak.

## Implication

- The moves view is a stronger bridge to the axes than the idea view, but mainly because moves *name* their decisions. It is a lexical bridge, not yet evidence of deeper semantic grounding.
- This fits the agreed roles. The idea view is for meaning and steering, not for locating structure; the axes locate structure.
- It supports keeping the moves view as a recorded view in Pilot 4, and a later steering test if Pilot 4 shows steering helps.
- Small sample: 15 seeds, 54 moves; moves from the same seed are not independent.
