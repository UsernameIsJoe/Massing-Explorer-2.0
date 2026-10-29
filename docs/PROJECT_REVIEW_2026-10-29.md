# Project review: is the direction intact, coherent and supported?

Date: 2026-10-29. Requested by the architect before planning the next steps. This review proposes no new experiments.

## 1. The direction as now agreed

The contribution is to make three parts work together ([CORE_CONTRIBUTION.md](CORE_CONTRIBUTION.md)):

- **The LLM** proposes ideas in language.
- **The embedding** shows how those ideas relate in meaning, and steers the LLM in words.
- **The axis system** locates every proposal exactly, through the structured record the LLM writes.

Over iterations, the LLM explores with a map instead of blindly.

An idea takes shape in three representations:
1. concept and intent;
2. strategy: key moves, locked decisions and the structured record;
3. scheme: dimensions and GSF.

## 2. What exists, and its role in that direction

| Item | Role now | Status |
|---|---|---|
| Seed format v2 (concept, intent, key moves, structure, optional commitments) | The LLM's output contract; links concept to strategy | Keep. The prompt still needs vertical intent and special-education placement in words (Experiment 1). **Not yet changed** |
| 15 seeds (3 runs × 5) | Starting ideas and the first paired text–structure data | Keep. They hold about 8 distinct ideas |
| Axes-v1 (`AXIS_RECORDS_SPEC.md`) | The exact anchor, computed by code | Keep. Strategy-stage axes are derived; loading and geometric character belong to the scheme stage |
| Encoders and Pilots 01, 01b, 01c | Tested the embedding as a **judge of similarity** | Evidence: weak as a judge; bge-m3 is paraphrase-robust |
| Experiment 1 and the Mantel results | First grounding map | Evidence: topology carried; storeys, vertical organization and special education not stated in concepts |
| Structural generator (Pilot 3, 1,050 valid variants) | Finds empty axis regions | Keep as the axis-side gap finder |
| Architect's weights (Pilot 2), Pilot 3 decisions, carrying marks | User input that shapes the space | Weights stay as **user configuration** of distance. Decisions and marks are validation data, never the mechanism. The region drafts are withdrawn |
| Research report and notes | Precedents and methods | Keep as reference |

## 3. Coherence issues found

1. **The docs still say "the boundary is primarily semantic embedding"** (README, backbone, memo, Steps 02–03 plan). The agreed framing gives the embedding two roles, meaning relations and steering, and gives the axes exact location. These documents contradict the core page and need updating once the architect confirms (§6).
2. **Two roles of the embedding were tested as one.**
   - Every test so far treated the embedding as a **judge** of similarity: Pilots 01, 01b, 01c, Mantel. In that role it is weak beyond topology. That is the "positive but not promising" part.
   - The role the agreed framing relies on is the embedding as a **map for steering** the LLM. That role has **never been tested**.
   - So the weak results do not undercut the direction; they do not support its central part either.
3. **"Seeds" and "grounding data" are mixed together.**
   - **Seeds** are the starting ideas of the space for a brief; a few are enough.
   - The 100–150 extra cases are a **grounding corpus**: paired text and structure for measuring and learning the meaning–axis relation.
   - Keeping them apart avoids two confusions: needing 150 seeds to run the pipeline, and calling a probe dataset a design space.
4. **Unguided LLM generation saturates.**
   - Our runs gave about 8 ideas in 15 seeds.
   - At scale, [Si, Yang & Hashimoto 2024](https://arxiv.org/html/2409.04109v1) found only about 200 non-duplicate ideas out of 4,000 generated, using embedding similarity above 0.8 as the duplicate rule, with the unique count plateauing.
   - So repeated prompting alone will not give a diverse corpus. That supports the need for steering, and it is a risk for the corpus plan.
5. **The axis system is staged, which fits the shaping of an idea.**
   - At the strategy stage: program organization, distribution balance, topology, heights and vertical organization.
   - At the scheme stage: loading and geometric character.
   - Mass count is fixed at 3 by this brief.
   - This is coherent. It also means the test bed exercises only part of the axis system, so generalizing beyond one brief and three masses remains untested.
6. **All evidence is small.**
   - At most 15 seeds (about 8 ideas) and at most 26 human judgments.
   - One small local extractor.
   - Some readings were decided post hoc: the llama-only map and the Pilot 2 special-education rule.

## 4. Evidence against the claims

| Claim | Evidence | Strength |
|---|---|---|
| Meaning alone is not trustworthy for structure | Pilots 01 and 01b (structure 8/10, 8/11); 01c edit test failed by all encoders; Experiment 1 | Consistent across tests |
| The LLM alone explores narrowly | 8 ideas in 15 seeds; 400 code variants never offered; Si et al. at scale | Consistent, and external support |
| The structured record anchors exactly | Validator passes; axes computed by code | By construction |
| Meaning and axes share a bridge | Topology: 4 of 4 encoders, extraction κ up to 1.0; partly named program placement | Real but narrow |
| Meaning adds something the axes miss | Pilot 01b: 3 items, best of 8 variants | Weak |
| The embedding steers the LLM to useful new ideas | None | **Untested** |
| The joint space beats either space alone | None | **Untested** (the central claim) |

## 5. Verdict

**Intact and coherent:** the parts fit one story, and nothing found contradicts it.

**Supported in its premises:**
- the semantic side needs grounding;
- the LLM needs a map;
- the anchor works.

**Not yet supported in its payoff:**
- that steering by meaning yields better exploration;
- that the joint space beats either alone.

**Fallback if steering by meaning adds nothing:** the contribution narrows to LLM exploration directed by axis gaps, with semantic deduplication. That is still useful, but it is a smaller claim. The test results should be read against this fallback.

## 6. For the architect

**One decision, needed before the docs are updated.** Replace "boundary primarily semantic" with the agreed joint wording:
- the axes locate and bound exactly;
- the embedding supplies meaning relations, steering and novelty checks, and cross-checks on the traits it carries;
- membership requires both.

Every other point above is either organizing or for the planning step.
