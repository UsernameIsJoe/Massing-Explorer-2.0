# Dynamic Boundary / Region Methods over a Joint Semantic + Structured Descriptor Space

Reading-depth legend: **[FT]** = full text (or a substantial full-text excerpt) was read via fetch; **[ABS]** = only the abstract or landing page was read; **[DOC]** = software documentation. Search-result snippets alone were never used as evidence for a claim.

Project context assumed throughout: 15 seeds with concept text, which gives text embeddings and a 9-axis descriptor. About 1,000 code-generated valid variants have the descriptor only. The 9 axes are mixed-type: binary co-location bits, a categorical link pattern, small-integer heights and ratios. The architect's input is scarce.

## 1. Support/region estimation in mixed spaces (OC-SVM, SVDD, KDE level sets, conformal, hulls, k-NN radius; mixed kernels and Gower)

### Takeaway
Kernel boundary methods (OC-SVM, SVDD, conformal KDE level sets) all depend only on a kernel or distance. A mixed-type kernel can therefore be dropped into them: CASMOPOLITAN's mixed categorical-continuous kernel is a ready-made example, and a Gower-style or product kernel is another option. Of these methods, only split/full conformal gives a finite-sample guarantee at small n, and only under exchangeability. Its regions are loose at n ≈ 100 in low dimensions and get worse as dimension grows. At 15 text seeds, a text-embedding boundary should be a simple k-NN or radius rule, not a fitted density.

### Cited Findings
- **OC-SVM (Schölkopf et al. 2001).** It estimates a "simple" subset S such that a draw from P falls outside S with an a-priori specified probability. The decision function is positive on S and negative outside it. It is a kernel expansion over a potentially small subset of the training data, obtained by solving a quadratic programme, and it extends SVMs to unlabeled data [ABS]. — [Schölkopf et al., Neural Computation 2001](https://mlanthology.org/neco/2001/scholkopf2001neco-estimating)
- **OC-SVM `nu` (scikit-learn).** `nu` is "an upper bound on the fraction of training errors and a lower bound of the fraction of support vectors," with nu in (0, 1]. The kernel can be `'precomputed'` or a callable [DOC]. For this project, that means any custom mixed kernel (product or Gower-derived) can be supplied as a Gram matrix. — [scikit-learn OneClassSVM docs](https://scikit-learn.org/0.18/modules/generated/sklearn.svm.OneClassSVM.html)
- **SVDD (Tax & Duin 2004).** It fits a "spherically shaped boundary" that tightly encloses the target data. Kernels make it non-spherical, it is designed to be robust to outliers in training, and labeled negative examples can be used to tighten the description [ABS]. The negative-example feature maps onto architect rejections: a "not this" selection can shrink the region directly. — [Tax & Duin, Machine Learning 2004](https://mlanthology.org/mlj/2004/tax2004mlj-support/)
- **Conformal KDE prediction sets (Lei, Robins & Wasserman 2013).** The construction augments the data with a candidate y, scores each point by its augmented KDE, and keeps y if its rank is high enough [FT]. — [Lei, Robins & Wasserman 2013](https://www.stat.cmu.edu/~brian/rm/764-2018/week02/lei-robins-wasserman-2013-distribution-free-prediction-sets.pdf)
  - Coverage is "guaranteed whether or not the smoothness conditions hold and regardless of the sample size." The only requirement for validity is exchangeability.
  - The set is sandwiched by two KDE level sets, L−n ⊆ C(α) ⊆ L+n. The outer set keeps finite-sample validity and is cheaper to compute. The inner (plug-in) set is generally not finite-sample valid: its coverage was 0.861 against a nominal 0.9 at n = 100.
  - At n = 100 in a 2D mixture, the conformal set had coverage 0.886 ± 0.005 and Lebesgue measure 35.6, against an oracle of about 28.02. The authors warn that in higher dimensions "the efficiency of the region can be poor."
  - Bandwidth can be selected on one half of the data while keeping validity (Prop. 4.1).
- **Mixed categorical kernel (CASMOPOLITAN).** The categorical kernel is k_h(h, h') = exp((1/d_h) Σ ℓ_i δ(h_i, h'_i)), an overlap kernel with ARD lengthscales. The mixed kernel is k = λ(k_x · k_h) + (1−λ)(k_h + k_x), with λ = 0.5 and a Matérn-5/2 k_x. The product term captures interactions and the sum term captures additive effects [FT]. — [Wan et al., ICML 2021 (arXiv 2102.07188)](https://arxiv.org/pdf/2102.07188)
- **Gower distance.** Gower distance for mixed categorical/numerical data is widely used in practice (for example, a Gower-based SOM R package exists). I did not read a primary methods paper on Gower-based one-class classification, so no specific performance claim is made. — [GowerSom CRAN manual](https://cran.r-project.org/web/packages/GowerSom/refman/GowerSom.html) [DOC, not read in detail]
- **One-class benchmarks.** A 2024 critical review of one-class classification exists; I did not read it in this pass. — [arXiv 2404.17931](https://arxiv.org/pdf/2404.17931) [not read]

### Inferences
- **Kernel for the 9 axes.** A practical choice is a product or sum of per-axis kernels: overlap/Hamming for the binary bits and the link-pattern category, and RBF/Matérn on normalized integer heights and ratios. Combine them as in CASMOPOLITAN's λ-mix and pass the result to OC-SVM or SVDD as a precomputed Gram matrix. ARD lengthscales cannot be fitted without a supervised target. With about 1,000 unlabeled variants, fixed equal weights (Gower-like) are more defensible until the architect supplies labels.
- **Calibrated threshold on any score.** Split conformal can wrap any nonconformity score (OC-SVM decision value, k-NN distance, Gower distance to the nearest seed) to give a calibrated threshold. With 15 seeds, a 90% region cannot be finer than about 1/16 granularity. That is fine for a coarse "inside / provisional / outside" banding, not for fine control.
- **Hulls.** Convex hulls and alpha shapes are ill-defined on binary and categorical axes and degenerate in 9-D with 15 points. I would not use them on the joint space. On the about-1,000 variants they could serve as a sanity view in a 2–3 axis projection only. (Inference; no source read.)
- **Text-embedding space.** With 15 points in hundreds of dimensions, density estimation is hopeless; Lei et al.'s high-dimension efficiency warning supports this. A k-NN or radius rule (cosine distance to the nearest seed ≤ r, with r set by leave-one-out conformal over the seeds) is the most defensible option.

### Gaps
- I found no primary paper benchmarking OC-SVM, SVDD or conformal methods on mixed binary/categorical/integer data at n ≈ 15–1,000.
- Alpha-shape and k-NN radius region literature was not fetched.
- I found no source on combining a sentence-embedding kernel with a categorical kernel in a one-class setting.

## 2. Joint membership rules: AND/OR/weighted combination, conditional neighborhoods, trust regions

### Takeaway
Trust-region BO gives a concrete, well-tested template for a bounded, self-adjusting region in mixed spaces. CASMOPOLITAN's version is a Hamming-ball on categorical variables plus a TuRBO-style box on continuous ones. Both expand after consecutive successes, shrink after consecutive failures, and restart when collapsed. The template maps naturally onto "restriction is the mechanism": the radius is the restriction, and success/failure counters are a principled, bounded way to grow or shrink it.

### Cited Findings
- **CASMOPOLITAN categorical trust region** [FT]. — [Wan et al. 2021](https://arxiv.org/pdf/2102.07188)
  - The categorical trust region contains all points within Hamming distance L^h of the best point h\*, with 0 ≤ L^h ≤ d_h.
  - Acquisition optimisation is a local search over Hamming-1 neighbours that stays inside the trust region.
- **Radius dynamics and restarts (CASMOPOLITAN)** [FT]. — [Wan et al. 2021](https://arxiv.org/pdf/2102.07188)
  - The region expands after a success tolerance of 2 consecutive improvements and shrinks after a failure tolerance of 40 consecutive failures.
  - Each change multiplies the length by α_s = 0.667 (shrink) or 1.5 (expand).
  - When the trust region hits its minimum, the GP and trust region are reset. The new centre is picked by UCB (√β = 1.96) on an auxiliary global GP fitted to earlier local optima.
- **Mixed-variable trust regions (CASMOPOLITAN)** [FT]. — [Wan et al. 2021](https://arxiv.org/pdf/2102.07188)
  - Continuous variables use a TuRBO-style hyper-rectangle with L_min = 0.5⁷, L_max = 1.6 and L_0 = 0.8.
  - The categorical and continuous regions shrink, expand and restart together. A restart triggers when either one hits its minimum.
  - Acquisition alternates a categorical local step with a continuous gradient step.
- **TuRBO (Eriksson et al., NeurIPS 2019)** is the origin of the local trust-region BO design CASMOPOLITAN builds on. Its paper was not fetched here; the TuRBO-style details above come from CASMOPOLITAN's description. — [NeurIPS 2019 paper](https://proceedings.neurips.cc/paper/2019/hash/6c990b7aca7bc7058f5e98ea909e924b-Abstract.html) [not read directly]
- **Locked elements (IC MAP-Elites).** Locked tiles are preserved in all suggestions while the rest evolves. The designer's edited "target room" is fed into the evolutionary process, so every manual change affects generated suggestions [FT excerpt]. This is a deployed instance of a conditional neighborhood ("preserve some aspects, vary others"). — [Alvarez et al., IC MAP-Elites (arXiv 2003.03377)](https://ar5iv.labs.arxiv.org/html/2003.03377)

### Inferences
- **Conditional neighborhood.** A "preserve X, vary Y" rule is a trust region with zero radius on the locked axes and nonzero radius on the free ones. With binary and categorical axes this is simply a Hamming ball restricted to the unlocked axes, which is cheap to enumerate over about 1,000 variants.
- **Combining the two spaces.** The structured descriptor is trusted and the text embedding is noisy at n = 15. That argues for an asymmetric rule:
  - The descriptor trust region is the hard gate (AND).
  - Text-embedding proximity is a soft score that ranks inside the gate, or admits a candidate to a "provisional" band (OR with a cap).
  - A weighted sum hides which space caused admission and is harder to explain to the architect. This is design reasoning, not a sourced result.
- **Accept/reject as success/failure.** Architect accept and reject events can stand in for BO success and failure, which gives bounded, logged growth instead of silent expansion. The specific tolerances (2/40) are tuned for thousands of BO evaluations. With scarce human input, much smaller tolerances would be needed (inference).

### Gaps
- I found no source that formally studies AND/OR membership combining a text-embedding region with a structured-descriptor region.
- The TuRBO paper was not read directly.

## 3. Updating the region from user input (preference elicitation, active learning, version spaces, interactive design tools)

### Takeaway
The most query-efficient ideas are:
- **BOPE:** run short, batched preference sessions on hypothetical outcomes, choosing queries with EUBO.
- **Active level-set estimation (LSE):** spend queries only where the classification of "inside/outside" is uncertain.
- **Preference-learning emitters:** turn each designer selection into extra automated search steps.

Human-study evidence that preference learning improves designer outcomes is weak: the PLE user study found no significant difference.

### Cited Findings
- **BOPE (Lin et al., AISTATS 2022)** [FT]. — [Lin et al. 2022 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2203.11382); [PMLR](https://proceedings.mlr.press/v151/jerry-lin22a)
  - It alternates a preference-exploration stage with an experimentation stage. In the preference stage, the decision-maker compares pairs of outcome vectors, which can be hypothetical and need no new experiments.
  - Utility is a GP with a probit likelihood (Laplace approximation).
  - EUBO selects queries and is motivated as one-step Bayes-optimal. EUBO-f̃ restricts queries to plausibly achievable outcomes.
  - It reportedly beats multi-objective BO and preferential BO baselines. The excerpt I read did not state the exact number of comparisons used.
- **LSE (Gotovos et al., IJCAI 2013)** [ABS]. — [IJCAI 2013](https://www.ijcai.org/Abstract/13/202)
  - It frames finding where an unknown function is above or below a threshold as sequential classification under a GP, using confidence bounds to choose samples and classify points.
  - It has sample-complexity guarantees and extensions to implicit thresholds (a percentage of the unknown maximum) and to batch queries.
- **Preference-learning emitters (Gallotta et al. 2022)** [FT]. — [arXiv 2210.13839](https://arxiv.org/pdf/2210.13839)
  - Designer bin selections in IC MAP-Elites are treated as implicit ratings, with a sliding window of the k most recent selections.
  - Models ranged from tabular to kNN, kernel ridge, linear and neural networks. Full solution context worked better than descriptors alone.
  - Each designer pick triggers several automated MAP-Elites steps, with bins sampled greedily, ε-greedily, by Boltzmann or by Thompson sampling.
  - In the user study (52 valid responses), there was no significant difference in final-solution rankings (Friedman p = 0.764). PLE gave more diverse populations but was rated slower. The authors suspect the search space was too constrained.
- **Designer edits as input (IC MAP-Elites)** [FT excerpt]. Designers can switch which feature-dimension pair is shown "anytime," change cell granularity, and feed edits back as the target. — [IC MAP-Elites](https://ar5iv.labs.arxiv.org/html/2003.03377)

### Inferences
- **Querying for a 1,000-item finite pool.** Because the pool is finite and enumerable, the most economical policy is uncertainty sampling on the boundary (LSE-style):
  - Score every variant with the current membership model.
  - Show the architect only the 3–5 variants nearest the threshold or most disagreed-upon, in one batch (BOPE-style session).
  - Each answer then also serves as an SVDD negative or positive label.
- **Version spaces.** A version-space framing (the set of region hypotheses consistent with all answers) is natural when the region is a conjunction of axis constraints, and it allows "decisive" queries that halve the hypothesis set. I did not fetch a source in this pass; treat it as unsourced.
- **Calibrate expectations.** Given the PLE null result, the project should not expect learned preferences to visibly improve outcomes. Explicit, inspectable boundary edits (lock an axis, exclude a link pattern) may serve the architect better than implicit learning.

### Gaps
- No HCI study was read that measures how many queries architects or designers tolerate.
- Version-space and interactive concept-learning sources were not fetched.
- The exact query counts in BOPE were not extracted.

## 4. Dynamic and novelty archives (novelty search, MAP-Elites/CVT, AURORA, adding new dimensions)

### Takeaway
Three QD archive designs bound growth in different ways:
- **CVT-MAP-Elites** fixes the number of niches regardless of dimensionality, which is a hard cap on growth.
- **Novelty-search archives** admit items above a novelty threshold ρ_min, which risks unbounded growth unless the threshold adapts.
- **AURORA** recomputes all descriptors when its learned descriptor changes, then re-tunes the distance parameter so the archive's resolution (maximum size) stays constant. That is a direct template for "re-descriptorize on a new concern, without silent growth."

### Cited Findings
- **Novelty search (Lehman & Stanley 2011)** [FT]. — [Lehman & Stanley, ECJ 2011](https://www.cs.swarthmore.edu/~meeden/cs81/f17/papers/lehman_ecj11.pdf)
  - Novelty is the mean distance to the k nearest neighbours in the population plus archive, with k = 15 in both experiments.
  - An individual enters the permanent archive if its novelty exceeds ρ_min (initial 6.0 for the maze, 1.0 for the biped).
  - The text I read did not describe a dynamic-threshold rule, so that is not confirmed here.
- **CVT-MAP-Elites (Vassiliades et al.)** [ABS]. — [arXiv 1610.05729](https://arxiv.org/abs/1610.05729)
  - It partitions feature space by a centroidal Voronoi tessellation with a user-set number of regions, "a constant, pre-defined number of regions irrespective of the dimensionality."
  - It contrasts this with the original grid, which grows exponentially with dimension.
- **AURORA (Cully 2019, arXiv 1905.11874)** [FT]. — [arXiv 1905.11874](https://arxiv.org/pdf/1905.11874)
  - Descriptors are the 2-D latent space of an autoencoder trained on the archive's own data.
  - The autoencoder is retrained on a decaying schedule (batches 0, 50, 150, 350, 750, 1550 and 3150 of 5,000).
  - After each retraining, every individual gets a new descriptor and is re-inserted. Collisions make the archive shrink and then regrow.
  - The distance parameter l is redefined after each update to keep the archive's resolution (maximum size) constant, so latent rescaling does not inflate the archive.
  - A later follow-up exists. — [arXiv 2106.05648](https://arxiv.org/pdf/2106.05648) [not read]
- **Switching dimensions at runtime (IC MAP-Elites).** It lets designers switch which two feature dimensions define the map at runtime. The paper excerpt did not explain how the archive is rebuilt on a switch. — [IC MAP-Elites](https://ar5iv.labs.arxiv.org/html/2003.03377)

### Inferences
- **Adding a new concern as a 10th axis (AURORA pattern).** When the architect adds a new concern, the archive can be re-indexed this way:
  1. Compute the axis for all about 1,000 stored variants (cheap, because the descriptor is code-computed).
  2. Re-insert all variants.
  3. Re-set the niche count or radius so the total capacity is unchanged.
  4. Log the change as a new boundary version.

  CVT makes the capacity cap explicit: re-run CVT in 10-D with the same K.
- **Admitting provisional items.** A novelty threshold with a per-version quota is a natural mechanism for admitting outside expansions: an item may enter as "provisional" only if it is novel beyond ρ_min, and at most N per version. This keeps growth explicit and countable (inference).

### Gaps
- The novelty-search dynamic threshold rule could not be confirmed from the text read.
- I found no QD paper specifically on adding a new descriptor dimension mid-run, beyond AURORA's re-learned descriptors and IC MAP-Elites' dimension switching.
- Not covered: Deep Grid / MAP-Elites with sliding boundaries, quality-diversity through human feedback (QDHF), and recent LLM-based QD such as QDAIF.
