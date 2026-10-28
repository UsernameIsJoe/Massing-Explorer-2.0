# Steps 02–03: task status

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

## Status

| Task | Done | Open | Evidence |
|---|---|---|---|
| 1. Comparable records | Explicit decisions. Semantic description: concept, intent, key moves, brief response, unresolved (seed spec v2.0). Nine-axis records for all 15 seeds (axes-v1, `docs/AXIS_RECORDS_SPEC.md`). | Loading and geometric_character stay unknown until realization. | `seeds_v2/axes/axes_v1.json` |
| 2. Embedding representation | Paraphrase robustness passes (bge-m3, concept and intent). | It is unknown whether the embedding carries meaning beyond structure. No trusted judge exists: human labeling is too costly and unreliable, and the LLM judges lean on structure. Aspect-conditioned descriptions have not been tested. | Pilots 01, 01b, 01c |
| 3. Intention → decisions → axes links | Done for 15 seeds. Key moves name all 9 departments in 13 of 15 seeds and all 3 links in every seed; pairs named together in one move fix about 10 of 36 co-location bits. | How a move locks (absolute placement vs relation) is part of the Task 4 semantic-lock decision. | `seeds_v2/axes/move_axis_links_v1.json` |
| 4. Joint membership | Architect's decision weights (department, floor and link). | **The rule.** It must cover unseen strategies, and an unseen strategy has no authored semantics (Pilot 3 addendum). Semantic lock vs implementation lock is not decided. | Pilots 02, 03 |
| 5. Generator | Structural edit generator with hard rules, including the custodial rule; a pool of 1,050 valid strategies. | Introducing a new organizing concept needs an LLM or the architect. | Pilot 3 |

Pilot 3's region file is a structure-only candidate, not the region. The Pilot 3 pool can be reused as the set of unseen test candidates for Task 4, once the region is frozen.
