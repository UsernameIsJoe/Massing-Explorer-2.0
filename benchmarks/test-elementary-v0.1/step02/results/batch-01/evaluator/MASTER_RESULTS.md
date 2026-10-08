# Batch 01 master run table

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../CONSTRAINT_ALIGNMENT_AUDIT.md).


Fable quality scores: 0–4. Quality input identity exposure is confirmed; behavior delivery verification remains unresolved. Feasibility shown below is evaluator-reported. All actual ME computational fields remain pending.

| Case | Model | Condition | Run | Coherence | Alignment | Efficiency | Robustness | Fable feasibility | Displayed duration |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R01 | ChatGPT | A1 | 3 | 2 | 4 | 1 | 1 | PASS | Worked for 10m 27s |
| R02 | ChatGPT | A0 | 3 | 3 | 4 | 2 | 2 | PASS | Worked for 7m 40s |
| R03 | Opus 5.5 | A1 | 2 | 3 | 4 | 1 | 2 | PASS | Thought for 9m 26s |
| R04 | Opus 5.5 | A0 | 3 | 3 | 3 | 3 | 3 | PASS | Thought for 5m 21s |
| R05 | ChatGPT | A0 | 1 | 3 | 4 | 2 | 2 | PASS | Worked for 11m 59s |
| R06 | Opus 5.5 | A1 | 3 | 3 | 3 | 2 | 3 | PASS | Thought for 7m 11s |
| R07 | ChatGPT | A1 | 2 | 2 | 4 | 1 | 1 | PASS | Worked for 5m 44s |
| R08 | Opus 5.5 | A0 | 1 | 3 | 3 | 3 | 2 | PASS | Thought for 6m 42s |
| R09 | Opus 5.5 | A1 | 1 | 3 | 3 | 2 | 2 | PASS | Thought for 4m 15s |
| R10 | ChatGPT | A0 | 2 | 3 | 3 | 2 | 2 | PASS | Worked for 7m 50s |
| R11 | ChatGPT | A1 | 1 | 3 | 4 | 2 | 3 | PASS | Worked for 10m 40s |
| R12 | Opus 5.5 | A0 | 2 | 2 | 2 | 2 | 1 | PASS | Thought for 5m 35s |

The full eleven-axis behavior scores and per-case observable evidence are retained separately within `MASTER_RESULTS.json`. Displayed Worked/Thought durations have different host meanings and are not used to rank compute efficiency.

