# Step 03 — cognition, ML and user assessment

Date: 2026-10-26 (America/New_York).
Status: research synthesis and user disposition; no new architectural experiment or implementation.
Read with the [current backbone](CURRENT_BACKBONE.md) and [project memo](PROJECT_MEMO.md).

## Scope

Assess support, challenges and upgrades for the existing ME 2.0 backbone: semantic strategy exploration under iterative briefs; shortlisting; dimensional realization; feedback; revise/archive/focus; and re-search toward a contextual local optimum.

Working memory and grokking were illustrative user examples, not selected mechanisms. No reviewed evidence establishes that the whole workflow reproduces the brain or matches hidden LLM latent geometry. Develop a method/script for existing LLMs.

The user's assessments below govern priority. Distinguish them from assistant proposals and the literature's actual findings.

## Six findings and user responses

### 1. Value-guided construal — multiple-tree hypothesis

**Research:** Ho et al. (2022) studied simplified task representations for planning in preregistered human experiments, modeling a balance of representation cost and usefulness. Ho et al. (2023) additionally explained rigidity through complexity and representation-switching costs. These are behavioral/modeling results, not architectural validation. [R1, R2]

**User assessment:** It could involve multiple trees operating, with weights suggesting how promising each is. Ongoing briefs decide which trees to include or exclude. Do not produce a median or average across all trees.

**Disposition:** Preserve as a structural hypothesis. Root/branch meaning, weighting and reopening remain open. This is not a finding that the brain runs the proposed forest, nor a choice of MCTS, model ensemble or storage schema.

### 2. Semantic control — high-level supporting theory

**Research:** Whitney et al. (2011) disrupted brain regions using TMS, selectively affecting demanding semantic judgments while strong automatic associations were unaffected. This supports task-sensitive access to conceptual knowledge. Separately, LILO showed that meaningful documentation can help an LLM use abstractions; documentation errors also limited that benefit. [R3, R4]

**User assessment:** Useful high-level supporting gate. Remember that we are creating a script or method that an existing LLM works with, not creating an LLM.

**Disposition:** Retain as supporting theory and a semantic-interface evaluation question. No neural architecture is to be implemented by default.

### 3. Adaptive language-guided abstraction — interaction background

**Research:** ALGAE alternates language-guided identification of missing interpretable features and reward-weight fitting/testing against demonstrations, with simulated and real robot experiments. It does not supply an architectural conditional-knowledge constructor. [R5]

**User assessment:** Mainly prompt engineering; revision is naturally part of the existing process. Useful knowledge, without structural differences.

**Disposition:** Keep as prompting/interaction background. Do not promote a new representation-revision subsystem or automatic feature learner into the backbone. Existing semantic revisability remains; its implementation is unselected.

### 4. Prioritized memory/replay — retain

**Research:** Mattar and Daw's (2018) normative model prioritizes memory access through expected decision gain and expected need, accounting for several hippocampal replay patterns. It is not proof that neurons explicitly calculate those quantities. [R6]

**User assessment:** Useful concept; keep.

**Disposition:** Retain as a candidate principle for refinement, archive revisiting and re-search. The operational quantities and selection rule require development and tests.

### 5. Hierarchical planning/selective realization — high priority

**Research:** Kaelbling and Lozano-Perez (2011) combine abstract planning, deferred detail and approximate geometric reasoning, while identifying failures that require reconsidering abstract commitments. Robotics evidence supports the engineering principle; it does not certify unrealized architectural strategies. [R7]

**User assessment:** Very important. Strategic cases need a good level of certainty, to be tested and discussed. Realization budget could depend on initial confidence and how promising/preferred the strategy is.

**Disposition:** Make pre-realization certainty and budget allocation core research questions. Cheap probes may support shortlisting; detailed realization follows it. No confidence threshold or allocation formula is selected. Keep evidence about realizability separate from user interest and expected benefit.

### 6. Multi-turn degradation/anchoring — high priority

**Research:** Laban et al. (2025) found reduced reliability when tested models received analytical-task requirements over multiple turns; early assumptions and reliance on previous answers were important patterns. Their text-based simulations do not establish an architectural effect size or a universal current-model limit. Self-critique findings are also method-dependent: Bohnet et al. report improvements on planning tasks using 2024 checkpoints. [R8, R9]

**User assessment:** Very important. LLM chat becomes old and stiff after enough iterations. Keep.

**Disposition:** Test conversation aging, anchoring and recovery explicitly. Compare continuation/context procedures with the same current brief, evidence access, model and total resource budget. Context renewal is a candidate, not a proven fix or a selected schedule; project state must survive any handoff.

## Consequences for current work

| Topic | Status |
| --- | --- |
| Semantic initial space and smart LLM navigation | Core contribution |
| Multiple weighted trees selected by ongoing briefs | User proposal; mechanism open |
| Context-sensitive semantic access | Supporting theory for existing-LLM interface |
| Feedback/feature revision | Interaction/prompting background; no new subsystem |
| Prioritized revisit/refine/re-search | Retained concept |
| Certainty before realization | High-priority discussion and testing |
| Budget linked to confidence and interest | User hypothesis; no formula |
| Long-chat stiffness and recovery | High-priority experiment |
| Whole-workflow brain likeness | Unestablished; not sufficient proof of value |

## Candidate experiments for discussion

These are assistant-proposed discriminating tests, not a frozen implementation plan:

1. Compare separately identifiable strategy branches with a matched baseline under changing briefs; measure valid diversity, appropriate selection and recovery of alternatives.
2. Record initial expectations/cheap-check evidence, then realize a controlled set including uncertain cases. Measure errors and total cost instead of equating model confidence with probability.
3. Compare equal realization effort with evidence/interest-informed allocation. Include cases outside the favorites so screening failures remain observable.
4. Compare a simple revisit schedule with a usefulness-based one under the same archive access and brief changes.
5. Compare uninterrupted chat with renewed context preserving equivalent project state; measure obsolete assumptions, hard-rule retention, repetition, valid new directions and handoff cost.

Frozen pilot scores, audit corrections and active hard requirements remain binding. No performance benefit is claimed until tested.

## Sources and inspection scope

- **[R1]** Ho et al. *People construct simplified mental representations to plan.* Nature 606, 129–136 (2022). [Published record](https://www.nature.com/articles/s41586-022-04743-9); [full manuscript inspected](https://arxiv.org/html/2105.06948v2). Behavioral experiments/value-guided construal.
- **[R2]** Ho, Cohen and Griffiths. *Rational Simplification and Rigidity in Human Planning.* Psychological Science (2023). [Author PDF inspected](https://cocosci.princeton.edu/papers/ho2023rational.pdf). Two preregistered studies and complexity/switching model.
- **[R3]** Whitney et al. *The neural organization of semantic control.* Cerebral Cortex 21, 1066–1075 (2011). [Primary abstract inspected](https://pubmed.ncbi.nlm.nih.gov/20851853/). Claims limited to reported task-selective intervention effects.
- **[R4]** Grand et al. *LILO: Learning Interpretable Libraries by Compressing and Documenting Code.* ICLR 2024. [Full paper inspected](https://proceedings.iclr.cc/paper_files/paper/2024/file/819cebb05f993840e8a52d7564c5c282-Paper-Conference.pdf), especially AutoDoc ablations and errors. Also covered in the October 13 construction review.
- **[R5]** Peng et al. *Adaptive Language-Guided Abstraction from Contrastive Explanations.* September 2024 preprint. [Full text inspected](https://arxiv.org/html/2409.08212v1). Feature specification/reward validation; robotics scope.
- **[R6]** Mattar and Daw. *Prioritized memory access explains planning and hippocampal replay.* Nature Neuroscience 21, 1609–1617 (2018). [DOI](https://doi.org/10.1038/s41593-018-0232-z); [primary abstract](https://pubmed.ncbi.nlm.nih.gov/30349103/); [author PDF](https://www.princeton.edu/~ndaw/md18.pdf). Abstract and indexed author-PDF extracts inspected; full-text retrieval failed this session. Gain/need summary is scoped accordingly.
- **[R7]** Kaelbling and Lozano-Perez. *Hierarchical Task and Motion Planning in the Now.* ICRA 2011. [Author PDF inspected](https://people.csail.mit.edu/tlp/pdf/2011/hpnICRA11Final.pdf). Hierarchy, deferred detail, geometric suggesters and refinement limitations.
- **[R8]** Laban et al. *LLMs Get Lost In Multi-Turn Conversation.* May 2025 preprint. [Full version inspected](https://arxiv.org/html/2505.06120v1). Analytical/text-only simulation scope retained; no architectural effect size inferred.
- **[R9]** Bohnet et al. *Enhancing LLM Planning Capabilities through Intrinsic Self-Critique.* December 2025 preprint. [Rendered full text inspected](https://arxiv.org/abs/2512.24103). Uses October 2024 checkpoints; no universal current-model claim adopted.
