# Validation of batch-01 scoring evidence

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../../CONSTRAINT_ALIGNMENT_AUDIT.md).


The archived scores remain unchanged. This validation supports using them as descriptive ratings of these 12 proposals, with the qualifications below. It does not establish that all 12 designs are physically feasible, that the ratings were blinded, or that one model or condition produces better architecture.

## Scope and provenance

Checked the frozen Step02 input, evaluator rubric, pinned benchmark configuration, canonical proposals, original response documents, and original evaluator rationales. Arithmetic inputs in REFERENCE_GEOMETRY.json are hand-extracted from the proposals; they are not ME-generated results. The reference engine/configuration commit is `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`. Source scoring document SHA-256: quality `6d56612840fffab2cc9a44371dd3062a4b80060d0a81d8900118c64d872ec6bf`; behavior `3f628dd40116a54b1f9a938e5e2a149c796337ea3fe2e7a768f3024c49c4fed3`. Original response hashes: A0 `4684bd0246b5f38bb3386cfa38e9b9bd60b7573d9c248fb07b1e8ecebae53d4d`; A1 `7c4c1ea60eea23e7c06fb5fdee88b591787835388c9a7e89521254114f6c50d5`.

Run `python audit_validation.py` in this directory to reproduce the numerical checks. No score is recomputed. Raw source documents are retained separately.

## What reconciles

All 12 proposals' gross areas reproduce from their declared floor plates, and their scheduled floor NFAs sum to 44,270 SF. All are inside the ±3% band around their explicitly chosen gross-area reference. Principal ratios pass under their declared interpretations; mass lengths meet the 60 m cap. Extracted core, special-education and custodial allocations conserve department totals, occupy contiguous floors, and exceed the stated approximately 753 SF minimum per occupied floor. Every floor's scheduled NFA is below its gross plate area.

These are necessary arithmetic checks. They do not demonstrate that all 41 room lines, circulation, walls, stairs and service connections fit in a realizable layout. The evaluator's “PASS” and “materially unverified: none” must not be read as independent certification of that layout.

| Case | Recomputed GFA (SF) | Chosen reference (SF) | Anchor evidence qualification |
|---|---:|---:|---|
| R01 | 78,360 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R02 | 74,340 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R03 | 77,600 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R04 | 67,080 | 66,405 | Explicit dimensions; room-area reconciliation still required |
| R05 | 76,300 | 76,365.75 | Gym minimum commitment; final dimensions absent |
| R06 | 76,264 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R07 | 78,540 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R08 | 67,384 | 66,405 | Explicit dimensions; room-area reconciliation still required |
| R09 | 74,620 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R10 | 76,374 | 76,365.75 | Gym and cafeteria minimum commitments; final dimensions absent |
| R11 | 75,860 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |
| R12 | 75,600 | 76,365.75 | Explicit dimensions; room-area reconciliation still required |

## Factual qualifications to quality rationales

- **Q01 — daylight applicability (R04, R06, R08, R09, R10, preference alignment):** wide gym/dining masses contain none of the pinned configuration's listed daylight departments (academic, special education, classroom, art, music, science). Applying the instructional/daylit 90 ft preference to these halls needs justification. The evaluator wording is broader than the configuration, so this is an applicability question rather than an automatic score correction. R12's wide hall contains art/music, making the corresponding applicability supported.
- **Q02 — R02 robustness:** “cannot shrink” is too absolute. Current GFA is 74,340 SF and the lower limit is 74,074.7775 SF. Shortening A from 169 to 168 ft removes 240 SF, leaving 74,100 SF inside the band and keeping its principal ratio permitted. Internal fit after shortening is not established. The supported claim is little shrink margin.
- **Q03 — R05 efficiency:** the C-ground numerator 7,570 SF is the scheduled arts, medical, administration and custodial sum. It does not contain a separately quantified lobby. The approximately 74% ratio is correct; “including lobby” is unsupported by that calculation.
- **Q04 — R07 efficiency:** B2 uses 4,570 / 10,240 = 44.63%; “37–44%” understates its upper end by rounding. This is a minor wording issue.

QUALITY_RATIONALE_AUDIT.json indexes all 48 ratings against these findings. Absence of a flagged factual issue does not validate a subjective 0–4 judgment or its inter-rater reliability.

## Additional proposal evidence limits

R10 explicitly uses principal envelope ratios. Its B upper plates have ratios 0.9524 and 0.875; they would fail a different per-floor interpretation. This audit preserves the declared interpretation allowed by the rubric rather than imposing a new rule.

Room-size figures need reconciliation with scheduled NFA: R04 cafeteria 2,816 vs 2,800 SF; R06 2,795 vs 2,800; R08 2,976 vs 2,800; R09 gym 6,600 vs 6,500 and cafeteria 3,168 vs 2,800; R12 cafeteria 3,128 vs 2,800, stage 924 vs 900, and chair/table storage 440 vs 400. Clear dimensions may describe bays or allowances rather than exactly the scheduled net room; these differences alone do not prove omission or program invention. R02's 60×100 figure is a clear court subset, not sufficient evidence that its whole scheduled gym loses 500 SF. R12's medical location is also inconsistent between its floor accounting and narrative and remains unresolved.

R09's stated gross reference 76,376 differs from 76,365.75 by 10.25 SF; the evaluator already acknowledged this. R11's middle B plate contains no scheduled program; a three-floor preference does not by itself establish productive use of all floors.

Recovered original diagrams provide additional source evidence: R03's schematic supports the stated arrangement; R09's diagram and narrative leave the arts/stage interface inconsistent. Those diagrams were absent from the archived text behavior packet. Their recovery does not retroactively change what the original behavior evaluator could inspect.

## Interpretation and next step

Quality identity exposure remains an audit limitation; later metadata removal cannot retroactively blind an earlier rating. The archived behavior packet is label-masked, but its identity with the exact packet delivered to the scorer has not been independently established; the frozen behavior protocol permits unblinded coding.

With three runs per cell, a single evaluator, no independent room-fit certification, and the applicability questions above, the scores support exploratory descriptions only. Two Opus A0 proposals choose the 66,405 SF reference while the others choose 76,365.75 SF; efficiency comparisons therefore also reflect a permitted choice of gross-area basis. Higher visible process ratings in A1 and unchanged/lower quality medians do not establish that search is ineffective or that A1 worsens design.

The next substantive validation is to reconcile room schedules and realize layouts under a common declared area/ratio policy, then obtain independent masked ratings from verified clean packets. Until then, retain original ratings and these annotations separately; ME coverage, legality and runtime measurements remain pending.

