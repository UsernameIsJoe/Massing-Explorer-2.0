# Batch 01 descriptive score analysis

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../CONSTRAINT_ALIGNMENT_AUDIT.md).


These results use the original audited Fable scores, with no score changes. The quality evaluator input was identity-exposed. The archived behavior input is label-masked, but correspondence to the file actually supplied to Fable is not independently established. These are exploratory comparisons of twelve independent runs, three in each cell.

## Quality scores

Scores are 0–4. Cells show median (minimum–maximum). All 12 hard-feasibility PASS labels are evaluator judgments; deterministic verification remains pending.

| Model and condition | Cases | Coherence | Alignment | Efficiency | Robustness |
| --- | --- | ---: | ---: | ---: | ---: |
| ChatGPT A0 | R02, R05, R10 | 3 (3–3) | 4 (3–4) | 2 (2–2) | 2 (2–2) |
| ChatGPT A1 | R01, R07, R11 | 2 (2–3) | 4 (4–4) | 1 (1–2) | 1 (1–3) |
| Opus 5.5 A0 | R04, R08, R12 | 3 (2–3) | 3 (2–3) | 3 (2–3) | 2 (1–3) |
| Opus 5.5 A1 | R03, R06, R09 | 3 (3–3) | 3 (3–4) | 2 (1–2) | 2 (2–3) |

## Behavior scores

Scores are 0–3. Cells show median (minimum–maximum). Unknown representation expansion is retained, not assigned zero.

| Axis | ChatGPT A0 | ChatGPT A1 | Opus A0 | Opus A1 |
| --- | ---: | ---: | ---: | ---: |
| problem structuring | 2 (2–2) | 3 (3–3) | 3 (2–3) | 3 (3–3) |
| search space framing | 0 (0–0) | 2 (2–2) | 1 (1–1) | 3 (3–3) |
| exploration breadth | 0 (0–0) | 2 (2–2) | 1 (1–1) | 3 (3–3) |
| exploration diversity | 0 (0–0) | 1 (1–2) | 1 (1–1) | 3 (3–3) |
| comparative evaluation | 0 (0–0) | 2 (1–2) | 1 (1–1) | 3 (3–3) |
| constraint verification | 2 (2–2) | 3 (3–3) | 3 (3–3) | 3 (3–3) |
| revision backtracking | 0 (0–0) | 0 (0–0) | 0 (0–0) | 1 (0–2) |
| tradeoff reasoning | 1 (1–1) | 3 (2–3) | 2 (2–2) | 3 (3–3) |
| selection stopping logic | 1 (1–1) | 2 (2–2) | 1 (1–1) | 2 (2–3) |
| representation expansion | unknown | unknown | unknown | unknown |
| uncertainty handling | 2 (2–2) | 3 (2–3) | 3 (3–3) | 3 (3–3) |

## Four primary comparisons

1. **ChatGPT A0 to A1:** Visible exploration breadth rises from median 0 to 2; diversity from 0 to 1; comparative evaluation from 0 to 2; constraint verification from 2 to 3. Quality coherence falls from 3 to 2, efficiency from 2 to 1, and robustness from 2 to 1. Alignment remains 4. A1 adds observable process but does not improve the median final-design scores in this batch.
2. **Opus A0 to A1:** Breadth, diversity and comparative evaluation each rise from 1 to 3. Coherence, alignment and robustness medians remain 3, 3 and 2. Efficiency falls from 3 to 2. A1 expands search without an accompanying median quality gain.
3. **ChatGPT to Opus under A0:** Opus has higher medians for breadth, diversity and comparison (1 versus 0), and verification (3 versus 2). Coherence and robustness medians are equal. Opus has higher efficiency (3 versus 2); ChatGPT has higher preference alignment (4 versus 3).
4. **ChatGPT to Opus under A1:** Opus has higher breadth, diversity and comparison medians (3 versus 2, 1 and 2). Its coherence, efficiency and robustness medians are each one point higher. ChatGPT has higher alignment (4 versus 3). Neither family is combined into a total or ranking.

## Behavior and outcomes

More visible exploration does not correspond to higher group-median efficiency in either model here. This is a descriptive co-occurrence, not evidence that exploration causes worse designs. The same dimensions and program allocations still require deterministic validation before treating the evaluator PASS labels as verified feasibility.
Within A1, Opus reports broader organizational search, while ChatGPT usually develops variants around a narrower organization. The evidence records preserve comparisons, rejected alternatives and calculations so that this distinction can be checked against the raw responses rather than inferred from scores alone.
Visible revision occurs only in R03 and R09, both Opus A1. Only R09 has a stated stopping condition according to the behavior evaluator. This describes visible output, not hidden internal reasoning.

## Master results and unfinished fields

`MASTER_RESULTS.json` contains all 12 run identities, unchanged score families, evaluator-reported feasibility, representation status, observable evidence and displayed duration metadata. Numeric alternative totals are not invented where the evaluator uses different staged or organizational units.
Layer 2 remains pending: normalized strategy, nine-axis mapping, actual ME encoding/realization status, feasibility distance, ME 0–1 metrics, distinctness and coverage. These fields are null with an explicit pending status.
The next substantive step is to normalize the twelve proposals against the frozen ME representation and independently test realizability and feasibility. Only then compare LLM outcomes and observable capabilities with the ME pipeline.


## Evidence validation qualification

The separate [validation report](validation/VALIDATION_REPORT.md) reconciles all 12 gross/net totals and declared principal ratios, but does not certify realized room fit. It identifies five daylight-preference applicability questions, limited anchor evidence in R05/R10, and three factual wording/rounding qualifications. Original scores remain unchanged. Group differences are descriptive; the quality identity exposure, n=3 per cell, single evaluator, and differing permitted gross-area bases prevent causal or general model-quality conclusions. Higher A1 behavior ratings do not establish that its search improves or worsens architecture.

