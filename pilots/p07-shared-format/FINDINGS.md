# Pilot 7 findings: does one shared writer and format close the gap?

Date: 2026-11-03.
- Protocol: [PROTOCOL.md](PROTOCOL.md).
- Scores: `results/scores_p07.json`, from `scripts/score_p07.py`, which was fixed before the embeddings arrived.

## In one line

**No. The declared reading is "families preserved, but the gap is not format alone: rethink before any map."** Post hoc diagnostics locate the cause: the **vocabulary the Pilot 4 cases were generated in**. They were shown the archive and told to differ "not only in names or wording", so they avoided the archive's words and wrote in a contrastive register. The embedding reads that register as distance.

## Declared results

| Encoder | C1: re-expressed seeds vs idea families (bar 0.40) | C2a: cases with a seed nearest (bar ≥ 8; baseline 0–1) | C2b: ARI(clusters, batch) (bar ≤ 0.10; baseline 0.18–0.81) |
|---|---:|---:|---:|
| qwen3 4b | **0.40** (pass) | 0 | 0.96 |
| mxbai | 0.39 | 0 | 0.88 |
| nomic | 0.01 | 2 | 0.54 |
| bge-m3 | **0.72** (pass) | 0 | 0.75 |

- **C1 passes:** qwen3 4b and bge-m3.
- **C2 fails everywhere**, and the batch separation got stronger than the baseline.
- **Reported:**
  - every re-expressed seed is nearest its own original, 15/15 in all encoders. The re-expression stayed close to the originals: word reuse was 54% for concept and 76% for intent;
  - the keyword lean is still near zero.

## Post hoc diagnostics (after the declared result)

**1. Structural twins.** 18 of the 40 cases are structurally the same strategy as an archive seed (the architect's weighted change < 1.0). With qwen3 4b:
- every one of the 18 is closer to some other case than to any seed;
- its twin seed is the nearest seed for only 3 of them (corrected from 4, 2026-11-03).

Same strategy, same writer (ChatGPT) and same format, yet the texts are far apart. So the gap is not the ideas.

**2. Vocabulary.** Share of texts (concept + intent) using a word, cases against re-expressed seeds:

| Mostly in cases | Cases | Seeds | Mostly in seeds | Cases | Seeds |
|---|---:|---:|---|---:|---:|
| scheme | 0.72 | 0.00 | arts | 0.05 | 0.93 |
| rather / than | 0.68 | 0.00 | library | 0.02 | 0.80 |
| distinct | 0.55 | 0.07 | crown | 0.00 | 0.53 |
| collective | 0.48 | 0.00 | bar | 0.02 | 0.53 |
| activities | 0.52 | 0.00 | masses | 0.02 | 0.40 |

The cases avoid the archive's concrete vocabulary (arts, library, crown, bar) and use a contrastive frame ("… rather than …"). That is what Pilot 4's prompts asked for: the archive was shown, and the instruction was to differ "not only in names, wording or renumbered masses". **Part of how the LLM "differs" is lexical,** and the embedding measures that as meaning distance.

## What this means

1. **Within one generation context, the address works** (Pilots 5 and 6, and C1 here). **Across contexts, it measures register.**
2. **This affects the loop directly.** A loop that shows the LLM the archive and asks for something different will produce texts that look new to the embedding even when the strategy is not: false novelty. The structural-twin check catches this, because the axes are exact.
3. **The re-expression here could not close the gap.** It was given the originals' text and allowed to reuse it, so it carried their register over. It also left the cases' register untouched.

## Root-level fix proposed (for the architect's decision)

A **canonical describer**: every item on the map, seeds and cases alike, is re-described by one fixed prompt in one archive-blind context.
- The describer sees the item's own record and text, never the archive.
- It writes in one fixed register with a controlled vocabulary: plain program names, no contrastive framing.

This separates *generating* an idea, where the LLM may be shown the archive and pushed, from *describing* it for the map, which is neutral and identical for everyone.

**Test (ground truth now available):** after canonical description, the 18 structural twins should land nearest their twin seed. This is in addition to C1 and C2.
