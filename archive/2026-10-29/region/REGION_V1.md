# Region v1: membership rule and result

Date: 2026-10-28. Status: **withdrawn as the region (2026-10-28).** The rule uses one system (decisions) and replaces the semantic side with human marks, against [the core contribution](../docs/CORE_CONTRIBUTION.md). Kept as a structural reference. Code: `membership_v1.py`. Result: `region_v1.json`.

Drafted for Task 4 of the Steps 02–03 plan. It left out the embedding side, which is why it was withdrawn; Task 2 is not settled by it.

## Rule

1. **Region membership is by idea.** A valid strategy is in the region if it keeps every idea mark of at least one seed. That seed's family is its idea. There are three kinds of idea mark:
   - a mass mark: the marked departments stay together or apart, as in the seed;
   - a floor mark: the marked department keeps its relation to the ground floor (on it or above it), and stays at the top of its mass where the seed has it there;
   - a link mark: the marked link keeps its state.
2. **Strategy identity is by weight.** Within the region, two strategies are different strategies when their weighted change is at least 1.0, using the architect's decision weights. Important marks are covered by those weights. They never decide membership.
3. **Outside the region, only by review.** A strategy that keeps no seed's idea enters only as a provisional expansion, through the architect's review (the Pilot 3 add or maybe answers).
4. **Grounding.** The nine axes are computed for every member. Embeddings are not used.

**Idea marks.** Taken from the architect's round-1 ticks, split into idea and important by the architect's stated rules (`carrying_v2_derived.json`):
- link ticks are idea;
- departments the concept talks about are idea;
- special education is important, not idea, in four seeds.

## Result

| | Count |
|---|---:|
| Organizations (grouping × links, floors free) in the region | 966 of 5,064 (19%) |
| …of which in two or more families | 117 |
| Pilot 3 pool (1,050 unseen strategies): members | 475 |
| …expansions the architect added / marked maybe | 67 / 71 |
| …rejected by the architect (heart link cut, custodial alone) | 17 |
| …outside, not reviewed | 420 |

| Family | Organizations | Pool members | Different strategies in pool | Other seeds inside |
|---|---:|---:|---:|---|
| S01 Civic Hinge | 486 | 270 | 179 | R1-S02, R2-S01, R2-S04, R3-S01, R3-S03 |
| S02 Arts Loft | 162 | 72 | 11 | R3-S03 |
| S03 Detached Pavilions | 27 | 70 | 22 | – |
| S04 Commons Heart | 81 | 81 | 23 | R3-S02 |
| S05 Academy Tower | 336 | 68 | 45 | R3-S04 |

**Consistency with the Pilot 3 review.**
- None of the 17 strategies the architect skipped is in the region.
- 61 strategies the architect added or marked maybe keep a seed's idea. Under this rule they are new strategies within that idea's family.

**Seeds from runs 02–03 outside every family:**
- R2-S02 (shared heart, but with an arts loft over the hall);
- R2-S03 (one self-contained bar);
- R2-S05 (civic tower);
- R3-S05 (single learning block).

Each differs from the nearest family on a marked decision.

**Axis coverage of the members:**
- topology: all eight link patterns occur;
- distribution balance: 0.35–0.65;
- mean height: 2.0–3.0.

## Point for the architect

**The Civic Hinge family is too wide.** It contains the Arts Loft seed and two other closed clusters (R2-S04, R3-S03). The cause: the hinge idea locks both hinge links but leaves "learning and commons not linked" free (architect, 2026-10-28). Any cluster with administration in the third mass and all three links therefore counts as a hinge. Locking that "not linked" would separate the families.
