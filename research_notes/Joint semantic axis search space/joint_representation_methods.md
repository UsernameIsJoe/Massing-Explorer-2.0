# Methods for fusing a text-embedding space with a structured, interpretable axis space

Reading depth key: **[full]** = I read the full text or an HTML rendering of the paper. **[abstract]** = I read only the abstract or landing page. **[search]** = only the search-result title or snippet. Project context assumed throughout: 15 seeds with text and a 9-axis record; about 1,000 structural variants with no text; off-the-shelf encoders run through Ollama.

## 1. Alignment methods between two views (CCA family, Procrustes, CLIP-style contrastive, multi-view metric learning): which ones work with tens to hundreds of pairs?

### Takeaway
With 15 text-plus-axis pairs, no learned alignment is statistically supportable. CCA and its kernel and deep variants overfit or are ill-posed when n is smaller than the number of dimensions. CLIP-style contrastive alignment needs thousands to millions of pairs, even when it starts from pretrained encoders. The method that does work at small n is a training-free one: represent each item by its similarities to a shared set of anchor pairs (ASIF, relative representations). At around 100 to 300 pairs, a heavily regularized CCA run after PCA reduction becomes testable.

### Cited Findings
- **Linear CCA in the small-n regime:** when the sample size is smaller than the number of features, the sample covariance matrices are singular, so the CCA problem is ill-posed without regularization. The penalty has to be tuned by (nested) cross-validation. In the authors' neuroimaging example (n=153), the cross-validated score of a reduced-feature model was overly optimistic, and its test correlation was only 0.044. **[full]** — [Tuzhilina, Tozzi, Hastie, "CCA in high dimensions with structured regularization"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10274416)
- **Fix for very small sample support:** reduce rank with PCA before running CCA, and select the number of PCA dimensions and correlated signals jointly with reduced-rank Bartlett-Lawley tests or MDL. The authors report that this works at very small sample sizes. **[abstract]** — [Song et al., arXiv:1604.02047](https://arxiv.org/abs/1604.02047)
- Sparse CCA variants are an active area for the n < p regime. **[search]** — [Sparse CCA via concave minimization](https://arxiv.org/pdf/1909.07947); [Support recovery limits of sparse CCA](https://arxiv.org/pdf/2108.06463)
- **Deep CCA** learns nonlinear transforms of both views to maximize correlation. It beat CCA and kernel CCA on two real datasets. It is parametric, unlike kernel CCA, which needs the training data to embed new instances. **[abstract]** — [Andrew et al., ICML 2013](https://proceedings.mlr.press/v28/andrew13.html)
- **ASIF (training-free alignment):** two frozen unimodal encoders plus a set of anchor pairs. Each new item is represented by its cosine similarity to every anchor *in its own modality*, keeping the top-k values (k=800) and raising them to a power p (p=8). Because both modalities produce vectors indexed by the same anchor pairs, they share a space. Each dimension is interpretable as "similarity to anchor pair i". Adding or removing an anchor needs no retraining. **[full]** — [Norelli et al., ASIF, arXiv:2210.01738](https://arxiv.org/pdf/2210.01738)
- **ASIF data efficiency:** about 18% ImageNet zero-shot accuracy with 10K pairs, and 60.9% with 1.6M pairs (CLIP-400M gets 68.6%). Adding just 100 domain pairs raised EuroSAT accuracy from 29.4% to about 82%. **[full]** — [ASIF](https://arxiv.org/pdf/2210.01738)
- **Relative representations:** each sample is encoded by its latent similarity to a fixed set of anchors. This makes the representation invariant to isometries and rescaling of the latent space without training, and enables zero-shot stitching across image, text and graph data. **[abstract]** — [Moschella et al., arXiv:2209.15430](https://arxiv.org/abs/2209.15430)
- **CLIP-style contrastive alignment at scale:** CLIP used 400M pairs and LiT used 901M (private) or 10M (public) pairs, as reported in the ASIF comparison. **[full]** — [ASIF](https://arxiv.org/pdf/2210.01738)

### Inferences
- **Most practical option for Massing Explorer:** an ASIF / relative-representation construction with the 15 seeds (and later more) as anchors. Represent each concept text as its vector of cosine similarities to the 15 seed texts in the embedding space. Represent each structural variant as its vector of axis similarities to the same 15 seeds, using an axis distance such as Gower (see section 3). Both land in a 15-dimensional "similarity to seed i" space that is interpretable by construction. With n=15, use small top-k (3–5) and moderate p, because the paper's k=800 assumes millions of anchors.
- **Tiny-data test for the anchor space:** leave-one-seed-out. Compute the seed's text-anchor vector and its axis-anchor vector over the other 14 seeds, then check rank correlation, and whether its nearest neighbour under text matches its nearest neighbour under axes. This is the same Spearman protocol the project already uses, now applied in a shared coordinate system.
- **When CCA becomes feasible:** only once there are a few hundred text-plus-axis pairs, and then only after PCA reduction of the 1024-d embedding to a handful of components, with nested CV. On 15 seeds the canonical correlations would be near 1 by construction and carry no information.
- **Procrustes and orthogonal mapping:** not researched here. The same n < d problem applies, so treat it as infeasible at n=15.

### Gaps
- I found no paper reporting CCA or Procrustes results specifically at n≈15–100 for text-to-attribute alignment. The sample-size guidance above is general.
- I did not fetch a primary source on multi-view metric learning (for example a multi-view metric learning survey). Its data requirements remain unverified.

## 2. Interpretable anchoring of embeddings (concept bottlenecks, CAVs / linear probes, interpretable embedding dimensions, supervised disentanglement)

### Takeaway
Two approaches fit the project well. The first maps embeddings onto the named axes with a probe or concept bottleneck, which shows *which* axes the text actually encodes. The second builds an embedding whose dimensions *are* yes/no questions (QAEmb, CQG-MBQA), which can be written to mirror the 9 axes and then answered by an LLM for each text. The second approach also gives the text-free variants a route into the space once they are textualized.

### Cited Findings
- **Concept Bottleneck Models:** predict human-defined concepts from the input, then the label from the concepts. They need concept annotations at training time, and accuracy is competitive with end-to-end models on x-ray grading and bird identification. Users can edit predicted concepts at test time, and correcting concept mistakes significantly improves accuracy. **[abstract]** — [Koh et al., arXiv:2007.04612](https://arxiv.org/abs/2007.04612)
- **TCAV / Concept Activation Vectors:** interpret a network's internal state through user-defined concepts, using directional derivatives to measure concept importance (for example "stripes" for "zebra"). **[abstract]** — [Kim et al., arXiv:1711.11279](https://arxiv.org/abs/1711.11279). Method details, such as linear classifiers on activations trained on concept versus random examples, were not verified from full text.
- **CQG-MBQA (ICLR 2025):** each embedding dimension is a yes/no question. Questions are generated contrastively per cluster, using positives, hard negatives and easy negatives, then filtered for discriminativeness and redundancy, leaving 9,614 questions. A frozen encoder plus one classification head per question (MBQA) matches LLM answers about 96% of the time. Labeling about 10K questions over about 1,000 texts each cost about $31 with GPT-4o-mini. **[full]** — [Sun et al., arXiv:2410.03435](https://arxiv.org/html/2410.03435v1)
- **Interpretability–quality tradeoff in CQG-MBQA:** a higher binarization threshold gives sparser, more readable vectors but lower STS Spearman. STS average is 77.6 versus 85.9 for black-box AnglE, and retrieval trails BM25. Quality plateaus around 3,000 dimensions. **[full]** — [CQG-MBQA](https://arxiv.org/html/2410.03435v1)
- **QAEmb (Benara et al., 2024):** prompts an LLM to generate yes/no question features and was shown useful for fMRI prediction. CQG-MBQA critiques it as producing generic questions with many "yes" answers. **[full, as described in CQG-MBQA]** — [CQG-MBQA related-work discussion](https://arxiv.org/html/2410.03435v1)

### Inferences
- **Hand-authored question embedding (no question generation needed):** the 9 axes already define the questions. Example questions: "Is the gym in the same mass as the cafeteria?" (one per co-location bit), "Are all three masses linked?", "Is the tallest mass more than 2 floors taller than the shortest?". Ask an LLM (or Ollama) to answer each question *from the concept text alone*. This gives a "text-claimed axis vector" that can be compared field by field with the code-computed axis vector. The disagreement per axis directly measures where text and structure diverge, and it explains the existing finding that text tracks topology but not heights.
- **Linear probes on 15 points:** a probe from the 1024-d embedding to each axis will overfit. Use leave-one-out with strong ridge regularization, or probe after PCA to 3–5 components, and treat results as exploratory.
- **Concept bottleneck framing:** the trusted axis record *is* the bottleneck. The search space can be "predicted axes from text" plus a residual semantic vector, and a user can edit an axis value and re-rank, which is CBM-style intervention.

### Gaps
- I did not read full-text sources on supervised disentanglement methods (for example β-VAE with supervision) or on probing-sample-size guidance. These are omitted rather than guessed.

## 3. Product and composite spaces (weighted distance sums, Gower, learned combinations, conditional similarity: C-STS, INSTRUCTOR)

### Takeaway
The most robust option for tiny data is a composite distance: a Gower-style weighted sum of per-axis distances plus one or more semantic-distance terms, with weights set by the user or a few tuned hyperparameters. Conditional or instruction-conditioned similarity is appealing, because it measures "similar *with respect to* vertical organization". However, evidence shows that off-the-shelf embedders largely ignore the condition, so it should be tested rather than trusted.

### Cited Findings
- **Gower's distance (1971):** per-variable partial dissimilarities, combined as a weighted average in [0,1]:
  - numeric variables use the range-normalized absolute difference;
  - binary and categorical variables use match/mismatch;
  - ordinal variables have later extensions (Kaufman & Rousseeuw; Podani 1999).

  **[full, Wikipedia]** — [Gower's distance](https://en.wikipedia.org/wiki/Gower%27s_distance) (original: Gower, *Biometrics* 27(4):857–871). Missing-value handling was not covered in the page I read; R's `gowdis` implements it per the documentation. **[search]** — [FD::gowdis](https://search.r-project.org/CRAN/refmans/FD/html/gowdis.html)
- **C-STS:** similarity is conditioned on a free-text aspect. The dataset has about 18.9K instances. Zero-shot bi-encoders score Spearman about 2 or below on C-STS despite strong STS-B performance, so they *ignore the condition*. A fine-tuned SimCSE-large bi-encoder reaches 47.5. Performance rose roughly linearly from 1K to 7K training examples (about 30 to 45). Few-shot GPT-4 is competitive, but every model stays below 50. **[full]** — [Deshpande et al., EMNLP 2023](https://ar5iv.labs.arxiv.org/html/2305.15093)
- **INSTRUCTOR:** each text is embedded together with a task instruction. It was trained contrastively on 330 instruction-annotated tasks and evaluated on 70 tasks (66 unseen). The authors report robustness to instruction wording. **[abstract]** — [Su et al., arXiv:2212.09741](https://arxiv.org/abs/2212.09741)

### Inferences
- **Recommended joint metric:** D(a,b) = Σ_k w_k · d_k(a,b) + w_sem · (1 − cos(e_a, e_b)).
  - The d_k terms are Gower partial distances over the 9 axes: Hamming/Jaccard on the 36 co-location bits, range-normalized for heights and mass count, and categorical for topology.
  - Unknown axes (loading, geometric character) drop out of the weighted average, as Gower missing-handling does.
  - Weights act as user-facing sliders, so semantic and axis spaces "work together" without either replacing the other.
  - **Tiny-data test:** have an architect rank-order or triplet-judge a few dozen seed pairs, then fit the few w's by maximizing agreement. Around 10 parameters is feasible with tens of judgments.
- **Learned combination:** with more judgments, a small learned metric over [axis features ∥ PCA(embedding)] becomes possible. It is not justified at 15 seeds.
- **Conditional similarity via qwen3-embedding:** qwen3-embedding is instruction-aware. Its instruction-awareness was not verified in sources fetched here; treat this as an assumption. A test would embed texts with an instruction such as "Represent the vertical organization of this school massing" and check whether Spearman against the vertical-organization axis rises compared with no instruction. Given the C-STS finding, expect weak effects.

### Gaps
- I did not find small-data evidence on how much instruction prefixes shift embedding geometry for aspect-specific similarity. Aspect-conditioned embedding methods beyond C-STS and INSTRUCTOR were not researched.

## 4. Graph/structure encoders sharing a space with text (MoleculeSTM, MoMu, Text2Mol), and how they handle structure-only samples

### Takeaway
The molecule–text literature is the closest analogue: structure graph versus description. It relies on contrastive training over roughly 15K to 280K pairs, starting from *separately pretrained* unimodal encoders. It handles abundant structure-only data by pretraining the structure encoder self-supervised on graphs alone (graph augmentations), not by inventing text. That data scale is two to four orders of magnitude beyond 15 seeds. What transfers is the *recipe*: a self-supervised structure encoder trained on the 1,000 variants, plus a light alignment.

### Cited Findings
- **MoleculeSTM:** jointly learns molecular structure and text through contrastive learning on PubChemSTM, which has more than 280K structure–text pairs. It supports zero-shot text-based retrieval and text-guided molecule editing. **[abstract]** — [Liu et al., arXiv:2212.10789](https://arxiv.org/abs/2212.10789v3)
- **MoMu:** a GIN graph encoder initialized from GraphCL (self-supervised on graphs) and a SciBERT/KV-PLM text encoder, projected to a shared 256-d space.
  - Training data: about 15.6K graph–document pairs.
  - Losses: inter-modal plus intra-modal InfoNCE. The intra-modal term contrasts two augmented views of the same graph, using node dropping (10%) and subgraph sampling (80%).
  - The authors note that paired data is scarce relative to image–text data, mitigate this by starting from unimodal pretrained encoders, and warn that retrieved texts may not describe structure, which risks spurious correlations.

  **[full]** — [Su et al., arXiv:2209.05481](https://ar5iv.labs.arxiv.org/html/2209.05481)
- **Text2Mol:** learns a shared semantic space for text-query molecule retrieval from a paired dataset. Cross-modal attention gives explainability by reading attention as association rules, and an ensemble raised MRR from 0.372 to 0.499. **[abstract]** — [Edwards et al., EMNLP 2021](https://aclanthology.org/2021.emnlp-main.47). Dataset size (ChEBI-20) and encoder details were not confirmed from the page I read.
- Surveys of this area exist. **[search only]** — [Bridging Text and Molecule survey](https://arxiv.org/pdf/2403.13830); [Biomolecule & NL survey](https://arxiv.org/pdf/2403.01528)

### Inferences
- **Mapping to the project:**
  - The massing record is a tiny graph: 3 mass nodes with department sets and floors as attributes, and links as edges.
  - The 1,000 variants are the analogue of "unpaired molecules". Use them only for the structure side, for example a GraphCL-style or simpler hand-crafted embedding.
  - The 9-axis descriptor is already a good, trusted structure embedding, so a learned GNN is unlikely to beat it at this scale.
- **MoMu's spurious-correlation warning applies directly.** LLM concept texts may not describe heights or vertical organization, which is consistent with the observed low correlation there. Contrastive alignment would learn only what the text actually encodes.

### Gaps
- I did not verify how MoleculeSTM handles structure-only molecules beyond its pretraining, or its exact encoders (the full text was not read).

## 5. Embedding items that have structure but no text (the 1,000 code variants)

### Takeaway
There are three viable routes, all cheap:
- **(a) Templated textualization:** deterministic text generated from the record, then embedded with the same encoder.
- **(b) Anchor or relative representation:** each variant becomes a vector of axis similarities to the text-bearing seeds, so it lives in the same anchor coordinates as text (ASIF).
- **(c) Neighbour imputation:** a semantic vector borrowed from axis-nearest seeds, weighted by axis similarity.

Routes (b) and (c) keep the axis space as the trusted backbone. Route (a) risks measuring template wording instead of design meaning.

### Cited Findings
- **Anchor representations need only same-modality similarity to the anchors.** A sample in one modality is placed in the shared space without any counterpart in the other modality, which is exactly the case of a text-free variant. **[full]** — [ASIF](https://arxiv.org/pdf/2210.01738); [Relative representations](https://arxiv.org/abs/2209.15430)
- **Structure-only data in molecule–text work is used for self-supervised pretraining of the structure encoder** (GraphCL initialization and intra-modal graph contrastive term), not for text generation. **[full]** — [MoMu](https://ar5iv.labs.arxiv.org/html/2209.05481)
- **Question-dimension embeddings (CQG-MBQA / QAEmb) can be computed from any text.** For a structured record, the "answers" can be read directly from code, giving the same coordinate system as LLM-answered text. **[full]** — [CQG-MBQA](https://arxiv.org/html/2410.03435v1)

### Inferences
- **(a) Templated text:** for example "Gym and cafeteria share the 2-storey north mass; the library sits alone in the 4-storey mass linked only to the classroom bar…".
  - Tiny-data test: textualize the 15 seeds' *structures*, then measure the cosine between template-embedding and authored-concept-embedding for the same seed versus other seeds (a retrieval rank). If authored text does not retrieve its own template above chance, templated embeddings are not comparable to authored ones.
  - Also check that template embeddings correlate with axis distance more strongly than authored ones do. If they do, the encoder is mostly reading template wording, a form of leakage.
- **(b) Anchor vectors (preferred):**
  - variant v → [sim_axes(v, seed_i)] for i = 1..15;
  - seed text t → [sim_text(t, seed_i)].
  - Query by text: embed the query, take its seed-similarity profile, and rank variants whose axis-similarity profile matches.
  - This makes semantic intent search over text-free variants while staying grounded in the trusted axes.
- **(c) Imputation:** e_v ≈ Σ_i softmax(−d_axes(v,seed_i)/τ) · e_seed_i. This is simple but collapses toward the seed centroid; with 15 seeds, variants far from all seeds get uninformative vectors. Flag a "low-support" confidence flag when the minimum axis distance is large.
- **Hybrid:** question-dimension coordinates (section 2) answered from code for variants and by an LLM for texts give a *shared interpretable* space directly. This is arguably the cleanest "one space" design, with the off-the-shelf embedding kept as a secondary semantic term in the composite metric (section 3).

### Gaps
- I found no published study on templated textualization of design or architectural structured records for embedding. Its validity must be tested empirically as above.
- I found no source quantifying neighbour-imputation error at n≈15 anchors.
