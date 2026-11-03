# Pilot 6: concept, intent, or both as the map's meaning coordinate?

Declared 2026-11-03, before any intent-only embedding or rewrite exists. Agreed with the architect the same day.

## Why

Pilot 5 validated concept neighbourhoods as an address. The architect noted that concept text is much harder to review than intent text, for a person, an LLM and probably an embedding. Concept text also partly restates the diagram (topology, placements), which the axes already hold exactly. Intent states purpose, which the axes cannot see.

So intent might add more of what the axes lack, which is the condition under which the embedding earns its place ([CORE_CONTRIBUTION § Key highlights](../../docs/CORE_CONTRIBUTION.md#key-highlights-the-joint-map-and-the-exploration-loop-architect-2026-11-03)). The risks are that purposes are widely shared, so the view collapses, or that intents are generic.

**Process rule.**
- Task: Task 2 (embedding representation): which text the map's meaning coordinate uses; open decisions 1–2 (plan §8).
- Depends on: Task 1 (resolved) and Pilot 5 (concept neighbourhoods, done).

## Views

| View | Archive (15) | Rewrites (15) | Pilot 4 cases (40) |
|---|---|---|---|
| **concept** | exists | exists (Pilot 01c) | exists |
| **intent** | new | new (this pilot) | exists |
| **idea** (concept + intent as one text) | exists | new: concept rewrite + " " + intent rewrite | exists |
| **two addresses** (concept and intent kept separate) | derived from the concept and intent results; no new embedding | | |

## Inputs to produce

1. **Intent rewrites.** `prompts/1_REWRITE_INTENT.txt` goes to one ChatGPT temporary chat, medium effort, as in Pilot 01c. P-ids equal E-ids and use the Pilot 01c key. The reply is saved raw in `responses/raw/`. Only formatting artefacts are removed. Rewrites are checked for 15/15 IDs, 20–40 words, and word reuse against the originals, as Pilot 01c did.
2. **Embeddings.** `local/RUN_P06.bat` on the architect's PC embeds the 15 archive intents, the 15 intent rewrites and the 15 idea rewrites with the four installed encoders, using the frozen settings of config p01-enc-v1 plus qwen3-embedding:4b. There are no new downloads.

## Method

- **Neighbourhoods:** exactly as in Pilot 5. Agglomerative clustering, average linkage, cosine distance; k chosen by best silhouette over k = 3–8; new texts assigned to the nearest centroid.
- **Correction:** **batch-centred is primary** (Pilot 5's reading, accepted by the architect when the work proceeded). Raw is reported.
- **Encoders:** all four are reported. **qwen3-embedding:4b is the primary encoder** (best in Pilot 5). A reading holds only if it holds in qwen3 4b **and** in at least one other encoder.
- **Structural distance:** the architect's weighted change (`pilots/p03-expansion/scripts/expand.py`, `change`), symmetrised as the mean of both directions.

## Questions

| # | Question | Measure | Bar |
|---|---|---|---|
| Q1 | Stable? | Rewrites assigned to their original's neighbourhood (archive views) | ≥ 12 of 15 |
| Q2 | Meaningful? | ARI against a reference. concept: the Pilot 5 idea families (architect-accepted). intent: the purpose families (`reference/purpose_families_claude_v1.json`, after architect review). idea: both reported | ARI ≥ 0.40, permutation p < 0.05 (10,000 shuffles, seed 20261103) |
| Q3 | Independent of the axes? | Mantel: Spearman ρ between the view's cosine distance and the weighted structural change, with an item-permutation p (9,999). Archive (15) primary; Pilot 4 cases (40; one writer and format) secondary | No bar. Compared between views: lower ρ means more information the axes lack |
| Q4 | Discriminating? | silhouette k; the share of items in the largest neighbourhood | Reported. "Collapsed" if k = 3 and the largest neighbourhood holds ≥ 60% |
| Q5 | Do concept and intent disagree? | ARI between the concept and intent neighbourhoods (archive; and the 40 cases) | Reported |

A view **qualifies** as an address if it passes Q1 and Q2 and is not collapsed (Q4).

## Readings, fixed now

| Outcome | Reading | Map design |
|---|---|---|
| Intent qualifies, and its Q3 ρ is lower than concept's | Intent carries more of what the axes lack | **Intent is the main meaning coordinate**; concept is kept for checking text against the record |
| Both qualify, and Q5 ARI < 0.5 | They see different things | **Two addresses** (purpose and idea) alongside the axis cell: the "balance" option |
| Both qualify, and Q5 ARI ≥ 0.5 | They largely agree | Use the one with lower Q3 ρ; tie goes to intent (easier to review) |
| Intent fails Q1 or Q2, or collapses | Purpose is too unstable or too shared | **Concept stays the coordinate**; intent is used only as the wording of guidance |
| idea qualifies and beats both singles on Q2 with no worse Q3 | Embedding them together is enough | One combined coordinate |

Limits: 15 seeds; the intent reference is an LLM grouping until the architect reviews it, and it is not blind to the concept families. Q3 measures independence, not usefulness; a view could be independent of the axes because it is noisy, which Q1, Q2 and Q4 guard against.
