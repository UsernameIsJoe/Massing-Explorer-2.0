# Pilot 3 findings: expansion and region v1

Date: 2026-10-28. Protocol: p03-v1.1. Decisions: `labels/user_expansion.json`. Region: `region/region_v1.json` (built by `scripts/build_region.py`).

## Result in one line

Code took five LLM seeds and produced about 400 valid strategies that the LLM never offered in three runs. The architect quickly reviewed 20 representatives. That review produced region v1: 5 seeds, 638 variations and 199 reviewed expansions (114 added, 85 maybe), plus clear rules for the unreviewed groups.

## Decisions on 20 representatives

| Defining move | Add | Maybe | Skip |
|---|---:|---:|---:|
| Special education moves mass | 5 | 1 | 0 |
| Core academic moves mass | 4 | 0 | 1 (custodial left alone) |
| Administration only | 0 | 5 | 0 |
| Gym and dining move | 0 | 0 | 3 (all left custodial alone) |
| Commons heart link cut | 0 | 0 | 1 |

Architect's notes:
- Administration or a link as the only change is "enough change but not enough", so it is a Maybe.
- Custodial cannot be a mass of its own. This is now a hard rule.

## Region v1

| Part | Groups | Structures |
|---|---:|---:|
| Seeds | n/a | 5 |
| Inside variations (weighted change < 1.0) | n/a | 638 |
| Expansion, added (reviewed) | 9 | 114 |
| Expansion, maybe (reviewed) | 6 | 85 |
| Expansion, inferred add (unreviewed; special education or core academic move) | 29 | 65 |
| Expansion, inferred maybe (unreviewed; administration only) | 5 | 68 |
| Needs review (the reviewed representative breaks the new custodial rule) | 4 | 7 |
| Unreviewed, other | 9 | 63 |
| Rejected direction (heart link cut) | 1 | 10 |

## What this shows

1. **Expansion is where the breadth comes from.** Three LLM runs gave about eight organizing ideas. Two code edits around each of the five seeds gave 412 structures outside the region, and only 27 of them resemble anything in runs 02–03.
2. **The architect's weights generalise.** The moves the architect said define a strategy (special education, core academic) produced new strategies worth adding. Administration alone sits on the boundary. Moving supporting program does not create a new strategy.
3. **Grouping makes quick review scale.** 20 decisions took about five minutes. They settled 15 groups directly and gave defensible inferences for 34 more.
4. **Review surfaces missing hard rules.** The custodial rule was not among the brief's representable rules. It only came out when the architect saw the cases.

## Limits

- There was one reviewer.
- Inferred statuses are not decisions and stay labelled as inferred.
- Feasibility is untested.
- Group membership assumes that the same defining move from the same seed means the same decision.

## Next

- An outside model writes concepts for the 15 added and maybe representatives (`prompts/DESCRIBE_EXPANSIONS.txt`). Then every reviewed member of the region is described the same way as the seeds.
- Then Step 04: exploration within region v1 under the brief, starting with a shortlist for realization.

## Addendum: concepts for the 15 added and maybe representatives

Source: ChatGPT temporary chat, medium effort, prompt `prompts/DESCRIBE_EXPANSIONS.txt`. The raw reply is in `responses/raw/`. The concepts are attached to their groups in `region/region_v1.json`, and the checks are in `responses/describe_expansions.json`.

- **Length rule followed:** all 15 are 55–61 words.
- **Naming rule broken:** every one names 4–7 program groups, using paraphrases (for example "specialized learning", "creative", "institutional"), and walks through each mass. They are placement inventories, which is the same problem the architect found in the Pilot 1 intent text.
- **The real concept content is the link pattern:** "triangular cluster" (all three linked, 6 cases), "hinge or chain" (two links, 6 cases), "detached pavilions" (no links, 3 cases). The wording follows the links exactly. Nothing in it comes from intent, because a model given only structure has no intent to report.

**Decision.** These are stored as `derived` descriptions, not concepts. Seed concepts come with generation and carry intent. A description written after the fact from structure only does not. Region members therefore carry the same diagram and structure as the seeds, but only seeds carry an authored concept. When an expansion needs a concept (for example when it is shortlisted), it gets one by regeneration: the LLM is given the structure as a commitment and asked to propose it as a strategy, under the same seed format.
