# Step 02 — Batch 01 artifact manifest

Benchmark: `test-elementary-v0.1`

This folder archives the first 12-run A0/A1 pure-LLM batch and the transformation artifacts used for masked design evaluation.

## Batch composition

- ChatGPT High — A0 × 3
- ChatGPT High — A1 × 3
- Opus 5.5 Medium — A0 × 3
- Opus 5.5 Medium — A1 × 3
- Total: 12 independent generation runs

## Files

| Path | Role |
| --- | --- |
| `raw/A0_RAW_RESPONSES.md` | Raw A0 response text in original order |
| `raw/A1_RAW_RESPONSES.md` | Raw A1 response text in original order |
| `canonical/PRE_SHUFFLE_UNMASKED.md` | Canonical records in source order, with run metadata |
| `canonical/POST_SHUFFLE_UNMASKED.md` | Canonical records after shuffle/ID reassignment, with run metadata |
| `canonical/MASKED_EVALUATION.md` | Evaluator-facing canonical records with run metadata withheld |
| `SHUFFLE_KEY.md` | Mapping from masked IDs back to source IDs and source runs |

## Original Word artifact hashes

| Source artifact | SHA-256 |
| --- | --- |
| `Test results A0.docx` | `4684bd0246b5f38bb3386cfa38e9b9bd60b7573d9c248fb07b1e8ecebae53d4d` |
| `Test results A1.docx` | `7c4c1ea60eea23e7c06fb5fdee88b591787835388c9a7e89521254114f6c50d5` |
| `Pre Shuffle.docx` | `ba14addb96775911a32216a90a832c37a8aa2a20ea9ef3253531fde7cf1597c9` |
| `after shuffle.docx` | `3b1e38330fde8138ec069409be83dd27e6495a28634102a0fb280225f529bee4` |
| `Masked evaluation.docx` | `da057c72add469ba8e1649c5795e629923bc528df05a033a76de2af679afa017` |

## Transformation chain

`raw A0/A1 → unmasked canonical source order → shuffle + new evaluation IDs → remove run metadata → masked evaluation set`

The repository copies are UTF-8 text exports for auditability and diffability. Embedded screenshots/diagrams in the Word sources are not serialized into the Markdown exports.

## Audited evaluator scores and unmasked analysis

The existing audited Fable scores are locked without numeric changes and analyzed descriptively. Quality input identity exposure is confirmed; behavior exposure is not established, and actual delivery correspondence remains unverified. See `evaluator/LOCK.md` and `evaluator/AUDIT.json` for the precise status.

| Path | Role |
| --- | --- |
| `behavior/MASKED_SHUFFLED_RAW_RESPONSES.md` | Archived label-masked raw packet for observable behavior coding |
| `evaluator/QUALITY_FABLE_LOCKED.csv` | Verified unchanged quality score transcription |
| `evaluator/BEHAVIOR_FABLE_LOCKED.csv` | Verified unchanged behavior score transcription |
| `evaluator/MASTER_RESULTS.json` | Twelve unmasked run records with separate score families, evidence, metadata and pending Layer-2 fields |
| `evaluator/MASTER_RESULTS.md` | Readable quality run table |
| `evaluator/GROUP_SUMMARIES.json` | Per-axis medians and ranges for four three-run cells |
| `evaluator/PRIMARY_COMPARISONS.json` | Four descriptive differences of group medians; independent runs |
| `evaluator/DESCRIPTIVE_ANALYSIS.md` | Descriptive interpretation and next computational work |

The original Word hashes above describe archived source versions, including the original identity-bearing after-shuffle file. They are not hashes of its later sanitized replacement. The masked evaluator inputs, unmasked archives and post-scoring results have different roles.

The untouched evaluator DOCX files remain in the existing user-supplied artifacts. Their original hashes are recorded in `evaluator/AUDIT.json`; full DOCX uploads were blocked by automatic approval review. Verified score transcriptions and descriptive derivatives are published here.
