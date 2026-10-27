# Steps 02–03 — axis-based evaluation and seed expansion

Created: 2026-10-26. Updated: 2026-10-27 (America/New_York).
Status: user-approved research direction, with subsequent scope clarification and candidate-method review; no implementation, experiment, calibrated thresholds or performance result.
Authority: the user's analytical-axis plan and acceptance, October 27 clarification of cross-dimensional scope, model-cost discussion and requested progress review. Method recommendations below remain proposals to test.
Workflow authority: [current backbone](CURRENT_BACKBONE.md#accepted-eight-step-pipeline-baseline).
Continuity: [seed-first construction](STEP03_SEED_FIRST_SPACE.md).

## Latest clarification and progress assessment — October 27

**Step 03 is scope construction, not similarity retrieval, clustering, or primarily local neighbourhood expansion.** Related cases can be distant in the overall coordinate system: they need a substantive connection to the brief or a seed on some strategic dimension/level, while adding missing distinctions and combinations. A shared trivial attribute alone is insufficient. Initial scope should be broad enough that later brief-guided changes are ordinarily refinements, not repeated reconstruction. This is a design expectation, not a proven stability result; retain recovery from major omissions.

Step 02 is clearer and ready for a small evaluation prototype once a minimal encoding is specified. Its measurements remain conditional on that encoding. Increasing count usually increases coverage, so evaluate marginal benefit and cost; there is no demonstrated optimal count. Seed usefulness must also be tested through Step 03.

Step 03 remains the main methodological uncertainty. Covering arrays and maximum coverage are useful experimental components, not a selected conceptual spine. Coherent architectural strategies must not be reduced to combinations of labels. Coverage saturation may reflect an impoverished vocabulary rather than sufficient scope.

The principal risk is recreating the original restricted-space problem: a comprehensive fixed axis vocabulary plus compatibility rules could defeat the reason for starting from LLM reasoning. Use axes for comparison, algorithms for gap detection and collection management, and semantic reasoning to introduce possibilities outside the encoding.

## 1. Scope and decision

For now, concentrate on pipeline Steps 02 and 03. Treat Step 01's confirmed brief as available. Defer detailed development of Step 04 onward until seed evaluation and initial-space construction are resolved; retain the accepted eight-step backbone.

- **Step 02:** compare prompt styles and initial case counts using reproducible measurements of strategic diversity, coverage, compliance, stability and cost.
- **Step 03:** use the strategic axes to assemble a broad, brief-relevant collection across dimensions, retain semantic relationships, and investigate a sufficient provisional initial scope. Added cases need not be close to any seed.
- Initial count X is an experimental variable. Five was an example; 3/5/8 are possible pilot levels, not selected settings or a universal optimum.
- Use existing advanced LLMs through manual chat/script exchanges. No model training or automated advanced-model API access is required for the first tests.

The user proposed locating cases in an axis system, then calculating distances, coverage and possibly cosine similarity or clusters. For construction, each seed would populate related alternatives, families or opposing strategies across relevant dimensions. Seeds plus related cases would anchor the initial space. The accepted refinement is to preserve this direction while researching the mathematical meaning of coordinates, relatedness and boundary.

## 2. Descriptive axes, separate from quality

Axes describe architectural commitments and observable strategic properties. Quality, brief alignment and feasibility are separate assessments: equal quality scores do not imply the same strategy.

Use a mixed-type representation rather than forcing all concepts onto continuous scales:

| Type | Illustrative strategic property | Comparison |
|---|---|---|
| Numerical | Share of program assigned upstairs | Difference divided by a fixed meaningful range |
| Ordered | Explicit levels of access separation | Declared ordinal comparison; do not assume equal semantic spacing without justification |
| Categorical | Centralized or distributed shared facilities | Match/mismatch, or a separately justified category relation |
| Relational | Department co-location and direct connections | Comparison of assignments/relations; encoding and weighting remain to be specified |

These examples do not freeze the axis list or replace the original ME axes wholesale. Review prior encodings and retain useful distinctions. A categorical label must not acquire artificial numerical order.

Each axis needs a definition, type, domain/range, extraction rule, evidence/source, treatment of unknowns, and version. Keep the semantic account alongside coordinates: intent, commitment, conditional consequences, trade-offs and relationships. Coordinates alone cannot replace architectural reasoning.

The main residual interpretation lies in choosing axes and mapping proposals into them. Analytical scoring can be deterministic conditional on those choices; it cannot establish that the representation captures every meaningful difference. Missing commitments remain unknown, not inferred compliance. Do not reward incomplete cases with deceptively small or large distances.

Check repeated encodings, paraphrases and relabelled masses for consistency. Equivalent mass-label permutations must not count as distinct strategies. Inspect related axes for repeated counting of the same difference.

## 3. Distance baseline and alternatives

**Starting candidate: Gower-style mixed-type dissimilarity.** For complete comparable coordinates:

d(a,b) = sum_j[w_j * delta_j(a,b)] / sum_j[w_j]

Here delta_j uses the comparison appropriate to axis j. Fixed numerical ranges and declared weights make contributions comparable. The final rules for missing, inapplicable, ordinal and relational fields require specification; do not assume every extension retains metric properties.

- Freeze ranges and evaluation weights across compared runs. Per-run min/max normalization would change the meaning of distance.
- Start with transparent weights and check sensitivity. Equal weights are not automatically neutral when axes overlap.
- Keep preference/quality weights distinct from descriptive diversity weights.
- Cosine similarity is not the default for mixed strategic coordinates: it measures direction relative to an origin and can ignore magnitude differences. It may be useful for suitable semantic embeddings as a supplementary analysis.
- Cluster analysis is exploratory, especially with very small seed sets; pooled independent runs are more informative than declaring five seeds to be five established families.
- Do not use an enclosing box or convex hull as the primary coverage measure. Extremes can enclose unexplored or invalid combinations; small seed sets in many dimensions also give degenerate volumes.

Gower is an established component, not a validation of this architectural encoding [1].

## 4. Step 02 measurements

Report complementary measurements rather than prematurely collapse them into one weighted score.

| Measurement | Calculation/question | Limitation |
|---|---|---|
| Encoded compliance | Cases passing all applicable checkable hard rules / generated cases | Not a full dimensional-feasibility certificate; report unknown and failed checks separately |
| Exact duplication | Repeated equivalent commitment configurations | Depends on canonicalization and representation |
| Pairwise separation | Distribution/mean of distances between seeds | Can reward extremes while missing intervening possibilities |
| Local redundancy | Each seed's distance to its nearest other seed | Depends on scale; not total coverage |
| Reference coverage | Fraction of independent reference cases close to a seed | Relative to the reference, not all architecture |
| Value-pair coverage | Fraction of declared valid categorical value-pairs represented | Pair coverage does not guarantee higher-order coverage |
| Stability | Across-run variation of coverage/separation/compliance | Stable omissions remain possible |
| Cost | Length, time, script effort and manual transfers/interventions | More cases generally require more resources |

For seed set S, independent reference set R and declared tolerance epsilon:

C_epsilon(S;R) = |{r in R : min_(s in S) d(r,s) <= epsilon}| / |R|

A complementary diagnostic is the largest reference-to-nearest-seed distance:
h(R,S) = max_(r in R) min_(s in S) d(r,s).
This asks where the largest reference gap remains. The k-center literature supplies a related established representative-coverage objective [2]; any algorithmic guarantee requires its own assumptions, including suitable metric properties.

Combinatorial testing provides methods for measuring t-way value-combination coverage [3]. Their transfer to architectural evaluation is proposed; software failure-interaction findings are not evidence that architectural interactions stop at pairs.

**Optional summary candidate: Vendi Score.** Its similarity-matrix spectrum gives an effective number of distinct elements [4]. It is not selected as the primary score. A valid positive-semidefinite similarity kernel and its scale must be specified; an arbitrary conversion of a mixed dissimilarity matrix is not automatically suitable. Compare against the interpretable metrics and account for sample-count effects.

## 5. Experiment design — not yet run

1. Freeze a controlled architectural brief and a small, independently specified strategic benchmark with explicit decisions and constraints. Enumerate valid reference configurations where practical. The LLM receives the brief, not the enumerated answer set.
2. Require comparable minimal commitment fields plus a semantic explanation from every condition. Do not prescribe architectural families in one condition while claiming it is an unguided baseline.
3. Cross prompt style with initial case count, using the same briefs and repeated independent fresh chats. This tests interactions between prompt and count. A staged pilot may screen prompts, but cannot establish that prompt rankings remain unchanged across counts.
4. Candidate prompt contrast: simple brief-responsive generation versus explicit strategic-distinctiveness instructions. Ask for differences in commitments and trade-offs rather than cosmetic names. Exact prompts remain to be written and frozen.
5. Hold model/version, supplied information, available settings and evaluation rules consistent. Log host details, actual output length, truncation and user intervention.
6. Distinguish comparable detail per case from a fixed total response budget; these test different trade-offs. More seeds must not win solely through a larger hidden budget, nor lose because each is described less adequately.
7. Set tolerances and acceptance criteria before judging results. Report variation and count-versus-cost curves in numerical tables; there is no current optimum or calibrated threshold.
8. Evaluate count provisionally on Step 02, then check whether its seeds support Step 03 construction. The smallest count meeting declared criteria is a candidate operating choice, not a universal optimum.

Freeze the evaluation axes/reference across conditions. The evolving working space may propose new distinctions, but rerun all compared sets under a common new evaluation version rather than silently changing the ruler for one condition.

A controlled benchmark enables exact conditional evaluation but limits generality. Later test transfer on the existing school program and real constraints. Preserve the whole-department/no-cross-mass-split rule. A pooled real-project reference offers estimated coverage, not an exhaustive ground truth.

## 6. Step 03 — broad scope construction

The October 27 clarification supersedes neighbourhood expansion as the primary framing. Seeds are starting anchors, not centres whose immediate surroundings define the target.

### Candidate generation and collection selection are separate

- **Generation:** obtain coherent cases expressing missing strategic commitments and combinations, including directions absent from all seeds.
- **Selection:** choose which cases add useful scope to the collection under a declared effort budget.
- **Boundary account:** distinguish the current vocabulary, explicit constraints, represented possibilities, and unknown directions. A selected collection alone does not establish all valid architecture within a continuous region.

Retain within-axis changes, coupled changes and commitment reversals as optional generation operations, but do not constrain expansion to small coordinate moves or descendants of individual seeds. Cross-seed recombination and independent reframing can introduce distant but substantively relevant cases. Preserve semantic intent, conditional trade-offs and dependencies alongside coordinates.

### Relevance is distinct from proximity and preference

A candidate must have an explicit substantive connection to the brief, such as an organizational question, intention or trade-off. Respect applicable hard requirements independently. A compliant but less-preferred strategy can still be important for defining scope.

Do not use global seed similarity as an admission gate. A brief connection on one dimension can coexist with significant differences elsewhere; it does not automatically excuse hard violations or establish useful relevance. Operationalizing semantic relevance remains unresolved and may require reviewed interpretation. Unsupported backend capabilities remain separate from architectural impossibility.

### Candidate algorithm A — constrained covering-array extension

IPOG-family algorithms, implemented in ACTS, construct t-way covering arrays over declared dimensions and values. ACTS documents extension of existing test sets, constraints and mixed-strength relations [10].

Proposed transfer:
1. Encode the initial seeds using a provisional vocabulary.
2. Identify combinations of declared values not yet represented.
3. Generate additional configurations that cover missing valid combinations; use stronger coverage for selected important interactions.
4. Complete/interpret configurations as architectural cases where the representation is insufficient, and verify actual commitments and encoded constraints.
5. Count coverage from the resulting case, not from the requested target coordinates.

For example, centralized/vertical and distributed/horizontal seeds cover both values on both axes but omit centralized/horizontal and distributed/vertical. Missing combinations can be far from existing cases. These are illustrative labels, not adopted axes or validated architectural possibilities.

**Strength:** systematic cross-dimensional breadth, with no LLM needed to manipulate already formalized decisions.
**Limit:** known vocabulary only; pairwise coverage does not cover every higher-order strategy, establish feasibility beyond encoded rules, or guarantee semantic coherence. Numeric axes need justified discretization. ACTS is a software-testing precedent, not an architectural validation result. Do not assume every feature combination works in every tool mode/version.

### Candidate algorithm B — weighted maximum coverage

For candidate pool V and declared coverage targets U, let C(x) be the targets actually represented by candidate x. Targets may include individual values, valid value combinations, or explicitly defined strategic commitments.

F(S) = sum_(u in U) w_u * indicator[u in union_(x in S) C(x)]

Starting with the initial seeds, greedily add the candidate with the greatest remaining coverage gain under a declared case budget. A separate minimum-set-cover formulation can ask for the fewest additions meeting a target; do not conflate these objectives. Cost-sensitive selection and its guarantees require separate specification.

This is an established monotone submodular coverage objective with available implementations [11]. It selects from a supplied pool; it does not invent missing cases or concepts. Its target universe and case-to-target mapping determine what the optimization means. Start with transparent/equal weights and examine sensitivity; preference weights must not silently remove useful contrasting strategies. No coverage target list or weights are locked.

### Other methods assessed

| Method | Position after review |
|---|---|
| MMR [12] | Cheap baseline balancing relevance and redundancy; not an explicit guarantee of cross-dimensional scope. |
| DPP / k-DPP [13] | Diversity-oriented subset selection; representation/kernel design adds complexity before encoding is validated. Keep as a later comparison. |
| Facility location [14] | Represents a supplied pool; common families can dominate a density-weighted objective. Not the primary scope criterion. |
| MAP-Elites / In-context QD [7,8] | Useful archive/generation precedents; predefined descriptors and automated repeated calls do not directly resolve initial scope or the manual-chat budget. |
| Novelty search [15] | Distance-based archive novelty is an optional diagnostic; sparse or distant points are not by themselves evidence of useful scope. |

An initial experiment may combine covering-array extension for known dimensions, a separate batch challenging shared assumptions, and coverage-based selection. This is a research candidate, not adopted production architecture. Independent proposals must be able to introduce new values, axes or relationships rather than being forced into the initial vocabulary.

## 7. Execution cost and model allocation

An advanced LLM call per seed/axis/variation could create excessive manual work. The user can use advanced models through chat, and suggested automatic local-model work through Ollama. Compare ordinary algorithms before adding LLM calls.

| Responsibility | Candidate allocation | Qualification |
|---|---|---|
| Coordinate extraction from explicit structured fields; canonicalization | Code | Ambiguous meaning must not be silently inferred |
| Distances, coverage, deduplication and missing combinations | Code | Conditional on declared encoding |
| Formalized variation, compatible completion and constraint checks | Code/solver such as CP-SAT [16] | Only encoded requirements and expressible cases; formulation/search cost still matters |
| Prose extraction, routine labeling, readable explanations | Local model through Ollama [17], if tested | Model/hardware dependent; schema validity is not semantic correctness |
| Initial coherent strategies, difficult trade-offs, missing concepts and shared-assumption challenges | Advanced LLM/user in consolidated batches | Proposed allocation, not a demonstrated requirement for the strongest available model |

Keep raw structured cases as authoritative. A local model should not invent explanations that alter their commitments. Validate extracted values and audit semantic fidelity. Ollama is a runtime, not one fixed model or a guaranteed speed/capability level.

A candidate economical loop is: advanced-model seed batch; automatic formalized generation/filtering/selection; optional tested local interpretation; one consolidated advanced-model review of unresolved gaps or missing concepts. No fixed call count or time saving is established. Local inference can still be slow, and preparation, repairs and manual transfer cost count.

Model-cascade research supplies a cost-allocation precedent [18], not an established routing policy or performance claim for ME2. The previously proposed continuous advanced-LLM archive loop is a comparison candidate rather than the default.

## 8. Boundary meaning, precedents and limits

The goal is sufficient initial strategic scope, not merely an increasingly dense archive. The user's expectation is that later changes are usually modest, but evidence of a major omission must allow substantial reopening.

Distinguish:
- the currently expressible domain under the axis vocabulary;
- actual cases and their semantic relationships;
- combinations admitted/excluded by explicit constraints;
- unresolved candidates, omitted distinctions and outside-vocabulary directions.

Anchors do not certify every intermediate configuration. No convex-fill rule, neighbourhood radius, learned manifold, density threshold or continuous boundary estimator is selected. A case/link record is not itself a complete membership algorithm. A scalar diversity score cannot certify boundary sufficiency.

General Morphological Analysis [5] supports parameter/value spaces and explicit compatibility judgments. Higher-order dependencies may require more than pairwise checks. Formal Concept Analysis's attribute exploration [6] supports testing proposed implications with confirmation/counterexamples. Implications observed in a few seeds and unsupported LLM confirmations remain hypotheses.

In-context QD [8] supports generation from organized examples with existing pretrained models, but uses defined features/evaluators in numerical and robotics benchmarks. QDAIF [19] demonstrates archive-based LLM variation and AI evaluation in creative writing; its subjective evaluator does not satisfy independent analytical assessment by itself. DiCE [9] supports constrained diverse alternatives but originally targets classifier-output changes and proximity; it is less directly aligned with broad initial-scope construction.

These are component precedents. The complete seed-to-semantic-boundary method and any neuroscience correspondence remain unvalidated.

## 9. Proposed next experiment and progress review

**Current assessment:** meaningful progress in specifying the problem; Step 02 is more tractable than Step 03. No evidence yet shows that the constructed space improves architectural reasoning beyond asking for additional distinct schemes. This is the assistant's candid assessment recorded at the user's request, not an empirical result.

Use the existing school program and active brief for a small discriminating comparison, preserving the whole-department/no-cross-mass-split rule. Do not repeat the earlier matched-constraints audit error.

Across multiple independent seed sets, compare equal-budget expansion conditions:
1. **Ordinary LLM broadening:** ask for additional distinct, brief-relevant strategies.
2. **Algorithmic coverage:** fill missing combinations within the provisional vocabulary.
3. **Hybrid:** algorithmic gap detection plus targeted LLM generation and challenges beyond the vocabulary.

Keep seed inputs and comparable information consistent within each comparison. An auxiliary algorithms-only / algorithms-plus-local-model / occasional-advanced-review ablation can investigate model allocation; it is not necessary to run every cross-product initially.

Measure:
- independently checkable valid strategic additions and semantic coherence;
- new target/combinational coverage and marginal gain per case;
- important distinctions omitted or collapsed by the encoding;
- recovery from different or narrow seed sets;
- interpretation errors and unresolved feasibility;
- total machine cost, output length, human review, repairs and manual exchanges.

A controlled reduced reference benchmark remains useful for exact conditional evaluation, held-out recovery and invalid-admission/exclusion tests. Real-brief transfer must not be confused with exhaustive ground truth. Preserve the broader same-seeds ordinary-chat/history versus semantic-space navigation comparison for later work. Do not develop Step 04 onward in detail now.

### Sufficiency and stopping

Coverage saturation is only evidence within the declared target vocabulary. Also test whether independent challenge proposals reveal substantive missing directions, whether the encoding distinguishes valuable alternatives, and how results change with plausible axis/weight choices. An LLM's failure to suggest anything new is not a completeness certificate.

Before implementation, specify a minimal encoding and reproducible mapping, provisional target universe, distance rules, exact prompts, budgets, repeats and decision criteria. Avoid requiring a comprehensive ontology before any test. Explain mathematics and mechanisms so the user retains authorship of the conceptual spine.

No algorithms, local-model setup, experiments or new performance scores were implemented by this documentation update.

## Sources checked in the discussion

[1] Gower (1971), A General Coefficient of Similarity and Some of Its Properties. [Original paper](https://cbio.mines-paristech.fr/~jvert/svn/bibli/local/Gower1971general.pdf); [official daisy documentation for mixed-type dissimilarities](https://search.r-project.org/CRAN/refmans/cluster/html/daisy.html).

[2] Gonzalez (1985), [Clustering to Minimize the Maximum Intercluster Distance](https://www.cs.columbia.edu/~verma/classes/uml/ref/clustering_minimize_intercluster_distance_gonzalez.pdf).

[3] Kuhn, Kacker and Lei, [Measuring and Specifying Combinatorial Coverage of Test Input Configurations](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142).

[4] Friedman and Dieng (2023), [The Vendi Score: A Diversity Evaluation Metric for Machine Learning](https://arxiv.org/abs/2210.02410).

[5] Ritchey (2015), [Principles of Cross-Consistency Assessment in General Morphological Modelling](https://www.swemorph.com/amg/pdf/amg-4-2-2015.pdf).

[6] Borchmann (2012), [A General Form of Attribute Exploration](https://arxiv.org/abs/1202.4824).

[7] Mouret and Clune (2015), [Illuminating Search Spaces by Mapping Elites](https://arxiv.org/abs/1504.04909).

[8] Lim, Flageat and Cully (2024), [Large Language Models as In-context AI Generators for Quality-Diversity](https://arxiv.org/html/2404.15794v2).

[9] Mothilal, Sharma and Tan (2020), [Explaining Machine Learning Classifiers through Diverse Counterfactual Examples](https://www.microsoft.com/en-us/research/publication/explaining-machine-learning-classifiers-through-diverse-counterfactual-examples/).

Related foundation: Shah, Vargas-Hernandez and Smith (2003), [Metrics for Measuring Ideation Effectiveness](https://people.tamu.edu/~stevesmith/SmithCreativity/ShahVargas-HernandezSmith2002.pdf), separates quantity, quality, novelty and variety. Its design-feature choices still require explicit modelling.


[10] NIST, [ACTS user guide](https://csrc.nist.gov/csrc/media/projects/automated-combinatorial-testing-for-software/documents/acts_user_guide_2_92.pdf): IPOG-family algorithms, extend mode, mixed strength and constraints. Version-specific documentation, not a claim about every current combination of features.

[11] [submodlib set-cover objective documentation](https://submodlib.readthedocs.io/en/latest/functions/setCover.html): weighted coverage and marginal-gain selection.

[12] Goldstein and Carbonell (1998), [Summarization: Using MMR for Diversity-Based Reranking and Evaluating Summaries](https://aclanthology.org/X98-1025/).

[13] Kulesza and Taskar (2012), [Determinantal Point Processes for Machine Learning](https://www.alexkulesza.com/pubs/dpps_fnt12.pdf).

[14] [submodlib facility-location documentation](https://submodlib.readthedocs.io/en/latest/functions/facilityLocation.html).

[15] Lehman and Stanley (2011), [Abandoning Objectives: Evolution through the Search for Novelty Alone](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehman_ecj11.pdf).

[16] Google OR-Tools, [CP-SAT solver documentation](https://developers.google.com/optimization/cp/cp_solver).

[17] Ollama, [structured outputs documentation](https://docs.ollama.com/capabilities/structured-outputs).

[18] Chen, Zaharia and Zou, [FrugalGPT](https://arxiv.org/abs/2305.05176).

[19] Bradley et al., ICLR 2024, [Quality-Diversity through AI Feedback](https://qdaif.github.io/).
