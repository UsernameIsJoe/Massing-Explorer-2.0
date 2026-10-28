# Pilot 01 — Can text embeddings represent strategic similarity?

Status: **locked 2026-10-28, revision p01-v1.3**. Change nothing below mid-run. Any change creates `p01-v2` and applies only to new runs.

## Question

When two school strategies are compared by an embedding of their descriptions, does the ranking match an architect's judgment of strategic closeness, more often than wording overlap alone and about as well as asking an LLM directly?

This decides whether embeddings can carry the semantic boundary into Pilot 2 (membership, expansion, generation). Pilot 01 does not build a region, generate candidates or test feasibility.

## Materials (frozen)

| Item | File | Notes |
|---|---|---|
| 15 cases | `benchmarks/test-elementary-v0.1/seed_scope_cases_2026-10-27/cases/all_15_cases.json` | 5 parents + 5 A + 5 B, all generated under the no-cross-mass rule (verified in that folder) |
| Descriptions | `data/descriptions.jsonl` | 90 texts, template `p01-desc-v1`, built by `scripts/render_descriptions.py` |
| Probes | `data/probes.json` | 19 texts written by Claude |
| Triplets | `data/triplets_SEALED.json` | 31 items; contains selection data and probe expectations — never show during labeling |
| Labeling set | `data/labeling_set.json` | the blind version the labeler and the LLM baseline see |

### Description variants

Every sentence is either rendered from the structured record (department → mass, floors, links) or copied verbatim from the record's own text. Nothing is added.

| Variant | Content | Tests |
|---|---|---|
| `struct` | rendered decisions only, neutral mass names (classroom / commons / third) | structure alone |
| `intent` | organizing principle + main trade-off, verbatim | the LLM's own strategic language |
| `full` | name, principle, decisions, trade-off, unresolved notes | everything together |
| `aspect_inclusion` / `aspect_civic_access` / `aspect_service` | relevant decisions + source sentences selected by keyword | aspect conditioning |

Known limitation: aspect views select sentences by keyword, so an unrelated sentence that mentions a keyword can be included (e.g. A-E04 inclusion picks up a ratio note).

## Ground truth

Two kinds of ground truth, set in revision p01-v1.2:

- **Real-case items (17, including 2 repeats): blind labels.** The labeler (Joe) picks which option is the closer **architectural strategy**, or "about equal" / "can't judge", with a diagram for every scheme. These labels are authoritative.
- **Probe items (13): construction review, not blind labels.** Each probe's answer is fixed by how it was written. The labeler checks the intended answer and its reason and marks agree / disagree / unsure. A probe is scored only if the labeler agrees.

| Kind | n | What it probes |
|---|---:|---|
| `real_disagree` | 12 | real cases where structural distance and wording overlap disagree about the closer option |
| `real_control` | 3 | real cases where both agree by a wide margin |
| `paraphrase` | 4 | same strategy in different words vs. a structurally nearest real case |
| `lexical_trap` | 4 | same words with changed relationships vs. a paraphrase of the anchor |
| `generic` | 2 | generic school text vs. a real case |
| `intent_vs_wording` | 3 | same intention / different implementation vs. similar words / opposite intention |
| repeats | 3 | items shown twice with options swapped (labeler consistency only); the probe repeat is retired in v1.2 |

Real-case display: a schematic massing diagram, the intent text and a compact structure line. Probe items: text only, because a diagram would either not apply or reveal the answer (a paraphrase has the same diagram as its anchor).

**Revision p01-v1.1 (2026-10-28, before any label was saved):** diagrams added at the labeler's request, as an aid to reading the text, not a replacement. Each diagram is drawn only from the structured record (`data/diagram_data.json`, keyed by the structure line it illustrates): three masses in a fixed left-to-right order (classroom, third, commons), departments as blocks on their floors, gym + dining always drawn as one double-height block, and direct links as lines. Screen position, block width and plate width carry no meaning; there are no dimensions. Items, order and the labeling-set hash are unchanged.

**Revision p01-v1.2 (2026-10-28, before any label was saved):** the labeler judged that blind labels on text-only probes would be unreliable. Probes moved from blind labeling to construction review (see Ground truth). Items, order, texts and all locked hashes are unchanged; only the role of the probe items changed. The review payload is `data/probe_review.json`, built by `scripts/build_probe_review.py`.

## Encoders (frozen config `p01-enc-v1`)

Run locally through Ollama: `nomic-embed-text` (prefix `clustering: `), `mxbai-embed-large`, `bge-m3`, `qwen3-embedding:0.6b`. Cosine similarity, no normalization step beyond cosine. The model digest is recorded in each `runs/<encoder>/run_log.json`. An encoder that cannot be pulled is dropped and noted, not substituted silently.

## Comparison predictors

- **Structure proxy:** grouping/floor/link distance (real triplets only).
- **Wording proxy:** TF-IDF cosine on intent text (real triplets only).
- **LLM baseline:** one fresh chat, one batch, prompt in `llm_baseline/PROMPT.md`, model and settings recorded. It sees exactly the blind labeling set.

On `real_disagree` items the two proxies always answer opposite ways by construction, so their scores also show whether the labeler judges more by structure or by wording.

## Procedure

1. Joe labels the 17 real-case items, then checks the 13 probes, in the labeling page. Do not look at embedding results first.
2. Run `python scripts/run_embeddings.py` on the PC with Ollama.
3. Run the LLM baseline in a fresh chat; save its answers as `labels/llm_labels.json`.
4. Export the page's record to `labels/user_labels.json` and `labels/probe_review.json` (Claude reads it).
5. Run `python scripts/score_triplets.py labels/user_labels.json --probes labels/probe_review.json --llm labels/llm_labels.json`.
6. Write `results/FINDINGS.md`, then apply the gate.

**Revision p01-v1.3 (2026-10-28, after real-case labeling, before any embedding was run):** the labeler could not review the text-only probes either (one verdict each was recorded for T16 agree and T17 disagree before stopping). Probes are now scored against their construction expectations as **unvalidated diagnostics** designed by Claude, reported separately and never used in the gate. Both real-case repeats were inconsistent (T01/T29, T02/T30); following the precondition, those two items are excluded as unstable rather than re-asked, since a second answer after seeing them would be biased. The T30 note referred to mass size, which the diagrams do not encode; diagram block widths could be misread as area, to be fixed in any later round.

## Decision gate

Scored on decisive labels only. "Best" means the best encoder × variant on `ALL_REAL`.

- **Precondition (v1.3):** real items whose repeat disagrees are excluded as unstable. The gate is decided on the remaining decisive real-case labels only.
- **PASS — embeddings carry the semantic boundary into Pilot 2:** best ≥ 70% on `ALL_REAL`; the best encoder × variant beats the structure proxy or matches it within one item; and the LLM baseline is no more than 2 items ahead overall.
- **PARTIAL — embeddings need structural support:** best ≥ 60% on `ALL_REAL` but the structure proxy is ahead by two or more items. Pilot 2 uses embedding neighbourhoods gated by explicit decision/axis checks, and favours the variant that scored best.
- **FAIL — embeddings do not define the boundary:** no encoder ≥ 60% on `ALL_REAL`, or the LLM baseline is 3 or more items ahead overall. Pilot 2 uses LLM judgment plus axes for membership; embeddings are kept for retrieval only.

These thresholds are coarse. With about 15 real items, one item is about 7 points, and 70% (≈11/15) is only weak evidence against chance (≈ p 0.06). The gate picks a direction for Pilot 2; it does not validate a method.

## Lock record (SHA-256)

| File | Hash |
|---|---|
| `data/descriptions.jsonl` | `a7de09905462166226f7c24d70fe4567ab24f4f5ac040ad0b395865f158495e9` |
| `data/probes.json` | `81eb372bc84b67a1ca066613c690d7456791aee97cd691927b75332344152ad3` |
| `data/triplets_SEALED.json` | `71c8471bbf8f95add1d183709de1bf87a591601d65af841e411d0d1c0bf6f15f` |
| `data/labeling_set.json` | `6d183eb34eb79cc236145e7f9bdcb16fa6dd83684605319248a47fa6b9af2f30` |

A rebuild from the scripts reproduced all three generated files byte for byte on 2026-10-28.

## Out of scope

Region construction, thresholds for membership, candidate generation, fine-tuning, geometric feasibility, and claims about LLM internal reasoning.
