# Pilot 01c findings — robustness checks

> **Status (2026-10-29):** evidence. Paraphrase robustness (bge-m3) still informs encoder choice ([pilots/README.md](../../README.md)).

Date: 2026-10-28. Protocol: `PILOT_01C_PROTOCOL.md`. Scores: `results/scores.json`. Outside model: ChatGPT, temporary chats, medium effort (model name to be recorded).

## Result in one line

One encoder, **bge-m3**, reads concepts faithfully (passes the paraphrase test) and is the same encoder that was complementary to structure in Pilot 01b; the other three do not. No encoder passes the edit test. ChatGPT qualifies as a stable judge, but it judges like the structure comparison, so it cannot settle the question that matters most.

## Test 1 — Paraphrase invariance (15 rewrites)

| Predictor | Own original nearest | Own or structural twin nearest |
|---|---:|---:|
| **bge-m3** | 10 | **12** (pass, bar 12) |
| mxbai-embed-large | 8 | 9 |
| nomic-embed-text | 7 | 8 |
| qwen3-embedding 0.6b | 6 | 7 |
| TF-IDF wording | 5 | 6 |

Chance is about 1–2 of 15. The rewrites reused on average 16% of the originals' longer words, so wording alone still found some matches (6), but bge-m3 doubled it.

## Test 2 — Edit sensitivity (30 variants of 5 bases)

| Encoder | Mean Spearman (bar 0.5) | Bases where 3 edits > 1 edit (bar 4/5) |
|---|---:|---:|
| bge-m3 | 0.48 | 4/5 |
| nomic-embed-text | 0.31 | 4/5 |
| qwen3-embedding 0.6b | 0.31 | 4/5 |
| mxbai-embed-large | 0.12 | 4/5 |

No encoder passes; bge-m3 misses by 0.02. Distances drift upward with edits on average but are noisy per base. Confound: ChatGPT's descriptions enumerated program (8 program terms each on average) instead of stating concepts, so this mostly tests embeddings of placement-style text, which Pilot 01 already showed is wording-driven.

## Test 3 — Outside judge (16 Pass B items)

| Run | Agrees with labeler (11) | Repeats consistent |
|---|---:|---|
| ChatGPT A | 8 | 2/2 |
| ChatGPT B | **9** | 2/2 |
| ChatGPT C (identical to B) | **9** | 2/2 |
| Claude baseline (Pilot 01b) | 8 | — |

- Self-agreement: A–B 15/16, B–C 16/16. ChatGPT A and the Claude baseline gave identical answers on all 16 items: two model families converge.
- Runs B and C meet the panel-judge bar (≥ 9/11 with labeler, ≥ 13/16 self).
- **But:** ChatGPT matches the structure proxy on 12 of 14 items. Both LLMs disagree with the labeler on C07 and C12, siding with structure; bge-m3 concept + intent sided with the labeler on both.

## What this means

1. **bge-m3 is a credible concept encoder.** It passes the paraphrase test, nearly passes the edit test, and in Pilot 01b was right on all three items where structure disagreed with the architect. The other encoders are not credible for concepts.
2. **Structure remains the primary basis.** Every independent check (structure proxy, two LLM families, struct embeddings) agrees with structure and with the architect most of the time.
3. **The open question is the minority of items where the architect departs from structure.** On those, concept similarity (bge-m3) agreed with the architect and the LLM judges did not. Whether that reflects real strategic insight or idiosyncratic calls cannot be settled by an LLM judge, because the LLM judges side with structure.
4. **Scaling with an LLM judge would therefore build in a structural bias.** A qualified LLM panel is useful for scale on questions where structure and judgment agree, not for deciding whether concepts add value.

## Next

- A **second architect** labels Pass B (16 items, about 25 minutes): the only way to tell whether the departures from structure are shared.
- Pilot 2 builds membership on structure, with **bge-m3 concept + intent** as a candidate secondary term, evaluated on new items not used to choose it.
- Record the ChatGPT model name.
