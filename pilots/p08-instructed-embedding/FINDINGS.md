# Pilot 8 findings: does a task instruction make the embedding ignore register?

Date: 2026-11-03.
- Protocol: [PROTOCOL.md](PROTOCOL.md).
- Scores: `results/scores_p08.json`, from `scripts/score_p08.py`, which was fixed and dry-run on the uninstructed vectors (reproducing every baseline) before the embeddings arrived.

## In one line

**No. The declared reading is "C1 fails: do not use the instruction."** The instruction barely moves the twins (1 → 2 of 18) and blurs the seed families (ARI 0.53 → 0.32).

## Declared results (qwen3-embedding:4b, uncentred)

| Measure | Uninstructed baseline | Instructed | Bar |
|---|---:|---:|---|
| **T:** twins whose nearest seed is their twin | 1/18 | **2/18** | ≥ 9/18 |
| **C1:** original seeds vs idea families | 0.53 | **0.32** (p 0.009) | ≥ 0.40 |
| C2a: cases with a seed as nearest neighbour | 0/40 | 0/40 | reported |
| C2b: ARI(clusters, batch) | 0.18 | 0.60 | reported |
| T with the re-expressed seeds | 3/18 | 1/18 | reported |

## Post hoc (after the declared result)

Twins whose nearest seed is in their twin's **family**, rather than being the twin itself:
- uninstructed 5/18;
- instructed 8/18;
- chance about 4.

The instruction shifts the twins slightly toward the right family, but not toward the right strategy, and not enough to place them.

## Reading

Telling the encoder to ignore wording does not make it ignore wording. Register stays in the vectors, and the instruction costs idea separation among the seeds. As planned, the next step is the **canonical describer**: control the input text itself rather than the encoder.
