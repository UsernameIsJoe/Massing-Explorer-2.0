# Which parts of the output are embedded: embedding views

Status: **design note for architect review**, 2026-10-29. Raised by the architect: should a case have more than one embedding?

## Principle

One embedding per case mixes several aspects of a strategy into one vector: the idea, the means, the weaknesses. Separate embeddings per aspect ("views") are already in the Steps 02–03 plan (Task 2: "compare an overall-description embedding with a small set of aspect-specific descriptions/embeddings"). Retrieval research supports the same point: one vector blurs distinct facets, and per-facet embeddings did better and were easier to interpret ([Multi-Aspect Dense Retrieval, Google, abstract](https://research.google/pubs/multi-aspect-dense-retrieval/)).

## Views (format v3)

| View | Text embedded | One or many per case | Role |
|---|---|---|---|
| **Idea** | `concept` + `intent` | One | The primary semantic coordinate: novelty and rephrasing checks, sparse idea directions. It is the view most independent of the axes (it carries topology only), so it has the best chance of adding something the axes lack |
| **Moves** | Each key move: `move` + `serves` | A set of 2–4 | The means. Two cases can share an idea but differ in moves, or share a move across different ideas. Each move also references explicit decisions, so this view is where meaning and structure meet most directly. It may ground far better than the idea view. Set distance: average best match |
| **Unresolved** | Each `unresolved` item | A set | The architect's proposed "negative steer" (clarified 2026-10-29: `unresolved`, not the trade-off). It shows recurring weaknesses across cases. As guidance, phrase it as a goal ("this problem recurs; propose an idea that resolves it"), not as "avoid X": telling an LLM to avoid something can prime it to produce that thing ([Pink Elephant problem](https://arxiv.org/pdf/2402.07896): GPT-4 still mentioned the forbidden topic 13% of the time when told to avoid it, and smaller models did no better than without the instruction). Items are often generic ("needs dimensional check"), so this view is noisy. `main_tradeoff` is not embedded for now |
| *Not embedded* | `section_intent`, `program_stance` | – | Grounding text. It is **read by extraction** and checked against the record. Embedding it would mostly re-encode structure: Pilot 01 found embeddings of placement prose at chance |
| *Not embedded* | `structure` | – | Axes, computed by code |
| *Not embedded* | `direction_response`, `name` | – | `direction_response` reveals the arm; `name` is too short to embed reliably |

## Pilot 4 scope

- **Steer with the idea view only.** The question of Pilot 4 is whether meaning adds anything beyond the axes. Adding views as arms would multiply arms beyond what 10 cases per arm can separate.
- **Embed every view of all 40 outputs anyway,** at no extra LLM cost, and analyse them as exploration, not decision.
- **Before Pilot 4, a free check on the existing 15 seeds:** does key-move text track its referenced decisions better than concept text tracks the whole record? It needs only a short local embedding run, about 50 short texts.
- **Follow-up pilot:** steering by moves or unresolved items, if the evidence justifies it.

## Variable mass count (architect, 2026-10-29)

The current brief fixes 3 masses, but future briefs may allow a range or several options. Format v3 takes the mass count from the brief. These parts still assume 3 masses and must be generalized before another brief is used:
- the role names of axes-v1 (C, G, T) and the topology patterns;
- the Experiment 1 questionnaire;
- the Pilot 4 gap cells.

The general form: masses identified by what they hold (the learning mass, the commons mass, others), and topology as a link graph over any number of masses. Mass count then becomes a live axis instead of a constant.
