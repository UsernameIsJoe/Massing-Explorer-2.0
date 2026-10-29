# Carrying decisions (semantic-lock input): first measurements

Date: 2026-10-28. Answers: `architect_carrying_v1.1.json` (v1 page answers plus three clarifications). Code: `scripts/carrying_lock.py`. Results: `lock_measurements_v1.1.json`.

**Status:** an input to Task 4. It does not decide membership.

## Caveat from the architect

> "I was also almost rating by how important the programs are and how their placement fits the intent."

## Measurements

**Organization space:** 5,064 combinations of grouping and link pattern. This counts gym and dining as one unit, keeps core academic apart from gym, does not allow custodial alone, and leaves floors free.

| Seed | Organizations admitted (floors free) | Other-run seeds admitted, floors locked | Other-run seeds admitted, floors free | Links-only lock admits |
|---|---:|---|---|---|
| S01 Civic Hinge | 162 (3.2%) | none | R2-S01, R3-S01, R2-S04 | 7 seeds |
| S02 Arts Loft | 162 (3.2%) | none | R3-S03 | R3-S03, R2-S04, R1-S05 |
| S03 Detached Pavilions | 9 (0.2%) | none | none | R2-S03 |
| S04 Commons Heart | 27 (0.5%) | none | R3-S02 | R2-S02, R3-S02 |
| S05 Academy Tower | 336 (6.6%) | R3-S04 | R3-S04 | all (no links locked) |

## Reading against the other runs' names

The other runs' names and concepts were written independently by the generating LLM. Which of them share an idea with an R1 seed is the assistant's reading, not yet confirmed by the architect.

- **Matches admitted with floors free:** "Civic Hinge Between Learning and Hall" (R3-S01) and "Civic gateway between learning and hall" (R2-S01) for S01; "Courtyard Cluster with Arts Loft" (R3-S03) for S02; "Shared Hall as Central Heart" (R3-S02) for S04.
- **Exact floor locks reject all of these,** each over one department's floor list: special education [1, 2] vs [1] or [1, 2, 3]; arts [3] vs [2, 3].
- **Same organizing idea, rejected by program relations:** R2-S02 "Shared heart with two wings" fails S04's lock only because special education sits in a different mass. R2-S03 "freestanding pavilions" fails S03's lock on program relations and floors, although its links match.
- **The ideas live in different layers:** S03 (detached) and S04 (heart) are carried by links. S05 (tower and care house) is carried by program placement, with no links locked. S01's two locked links admit too much on their own.

## Open, for the architect

1. Floors: lock exact floor lists, or relations such as "ground floor" or "crown of its mass"?
2. Importance: ticks that reflect program importance rather than the idea over-restrict, as with R2-S02. Should "the idea needs this" be separated from "important program"? The second would be weighted (the decision weights), not locked.
