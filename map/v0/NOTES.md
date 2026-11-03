# Map v0: build notes and problem found (2026-11-03)

Status: **draft. Built as defined in [../README.md](../README.md), but the meaning address does not hold on the full item set.** Data: `map_v0.json`. Not for use in a loop until resolved.

## What works

- **Centring mixes the batches.** Seeds and Pilot 4 cases share 7 of 12 neighbourhoods. Without centring, the best clustering has 3 neighbourhoods and only 1 of them mixes: the clusters follow the writer/format, not the idea.
- **Axis side and co-location** work as intended:
  - 25 of 72 cells hold a texted idea;
  - 20 cells hold valid code-generated structures but no idea yet;
  - 13 cells are reached by one neighbourhood only.
- **Pilot 4 re-read (diagnostic):** A and J reach 10 new cells each, U 4, S 5. J has the most cases (4) in neighbourhoods that contain no seed.

## Problem 1: no natural neighbourhoods across all 55 items

- The silhouette is 0.05–0.09 for every k and keeps rising up to k = 20, in all four encoders. "Best k" (12, the top of the declared range) is arbitrary.
- The 40 cases form no clusters among themselves either (silhouette about 0.08).
- With all 55 items, the seed families are recovered poorly (ARI 0.17–0.41 by k), against 0.59–0.88 when the 15 seeds are clustered alone.
- The encoders disagree (ARI about 0.3).

**Partly expected.** The 15 seeds hold about 8 ideas repeated across three runs, so they cluster. The Pilot 4 cases were each told to differ from everything. Pilots 5–6 therefore validated that the embedding **groups repeated ideas**, which is what saturation detection needs. They did not show that diverse, non-repeating ideas form neighbourhoods.

## Problem 2: meaning barely transfers across writer and format

After centring:
- every one of the 40 cases is less similar to its nearest seed family (median 0.10) than every seed is to its own family (median 0.66; minimum 0.44);
- 35 of 40 cases have another case, not a seed, as their nearest neighbour.

**Keyword sanity check** (crude, small n): cases whose concept uses a family's own words lean toward that family only slightly. The words are "hinge", "gateway", "courtyard", "free-standing" and "pavilion". Similarity is 0.06–0.09 against about −0.02 for the others, in qwen3, bge-m3 and mxbai. The direction is right; the size is too small to place a case.

So the seeds (seed format v2, written by the architect's earlier advanced-model runs) and the cases (format v3.1, written by ChatGPT under directed prompts) do not share a usable meaning frame, even after centring. Pilot 5's rewrites stayed home because they kept the same idea and the same concept-only format; the cases differ in both writer and format.

## Implication

The map's meaning address is reliable **within one writer and format**. Across them, it needs either one shared format for every item on the map, or a calibrated way to bridge formats. The loop will produce format v3.1 from one model, so the cleanest fix is to re-express the archive in that same format and writer, then re-test whether cases that share an idea land with their family.
