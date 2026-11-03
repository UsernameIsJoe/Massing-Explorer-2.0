# Pilot 5: is a meaning neighbourhood a reliable address?

Declared 2026-11-03, before computing anything. Agreed with the architect the same day.

## Why

The joint map ([CORE_CONTRIBUTION § Key highlights](../../docs/CORE_CONTRIBUTION.md#key-highlights-the-joint-map-and-the-exploration-loop-architect-2026-11-03)) gives every idea two addresses: a meaning neighbourhood and an axis cell. Pilot 4 showed the embedding cannot tell individual strategies apart. It never tested the coarser level the map needs. If neighbourhoods are unstable, the journey record, saturation detection and "avoid / borrow" guidance all fail.

**Process rule.**
- Task: Task 2 (embedding representation), at neighbourhood resolution; open decision 1 (plan §8).
- Depends on: Task 1, resolved.
- Downstream (joint map v0, loop pilot) waits on this result.

## Data (all already in the repo; no chats, downloads or PC runs)

Vectors come from `pilots/p04-guided-exploration/scoring/local/embeddings.jsonl`.
- **A:** the 15 archive concepts (`archive:*::concept`).
- **W:** their 15 ChatGPT rewrites from Pilot 01c (`p01c:P*::rewrite`). Each rewrite's home is its original's archive id (`pilots/p01c-robustness/data/rewrite_key_SEALED.json`). The Pilot 01c originals are the same texts as A.
- **C:** the 40 Pilot 4 cases (`case:*::concept`).

The concept view is used throughout, because the rewrites are concepts.

**Encoders.** mxbai, nomic, qwen3-embedding:4b and bge-m3 for criteria 1–3. bge-m3 is excluded from criterion 4, because it built the J arm's context.

## Reference families

`reference/families_claude_v1.json`: Claude's grouping of E01–E15 into 6 idea families, committed before the E-to-archive-id mapping or any result was looked at. The architect reviews it after the run. If the architect amends it, criterion 2 is recomputed and both versions are reported; the architect's version governs.

## Method

1. **Neighbourhoods.**
   - Agglomerative clustering of A: average linkage, cosine distance.
   - k chosen per encoder by the best silhouette over k = 3–8, without consulting the reference.
   - Sensitivity: k = the number of reference families (6).
2. **Assigning a new text** (rewrite or case): nearest neighbourhood centroid by cosine.
3. **Corrections, in this fixed order:**
   - raw;
   - batch-centred: subtract each batch's own mean (A, W, C separately), renormalise, and rebuild the neighbourhoods on the centred A.

## Criteria

1. **Paraphrase stays home:** at least 12 of 15 rewrites are assigned to their original's neighbourhood. This is the Pilot 01c bar.
2. **Families separate:** adjusted Rand index (ARI) between the neighbourhoods and the reference families is at least 0.40, with permutation p < 0.05 (10,000 label shuffles, seed 20261103).

An encoder **passes** when it meets 1 and 2 under the same correction, at the silhouette k. The chosen correction is the first in the order above at which any encoder passes.

3. **Encoder agreement (reported, not gated):** pairwise ARI between the four encoders' neighbourhoods.
4. **Preview of J vs A (reported, no decision).**
   - Use the chosen correction, or raw labelled "unreliable" if nothing passes, with mxbai, nomic and qwen3.
   - A and J share the same 10 axis gaps. For each gap, check whether the A case and the J case land in the neighbourhood of either seed J was told not to rephrase.
   - Also report the distinct neighbourhoods reached per arm (U, A, S, J), and the share landing in the largest archive neighbourhood.

## Readings

| Result | Reading | Next |
|---|---|---|
| At least one encoder passes | The meaning neighbourhood is a usable address | Build joint map v0: 15 seeds, 40 cases and the 1,050-variant pool via axis cells |
| Criterion 1 fails everywhere | The address is unstable to wording | Try the key-move view before any map work |
| Criterion 1 passes, 2 fails | Stable, but not aligned with idea families | Try the key-move view; check whether the neighbourhoods follow topology only |

Limits: 15 seeds hold about 6–8 ideas, so the family check rests on a few groups. The reference is an LLM grouping until the architect reviews it.
