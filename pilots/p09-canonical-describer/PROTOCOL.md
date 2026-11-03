# Pilot 9: does a canonical, archive-blind describer make the meaning address work?

Declared 2026-11-03, before any description is generated. Agreed with the architect the same day.

## Why

Pilot 7 found that the meaning address measures the **register** a text was generated in. Pilot 4's cases avoided the archive's vocabulary, so structural twins land far from their seeds. Pilot 8 showed the encoder cannot be instructed to ignore register. The remaining root-level fix is to control the **input text**: describe every item for the map with one fixed prompt, in one register, without the archive. Generation and description become separate steps in the method.

**Process rule.**
- Task: Task 2 (embedding representation).
- Depends on: Pilots 5–8, done.
- Blocks: map v0.1.

## Describer

- **Prompts:** `prompts/DESCRIBE_1–4.txt`, built by code.
- **Items:** all 55 (15 seeds and 40 Pilot 4 cases), shuffled with seed 20261103 and given anonymous IDs X01–X55. The key is sealed in `data/item_key_SEALED.json`. They are split 14/14/14/13 into four chats.
- **What the describer sees for each item:** its own concept, intent, key moves (move and serves) and structure. It sees no name, no archive and no other context.
- **Rules:**
  - a fixed glossary of terms for parts, program and relations, with no synonyms;
  - concept 40–60 words, intent 20–35 words starting "Aims to";
  - no comparison or contrast words;
  - no run of four or more words copied from the original;
  - no evaluation or metaphor;
  - agreement with the structure.
- **Host:** ChatGPT, four fresh temporary chats, medium effort. Replies are saved raw; only formatting artefacts are removed.

**Checks on the replies (reported):**
- 55/55 IDs and word counts;
- banned contrast words;
- the share of descriptions containing a copied 4-word run from their original;
- the per-item glossary hit rate.

## Embedding

- Concept and intent descriptions are each embedded (110 texts) with the four installed encoders, no instruction (`local/RUN_P09.bat`).
- The representation is the map's: concept and intent each normalised, concatenated ÷ √2. **Uncentred:** with one register for all items, no correction should be needed.
- qwen3-embedding:4b is primary. A criterion holds only if it holds in qwen3 4b **and** in at least one other encoder.

## Ground truth

The 18 structural twins: Pilot 4 cases whose weighted structural change to their nearest seed is below 1.0. Their twin is that seed.

## Criteria

| # | Measure | Baseline (original texts, qwen3, uncentred) | Bar |
|---|---|---|---|
| **T** (primary) | Twins whose nearest seed is their twin (chance about 1.2/18) | 1/18 | **≥ 9/18** |
| **C1** | Described seeds' neighbourhoods (k by silhouette 3–8) against the idea families (ARI) | 0.53 | ≥ 0.40, permutation p < 0.05 |
| C2a (reported) | Cases with a seed as their overall nearest neighbour | 0/40 | about 11 if there were no batch effect |
| C2b (reported) | ARI(clusters, seed/case), k by silhouette 3–12 | 0.18 | ≤ 0.10 would mean no batch structure |
| T-fam (reported) | Twins whose nearest seed is in the twin's family (chance about 4) | 5/18 | – |

**Baselines in all encoders** (dry run of `scripts/score_p09.py` on the original texts, before any description exists):

| Encoder | T | T-fam | C1 | C2a | C2b | Q3 ρ |
|---|---:|---:|---:|---:|---:|---:|
| qwen3 4b | 1 | 5 | 0.53 | 0 | 0.18 | 0.11 |
| mxbai | 4 | 6 | 0.50 | 0 | 0.81 | 0.13 |
| nomic | 3 | 4 | 0.01 | 1 | 0.24 | 0.14 |
| bge-m3 | 2 | 4 | 0.39 | 0 | 0.54 | 0.15 |

**Pass** = T and C1, each in qwen3 4b plus one other encoder.

## Readings, fixed now

| Outcome | Reading | Next |
|---|---|---|
| Pass | Describing every item in one canonical register makes the address work | The describer becomes a method step. Map v0.1 is built on the described texts. Format v3.2 also adds the glossary and drops "differ in wording" from generation |
| T 5–8 | The describer helps but does not place strategies reliably | Use described texts for the family level only; test the questionnaire representation for the strategy level |
| T < 5 | Even a canonical register does not place strategies | Questionnaire representation (categorical answers about idea and aims) as the meaning side |
| C1 fails | The describer flattens real differences between ideas | Revise the describer (looser glossary) before anything else |

## Limits

- One describer model; 18 twins.
- The structural twins are defined by the architect's weights. Two cases can be the same strategy structurally yet carry different intents, so a perfect T is not expected.
- The describer sees structure, which could make descriptions track structure too closely. Pilot 6's Q3 (Mantel correlation with the axes) is reported on the described texts to show this.
