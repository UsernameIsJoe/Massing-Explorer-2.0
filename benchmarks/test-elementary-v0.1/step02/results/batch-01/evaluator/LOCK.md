# Batch 01 evaluator score lock

Scores are preserved exactly as supplied by Fable. No score is changed by unmasking or by the descriptive analysis.

## Quality provenance

Status: IDENTITY-EXPOSED INPUT CONFIRMED.

The original after shuffle.docx supplied for quality evaluation retained model, condition, source-run, reasoning-setting, duration and source-tag metadata. This pass cannot be described as blinded. Whether exposure affected any particular score is unknown. Sanitizing the input afterward does not change that provenance.

## Behavior provenance

Status: ARCHIVED INPUT LABEL-MASKED; ACTUAL DELIVERY NOT VERIFIED.

The current archived behavior/MASKED_SHUFFLED_RAW_RESPONSES.md contains no direct model, condition, original run, timing or prompt-tag labels within the twelve records. The evaluator report states metadata was masked. The exact file actually delivered has not been independently matched to the archived packet, so exposure is not established and full blinding is not claimed. The frozen behavior protocol permits unblinded coding; the archived packet separately describes itself as label-masked.

## Preservation and use

- The original user-supplied scoring DOCX files remain unchanged. Their SHA-256 hashes are recorded in AUDIT.json; full DOCX publication was blocked by automatic approval review.
- QUALITY_FABLE_LOCKED.csv and BEHAVIOR_FABLE_LOCKED.csv reconcile to both individual case tables and batch summaries.
- AUDIT.json records source hashes, mapping checks and methodological status.
- Existing scores are used for exploratory descriptive analysis at the user's instruction.
- Score families remain separate. Unknown representation fields remain unknown.
- No score changes are permitted after unmasking except documented extraction or factual-reading errors, with before/after values and reasons.
- Fable feasibility judgments are not substitutes for pending deterministic ME verification.
