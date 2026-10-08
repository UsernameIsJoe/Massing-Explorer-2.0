# Batch 01 evaluator score lock

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../CONSTRAINT_ALIGNMENT_AUDIT.md).


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

