# ME 2.0 project memo — semantic possibility space

Updated: 2026-10-26 (America/New_York).
Status: seed-first construction selected as the starting approach; representation, expansion mechanisms and performance benefits remain open.
Sources: October 26 user directions, backbone and research responses; October 13 project discussion; October 8 research review.

This memo records the current working direction for future project work. It supersedes the assumption that Step 1 is simply asking an LLM to build a sample space, and the earlier development sequence that made toolkit/MCP extraction the immediate Step 03 task. It does not change historical experiments or claim a new pipeline has been implemented.

## Latest acceptance — eight-step pipeline baseline, October 26

The user accepted the [eight-step pipeline](CURRENT_BACKBONE.md#accepted-eight-step-pipeline-baseline) as the baseline to work from. It develops the seed-first decision below into: confirmed brief; distinctive strategic seeds; semantic space/boundary construction; iterative exploration and expansion; maturity assessment before narrowing; realization/testing; revise/focus/archive or re-search; and final case presentation.

Boundary stability is one maturity signal, not sufficient evidence to stop. Deliberate expansion attempts, useful discoveries and current user concerns also matter. Cheap feasibility probes may precede detailed realization. Realization or feedback can reopen the boundary and strategic search. Record history throughout rather than only at output.

This workflow is now accepted; representation, seed count, boundary construction/update mechanisms, maturity thresholds, confidence/budget policies and stopping criteria still require development and testing. Manual chat/script interaction remains the practical constraint. No implementation or experimental result is claimed.

## Latest decision — seed-first entry, October 26

The user chose to start with [LLM-generated strategic seeds and progressive space construction](STEP03_SEED_FIRST_SPACE.md). Generate a small set of distinct proposals against the active brief (five initially suggested), derive an initial semantic account, and research how to extend its boundary as new briefs and evidence arrive.

This uses LLM reasoning immediately, retains semantic connections originating in the proposals, avoids comprehensive upfront enumeration/new case-format design, and establishes brief-specific focus. A minimal comparable record and grounded relationships are still needed. Initial outputs are seeds, not the limits of the design space.

The research priority shifts to **expansion beyond shared seed assumptions and robustness across different initial sets**. The proposed first test compares the same seeds with ordinary chat/history versus a reconstructed semantic space, repeated with different and deliberately narrow seed sets. It is not yet executed.

First experiments must work through **manual chat/script exchanges** because the user cannot automatically call advanced LLMs from the pipeline. Preserve user direction and record transfers/interventions. API integration is not required to investigate the method.

This selects the entry route without freezing a representation, space-expansion algorithm or initial count. Earlier concepts-before-cases and source/expert/hybrid constructors remain research alternatives rather than current starting requirements.

## Current authority — October 26

The [current backbone](CURRENT_BACKBONE.md) records the latest workflow and nine governing directions. The [cognition/ML assessment](STEP03_COGNITION_AND_LLM_ASSESSMENT.md) records the subsequent six user responses. They govern current priorities where earlier proposals differ.

Preserve prior ME/ME 2.0 work. The core is the semantic initial sample space and smart interaction with an existing LLM through a script/method and supporting tools. A new LLM is not the deliverable.

The active workflow is **semantic strategy search under iterative briefs → shortlist → dimensional realization → user selection/brief → revise/archive/focus existing cases and/or re-search the broader space → evolve and test → contextual local optimum**. It remains revisable.

The user proposes multiple trees weighted by promise and selected through ongoing briefs, not an average/median across trees. This is a candidate mechanism, not a chosen schema, MCTS policy or model ensemble.

Retain semantic control as supporting theory and prioritized replay as a useful concept. Adaptive language-guided revision remains interaction/prompting background, not a selected structural addition. Prioritize **strategic certainty before realization, realization effort associated with confidence and interest, and degradation/anchoring during long LLM interactions**. Evidence, thresholds, budget policies and context-renewal mechanisms require discussion/testing.

The three-part structure below remains compatible background. Its October 13 proposed next clarification is historical; the October 26 notes now set priorities. Construction and representation remain open; neuroscience/ML analogies are not architectural validation.

## 1. What the pseudo sample space means

The proposed space describes architectural possibilities with semantic meaning before every possibility has been instantiated or independently evaluated. The LLM should be able to locate a proposal, infer related or contrasting possibilities, and generate a concrete case using the brief and current context.

“Pseudo” means that membership, feasibility and predicted benefits are not all established through actual samples. A region may describe a family, partial strategy, construction recipe or architectural hypothesis. It must not be counted as a completed, compliant design merely because it has a meaningful name.

The aim is to keep broader possibilities referenceable while directing expensive realization and evaluation toward useful depth. Changing user input should redirect exploration through shared project state, rather than repeatedly refining only the latest answer.

Potential relationships include relevance, similarity, contrast/opposition, mutation/adaptation and conditional trade-offs. Their representation and derivation are research questions. A graph, fixed grid or learned embedding has not been selected.

The project remains strategy-first: program organization, topology, stacking, connections and other architectural commitments are the reasoning objects; concrete forms realize and test those commitments.

## 2. Agreed three-part structure

| Part | Responsibility | What remains to establish |
|---|---|---|
| **1. Research and develop the construction method** | Determine the representation, knowledge sources and pipeline that create a referenceable semantic possibility space. | How meanings and relations are derived, grounded, organized and revised; which method improves downstream navigation. |
| **2. Test LLM navigation, generation and iteration** | Use the space, brief and evidence to position proposals, infer cases, realize candidates and respond to iterative user input. | Whether semantic guidance improves valid, useful exploration; whether ME axes or explicit search methods add value. |
| **3. Learn, refine, archive and present** | Revise hypotheses from results, deepen promising candidates, retain alternatives and present concrete outputs with trade-offs and uncertainty. | Reliable update/retention policies, contextual comparison, and how evidence feeds back without corrupting hard requirements. |

Part 3 operates throughout exploration and feeds back into Parts 1 and 2. It is not only a terminal stage after all sampling is finished.

### Essential correction about Part 1

**The request is to research a method for constructing the space, not to assign its construction to an LLM by default.**

LLM assistance is one possible component. Symbolic/compositional methods, domain knowledge, relational structures, learned representations and hybrids are candidate approaches to compare. Do not freeze an LLM-only constructor, an ontology, an embedding model or a graph schema before researching their implications.

Part 1 is the likely methodological research centre. Parts 2 and 3 have tested ingredients and precedents, but their operation with this new representation still requires evaluation.

## 3. Intended mechanism and limits

The semantic layer is intended to help an LLM use learned associations and contextual reasoning to propose useful cases before extensive project-specific evaluation. “Direction,” “instinct” and “guesses” refer to this proposed behavior, not verified access to the model's hidden reasoning or a calibrated probability of success.

A meaningful space should connect intentions and architectural commitments to possible transformations and consequences. Generic labels alone may add little beyond the brief. The proposed added value is project-specific organization of commitments, contrasting possibilities, unresolved questions and measured outcomes.

Keep these distinctions explicit:

- **Facts and hard requirements:** independently grounded and enforced.
- **Possible transformations:** available operations or recipes whose supported scope is stated.
- **Expected consequences:** hypotheses, with context and an observable test.
- **Observed consequences:** measurements tied to an actual candidate and evaluation version.
- **Unsupported possibilities:** not currently realizable/checkable by the backend; not automatically architecturally illegal.

Not every semantic relationship should become a mandatory rule. Predictions and organizational choices must remain revisable. The method should permit missing relationships or new distinctions to be introduced.

A semantic layer can reduce evaluations needed for useful proposals if its guidance is informative. It cannot establish comprehensive coverage, feasibility of unsampled possibilities or a globally best design. Its own construction and inference costs count toward any efficiency comparison.

## 4. Position of existing ME components

| Component | Current agreed position |
|---|---|
| **CSP sampling and initial shortlist** | No longer required as the main generator/admission gate in the proposed architecture. Actual removal or reuse is an implementation decision after method research. |
| **Constraint checks / solvers** | Independent enforcement remains necessary. CSP or numerical/geometry solvers may assist completion or repair where useful; semantic descriptions are not feasibility certificates. |
| **ME's nine axes** | Optional positioning/comparison support to test. Semantics can complement axes; no decision requires preserving or discarding the exact previous encoding. |
| **MCTS** | Optional explicit mechanism for selecting exploration actions. Branch reasoning by an LLM is not automatically MCTS. |
| **BO** | Optional explicit mechanism for allocating expensive evaluations. LLM guessing is not automatically a surrogate with calibrated uncertainty and an acquisition policy. |
| **Learn/refine/archive** | Continuous evidence and memory functions, adapted to new representation and user updates; not automatically transferred unchanged. |
| **MCP/toolkit** | A later integration option. It is not the immediate central research deliverable. |

If used, MCTS/BO would primarily select experiments in Part 2 using Part 3's evidence. They are not assumed to be contained inside the LLM.

Preserve the explicit no-cross-mass department-split hard requirement in the school experiment: each whole department belongs to one mass. Neither semantic generation nor a repair may silently waive it. Hard constraints must come from the active brief/requirement ledger, with changes explicitly recorded.

## 5. Main research questions for construction

1. **Representation:** What makes a location, region, relationship or direction identifiable? Can relationships be non-orthogonal and context-dependent?
2. **Knowledge sources:** How do briefs, program relationships, architectural precedents, symbolic rules and prior observations establish meanings? What is provided by an LLM versus independently grounded?
3. **Implicit generation:** How does a region or relationship specify a constructible case without enumerating its members?
4. **Grounding:** How are architectural concepts connected to executable strategies and observable properties, with uncertainty and capability limits visible?
5. **Revision:** How can evidence or a new user concern change the representation without erasing alternatives or making comparisons misleading?
6. **Evaluation:** Does the construction method improve actual navigation and valid candidate generation beyond useful descriptions, diverse memory and contextual retrieval?

Seed-first construction is now the selected starting route; its representation and expansion mechanisms are unresolved. The next methodological deliverable is a small discriminating experiment, including different seed sets, before full-system implementation.

## 6. Research guardrails and comparisons

The initial comparison should hold the LLM, brief, candidate language, validation and resource limits constant where possible. Compare candidate space-construction methods against the same model with the same brief and diverse history but without the additional semantic relationships.

Test sparse-evidence generation and separate user-update scenarios: preference changes within existing criteria, a newly introduced criterion, and a hard-requirement/program change. The new-criterion case is central because a map may have merged designs that later need to be distinguished.

Measure independently valid strategic diversity, useful improvements, adaptation, transformation fidelity and total resource cost. New names, longer rationales and subdivided regions are not evidence of new architecture. Preserve raw candidates and version the context, representation and evaluation.

Neither deterministic programming nor CSP is intrinsically inflexible. The target limitation is a narrow representation or fixed architectural judgment. An LLM can also amplify familiar patterns and convergence. The proposed construction method must help expose and revise those biases.

Novelty and superiority remain hypotheses. A negative result may relocate the contribution to the design language, retrieval or memory rather than the semantic map.

## 7. Relevant precedents from the discussion

These links record literature already checked in the conversation; they are starting points for construction-method research, not proof of this architecture's novelty or performance.

- [LLAMBO — Large Language Models to Enhance Bayesian Optimization](https://arxiv.org/html/2402.03921v2): contextual prior knowledge and sparse-data proposals; tested in hyperparameter optimization, with additional inference cost.
- [In-context QD](https://arxiv.org/html/2404.15794v2): descriptors and diverse organized examples guide generation; assumes a defined feature space and can struggle when relevant patterns are unclear.
- [Semantic Navigation for AI-assisted Ideation](https://arxiv.org/html/2411.03575v1), 2024 preprint: traversal between related problem and solution statements, including newly generated statements.
- [Luminate](https://luminate-research.github.io/), CHI 2024: task-relevant dimensions and values structure generation and human exploration.
- [IDEA](https://arxiv.org/html/2506.10587v1), 2025 preprint reviewed: abstract design decisions, LLM-derived constraints, MCTS and subsequent realization; evaluated in article composition and visualization.
- [Hypothesis Graph Refinement](https://arxiv.org/html/2604.04108v1), 2026 preprint: unverified semantic predictions guide exploration and are corrected from observations; embodied navigation is an analogy, not an architectural validation result.

The untested-semantic-space principle has precedents. The potential architectural contribution concerns the construction, grounding and revision of useful semantic possibilities under changing user intent and independently enforced constraints.

## 8. Evidence and document status

- This is a project-direction memo, not a performance report or approved implementation specification.
- The [October 8 research review](STEP03_RESEARCH_REVIEW.md) remains a literature/code assessment. The clarification above governs how its illustrative proposals should be interpreted.
- The [constraint alignment audit](../benchmarks/test-elementary-v0.1/step02/CONSTRAINT_ALIGNMENT_AUDIT.md) governs the scope of claims from the earlier pilot.
- This update does not rerun experiments, revise locked scores or modify the original ME engine.

## 9. Step 1 clarification — research session 2026-10-13

The user selected **concepts and relationships**, **relational navigation**, and **a reusable core with a contextual project layer**. A link should primarily carry **conditional reasoning**: why concepts may support or conflict with one another, leaving the LLM to devise the particular case. These historical preferences did not select a graph schema or construction algorithm, and executable recipes were not required as the primary semantic content. The later seed-first decision now governs the order of construction: derive an initial account from strategic proposals, then expand it.

[Construction research — pass 1](STEP03_SPACE_CONSTRUCTION_RESEARCH.md) compares expert-structured, source-grounded, evidence-induced and hybrid acquisition methods. The next clarification should use a concrete navigation example to distinguish what the core knows, what the LLM infers and what realization tests. No new implementation or architectural performance result is claimed.
