# Pilot 01b findings — concept embeddings

Date: 2026-10-28. Protocol: p01b-v1.1. Scores: `results/scores_user_labels_full.json` (Pass B, decides the gate) and `results/scores_user_labels_concept.json` (Pass A, diagnostic only).

## Result in one line

Concept embeddings carry some strategic signal, but it is inconsistent across encoders and no concept variant met the pre-registered bar for leading the space. One combination, bge-m3 on concept + intent, matched structure overall and was right on all three items structure got wrong, which is the pattern the gate calls complementary. Embeddings of code-written structure scored highest again.

## Pass B — whole scheme (11 decisive items)

| Predictor | cross_run (4) | disagree (6) | control (1) | All (11) |
|---|---:|---:|---:|---:|
| Structure proxy | 4 | 3 | 1 | **8** |
| LLM baseline | 4 | 3 | 1 | 8 |
| Concept wording (TF-IDF) | 3 | 3 | 1 | 7 |
| bge-m3 · concept | 3 | 3 | 1 | 7 |
| **bge-m3 · concept + intent** | 2 | 5 | 1 | **8** |
| mxbai · concept | 4 | 2 | 1 | 7 |
| mxbai · concept + intent | 4 | 1 | 1 | 6 |
| nomic · concept / concept + intent | 2 / 3 | 2 / 2 | 1 / 1 | 5 / 6 |
| qwen3 · concept / concept + intent | 3 / 3 | 2 / 2 | 1 / 1 | 6 / 6 |
| bge-m3 · struct | 4 | 4 | 1 | **9** |
| qwen3 · struct | 4 | 5 | 0 | **9** |

Excluded: C05 (inconsistent with its repeat C15); 2 items labeled "about equal".

The structure proxy was wrong on C07, C09 and C12. On those three, bge-m3 concept + intent was right on 3, the struct embeddings on 2, and the LLM baseline and other concept variants on 1.

## Gate (fixed before results)

- **SEMANTIC SUPPORTED — not met.** The only concept variant at ≥ 70% (bge-m3 concept + intent, 8/11) ties the structure proxy but recognised only 2 of 4 cross-run twins (the bar was 3). The variant that recognised all four twins (mxbai concept) scored 7/11.
- **COMPLEMENTARY — met in substance, with a gap in the wording.** The rule was written for a concept variant *below* structure overall; bge-m3 concept + intent *ties* it while being right on all three items structure misses. That is the complementary pattern; the tie case was not anticipated in the rule's wording.
- **NOT SUPPORTED — not met.** Best concept is above 60% and above the concept-wording proxy.

Reading: **complementary, weakly**. Pilot 2 should keep structure primary and test whether adding a concept signal helps.

## Why "weakly"

- The complementary variant was one of eight concept predictors (4 encoders × 2 variants). Picking the best of eight after the fact favours chance; the other three encoders on concept + intent scored 6/11 each.
- Concept results flip between variants: bge-m3 gained two disagree items and lost two cross-run twins when intent was added.
- Eleven items; one item is 9 points. The three items structure missed are three items.

## Pass A — concepts only (diagnostic)

The labeler judged Pass A less reliable: a single keyword sometimes decided an answer. With that caveat:

- The concept-wording proxy matched Pass A on only 3 of 12, so concept-only reading did not follow word overlap.
- The structure proxy matched 8 of 12: reading only the concepts, the labeler often recovered the structural answer, which suggests the concepts do describe their structure.
- Best encoders on Pass A: qwen3 struct 9/12, mxbai concept 8/12.
- The labeler's own Pass A and Pass B answers agreed on 6 of 11 items decided in both, so the concept alone often points somewhere other than the whole scheme.

## Findings across Pilots 01 and 01b

1. Structure carries most of what the architect judges: the structure proxy scored 8/10 (Pilot 01) and 8/11 (Pilot 01b).
2. Embeddings of code-written structure did as well or slightly better: 7/10 and 9/11.
3. Concept text written by the generating LLM is a meaningful description, unlike Pilot 01's placement prose, but as an embedding it does not reliably beat structure. Its possible value is on the items structure misses.
4. Asking an LLM directly matched structure, never beat it: 4/8 and 8/11.
5. Repeated generation returns about eight recurring organizing ideas across 15 seeds; breadth must come from Step 03 variation, not more seeds.

## Implication for Pilot 2

Membership and distance should be built on explicit decisions (the structure), with a concept signal tested as a secondary term on new items, for example structure distance adjusted by bge-m3 concept + intent similarity, and judged only on items not used to choose it.

## Limits

Small item counts; one labeler; generator, item construction and LLM baseline from one model family; diagrams in Pass B show structure and may tilt judgments toward it; concepts use "library" for the Media Center.
