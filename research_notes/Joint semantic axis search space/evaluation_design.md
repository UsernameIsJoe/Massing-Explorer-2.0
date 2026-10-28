# Evaluating whether a joint semantic + axis search space beats either space alone (small data, scarce human judgment)

Reading-depth legend used on every citation:
- **[FT]** = full text (or a substantive body section) was fetched and read in this session.
- **[ABS]** = only the abstract or landing page was read.
- **[SR]** = seen only as a search-result title/URL; not opened. Claims tagged [SR] are limited to what the title itself establishes. Anything beyond that is in Inferences or Gaps.

Project framing assumed throughout (from the assignment, not from a source): three arms are compared. **S** is semantic embeddings of concept text. **A** is the code-computed 9-axis descriptor record. **J** is the joint/fused space. The available data are 15 seeds x 3 independent LLM runs, about 1,000 text-less code variants, a few dozen architect ratings, local encoders, and manual chat access to frontier LLMs.

---

## 1. Ablation designs for multi-view / fusion systems: how to show fusion beats single views, and the pitfalls

### Takeaway
The most recent large audit found that well-tuned simple baselines, and often the single best modality alone, match or beat complex fusion methods. Common reasons for apparent fusion gains are untuned baselines, single runs, and selecting models on the test set. A credible "J beats S and A" claim needs: equal tuning effort for all three arms; a simple-fusion baseline (for example, concatenation of normalized blocks) to separate "extra information" from "better organization"; resampling-based uncertainty; and a held-out set that was never used for selection.

### Cited Findings
- An audit across nine datasets found that no complex multimodal method reliably beat a simple late-fusion Transformer baseline (SimBaMM). The best complex method had about a 30% probability of winning. — [Fusion or Confusion? Multimodal Complexity Is Not All You Need (arXiv 2512.22991)](https://arxiv.org/pdf/2512.22991) [FT]
- In the same audit, several published fusion architectures (DGL, OMIB, LMF, PDF) were "likely worse than simply using the best single modality (P(Unimodal > Method) > 80%)". The simple fusion baseline itself beat the best unimodal baseline with a probability of only about 0.53. — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- In that audit's survey of prior fusion papers, 0% did hyperparameter tuning of baselines, 0% reported statistical significance, 11% used cross-validation and 21% reported error bars. 82% did include unimodal baselines. — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- The audit's reliability checklist:
  - tune all methods, including baselines;
  - include simple and unimodal baselines;
  - use cross-validation with independent splits and report mean ± SD;
  - standardize optimizers, initialization, splits and protocols;
  - use an identical base architecture across the proposed method and baselines;
  - evaluate on multiple datasets.

  — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- Case study: one method (AUG) inherited splits with only train and test sets, "resulting in model selection on the test set". Under corrected splits and consistent tuning, the simple baseline matched or exceeded it. This is a concrete instance of the selection-bias pitfall. — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- The audit compared methods with a Bayesian hierarchical model and a ±1% ROPE (region of practical equivalence). It reported probabilities of "better / equivalent / worse" rather than p-values. — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- Benchmark results vary noticeably with data sampling, parameter initialization and hyperparameter choice. Randomizing more sources of variation brings an imperfect estimator closer to the ideal one, at a reported 51-fold compute saving. — [Bouthillier et al., Accounting for Variance in ML Benchmarks (MLSys 2021)](https://arxiv.org/abs/2103.03098v1) [ABS]
- A per-modality contribution metric exists for vision-language models, based on Shapley values and independent of task accuracy (MM-SHAP). — [MM-SHAP, ACL 2023](https://virtual2023.aclweb.org/paper_P600.html) [SR]
- The "garden of forking paths" refers to flexible analysis choices that inflate false positives even without deliberate fishing. — [Forking paths problem (Wikipedia overview)](https://en.wikipedia.org/wiki/Forking_paths_problem) [SR]; [FORRT glossary](https://forrt.org/glossary/english/garden_of_forking_paths/) [SR]

### Inferences
Inferences are tied to this project. They are not claims from the sources.

- **Minimum arm set.** Use the following arms:
  - **S** alone.
  - **A** alone, with z-scored axes.
  - **J-concat**: L2-normalized S block plus z-scored A block, each scaled so that the two blocks contribute equal variance.
  - **J-proposed**: whatever learned or weighted fusion is being claimed.
  - **J-shuffled**: A rows permuted across items before fusion.
  - Random-feature controls of the same dimension as the extra block.

  The key reading: if J-proposed beats J-concat, that is evidence for better organization. If J-concat beats S and A but J-shuffled does not, that is evidence that the extra information is real. If J-shuffled ≈ J, the gain is dimensionality or regularization, not information.
- **Matched budgets.** Matched budgets here mean:
  - the same number of fusion-weight settings tried per arm, for example the same grid of the mixing weight α tried for the S-only kNN temperature or the A-only axis weighting;
  - the same number of items retrieved;
  - the same exploration budget (number of generated or selected candidates) in downstream tasks.

  If J has a tunable α and S and A do not, then J got extra degrees of freedom. Either give S and A comparable knobs (axis weights; embedding PCA dimensionality), or select α on a separate split.
- **Best-of-many selection bias.** If several encoders x fusion weights x distance metrics are tried and the best J is reported, the reported margin is optimistically biased. Mitigations:
  1. Pre-register one primary J configuration.
  2. Use nested selection: choose α on runs 1–2 and test on run 3, rotating through all three run orders.
  3. Report the full distribution across all configurations tried, not just the max.
- **Natural CV unit.** The 3 independent LLM runs give a natural cross-validation unit ("leave-one-run-out"). Seeds give a second unit ("leave-one-seed-family-out"). Splitting must be at the seed or idea level, not the item level. Otherwise near-duplicates leak across folds, the analogue of the audit's "subject-wise" splits.
- **Equivalence, not just superiority.** A ROPE-style analysis fits the research claim well. For example, report P(J better than max(S, A) by more than a pre-stated margin), so that "J ≈ S" is a reportable outcome.

### Gaps
- No source was found that specifically ablates text-embedding + hand-crafted-descriptor fusion for retrieval or search-space construction in design domains. The fusion audit is about supervised multimodal classification.
- The specific recommendations of Bouthillier et al. were not read (abstract only).

---

## 2. Ground truth without heavy labeling

### Takeaway
Several weak-but-free ground truths are available. They are best used as a battery, each probing a different property:
- cross-run recurrence as natural positive pairs;
- known-transformation probes: paraphrase should not move items, and controlled structural edits should move them along the right axis;
- conditional-similarity (C-STS-style) counterfactual pairs, where "same idea under aspect X" can differ from "same idea overall";
- round-trip recovery accuracy;
- downstream task success.

C-STS shows that even strong models score below 0.5 Spearman on aspect-conditioned similarity. This motivates conditioning probes on specific aspects.

### Cited Findings
- C-STS defines sentence similarity *conditioned on a natural-language aspect*. Example: two sentences are more similar under "the motion of the ball" than under "the size of the ball". The dataset has about 20,000 instances. Strong models, including GPT-4, Flan and SimCSE in fine-tuned or in-context modes, reach Spearman below 50 (i.e., below 0.50). — [C-STS, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.345) [ABS]; also [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2305.15093) [SR]
- Representational Similarity Analysis (RSA) compares representations via their pairwise dissimilarity matrices, which lets heterogeneous representations be related through a common "distance-matrix" currency. This is the basis for comparing S, A and J geometries against each other and against any judged dissimilarities. — [Kriegeskorte et al. 2008, Frontiers in Systems Neuroscience](https://www.frontiersin.org/articles/10.3389/neuro.06.004.2008/text) [SR]; [PubMed record](https://pubmed.ncbi.nlm.nih.gov/19104670/) [SR]

### Inferences
These are concrete probe designs for this project. They are not from sources.

- **Cross-run recurrence (natural positives).** For each idea that recurs across runs (same seed concept, independent generations), treat the cross-run pair as a positive and other items as negatives.
  - Metrics: Recall@k, MRR, AUC of positive vs negative distances, all per arm.
  - Ground truth needed: a one-time grouping of recurring ideas. An LLM can propose the grouping, and the architect only spot-checks a sample of groups.
  - Caveat: if recurrence was itself detected with the S encoder, S gets a circular advantage. Define recurrence groups with a different instrument (a different encoder, an LLM, or the architect) or by seed ID.
- **Paraphrase invariance.** An LLM paraphrases concept text while keeping the structured record fixed.
  - Metric: displacement ratio d(x, paraphrase(x)) / median nearest-neighbor distance. Lower is better.
  - Expected result: A is trivially invariant, because its record is unchanged. S should move a little. J should sit between them.
  - This probe guards against S's sensitivity to wording.
- **Controlled structural edits.** Code changes one axis by a known amount (for example, footprint compactness up one step) without changing the text.
  - Metric: does the item move in the expected direction and roughly monotonically with edit size? Measure with Spearman of distance vs edit magnitude.
  - S is blind to these edits by construction. This is exactly the failure mode J is supposed to fix.
  - The roughly 1,000 code variants without text are a ready-made edit set for A and J. For S, they need generated text, or they must be treated as an "A-only items" condition.
- **C-STS-style counterfactual pairs.** Build triples of the form (anchor, same-concept-different-structure, different-concept-same-structure).
  - Ask which item is "closer under aspect X" for two aspects: "organizing idea" and "massing geometry".
  - Prediction: J ranks correctly under both aspects, while S wins only on concept and A only on geometry.
  - Ground truth is known by construction, so no labeling is needed.
- **Round-trip recovery accuracy.**
  - From J coordinates (or a nearest-neighbor decode), recover the seed ID and the axis values. Metrics: top-1 seed accuracy; axis MAE.
  - From text alone, predict axis values. This measures how much A information S already contains. If S → A recovery is high, J's "extra information" is small.
- **Downstream task success.** Run a fixed-budget exploration task, for example "find K candidates satisfying a new criterion" or "cover all seed families", with each arm as the search space. This is the most decision-relevant test and uses no labels if success is code-checkable.
- **Consistency tasks.**
  - Triangle or transitivity checks on any judge, human or LLM.
  - Agreement of neighbor sets across the 3 runs: Jaccard of each item's kNN set under each arm, computed across runs.

### Gaps
- How the C-STS conditions were constructed was not read (abstract only).
- No published benchmark was found for round-trip recovery in architectural massing.

---

## 3. Search-space quality metrics (QD / generative-model evaluation)

### Takeaway
Useful quantities fall into four groups:
- **QD-style archive metrics**: coverage = occupied cells / total cells; QD-score = summed (offset-normalized) quality over occupied cells.
- **Reference-free diversity**: the Vendi score, an effective number of distinct items under a chosen kernel.
- **Fidelity/coverage against a reference set**: k-NN-manifold precision/recall, with k = 3 in the original paper.
- **Stability and generalization diagnostics**: built with resampling and held-out briefs.

Every one of these depends on the chosen feature space or kernel. That is the central trap: S, A and J cannot each be scored "in their own space". All arms must be scored in a common, independent measurement space, or in each space crossed with each other.

### Cited Findings
- **QD-score** is "the sum of f values of all cells in the archive". It is credited to Pugh et al. 2015, and the paper normalizes it by archive size. **Coverage** is "the number of occupied cells in the archive divided by the total number of cells". Objectives were linearly mapped to [0, 100] (f' = af + b) so that QD-scores are non-negative and comparable. — [Fontaine & Nikolaidis, Differentiable Quality Diversity (arXiv 2106.03894)](https://arxiv.org/pdf/2106.03894) [FT, definitions section]
- Original QD framing papers: [Pugh, Soros, Stanley — Confronting the challenge of quality diversity (GECCO 2015)](https://stars.library.ucf.edu/scopus2015/2084) [SR]; [Quality Diversity: A New Frontier for Evolutionary Computation (Frontiers 2016)](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/epub) [SR, fetch returned binary]; [Searching for Quality Diversity When Diversity Is Unaligned With Quality](https://stars.library.ucf.edu/scopus2015/4548) [SR]. The last title directly addresses whether the behavior descriptor (here: A, S or J) aligns with what matters.
- **Vendi score**: VS = exp(−Σ λᵢ log λᵢ), where λᵢ are the eigenvalues of K/n and K is a PSD similarity matrix with k(x,x) = 1.
  - It ranges from 1 (all identical) to n (all mutually dissimilar) and is the "effective number of dissimilar elements".
  - It is reference-free. The paper says it should be paired with a quality metric.
  - It costs O(d²n) when embeddings are given.
  - Its convergence is about 1/√n under independent sampling.
  - Duplicates leave it unchanged, and it satisfies a partition property.

  — [Friedman & Dieng, The Vendi Score (arXiv 2210.02410)](https://arxiv.org/html/2210.02410v2) [FT]
- **Improved precision/recall.**
  - Feature vectors of each set get k-NN hyperspheres, with the radius equal to the distance to the k-th nearest neighbor, and k = 3 by default.
  - Precision is the fraction of generated samples inside the real manifold. Recall is the fraction of real samples inside the generated manifold.
  - Larger k raises both, and extreme k saturates them at 0 or 1.
  - Sparse regions make individual-sample scores unreliable.
  - Results depend on the feature extractor.
  - The paper used 50k samples, but reports only weak sensitivity to sample count.

  — [Kynkäänniemi et al., NeurIPS 2019](https://proceedings.neurips.cc/paper_files/paper/2019/file/0234c510bc6d908b28c70ff313743079-Paper.pdf) [FT]

### Inferences
These are adapted for this project. They are not from sources.

- **Common measurement space.** Score every arm's selected set (for example, the top-N items its exploration returns, or the archive it builds) in the *same* independent spaces:
  1. A-space grid cells: coverage / QD-score.
  2. A held-out encoder different from the one inside S (for example, a second local text encoder, or LLM-written descriptions of code variants). Use it for Vendi and precision/recall.
  3. Seed-family labels: number of distinct families recovered.

  Report the full arm x measurement-space matrix. A J that only wins in J-space is not evidence.
- **Validity rate.** The fraction of candidates that pass the code's hard checks (site fit, program area tolerance). This is cheap, objective and needs no labels.
- **Novelty.** Mean distance from each candidate to the nearest of the 15 seeds, or to the prior archive, in the common space. Pair it with validity so that novelty is not rewarded for junk.
- **Precision/recall against a reference.** With about 45 seed texts, the k = 3 hyperspheres will be very coarse; the original paper used 50k. Treat P/R here as a rough, descriptive measure. Possible reference sets: the seed concepts across runs, or architect-endorsed items.
- **Boundary stability under resampling.** Bootstrap the seed set by resampling the 15 seeds with replacement, or leave out one run. Rebuild the space or archive each time and measure:
  - Jaccard of occupied cells or neighbor sets;
  - variance of the Vendi score;
  - for hull-type boundaries, overlap of the convex hulls or support estimates.

  The claim "J is a better boundary" should mean more stable *and* more covering, not just larger.
- **Sensitivity to seed sets.** Use leave-k-seeds-out. Does J still reach the held-out seeds' regions (recall of held-out families)? This is the analogue of held-out recall in generative evaluation.
- **Held-out brief generalization.** Write 2–3 new briefs, for example a different site or program. Check whether the exploration built on the original space covers the LLM's fresh seeds for the new brief better under J than under S or A. Metric: recall of new-brief seeds within distance r.
- **Adaptation to a newly introduced criterion.** After the space is built, introduce a new code-computable criterion (for example, a daylight proxy). Measure the number of evaluations each arm needs to find K items above threshold. This is a standard "sample efficiency of downstream search" readout and needs no human labels.

### Gaps
- The Pugh et al. originals were not read. QD-score's origin is cited secondhand via the DQD paper.
- No literature was found that applies Vendi or improved precision/recall to architectural design spaces specifically, or to sets of fewer than 100 items. Small-n behavior of k-NN precision/recall is untested here.

---

## 4. Small-sample statistics

### Takeaway
The data are tiny and the units are dependent: pairs share items, and items share seeds and runs. Inference should therefore use:
- permutation or randomization tests whose resampling unit matches the dependence structure (seeds or ideas, not pairs);
- bootstrap CIs over seeds or ideas;
- Mantel/RSA-style permutation tests that shuffle *item labels* for distance-matrix correlations;
- a pre-specified primary metric and analysis plan to avoid forking paths.

Use Bayesian or ROPE equivalence statements where "no difference" is a meaningful outcome.

### Cited Findings
- Mantel test steps:
  1. Compute the correlation between two distance matrices over the same sample units.
  2. Build the null by permuting row and column identities *together* (equivalently, permuting the rows of one raw data matrix and recomputing distances).
  3. Take p as the proportion of permutations with an equal or stronger correlation.

  Rank (Spearman/Kendall) variants exist for nonlinear relations. — [Applied Multivariate Statistics, Mantel test chapter (U. Washington Pressbooks)](https://uw.pressbooks.pub/appliedmultivariatestatistics/chapter/mantel-test/) [FT]
- Cautions from the same chapter:
  - Mantel tests should test hypotheses about distances, not the original variables (citing Legendre & Legendre 2012).
  - The partial Mantel test is contested (citing Guillot & Rousset 2013).
  - With small n, a strong correlation can be non-significant; the worked example had r = 0.939 with p = 0.1.

  — [UW Pressbooks Mantel chapter](https://uw.pressbooks.pub/appliedmultivariatestatistics/chapter/mantel-test/) [FT]
- Implementations: R `ncf::mantel.test` ([docs](https://search.r-project.org/CRAN/refmans/ncf/html/mantel.test.html) [SR]); `ape::mantel.test` ([docs](https://quantargo.com/help/r/latest/packages/ape/5.5/mantel.test) [SR]); Python `qdiv.stats.distance_tests` ([docs](https://qdiv.readthedocs.io/en/latest/qdiv.stats.distance_tests.html) [SR]).
- A practitioner reference on permutation testing for neuroimaging/RSA: [Glerean, permutations notes (Aalto)](https://users.aalto.fi/~eglerean/permutations.html) [SR].
- Significance-testing guidance for NLP comparisons (choice of test given the metric and data dependence): [Dror et al., The Hitchhiker's Guide to Testing Statistical Significance in NLP, ACL 2018](https://aclanthology.org/P18-1128/) [SR].
- The fusion audit used a Bayesian hierarchical comparison with a ROPE of ±1% and reported probabilities of better / equivalent / worse. — [arXiv 2512.22991](https://arxiv.org/pdf/2512.22991) [FT]
- Variance from data sampling, initialization and hyperparameters noticeably changes conclusions. — [Bouthillier et al. 2021](https://arxiv.org/abs/2103.03098v1) [ABS]

### Inferences
These are suggestions for this project. They are not from sources.

- **Paired design.** Every arm is evaluated on the same items, probes and seeds. Use paired permutation (sign-flip) tests on per-seed or per-idea score differences: J − S and J − A per seed, with 15 seeds. With 15 units, the exact sign-flip test has 2^15 = 32,768 permutations, which is fully enumerable.
- **Bootstrap.** Bootstrap 95% CIs by resampling *seeds* (cluster bootstrap), not pairs or items. Pairs that share an anchor are not independent.
- **Comparing each space to a target geometry.** To test whether J's geometry agrees with a target geometry better than S's does, compute RSA-style rank correlations between each arm's distance matrix and the target. Targets could be architect-judged dissimilarities, recurrence structure, or an LLM judge. Test the *difference* of correlations by permuting item labels jointly, or by bootstrapping items with matrix-consistent resampling.
- **Multiple comparisons.** Two primary contrasts (J vs S, J vs A): use Holm correction, or pre-declare a single "J vs best-single" contrast.
- **Pre-registration (lightweight).** Before looking at test-run results, write down in a dated file:
  - the primary metric;
  - the primary J configuration;
  - the split (for example, select on runs 1–2, test on run 3);
  - the margin of practical equivalence;
  - the exclusion rules.

### Gaps
- The Dror et al. and Gelman/Loken texts were not read; only titles were seen. Power analysis for 15-seed paired designs was not found in a source.

---

## 5. Evaluating with a limited human budget

### Takeaway
Treat the architect's few dozen judgments as a scarce *calibration and anchor* resource, not as the main test set:
- Choose which items to label actively (active testing / active surrogate estimators remove the selection bias this introduces).
- Elicit pairwise or triplet comparisons and aggregate them with Bradley–Terry-style models, sampling pairs adaptively.
- Use LLM judges at scale, but correct and bound them with the human sample (prediction-powered inference gives valid CIs with a small labeled set plus many model predictions).
- Explicitly test LLM judges for position, verbosity and self-enhancement bias. Strong LLM judges reach about 80% agreement with humans on chat, but that is not evidence for architectural judgment.

### Cited Findings
- **Active testing** chooses which test points to label for label-efficient evaluation. Choosing points introduces bias, and the method removes that bias while reducing variance. Its acquisition differs from active learning. — [Kossen et al., Active Testing (ICML 2021)](https://oatml.cs.ox.ac.uk/publications/20210510_Kossen2021Active.html) [ABS]
- **Active Surrogate Estimators** are a follow-up that uses a surrogate model to estimate the test loss from few labels. — [Kossen, Farquhar, Gal, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9b9cfd5428153ccfbd4ba34b7e007305-Abstract.html) [SR]
- **Prediction-powered inference (PPI).** It combines a small labeled dataset with a large set of ML predictions to produce "provably valid confidence intervals" for means, quantiles and regression coefficients. It makes no assumptions about the predictor, and more accurate predictions give tighter intervals. — [Angelopoulos et al., PPI (arXiv 2301.09633)](https://arxiv.org/abs/2301.09633v4) [ABS]. An efficiency extension exists: [PPI++ (arXiv 2311.01453)](https://arxiv.org/html/2311.01453v2) [SR].
- **LLM-as-judge.** Documented biases are position bias, verbosity bias, self-enhancement bias and limited reasoning. GPT-4-class judges reach "over 80% agreement" with human preferences, about the level of human–human agreement, on MT-Bench / Chatbot Arena chat tasks. — [Zheng et al., Judging LLM-as-a-Judge (NeurIPS 2023)](https://arxiv.org/abs/2306.05685v1) [ABS]
- **Pairwise-comparison / Bradley–Terry with adaptive sampling.** Search results only:
  - [JMLR vol. 17, paper 16-066](https://jmlr.csail.mit.edu/papers/v17/16-066.html) [SR, title/topic not verified];
  - [Bayesian Decision Process for Cost-Efficient Dynamic Ranking via Crowdsourcing (arXiv 1612.07222)](https://www.arxiv.org/abs/1612.07222) [SR];
  - [Horvitz et al., crowd pairwise (PDF)](https://www.erichorvitz.com/crowd_pairwise.pdf) [SR];
  - [CrowDC: divide-and-conquer paired comparisons (arXiv 2302.11722)](https://ar5iv.labs.arxiv.org/html/2302.11722) [SR].
- **HCI design-support evaluation.** The Creativity Support Index (Cherry & Latulipe) is the standard psychometric survey for creativity-support tools: [ACM DOI 10.1145/1640233.1640255 (search hit)](https://dx.doi.org/10.1145/1640233.1640255) [SR]. A relevant architecture-ideation tool study is [Using Text-to-Image Generation for Architectural Design Ideation (arXiv 2304.10182)](https://arxiv.org/pdf/2304.10182) [SR].

### Inferences
These are protocol suggestions. They are not from sources.

- **Budget allocation (a few dozen judgments).**
  - About 10 judgments for *calibration*: repeat items to measure the architect's own test–retest consistency, which sets a ceiling on achievable agreement.
  - About 20–30 judgments for the *decisive disagreements*: triplets where S, A and J give different answers. Choosing these is an active-testing-style acquisition, so record the selection probabilities so the estimates can be importance-weighted.
  - The rest on *new-criterion or downstream outcomes*, for example "would you develop this candidate further?" on items surfaced by each arm, blinded and in randomized order.
- **Disagreement-only labeling.** Labeling only triplets where the arms disagree is far more informative per judgment than random triplets. It answers "when they differ, who is right?". Report it together with the agreement rate between arms, because a J that rarely differs from S has little practical effect even if it wins those cases.
- **LLM judge calibration via PPI.**
  - Run the frontier-LLM judge on hundreds of triplets.
  - Run the architect on a random subset of a few dozen.
  - Use PPI to get a valid CI on the "human-judged" win rate of J over S. The LLM's structural bias is then corrected by the rectifier term rather than ignored.
- **Bias checks for LLM judges.** These follow the MT-Bench bias categories, adapted:
  - Swap A/B order (position).
  - Lengthen or shorten concept text without changing content (verbosity).
  - Present the same pair as text-only vs record-only vs both. This exposes the known "structure bias" from the prior pilots.
  - Use a judge from a different model family than the generator (self-enhancement).
  - Report judge–architect agreement with Cohen's κ on the calibration subset.
- **Bradley–Terry aggregation.** If the architect does pairwise "which of these two candidate sets better covers the brief?" judgments, fit Bradley–Terry over the arms (S, A, J and controls). With very few comparisons, a Bayesian BT with a weak prior gives credible intervals on arm strengths. Note this is reasoned here, not drawn from a fetched source.

### Gaps
- None of the adaptive Bradley–Terry papers were read. No source gives concrete label-saving figures for active testing at n ≈ 30.
- No published validation was found of LLM judges for architectural massing similarity specifically. The 80% figure is for chat-response preference only.
- The mechanics of the PPI estimator and its small-n behavior (labeled n ≈ 30) were not read beyond the abstract.
