# Pilot 01b — Do concept embeddings represent strategic similarity?

Status: **locked 2026-10-28** before any label or embedding; **revision p01b-v1.1** recorded below. Changes create `p01b-v2` and apply to new runs only.

## Question

Pilot 01 embedded placement-style rationale text and found it followed wording, not strategy. That did not test the semantic idea. Pilot 01b embeds the **concept** written by the generating LLM at generation time (seed format v2.0) and asks: does concept similarity match the architect's judgment as well as structure does, and does it capture what structure misses?

## Materials

- Pool: 15 seeds from three independent generation runs of the same message (`benchmarks/test-elementary-v0.1/seeds_v2/cases/`), all schema-valid with 0 checker errors; run 01 coherence-reviewed by the user (4 coherent, 1 minor). Case IDs `R1-S01` … `R3-S05`.
- Texts per case (`data/descriptions.jsonl`, built by `scripts/build_p01b.py`):
  - `concept` — the seed's concept, verbatim.
  - `concept_intent` — concept followed by intent, verbatim.
  - `struct` — placements and links rendered by code, for comparison with Pilot 01.
- Encoders and settings: unchanged from Pilot 01 (`p01-enc-v1`).

## Ground truth: blind triplets

16 items: 4 `cross_run`, 8 `disagree`, 2 `control`, 2 repeats. The labeler sees, for every scheme, the diagram, the concept, the intent and the structure line, and picks the closer architectural strategy (or about equal / can't judge).

Selection rule, fixed before embeddings (`build_p01b.py`):
- `cross_run`: anchor plus its nearest structural twin from a different run (structure distance ≤ 0.10), against the most concept-wording-similar case that is not a twin. These are independently written versions of the same idea, the natural paraphrase test.
- `disagree`: structure distance and concept wording (TF-IDF) disagree about the closer option; one per anchor, largest margin first.
- `control`: both agree by a wide margin.

## Revision p01b-v1.1 (2026-10-28, after 4 of 16 labels, before any embedding)

The labeler noted that items showed only part of each record. Labeling is now two passes over the same 16 items in the same order:

- **Pass A — concepts only** (`data/labeling_set_concept.json`, page `labeling_page_concept.html`, record `labels_concept`): each scheme shown by its concept alone. Question: which option's concept describes the closer organizing idea. Truth for **fidelity**: does an embedding capture what the concept means?
- **Pass B — whole scheme** (`data/labeling_set_full.json`, page `labeling_page.html`, record `labels_full`): diagram, concept, intent, key moves with their structural references, trade-off, structure line; commitments collapsed; unresolved notes omitted. Truth for **usefulness**: does concept meaning predict overall strategic closeness?

The gate below is decided on Pass B. Pass A diagnoses a failure: an encoder that fails Pass A cannot read the concepts; one that passes A but fails B shows that concepts alone do not carry the strategy. Agreement between the labeler's own A and B answers shows how much the concept drives the overall judgment.

The 4 labels saved under v1 (partial view) are kept in `labels/v1_partial_view_labels.json` and not scored. The labeler judged prior exposure to those diagrams negligible for this check. The LLM baseline is re-run on the Pass B set; the v1 baseline is kept as `labels/llm_labels_v1_partial.json`.

## Predictors

- Structure proxy (grouping, floors, links distance).
- Concept-wording proxy (TF-IDF on concept text).
- Each encoder × `concept`, `concept_intent`, `struct`.
- LLM baseline: a fresh assistant given only the blind labeling set.

## Decision gate (fixed now)

Decided on decisive, stable labels. "Best concept" = best encoder on `concept` or `concept_intent`.

- **SEMANTIC SUPPORTED:** best concept ≥ 70% overall, ≥ the structure proxy overall, and ≥ 3 of 4 `cross_run` items (it recognises the same idea written independently).
- **COMPLEMENTARY:** best concept below the structure proxy overall, but right on at least half of the items where the structure proxy is wrong. Then Pilot 2 combines both, with structure primary.
- **NOT SUPPORTED:** best concept < 60% overall, or not better than the concept-wording proxy. Then the boundary is built on explicit decisions; concepts stay as descriptions.

With about 12–14 decisive items, one item is roughly 7–8 points. The gate selects a direction for Pilot 2; it does not validate a method.

## Known issues

- Concepts call the Media Center a "library"; the generation message was kept unchanged across runs so the pool stays comparable.
- Generator, probe-free item selection and LLM baseline all involve the same model family (Claude Opus 5.5).
- Diagram block width carries no meaning; the labeler read it as size once in Pilot 01.

## Lock record (SHA-256)

| File | Hash |
|---|---|
| `data/descriptions.jsonl` | `1191cdbf9a04a03c44cbb6ca95ac688031e86c4c0454efaf4fcc84fac748e997` |
| `data/triplets_SEALED.json` | `165054d36c2847c0243f5d32ee7fb8d4775532ef2bb15c107349d43ca73d40c7` |
| `data/labeling_set.json` | `1a5e415925257a36129de3f8b03d04969b5e99462bae21eed0ed4523c693d7d2` |
| `data/diagram_data.json` | `185db4f1f7b696d164c0871469faed1b1bd75a82b2e5d66559b45c4ede440e8c` |
