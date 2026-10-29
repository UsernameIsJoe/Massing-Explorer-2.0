# Nine-axis records: extraction rules axes-v1

Updated: 2026-10-28 (America/New_York). Task 1 of the [Steps 02–03 plan](STEP02_03_SEMANTIC_FIRST_PLAN.md).

Code:
- `benchmarks/test-elementary-v0.1/seeds_v2/scripts/extract_axes.py` produces `axes/axes_v1.json`.
- `scripts/link_moves_axes.py` (Task 3) produces `axes/move_axis_links_v1.json`.

## Source of the legacy definitions

The legacy definitions come from ME at commit `751ba24` (`explore/axes.py`, `topology.py`, `strategy_contract.py`). The legacy code describes them as a "projection of requested strategy", built for search. As the plan requires, each one was checked before reuse.

## Rules

All values are label-free: they do not depend on mass ids or the order masses are listed in. C is the mass with core academic, G the mass with gym and dining, and T the third mass. An unknown is recorded as unknown and never given a default value.

| Axis | axes-v1 rule | Legacy rule | Change and authority |
|---|---|---|---|
| program_organization | Same-mass bit for each of the 36 department pairs | Same-mass pairwise block | Kept |
| mass_count | Number of masses | Same | Kept. Always 3 under this brief, so it does not separate cases |
| distribution_balance | 1 − (largest mass's share of program area, NFA) | 1 − largest mass's share of the department count | **By area** (architect, 2026-10-28): counting treats medical (730 SF) the same as academic (14,280 SF) |
| topology | Link pattern between C, T and G: all linked; chain through X; single link XY; detached | Geometric bar arrangement (independent bars, paired bars, L around a void) | **Redefined as the link pattern** (architect, 2026-10-28). The bar arrangement moves to geometric_character |
| loading | Unknown until realization | Single- or double-loaded | Needs geometry |
| mean_height | Mean of the masses' program heights (top occupied floor; gym and dining on floor 1 count as 2) | Weighted by the order of mass ids | Legacy value changes when two identical masses swap ids, so it was replaced. Measures program height, not built height |
| height_articulation | Max − min of the masses' program heights | Order-weighted moment | Same defect as mean_height, so replaced |
| vertical_organization | Floors occupied by each department | Hash of department names plus pinned levels | Legacy distances carry no architectural meaning. **Floors per department** (architect, 2026-10-28) |
| geometric_character | Unknown until realization; includes the bar arrangement | Envelope and plate profile | Needs geometry |

Links between masses are part of topology. Department floors are part of vertical_organization.

## Coverage

From the current seed records, 6 axes are derived and 1 is constant (mass_count). Loading and geometric_character stay unknown until realization.

## Known limitation (2026-10-29)

The C/G/T role names and topology patterns assume exactly 3 masses (this brief). Future briefs may allow a range of mass counts (architect). Before another brief is used, generalize: masses are identified by what they hold, topology becomes a link graph over any number of masses, and mass_count becomes a live axis.
