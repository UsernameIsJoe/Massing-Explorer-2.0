# Steps 02–03: task status

Read [the core contribution](CORE_CONTRIBUTION.md) first.

Updated: 2026-10-28 (America/New_York).

This file tracks the five tasks in the [Steps 02–03 plan](STEP02_03_SEMANTIC_FIRST_PLAN.md) against the evidence collected so far.

## Process rule (architect, 2026-10-28)

Every proposed pilot or step must state:
- which task and which open decision (plan section 8) it addresses;
- which earlier tasks it depends on;
- whether those earlier tasks are resolved.

Nothing downstream (membership, region, shortlist) is proposed or used while a task it depends on is open. When a result is complete as code, that does not make it resolved as a definition.

Origin of the rule: after Pilot 3, a structure-only region was built and a shortlist was proposed while Tasks 1–4 were still open.

## Asking the architect (2026-10-28)

The architect's time and attention are the scarcest input; too many asks lower the quality of the answers. Ask only for input that changes a decision, batch the asks, state in one line why each matters, and settle anything that has a sensible default without asking.

Before any committed run (downloads, long local runs, chat batches), tell the architect beforehand: what it is for, what it costs (time, downloads, their steps) and what it decides. Then wait for a go.

## Status

| Task | Done | Open | Evidence |
|---|---|---|---|
| 1. Comparable records | Explicit decisions. Semantic description: concept, intent, key moves, brief response, unresolved (seed spec v2.0). Nine-axis records for all 15 seeds (axes-v1, `docs/AXIS_RECORDS_SPEC.md`). | Loading and geometric_character stay unknown until realization. | `seeds_v2/axes/axes_v1.json` |
| 2. Embedding representation | bge-m3 concept + intent is paraphrase-robust. First correspondence (`grounding/correspondence_v1.json`, 15 seeds): semantic distance tracks topology (rho 0.40), weakly program organization and balance (about 0.15–0.19), not heights or vertical organization. | Round-trip grounding (concept text → traits) not yet run. | Pilots 01, 01b, 01c; `grounding/` |
| 3. Intention → decisions → axes links | Done for 15 seeds. Key moves name all 9 departments in 13 of 15 seeds and all 3 links in every seed; pairs named together in one move fix about 10 of 36 co-location bits. | How a move locks (absolute placement vs relation) is part of the Task 4 semantic-lock decision. | `seeds_v2/axes/move_axis_links_v1.json` |
| 4. Joint membership | Draft rule `region/REGION_V1.md` uses decisions only (one system). It does not meet the core contribution and is not the region. | Joint rule: semantic relation plus axis grounding (`docs/CORE_CONTRIBUTION.md`). Depends on Task 2 round trip. | Pilots 02, 03; `region/` |
| 5. Generator | Structural edit generator with hard rules, including the custodial rule; a pool of 1,050 valid strategies. | Introducing a new organizing concept needs an LLM or the architect. | Pilot 3 |

Pilot 3's region file is a structure-only candidate, not the region. The Pilot 3 pool can be reused as the set of unseen test candidates for Task 4, once the region is frozen.

## Agreed plan (architect, 2026-10-28)

1. Experiment 1 (per-axis grounding map) on the current 15 seeds: a cheap check of which traits the concept text carries.
2. Adjust the seed-generation prompt from that result, then generate 100–150 cases across 2–3 LLMs with diversity rules.
3. Rerun Experiment 1 on the full set, then Experiments 2–5 (`reports/Joint semantic axis search space.md`).

## Options noted, not prioritized

- **Larger seed set (architect, 2026-10-28).** Seeds are LLM-generated, so more runs could raise the paired text-and-structure data from 15 to 100 or more. That would make learned alignment testable. Conditions:
  - count distinct ideas, not seeds, and push each run toward difference;
  - use 2–3 different LLMs;
  - split train and test by run or model;
  - match the experiment design in `reports/Joint semantic axis search space.md`.

  Priority is not decided; the architect has not yet reviewed the report.
