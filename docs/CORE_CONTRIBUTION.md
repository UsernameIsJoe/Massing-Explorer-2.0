# ME 2.0: core contribution

Stated by the architect, 2026-10-28. Every task, pilot and proposal is checked against this page first.

## The contribution

Ground the semantic meaning of a strategy or concept in a firm strategy axis system.

- **Semantic side:** the LLM explores freely in a semantic embedding space. This is where flexibility, creativity and reframing come from.
- **Axis side:** a firm system of concrete traits that can be seen and counted in each case. Examples: how many masses there are, how the masses relate to each other, what is stacked or linked. These are traits, not IDs.
- **Grounding:** every strategy the LLM proposes is reflected robustly onto the axis system. The output keeps the LLM's strengths and is trustworthy because it is grounded.

Making the two systems work together is the research. Surveys, labeling and human judgment are minor supports. They are never the mechanism.

## How the three work together (architect, 2026-10-29)

**The embedding steers the LLM in words, and the structured record anchors every proposal to the axes exactly.** Over iterations, the LLM does not explore blindly; it explores with a map.

| Part | Role | Nature of its link |
|---|---|---|
| LLM | Proposes ideas in language: concept, intent, key moves and a structured record | – |
| Embedding | Shows how ideas relate in meaning. It decides what the LLM is shown: contrasts, combinations, underexplored directions. It also flags rephrasings | Statistical, measured |
| Axis system | Locates every proposal concretely. Computed by code from the structured record | Exact |

A gap can be found on either side:
- **A sparse meaning region:** the LLM is asked, in words, for an idea in that direction, and the axes show whether the result is concretely new.
- **An empty axis region:** the LLM is asked for a meaningful idea that produces that structure, and the embedding shows whether the result is a real idea or a forced one.

Every result is located in both spaces and checked for agreement. A vector is never decoded directly into an idea.

**Who explores what.**
- **The LLM brainstorms in language.** It does not explore the axis space naturally: unguided runs repeat a few ideas, it never offered the 400 valid variants that code found, and forcing explicit targets or rigid formats is known to degrade its outputs.
- **Code explores the axis space systematically.** The LLM is brought into an axis gap only by being asked, in words, for a meaningful idea there.

**Joint boundary.** The axes locate and bound strategies exactly. The embedding supplies meaning relations, steering and novelty checks, and cross-checks the traits it carries. Membership requires both.

## Key highlights: the joint map and the exploration loop (architect, 2026-11-03)

> **Do not lose these.** Agreed after Pilot 4. They answer "should LLM creativity or axis strategy go first?" and define the grounded product the contribution is about. Every later pilot should be read against them.

### 1. The connecting space is a joint map, not the embedding itself

The embedding alone cannot be the space where creativity and strategy meet:
- it is coarse: it resolves neighbourhoods of ideas, not individual strategies (Pilot 4 yardstick);
- it carries only some axes: concept text carries topology, not storeys or special-education placement unless the format makes the text state them (Experiment 1, format v3.1);
- fusing the two into one vector space needs thousands of paired examples, and the project has dozens; a fused distance would also hide which system made a call.

The connecting space is a **joint map in which every idea has two addresses**:
- its **meaning neighbourhood** (embedding);
- its **axis cell** (computed by code from the structured record).

The two are linked case by case, because every case carries both text and a record. **That case-by-case link is the grounding, and the joint map is the grounded product.** Over time the map shows, for example, "the commons-as-heart family has only ever landed in these cells" or "this cell has been reached by three different idea families". Guidance is composed from both addresses together. The embedding is one coordinate of the meeting place, not the meeting place.

Roles that follow:
- **Novelty is judged on the axes**, the robust system.
- **The embedding records the exploration journey**: which idea neighbourhoods have been visited and how often. The axes cannot see this, because the same idea placed in five structures counts as five new cells.
- **The embedding chooses the words around an axis gap**: ideas to avoid (over-used), idea families never paired with that structure (to borrow), contrasts.
- **Risk to test against:** if the guidance becomes derived only from the axes, it is axes-only with extra steps and J will equal A. The embedding earns its place only by adding what the axes lack: which *ideas* are worn out or untried.

### 2. It is a loop, not an order

Neither the LLM nor the axes goes first permanently. Each round:

**joint map → guidance → LLM proposes → code locates the proposal (axes + meaning) → map updated → …**

- **Round 0 is the LLM, freely** (the seed-first decision): creativity sets the starting ideas.
- **From then on, the map goes first in each round:** it decides *what to ask for*. The LLM always owns *how*: the idea itself.
- So "strategy first" means the **plan** comes first, not the axes dictating a structure; "creativity first" means the **idea** comes from the LLM every round. Both hold inside every round.

### 3. Keeping creativity under a plan

1. **The plan says where to end up and what to avoid, never what the idea is.** Pilot 4's prompts did this ("find a meaningful idea that leads there"), and validity held.
2. **Give the LLM room inside the target:** a region, or a choice of 2–3 gaps, rather than one exact cell.
3. **Alternate free and directed rounds, and let the map decide when to switch.** While free rounds keep reaching new idea neighbourhoods, let the LLM roam. When they start repeating (saturation, detected by the embedding), switch to directed rounds aimed at axis gaps. The LLM is free until the map shows it has stopped finding new ground.

**Test this framing implies (proposed, not yet planned):** "free until saturation, then joint-directed" against "free until saturation, then axes-directed". Structure is judged on the axes; repetition is judged by meaning neighbourhood.

## How an idea takes shape

The idea goes through three representations; the axis record is computed from the strategy record at each point.

1. **Concept and intent:** the idea, written by the LLM.
2. **Strategy:** key moves, locked decisions, and the structured record (program by mass, floors, links).
3. **Scheme:** realized dimensions and GSF, produced by the realization engine for selected strategies.

## What this rules out

- Dropping the semantic side when an embedding test is weak. A weak result locates what still needs grounding; it does not remove the semantic side.
- Replacing either system with human input.
- Treating the axes as after-the-fact description only.
- Building a region, membership rule or shortlist that uses only one of the two systems.

## The mechanism to research

1. **Projection.** A proposal is concept text plus explicit structure (seed format v2). Code computes its axis record deterministically.
2. **Grounding strength.** Measure, axis by axis, how far the semantic side determines the axis side.
   - Correspondence: which axes semantic distance tracks.
   - Round trip: from the concept text alone, can the traits it claims be recovered?

   Axes the semantics carries are cross-checks. Axes it does not carry must be grounded explicitly.
3. **Consistency.** A proposal is trustworthy when its text and its axis record agree. A disagreement is reported, never silently resolved.
4. **Exploration.** The LLM moves in semantic space, for example by developing, connecting or reframing. Each proposal is projected onto the axes, so the system can always say where in strategy space it landed. The axis coverage, meaning which trait combinations are still empty, is fed back to the LLM as direction.
5. **Region.** Membership combines semantic relation and axis grounding: joint membership, plan Task 4.

## Precedents for the division of labour

- [LLM-Modulo (Kambhampati et al., ICML 2024)](https://arxiv.org/abs/2402.01817): the LLM proposes as an approximate knowledge source, and sound external verifiers check, in both directions.
- [DStruct2Design (2024)](https://arxiv.org/pdf/2407.15723) and [floor-plan generation with verifiable rewards (NeurIPS 2025)](https://arxiv.org/pdf/2605.14117): LLM output as a structured record, with numerical checks of the constraints it claims.

These ground layouts, not strategy semantics. Grounding an open semantic strategy space in a strategy axis system is the part they do not cover.
