# Batch 01 shuffle key

**Withhold this file from the masked design evaluator until scores are locked.**

Source canonical IDs before shuffling:

`R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12`

Operator-supplied shuffle order:

`R09, R03, R11, R06, R01, R12, R08, R04, R10, R02, R07, R05`

| Masked evaluation ID | Pre-shuffle canonical ID | Original source run |
| --- | --- | --- |
| R01 | R09 | ChatGPT High / A1 run 03 |
| R02 | R03 | ChatGPT High / A0 run 03 |
| R03 | R11 | Opus 5.5 Medium / A1 run 02 |
| R04 | R06 | Opus 5.5 Medium / A0 run 03 |
| R05 | R01 | ChatGPT High / A0 run 01 |
| R06 | R12 | Opus 5.5 Medium / A1 run 03 |
| R07 | R08 | ChatGPT High / A1 run 02 |
| R08 | R04 | Opus 5.5 Medium / A0 run 01 |
| R09 | R10 | Opus 5.5 Medium / A1 run 01 |
| R10 | R02 | ChatGPT High / A0 run 02 |
| R11 | R07 | ChatGPT High / A1 run 01 |
| R12 | R05 | Opus 5.5 Medium / A0 run 02 |

The shuffled canonical set was audited before masking: all 12 source cases appear exactly once, with no omissions or duplicates and no architectural-content changes.
