# Steps 02–03 — axis-based evaluation and seed expansion

Date: 2026-10-26 (America/New_York).
Status: user-approved research plan; no implementation, experiment, calibrated thresholds or performance result.
Authority: the user's discussion of analytical evaluation, shared axes, and expansion from initial cases into related alternatives; subsequent acceptance of the researched plan.
Workflow authority: [current backbone](CURRENT_BACKBONE.md#accepted-eight-step-pipeline-baseline).
Continuity: [seed-first construction](STEP03_SEED_FIRST_SPACE.md).

## 1. Scope and decision

For now, concentrate on pipeline Steps 02 and 03. Treat Step 01's confirmed brief as available. Defer detailed development of Step 04 onward until seed evaluation and initial-space construction are resolved; retain the accepted eight-step backbone.

- **Step 02:** compare prompt styles and initial case counts using reproducible measurements of strategic diversity, coverage, compliance, stability and cost.
- **Step 03:** continue with the same strategic axes; generate relevant alternatives around seeds, retain their semantic relationships, and investigate a provisional sample-space boundary.
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

## 6. Step 03 — proposed expansion mechanism

Generate semantically justified candidates through:

1. **Within-axis variation:** change one commitment while preserving others where coherent.
2. **Coupled variation:** change multiple commitments together when dependencies require it.
3. **Commitment reversal:** challenge a defining strategic assumption and identify consequential changes. An opponent is not automatically a numerical negative.
4. **Reframing:** introduce a missing decision/value or shared-assumption challenge when the current coordinates cannot express it.

The first three refine the user's alternatives/families/opponents proposal. Reframing preserves the earlier requirement to escape shared seed omissions. These operations remain hypotheses, not implemented or validated architectural operators.

Record parent seed(s), intended change, actual changed coordinates, dependencies, semantic rationale, expected trade-offs, and check status. An attempted one-axis change that necessarily changes other axes should be recorded as coupled rather than silently treated as independent.

A provisional representation can use:
- **Nodes:** seeds and generated alternatives, coordinates, semantic accounts and validation status.
- **Links:** recorded transformations and conditional relationships.
- **Unresolved directions:** proposed alternatives, missing combinations or distinctions awaiting investigation.

This is a candidate operational account, not a frozen graph database/schema. Retain families as explicit hypotheses until their membership and distinguishing commitments are defined.

## 7. Meaning and limits of the initial boundary

Seeds and checked related cases anchor an **explored region**. They do not prove that all points between them are viable or that possibilities outside them are impossible.

Distinguish:
- the currently expressible domain under the axis vocabulary;
- generated cases and their known relationships;
- combinations admitted or excluded by recorded constraints;
- unresolved candidates, gaps and outside-vocabulary directions.

No convex-fill rule, neighbourhood radius, density threshold, learned manifold or continuous boundary estimator is selected. Research must determine which implicit membership/expansion rule is useful and testable. The node/link record alone is not a complete boundary algorithm.

General Morphological Analysis provides an established parameter/value and cross-consistency construction precedent [5]. Pairwise checks can expose exclusions, but higher-order dependencies still need representation. Formal Concept Analysis's attribute exploration provides a precedent for testing proposed implications with confirmation/counterexamples [6]; an implication observed in a few seeds is not a universal architectural rule. LLM confirmation without independent evidence stays hypothetical.

## 8. Closest ML precedents and transfer limits

- **MAP-Elites / quality-diversity [7]:** maintain alternatives located by descriptive features, with quality assessed separately. Supports the archive/axis distinction. Its fixed descriptor structure does not solve dynamic architectural axis discovery or boundary inference.
- **In-context QD [8]:** pretrained LLMs generate candidates using organized archive examples. Supports retaining LLM capabilities while supplying external state. Benchmarks use defined descriptors/evaluators; architectural semantic transfer and manual-chat efficiency remain untested.
- **Diverse counterfactual explanations / DiCE [9]:** generate diverse constrained alternatives around an instance. Supports principles of proximity, diversity and feasible changes. It originally changes classifier outcomes; ME2 has not chosen a classifier or adopted DiCE unchanged.

The complete seed-to-semantic-boundary method is a project hypothesis assembled from supported components, not an existing proven architecture and not a claim about literal brain mechanisms.

## 9. Validation and outstanding work

On the controlled benchmark, hold out valid strategies from the seeds and test recovery. Measure invalid admissions, mistaken exclusions where a membership rule is available, unresolved cases, expansion cost and sensitivity to different/narrow seed sets. Compare seeds alone, ordinary additional generation, and targeted expansion under matched budgets. Do not let larger seed sets gain an uncontrolled expansion allowance per seed.

Preserve the broader same-seeds ordinary-chat/history versus semantic-space comparison in the seed-first document. Subsequent user-brief navigation is retained for later work, not developed now.

Before implementation, resolve:
1. Minimum comparable strategic encoding and the axis list/types.
2. Deterministic mapping, canonicalization, unknown handling and semantic fidelity checks.
3. Distance rules, scales/weights and reference-set construction.
4. Frozen prompt variants, count levels, repeats, budgets and decision criteria.
5. Expansion operator definitions and how recorded cases support an implicit boundary/membership rule.
6. Independent tests showing useful recovery rather than numerical spread alone.

The user directs the conceptual spine. Explain the mechanism and mathematics before building it. No new tests or scores are reported by this documentation update.

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
