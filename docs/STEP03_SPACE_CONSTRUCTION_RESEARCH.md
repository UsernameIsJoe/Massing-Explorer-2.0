# Step 03: construction of a semantic possibility space — research pass 1

Research date: 2026-10-13. Status: exploratory synthesis, not a selected construction algorithm or implemented capability.

## 1. User clarifications obtained in this session

The user selected:

1. **Concepts and relationships** should exist before concrete schemes, rather than a population of imagined complete candidates.
2. **Relational navigation** is the primary model, rather than requiring continuous latent positions.
3. **A reusable core with a contextual project layer** is preferred.
4. **Conditional reasoning** is the primary content of a link: explain why concepts may support or conflict with one another, leaving the LLM to devise the case.

These choices clarify the target but do not determine the constructor. The construction method remains the main research question. LLM extraction, symbolic structures, expert knowledge and empirical learning are candidate components, not predetermined owners.

A working description is: **a source-grounded relational space of concepts and conditional design reasoning, instantiated for a brief and revised through candidate evidence**. This is an interpretation of the answers, not an established method or novelty claim.

## 2. The most relevant construction precedents

Primary sources were searched across design theory, program synthesis, scientific ideation, robotics and quality-diversity. This is a targeted review, not an exhaustive survey or universal state-of-the-art ranking.

| Precedent | Construction mechanism | Transferable lesson | Limit |
|---|---|---|---|
| **C-K design theory**, Hatchuel & Weil, 2009 [C1] | Distinguishes interacting concept and knowledge spaces; considers generation of new objects and knowledge. | Keep proposed possibilities distinct from established knowledge, with exploration able to revise the framing. | A design theory, not a ready-made LLM constructor or efficiency guarantee. Only the publisher abstract was accessible here. |
| **General Morphological Analysis / cross-consistency assessment**, Ritchey, 2015 [C2] | Defines qualitative dimensions/values and documents relations between them. Distinguishes logical, empirical and normative assessments, including conditional flags. | Relationships can organize an implicit combination space without testing every full configuration. Record reasons and scope of judgments. | Depends on chosen variables and assessments; pairwise consistency does not prove global feasibility. Avoid turning preference judgments into hard exclusions. |
| **IdeaSynth**, CHI 2025 [C3] | Uses literature-grounded idea facets and links; users create alternatives and compose connected facets into research briefs. | Partial conceptual elements can remain manipulable before a complete result exists. Sources, links and variants support iterative thinking. | Human research-ideation support with predefined facets; not evidence of independently compliant designs. |
| **Ada**, ICLR 2024 [C4] | Proposes high-level actions from language, grounds them through low-level planning/execution, and retains useful action abstractions. | General knowledge can yield reusable, context-relevant abstractions corrected by interaction. | The reviewed formulation supplies a fixed predicate vocabulary/state mapping. It does not solve all concept discovery; planning domains differ from design. |
| **LILO + Stitch**, ICLR 2024 [C5] | Synthesizes programs, extracts reusable abstractions by symbolic compression, then supplies natural-language documentation. | Semantic legibility matters when an LLM uses a new representation. Executable examples can ground meanings. | Starts with a DSL and examples/tasks. Documentation helps in some domains, but errors removed its benefit in LOGO. Code compression is not automatically architectural abstraction. |
| **UniPred**, accepted IEEE T-RO 2026 according to authors [C6] | Combines LLM predicate hypotheses with demonstration-based classifier learning and feedback. | A top-down semantic prior and bottom-up evidence can jointly construct a useful abstraction. | Requires demonstrations and a provided controller set. It is not sample-free discovery or unrestricted creative generation. |
| **AURORA**, 2021/2022 [C7] | Learns behavioral descriptors from raw sensory data during QD exploration. | A useful representation need not consist only of predefined axes. | Data-grounded descriptors do not automatically provide readable conditional reasoning, especially before current-project samples exist. |
| **Hypothesis Graph Refinement**, 2026 preprint [C8] | Stores unverified frontier predictions separately from observed nodes and retracts dependent hypotheses after contradictions. | Untested semantics should be represented as revisable hypotheses with dependencies. | Physical navigation with VLMs; not design generation or proof of unsampled architectural feasibility. |

Two additional cross-domain construction leads:

- **Tong et al., 2024 [C9]:** extract reported causal relations from psychology literature, build a graph and predict new hypothesis links. Novelty evaluation does not establish the actual causal truth of those hypotheses. For ME, source extraction must preserve the difference between reported claims and independently established relations.
- **Graph-PRefLexOR, July 2026 preprint [C10]:** graph-native, fine-tuned reasoning for materials-science hypotheses. The abstract reports increased conceptual recombination within a bounded semantic space. Only its abstract was inspected; it is a frontier lead, not an architectural recommendation or verified explanation of hidden reasoning.

No single precedent supplies the whole proposed system. Different methods address organization, grounding, abstraction learning or correction.

## 3. Separate the shape of the space from how it is acquired

Selecting a relational map does not tell us how its contents should be obtained.

| Candidate constructor | How it acquires concepts and links | Strength | Risk |
|---|---|---|---|
| **Expert-structured** | People define a small conceptual vocabulary and conditional relations, with reasons and examples. | Inspectable, low-data starting point; useful controlled baseline. | Labor and designer bias; a rigid list of archetypes would repeat the original problem. |
| **Source-grounded synthesis** | Extract concepts, conditions, mechanisms and conflicting claims from briefs, literature and precedents; normalize and review them. | Makes the semantic content traceable and can cover more than existing pipeline cases. | Source selection, extraction errors and ambiguous terminology. A citation is not proof that a relation applies to this project. |
| **Evidence-induced** | Learn useful distinctions and relationships from examples, contrastive outcomes or successful transformations. | Grounds the map in observed behavior and supports reuse. | Requires data, inherits corpus/geometry limits and may miss possibilities outside the existing generator. |
| **Hybrid** | Begin with an inspectable source/expert core, bind it to the brief, and revise relations using outcomes. | Fits reusable knowledge plus contextual hypotheses. | Greater complexity; must show added value over simpler sources or memory. |

**Working preference:** compare an expert-structured baseline, a source-grounded constructor and an evidence-updated hybrid. This is a proposed experiment, not a final decision. A new trained latent representation is not presently required by the user's relational-map preference; embeddings can remain retrieval assistance.

## 4. What a conditional link would contain

A meaningful link should be more informative than “related to,” but need not prescribe a finished case.

Illustrative record:

- Concepts: public operational autonomy and separation of public/academic access.
- Condition: public facilities need to operate while the academic zone is closed.
- Reasoning hypothesis: separate access paths may permit independent operation.
- Possible counterpressure: separation may increase connection or circulation burden.
- Open means: different entrances, access boundaries, whole-department groupings or connections.
- Grounding: identify how the selected access property will be measured.
- Evidence status: source claim, first-principles argument, expert hypothesis, observed instance or unresolved.
- Scope: which programs, site assumptions and access model the reasoning concerns.

This example is an illustrative design hypothesis, not a finding about any existing case. It does not prove that separate masses are required or that every separated scheme performs better.

The core should hold reusable concepts and qualified relations. The project layer binds roles to actual departments and requirements. A candidate branch records the particular commitments selected and which predictions remain untested.

“Why these concepts connect” and “how this exact case is constructed” have different roles. The user's preference puts the former in the semantic layer and leaves much of the latter to LLM generation. Realization still requires executable representation and independent checks.

## 5. A candidate construction pipeline

The following is a research scaffold rather than a commitment to one algorithm:

1. **Define source roles.** Separate actual requirements, source claims, expert judgments, examples and observations. Retain provenance and scope.
2. **Acquire a small reusable vocabulary.** Define concepts with positive/negative or contrasting examples and enough precision for their intended use.
3. **Construct conditional relations.** Preserve conditions, reasons, counterpressures and uncertainty. Include contrasting claims rather than collapsing them into a single “best” rule.
4. **Bind a project layer.** Map concepts to program/site entities and user concerns; check that interpretations correspond to the supplied brief.
5. **Describe untested possibilities lazily.** Compose partial commitments or goals into referenceable hypotheses without enumerating complete schemes.
6. **Audit grounding.** Check whether the concepts refer to expressible, observable properties; record unsupported or ambiguous meanings. Full feasibility remains undecided until the relevant checks can be completed.
7. **Generate, measure and revise.** Feed scoped evidence back into relations and candidate history. New distinctions can enter when the existing vocabulary merges cases that now matter differently.

The reusable vocabulary must be extensible. A hierarchy or ontology should clarify meanings without making the first vocabulary the boundary of all admissible architectural reasoning.

## 6. Limits that the constructor must handle

**Association versus intervention.** Two concepts co-occurring in literature does not establish that changing one improves the other. Directional consequences should retain their evidential basis.

**Pairwise versus joint compatibility.** Three hypothetical allocations of four units each can fit a ten-unit capacity in every pair, but not all together. This elementary counterexample is derived here: a relational map needs to express joint conditions, such as through condition records, factor nodes or hyperedges. Pairwise edges alone cannot certify feasibility.

**Contextual meanings.** “Separate,” “compact” or “public” can have different meanings across briefs. A reusable concept needs binding and qualification, not an assumed universal benefit.

**Prior bias.** Expert, literature-mined and learned cores all have priors. An apparently comprehensive graph can remain a narrow catalogue. Track the source scope, allow new distinctions and reserve exploration outside familiar relations.

**Data dependence.** Learning from a corpus can support new combinations without evaluating all current-project cases. This is different from needing no prior data anywhere.

**Grounding errors.** LILO's documentation failure is a concrete warning: attaching persuasive language to an abstraction can misdescribe it. Meaning needs examples, tests or scoped independent review; names alone are insufficient.

**Map revision versus backend expansion.** Adding a concept does not give the geometry backend a missing capability. Preserve unsupported status while investigating a useful extension.

## 7. A first discriminating study

Start small enough to inspect every relation. The research object is the constructor, not a polished UI or a new search controller.

Compare:

- A small expert-built conditional map.
- A source-grounded map built from the same stated corpus and source budget.
- A hybrid that updates the source-grounded map from a limited, common set of outcomes.

Use controls with ordinary LLM briefing/history and with the same conditional knowledge presented as flat records. The latter distinguishes relational organization/navigation from merely providing more useful information.

Keep candidate language and checks common. Count construction, inference, retrieval, failures and validation in resource totals. Report reusable-core preparation cost separately from per-project cost.

Probe:

- Whether a requested direction changes the intended architectural commitment.
- Whether unrelated commitments and hard rules survive the change.
- Whether the LLM constructs genuinely different strategies from concepts not tied to a single exemplar.
- Whether conditioned predictions match observed outcomes or are appropriately revised.
- Whether the map adapts when a new user concern requires a new distinction.
- Whether benefits persist on a held-out brief.

The no-cross-mass department-split rule remains an explicit invariant in the existing school experiment. Do not let a promising semantic transformation waive it.

Exact finite-domain tests can check some abstraction/constraint behavior. Architectural value and generalization require separate experiments. No study was executed in this research pass.

## 8. Next clarification

The answers establish relational concepts, conditional reasoning and reusable/contextual layers. The remaining distinction is which level of reasoning should occupy the core:

- General intentions and tensions, such as integration versus autonomy.
- Architectural commitments, such as ownership, stacking or access organization.
- Conditional mechanisms connecting those intentions and commitments.

The next useful discussion should use one concrete imagined navigation move and specify what the map already knows, what the LLM infers and what realization subsequently tests. This will help define the granularity and knowledge-acquisition method without selecting a schema prematurely.

## References and inspection scope

- **[C1]** Hatchuel & Weil. *C-K design theory: an advanced formulation.* Research in Engineering Design 19, 181–192 (2009). [Publisher](https://link.springer.com/article/10.1007/s00163-008-0043-4). Abstract only; no unavailable formal results used.
- **[C2]** Ritchey. *Principles of Cross-Consistency Assessment in General Morphological Modelling.* Acta Morphologica Generalis 4(2), 2015. [Author publication PDF](https://www.swemorph.com/amg/pdf/amg-4-2-2015.pdf). Relation types, conditional flags, documentation and resolution sections inspected.
- **[C3]** Pu et al. *IdeaSynth: Iterative Research Idea Development Through Evolving and Composing Idea Facets with Literature-Grounded Feedback.* CHI 2025, DOI 10.1145/3706598.3714057. [Earlier full preprint](https://arxiv.org/html/2410.04025v1), [published record](https://dl.acm.org/doi/10.1145/3706598.3714057). Construction and limitations inspected.
- **[C4]** Wong et al. *Learning Adaptive Planning Representations with Natural Language Guidance.* ICLR 2024. [Published paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/99dec5837aae1a7459960c6121b9e3b8-Paper-Conference.pdf), [preprint](https://arxiv.org/html/2312.08566v1). Operator acquisition, fixed predicate assumption and grounding inspected.
- **[C5]** Grand et al. *LILO: Learning Interpretable Libraries by Compressing and Documenting Code.* ICLR 2024. [Published record](https://proceedings.iclr.cc/paper_files/paper/2024/hash/819cebb05f993840e8a52d7564c5c282-Abstract-Conference.html), [full preprint](https://arxiv.org/html/2310.19791v2). Construction, AutoDoc ablations and semantic errors inspected.
- **[C6]** Wang et al. *Unifying Deep Predicate Invention with Pre-trained Foundation Models.* [Authors' current project page](https://unipred.github.io/) reports acceptance at IEEE T-RO 2026; [reviewed preprint v1](https://arxiv.org/html/2512.17992v1) is from 2025. Methods/limitations inspected. The current page and v1 differ in authorship and experiment scope; no mixed numerical results are used.
- **[C7]** Grillotti & Cully. *Unsupervised Behaviour Discovery with Quality-Diversity Optimisation.* [Original record, revised 2022](https://arxiv.org/abs/2106.05648). This pass refreshed the abstract; prior project review contains fuller discussion.
- **[C8]** Chen et al. *Hypothesis Graph Refinement: Hypothesis-Driven Exploration with Cascade Error Correction for Embodied Navigation.* April 2026 preprint. [Paper](https://arxiv.org/html/2604.04108v1). Representation and correction were inspected earlier in this discussion; domain transfer is an inference.
- **[C9]** Tong et al. *Automating psychological hypothesis generation with AI: when large language models meet causal graph.* Humanities and Social Sciences Communications, 2024. [Primary abstract and journal metadata](https://arxiv.org/abs/2402.14424). Claims limited to this inspection scope.
- **[C10]** Pal et al. *Graph-Native Reinforcement Learning Enables Traceable Scientific Hypothesis Generation through Conceptual Recombination.* July 2026 preprint. [Primary abstract](https://arxiv.org/abs/2607.00924). Abstract-only frontier lead; quantitative claims and hidden-reasoning claims are not adopted.
