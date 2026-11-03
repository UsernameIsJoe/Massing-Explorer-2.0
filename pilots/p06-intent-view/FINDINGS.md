# Pilot 6 findings: concept, intent, or both as the map's meaning coordinate?

Date: 2026-11-03.
- Protocol: [PROTOCOL.md](PROTOCOL.md).
- Scores: `results/scores_p06.json`, from `scripts/score_p06.py`, which was fixed before the embeddings arrived.
- Inputs:
  - intent rewrites (`responses/`);
  - local embeddings (`local/embeddings.jsonl`): 180 vectors, 45 texts × 4 encoders, all present.

## In one line

**By the pre-set rule, intent fails narrowly, so concept stays the coordinate and intent becomes the wording of guidance.** Intent alone is stable, less tied to the axes than concept in every encoder, and sees something different from concept. It just does not reproduce the purpose families at the bar. **The combined text (concept + intent) matches both the idea families and the purpose families well.** No other view does that, but its pre-set reading did not fire.

## Results (centred, the primary correction)

| Encoder | View | Q1 rewrites stay home (bar 12) | Q2 vs idea families | Q2 vs purpose families | Q3 ρ with axes (archive) | Qualifies |
|---|---|---:|---:|---:|---:|---|
| **qwen3 4b** | concept | 14 | **0.88** | 0.51 | 0.29 | **yes** |
| | intent | 14 | 0.36 | 0.38 | **0.20** | no (Q2) |
| | idea | 13 | 0.77 | **0.72** | 0.30 | **yes** |
| mxbai | concept | 13 | 0.64 | 0.34 | 0.28 | yes |
| | intent | 13 | 0.42 | 0.36 | **0.24** | no (Q2) |
| | idea | 14 | 0.51 | 0.46 | 0.30 | yes |
| nomic | concept | 10 | 0.56 | 0.51 | 0.24 | no (Q1) |
| | intent | 10 | 0.36 | **0.56** | **0.20** | no (Q1) |
| | idea | 12 | 0.29 | 0.31 | 0.17 | no (Q2) |
| bge-m3 | concept | 14 | 0.57 | 0.29 | 0.43 | yes |
| | intent | **15** | 0.25 | 0.37 | **0.29** | no (Q2) |
| | idea | **15** | 0.59 | 0.53 | 0.42 | yes |

- Each view's own reference: concept uses the idea families, intent the purpose families, and idea either.
- ARI bar 0.40 with p < 0.05.
- No view collapsed (Q4: the largest neighbourhood holds 20–40%).
- **Q5, concept vs intent neighbourhoods:** ARI 0.13–0.22 on the archive and about 0 on the 40 cases. **They see different things.**
- **Q3 on the 40 cases** (secondary) is low for every view (0.04–0.17). It does not separate the views.

## What the numbers say

1. **Intent is a stable, meaningful signal, not noise.**
   - Its rewrites reused only 6% of the originals' words (concept rewrites: 16%), yet 13–15 of 15 stayed home in three encoders.
   - So the encoders read intent by meaning, not by wording.
2. **Intent is consistently less tied to the axes than concept:** lower ρ in all four encoders (qwen3 0.20 vs 0.29; bge-m3 0.29 vs 0.43). This is the property that would let it add what the axes lack.
3. **Intent misses the purpose reference narrowly, mostly at the borderlines.** qwen3's intent neighbourhoods are:
   - E01, E09, E15;
   - E08, E10, E11, E14;
   - E02, E04, E05;
   - E06, E07;
   - E03, E12, E13.

   The differences from the reference sit at E13 and E15 (both flagged borderline), E11 and E04. The reference is an LLM grouping of a hard judgment, and it may be the weaker side here. It cannot be changed after the fact.
4. **The combined text gets most of both.** qwen3 idea neighbourhoods are five clean groups of three:
   - E03, E11, E12;
   - E06, E07, E13;
   - E08, E10, E14;
   - E02, E05, E15;
   - E01, E04, E09.

   Its match to the purpose families (0.72) is far above concept (0.51) or intent alone (0.38), at a small cost on the idea families (0.77 vs 0.88).

   Its pre-set reading ("beats both singles on Q2 with no worse Q3") did **not** fire, for two reasons:
   - concept alone matches the idea families better (0.88);
   - its tie to the axes equals concept's (0.30 vs 0.29).

## Reading

- **Declared:** intent fails, so **concept stays the meaning coordinate, and intent is used as the wording of guidance.** The reading holds in qwen3 4b and in mxbai and bge-m3.
- **Not declared, for the architect's decision:** the combined text is the only coordinate that groups strategies by both idea and purpose. Using it would not make the map less tied to the axes than concept. Intent alone is the least tied, but it does not group by purpose well enough to be an address on its own.

## Limits

- 15 seeds.
- Both references are Claude's groupings, accepted by the architect.
- The purpose reference was not blind to the idea families.
- One intent-paraphrase batch from one model.
- Q3 measures independence, not usefulness.
