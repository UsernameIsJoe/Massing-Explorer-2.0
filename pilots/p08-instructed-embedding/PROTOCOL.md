# Pilot 8: does a task instruction make the embedding ignore register?

Declared 2026-11-03, before any instructed embedding exists. Agreed with the architect the same day.

## Why

Pilot 7 found that the meaning address measures **register**, not only meaning. The Pilot 4 cases were shown the archive and told to differ, so they avoided its vocabulary. As a result, cases that are structurally the same strategy as a seed still land far from it.

qwen3-embedding:4b accepts a task instruction, and every embedding so far was made without one. This is the cheapest possible fix: one local run, no ChatGPT.

**Process rule.**
- Task: Task 2 (embedding representation).
- Depends on: Pilots 5–7, done.
- Blocks: the canonical describer test (needed only if this test fails) and map v0.1.

## Inputs (all existing texts; `local/texts.json`, 140 texts)

| Set | Texts |
|---|---|
| Original seeds | 15 concepts (seed format v2), 15 intents |
| Re-expressed seeds (Pilot 7) | 15 concepts, 15 intents |
| Pilot 4 cases | 40 concepts, 40 intents |

**Instructions** (`local/instructions.json`; same template for every text of a view):
- **concept:** "Instruct: Represent the organizing architectural idea of this school massing strategy (how its parts are arranged and related), ignoring wording and writing style\nQuery: " + text
- **intent:** "Instruct: Represent the aims of this school massing strategy (what it tries to achieve and for whom), ignoring wording and writing style\nQuery: " + text

**Encoder:** qwen3-embedding:4b only. It is the only instruction-aware encoder installed, so the "primary plus one other encoder" rule cannot apply here. This is a stated limit.

**Representation:** as decided for the map. Concept and intent are each normalised, then concatenated ÷ √2. Uncentred, so writer or register offsets are not removed by correction.

## Ground truth: the 18 structural twins

These are the Pilot 4 cases whose weighted structural change to their nearest archive seed is below 1.0, the architect's bar for "the same strategy". Their twin is that seed.

## Criteria

| # | Measure | Baseline, uninstructed (measured 2026-11-03 before this declaration) | Bar |
|---|---|---|---|
| **T** (primary) | Twins whose nearest **seed** is their twin (chance about 1.2 of 18) | original seeds 1/18; re-expressed seeds 3/18 | **≥ 9/18 with the original seeds** |
| **C1** | ARI of the original seeds' neighbourhoods (k by silhouette, 3–8) against the idea families | 0.53 uncentred (dry run on the uninstructed vectors, which reproduced every baseline above) | ≥ 0.40, permutation p < 0.05 |
| C2a (reported) | Cases with a seed as their overall nearest neighbour | 0/40 | – |
| C2b (reported) | ARI(clusters, seed/case batch), k by silhouette 3–12 | 0.18 | – |
| T-re (reported) | T with the re-expressed seeds | 3/18 | – |

**Pass** = T and C1.

## Readings, fixed now

| Outcome | Reading | Next |
|---|---|---|
| Pass | The instruction makes the address robust to register | Map v0.1 with instructed qwen3 embeddings. Format v3.2 still adds the glossary and drops "differ in wording", as prevention |
| T improves (≥ 5/18) but below 9 | The instruction helps, but not enough | Canonical describer, embedded with the instruction |
| T < 5/18 | The instruction does not change register sensitivity | Canonical describer, as proposed after Pilot 7 |
| C1 fails | The instruction blurs real idea differences | Do not use the instruction |
