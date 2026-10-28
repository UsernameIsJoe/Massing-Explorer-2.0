# ME 2.0: core contribution

Stated by the architect, 2026-10-28. Every task, pilot and proposal is checked against this page first.

## The contribution

Ground the semantic meaning of a strategy or concept in a firm strategy axis system.

- **Semantic side:** the LLM explores freely in a semantic embedding space. This is where flexibility, creativity and reframing come from.
- **Axis side:** a firm system of concrete traits that can be seen and counted in each case. Examples: how many masses there are, how the masses relate to each other, what is stacked or linked. These are traits, not IDs.
- **Grounding:** every strategy the LLM proposes is reflected robustly onto the axis system. The output keeps the LLM's strengths and is trustworthy because it is grounded.

Making the two systems work together is the research. Surveys, labeling and human judgment are minor supports. They are never the mechanism.

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
