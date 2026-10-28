# Pilot 01 findings — representation

Date: 2026-10-28. Protocol: p01-v1.3. Scores: `results/scores.json` (from `scripts/score_triplets.py`).

## Result in one line

Embeddings agreed with the architect only when they were fed **code-rendered structure**; on the seeds' placement-style rationale text they were at chance and failed every wording trap. A plain structural distance matched the architect better than any embedding and better than an LLM asked directly.

## Agreement with the architect (10 decisive real-case items)

| Predictor | Agreement |
|---|---:|
| Structure proxy (grouping / floors / links distance) | **8/10** |
| bge-m3 on `struct` text | 7/10 |
| mxbai-embed-large on `struct` text | 7/10 |
| nomic-embed-text, qwen3-embedding on `struct` text | 6/10 |
| Best aspect view (`aspect_inclusion`, bge-m3 / mxbai / nomic) | 6/10 |
| Any encoder on `intent` text (the seeds' own strategy prose) | 3–4/10 |
| Any encoder on `full` text | 2–4/10 |
| Wording proxy (TF-IDF on intent text) | 4/10 |
| LLM baseline, asked directly (8 decisive answers) | 4/8 |

Excluded: T01 and T02 (inconsistent with their repeats); 4 items labeled "about equal".

## Probe diagnostics (designed by Claude, not validated by the labeler)

All four encoders on `intent` text: lexical traps **0/4**, intent-vs-wording **0/3**, paraphrase 1–2/4, generic 2/2. In every trap, the encoder judged the text that reused the anchor's words as closer than a faithful paraphrase. These are not part of the gate, but the direction is unambiguous.

## Gate

By the letter of p01-v1.3, **PASS**: best encoder × variant 7/10 (70%), within one item of the structure proxy, LLM baseline not ahead.

The substantive reading is narrower, and it is the one that should guide Pilot 2:

1. The passing variant is `struct`: text rendered by code from the structured decisions. On the 15 real items, bge-m3 `struct` picks the same option as the structure proxy on 13. It reproduces the structural distance; it does not add semantic information beyond it.
2. On the strategy descriptions themselves (`intent`, `full`), embeddings perform at chance and follow wording, not strategy. Aspect conditioning by keyword sentence selection did not fix this.
3. The architect's judgment is mostly structural: 6 of the 8 decisive disagreement items sided with structure, and the notes cite connections, program split and couplings (academic with custodial, custodial as an attached program).
4. Asking an LLM directly did not beat structure either (4/8).

## Implication for Steps 02–03

**Correction (2026-10-28, after review with the labeler):** the `intent` text tested here is the v1.0 `organizing_principle` and `main_tradeoff`, which mostly restate placements. It is not a concept-level description of the scheme. Pilot 01 therefore shows only that embeddings of literal placement prose follow wording rather than strategy. It does **not** test, and does not refute, a semantic space built from concept descriptions written by the generating LLM.

Next: the seed record specification v2.0 (`docs/SEED_RECORD_SPEC.md`) asks the generating LLM for concept, intent, key moves and commitments at generation time. Pilot 01b will test embeddings of those concept fields against the same kind of labels.

## Limits

- Ten decisive items. One item is 10 points; 7/10 versus 8/10 is not a meaningful difference, and 70% is only weak evidence against chance.
- The diagrams (added in v1.1 at the labeler's request) show structure and not intention, which may have pushed labels toward structure. The labeler also read diagram block width as mass size in one note (T30), though width encodes nothing.
- The structure proxy and the `struct` descriptions come from the same records, and the real-case items were selected using that proxy, so the proxy had a structural advantage by design. The wording proxy had the mirror advantage and still scored 4/10.
- The LLM baseline is the same model family that built the pilot; it saw structure lines but no diagrams.
- Four encoders, one configuration each, no fine-tuning. A different description protocol might perform differently.

## Suggested next step

Regenerate seeds under spec v2.0, then run Pilot 01b on their concept fields before deciding which space carries membership in Pilot 2.
