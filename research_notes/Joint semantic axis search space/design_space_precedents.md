# Precedents: Joint Semantic + Structured Descriptor Spaces for Design Exploration

Reading-depth legend: [FT] = full text read (HTML/PDF fetched via a summarizing fetch tool, so not every section was checked by hand); [ABS] = abstract or project page only; [SR] = search-result listing only, not opened.
Every precedent below follows the same fields: semantic side / structured side / interaction (generate, verify, steer, archive) / how the space is updated / evaluation / transfer to Massing Explorer 2.0 (ME2).

## Q1. Quality-diversity with language: how do LLM-judged semantic descriptors combine with numeric descriptors?

### Takeaway
In this literature, LLM generators are usually paired with archives whose axes are either (a) LLM-judged semantic labels (QDAIF, ACES) or (b) code-computed numeric or embedding coordinates (ELM, OMNI-EPIC cell coverage), with code execution as the validity gate. I found no paper that grids a single archive on both LLM-judged semantic axes and code-computed numeric axes at once. The closest patterns are ACES (semantic labels as niches, code execution as the trust gate), OMNI-EPIC (an embedding archive used for retrieval and novelty, plus code-generated success checks), and QDHF (embedding features projected onto a small learned axis space, refit online from feedback).

### Cited Findings

**QDAIF: Quality-Diversity through AI Feedback** (Bradley et al., ICLR 2024) [FT of arXiv PDF; ABS of ICLR page]
- Semantic side: an LM is prompted with a natural-language question about a diversity trait (e.g., sentiment); the log-probability of each label gives a position on the diversity axis. Quality is the log-probability of "yes" vs "no" to a quality question. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- Structured side: a MAP-Elites grid over those LLM-derived scalar axes. Because LM logits do not move linearly with qualitative change, bins are non-uniform and denser toward the ends of each axis; the human study used a 20-bin axis. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- Generation: Language Model Crossover (LMX) concatenates archive elites into a few-shot prompt ("Here is a random example of..."). Initialization used 3 hand-chosen seeds per domain spanning the diversity axes; zero-shot initialization was also tested. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- Domains: opinions (1D sentiment), stories (genre, ending, and a 2D genre x ending archive), poetry (genre x tone). — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032); [project page](https://qdaif.github.io)
- Evaluation: 2000 iterations, 5 seeds. QDAIF had significantly higher QD score than Fixed-Few-Shot, Shuffling-Few-Shot, Random-Search, and LMX Quality-Only. In 2D, Quality-Only more often found the single best story. In the human study, human QD score was 0.772 (QDAIF) vs 0.767 (Fixed-Few-Shot), Fixed-Few-Shot had the higher mean quality (4.133 vs 3.900), and AI and humans agreed on the category about 73% of the time. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- **Direct comparison of semantic-judgment vs embedding axes:** QDEF (embedding feedback, cosine similarity to text queries) did much worse than QDAIF. With LMX and seeded initialization, human QD score was 0.617 (QDAIF) vs 0.308 (QDEF). The authors attribute this to reward hacking: high-scoring texts converged toward the query text itself. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- Failure modes: human-rated quality decoupled from AI quality in the highest AI-score range (0.995 to 1). Axes must be user-specified, and a poorly chosen axis ("hero spy vs hero politician") produced off-target stories. — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- ME2 transfer: (1) Do not use cosine similarity between an off-the-shelf text embedding and an axis label as the "trusted" axis value; QDEF shows this is hackable. Keep axis values code-computed from the structured record, and use the LLM or embeddings only for semantic coverage. (2) LMX (few-shot prompting from archive elites) is a cheap generation operator that fits the 15-seed regime. (3) If LLM-judged axes are ever added, use non-uniform bins.

**ACES: Autotelic Code Exploration via Semantic descriptors** (Pourcel et al., 2023) [FT]
- Semantic side: each Python puzzle is LLM-labeled (gpt-3.5) with 10 binary programming skills. Each skill combination is a niche (2^10 = 1024 cells), and distance is Hamming distance. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- Structured side and trust gate: every puzzle and solution pair is executed (`assert f(g())`), and only passing pairs are labeled and archived. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- Steering: each cycle samples a target cell uniformly. The generator gets the target skills plus 2 nearest archive examples (by Hamming distance) and 1 training example. The authors note that landing in a new cell matters more than hitting the target exactly. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- Labeler reliability: on a 60-puzzle manual check, the labeler sometimes missed skills that were present (e.g., Stacks and Queues, Geometry and Grid). — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- **Semantic archive vs embedding archive:** an ELM baseline whose archive was CodeT5p embeddings partitioned by CVT-MAP-Elites (1024 cells) produced more valid puzzles, but mostly in cells the training set already covered. The semantic-archive methods discovered more cells beyond the training distribution, and ACES had the highest cell-distribution entropy. Optimizing semantic diversity also raised diversity measured in two of three independent embedding spaces. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- Caveat: higher diversity did not improve downstream fine-tuning performance, and no coverage metric correlated significantly with it. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- ME2 transfer: closest analogue to "LLM explores freely, every proposal gets a trusted structured coordinate." Swap ACES's LLM-labeled skills for ME2's code-computed 9 axes and code execution for ME2's geometry and descriptor computation. ACES-style goal sampling (pick an under-filled target cell and prompt with its nearest archive neighbours) is a concrete way to bound and direct LLM exploration. It also shows that an embedding-defined archive tends to stay inside the prior distribution.

**OMNI-EPIC** (Faldor et al., ICLR 2025) [FT of arXiv PDF]
- Semantic side: tasks are natural-language descriptions embedded with text-embedding-3-small. The generator is conditioned on the N nearest archive tasks to a randomly chosen one, and a post-generation "model of interestingness" (an LLM) compares each new task with its M nearest archive tasks and discards uninteresting ones before any training. — [arXiv 2405.15568](https://arxiv.org/pdf/2405.15568)
- Structured side: each task is executable environment code plus an LLM-written `get_success` function, kept separate from the shaped reward to reduce reward hacking. Code is compile-checked with tracebacks fed back for up to 5 tries, then discarded. The archive stores both successes and failures. — [arXiv 2405.15568](https://arxiv.org/pdf/2405.15568)
- Evaluation: (a) cell coverage, computed by projecting task embeddings to 2D with PCA and binning (e.g., 50 per axis); (b) ANNECS-OMNI, a progress metric that also requires interestingness. The full system beat the no-archive and learning-progress-only ablations on both (Mann-Whitney U, p < 0.05). Human agreement with the success detector was 72.7% (50 participants). — [arXiv 2405.15568](https://arxiv.org/pdf/2405.15568)
- ME2 transfer: (1) Use the text embedding of concept text for retrieval (nearest-neighbour context) and as an LLM novelty gate, not as the trusted coordinate. (2) Keep failed or invalid proposals in the archive as negative context. (3) "Embedding PCA to 2D, then count filled bins" is a cheap semantic-coverage metric to report alongside coverage on the 9 axes. (4) Compile-and-repair loop with a retry cap matches parsing the structured record and repairing it.
- Older foundation: OMNI (Zhang et al., 2023) introduced FM-based models of interestingness. — [arXiv 2306.01711](https://arxiv.org/pdf/2306.01711) [SR]

**QDHF: Quality Diversity through Human Feedback** (Ding et al., ICML 2024 / NeurIPS 2023 workshop) [FT]
- Semantic side: pretrained embeddings (CLIP, DreamSim) of solutions. — [arXiv 2310.12103](https://arxiv.org/html/2310.12103v3)
- Structured side: a learned linear projection of those features into a low-dimensional (2D in experiments) descriptor space, trained with a triplet hinge loss on two-alternative "which is more similar to the reference" judgments from humans, heuristics, or AI. — [arXiv 2310.12103](https://arxiv.org/html/2310.12103v3)
- Update mechanism: the projection is refit online at iteration 1 and at 10%, 25%, and 50% of the run, each time using a quarter of the feedback budget, and QD is re-initialized under the new descriptors. — [arXiv 2310.12103](https://arxiv.org/html/2310.12103v3)
- Sample sizes and results: 200 to 1,000 simulated judgments (maze, robot arm). Robot arm QD score was 72.5 vs 74.8 with ground-truth descriptors and 53.0 for the best AURORA variant. Text-to-image (10,000 DreamSim judgments): mean pairwise distance 0.517 vs 0.405 for best-of-n at similar CLIP score. In the MTurk study, 66.7% judged QDHF more diverse vs 24.8%. Results held at 5% label noise and still beat AURORA at 20% noise. — [arXiv 2310.12103](https://arxiv.org/html/2310.12103v3)
- ME2 transfer: the clearest published recipe for making a semantic space updatable with user input from small data. Fit a small projection from text embeddings (or embeddings concatenated with the 9 axes) using a few hundred "A is more like X than B" judgments, and refit on a schedule. With 15 texted seeds, judgments could cover code variants by pairing each with the nearest texted seed or with LLM-written descriptions.

**ELM: Evolution through Large Models** (Lehman et al., 2022) and **LLMatic** (2023) [not fetched in this session; cited from search listing and prior knowledge]
- ELM uses a code LLM as the mutation operator inside MAP-Elites (Sodarace), and the archive axes are code-computed morphology descriptors. This is the "LLM generates, code measures" pattern ME2 already uses. — [LLMatic arXiv 2306.01102](https://arxiv.org/html/2306.01102v8) [SR]; ELM is arXiv 2206.08896 (not verified in this session)
- Related listings not opened: "Large Language Models as In-context AI Generators for Quality-Diversity" (In-context QD) — [arXiv 2404.15794](https://arxiv.org/pdf/2404.15794) [SR]; "Integrating LLMs and Decision Transformers for Language Grounded Generative QD" — [arXiv 2308.13278](https://arxiv.org/pdf/2308.13278) [SR]; AutoQD (automatic behavior discovery) — [arXiv 2506.05634](https://arxiv.org/html/2506.05634v1) [SR].

### Inferences
- A defensible ME2 architecture can be assembled from these parts: an ACES/ELM-style trusted archive on code-computed axes, OMNI-EPIC-style embedding retrieval plus an LLM novelty gate on the semantic side, and QDHF-style learned projection for user updates.
- Taken together, QDAIF (QDEF) and ACES (ELM embeddings) suggest that embedding-similarity "descriptors" are vulnerable: they are hackable and tend to stay near the prior distribution. That supports ME2's choice to make the axes code-computed, and to use embeddings only for the semantic, exploratory side.

### Gaps
- No paper found that builds a single MAP-Elites grid mixing LLM-judged semantic axes with code-computed numeric axes and reports an ablation against each alone. The closest are the QDAIF-vs-QDEF and ACES-vs-ELM-embedding comparisons (semantic vs embedding, not semantic vs numeric).
- ELM, In-context QD, and AutoQD were not opened this session; their details above are not verified.

## Q2. Architecture and engineering precedents

### Takeaway
Architectural QD work (UC-ME, TileGPT, FI-MAP-Elites shells) is structured-descriptor-first. Language enters either as discretized descriptor-to-text prompts (TileGPT) or as LLM-generated dimensions in the HCI tool Luminate. Structured-text generators (DS2D, CoMa) show that LLMs can emit JSON design records that code then checks for self-consistency and prompt-consistency, which mirrors ME2's text-plus-record seeds.

### Cited Findings

**Luminate** (Suh et al., CHI 2024) [FT]
- Semantic side: from the user's prompt, an LLM generates categorical dimensions as JSON (up to 5 nominal dimensions with up to 8 values each, and up to 3 ordinal dimensions with 5 levels). Numerical dimensions were dropped because pilots showed they did not give meaningful interactions. — [arXiv 2310.12953](https://arxiv.org/html/2310.12953v3)
- Structured generation: each response gets one randomly chosen value per dimension (a "requirement list") and is generated by its own parallel LLM call; 40 responses per prompt. — [arXiv 2310.12953](https://arxiv.org/html/2310.12953v3)
- Navigation and update: responses are laid out as 1D or 2D scatters on the chosen dimensions, with semantic zoom (dot, title, keyword, summary, full text). A user can type a new dimension, after which the LLM generates its values and re-labels existing responses. "Add more" generates within a filtered subspace, and "more like this" generates near a chosen response. — [arXiv 2310.12953](https://arxiv.org/html/2310.12953v3)
- Evaluation: 14 professional writers. Creativity Support Index 82.16, and 10 of 14 preferred it to ChatGPT for creative writing. Several found 40 responses overwhelming. — [arXiv 2310.12953](https://arxiv.org/html/2310.12953v3)
- ME2 transfer: Luminate's "user adds a dimension, the LLM re-labels all items" is the HCI model for making the search space updatable with user input. In ME2, user-added dimensions would be LLM-judged "soft" axes sitting beside the 9 trusted axes. Generating each item from an explicit requirement list (targeting coordinates) is the same move as ACES's target cells.

**UC-ME: Controllable Exploration of a Design Space via Interactive QD** (Bahrami / Liapis et al., GECCO 2023) [FT]
- Structured side only: floor plans for a 10-space-unit apartment, with descriptors for compactness and orthogonality and fitness for area precision. Feasible and infeasible archives are kept separately (FI-MAP-Elites). — [arXiv 2304.01642](https://ar5iv.labs.arxiv.org/html/2304.01642)
- Steering: 4 alternatives are drawn from a 9x9 window of a 64x64 map. The user picks one, the window re-centers on it, and 10,000 parent selections run inside the window. No preference model is learned. — [arXiv 2304.01642](https://ar5iv.labs.arxiv.org/html/2304.01642)
- Evaluation: 12 simulated users (some switch criteria midway), 10 runs each. Unguided MAP-Elites gave higher coverage and QD score, while UC-ME matched user criteria better. "Corners" sampling gave the most diverse alternatives and "Medoids" the fittest. — [arXiv 2304.01642](https://ar5iv.labs.arxiv.org/html/2304.01642)
- ME2 transfer: a simple, well-evaluated way to bound later exploration by user input, by moving a window in descriptor space rather than learning a model. Keeping invalid massings in a separate infeasible archive is useful too. Simulated users are a cheap evaluation protocol for small data.

**Liapis constrained novelty and two-population line** [ABS, research page]
- Sentient Sketchbook (FDG 2013) uses constrained novelty search with feasible and infeasible populations to suggest real-time alternatives to a designer's sketch. FI-MAP-Elites has been applied to shell structures (IASS 2023, Rhino/Grasshopper + Karamba), and graph-specified room layouts have been explored with QD (FDG 2022). — [Liapis research page](https://antoniosliapis.com/research/research_constrainedopt.php)

**TileGPT: Generative Design through QD Data Synthesis and Language Models** (Gaier et al., Autodesk Research, GECCO 2024) [FT]
- Structured side: MAP-Elites over Wave Function Collapse site layouts (25x15 grid) with 5 numeric descriptors (parks, largest park, units, sequestered carbon, privacy), producing a 50,000-design dataset. — [arXiv 2405.09997](https://arxiv.org/html/2405.09997v1)
- Semantic side: each descriptor is discretized into low, medium, or high and turned into text (3^5 = 243 prompts). A frozen BART encoder conditions a fine-tuned DistilGPT2 via cross-attention. The output is a coarse blueprint that WFC completes, and WFC enforces validity. — [arXiv 2405.09997](https://arxiv.org/html/2405.09997v1)
- Evaluation: compared with a model trained on 50,000 randomly sampled designs, the QD-trained model had more uniform feature coverage, higher prompt fidelity in almost all categories, and higher validity. Results were reported mainly as heatmaps and Gini coefficients. — [arXiv 2405.09997](https://arxiv.org/html/2405.09997v1)
- ME2 transfer: closest architecture-domain precedent for joining a numeric descriptor archive with language, here by verbalizing the axes. For ME2, the ~1,000 code variants without text could be given templated or LLM-written text from their 9-axis coordinates ("verbalized axes") to bridge them into the semantic space. TileGPT also shows that QD-generated data, rather than random sampling, gives a better-conditioned text-to-design mapping.

**DStruct2Design (DS2D)** (Luo et al., Mila, 2024) [FT]
- Structured side: each floor plan is JSON (room count, total area, room types, per-room area, width, height, and polygon) plus bubble-diagram edges. Llama3-8B is fine-tuned with LoRA on constraint strings and adjacency strings. — [arXiv 2407.15723](https://arxiv.org/pdf/2407.15723)
- Verification: self-consistency (stated area vs polygon area, overlap, duplicate IDs), prompt-consistency (requested vs produced count and area), and compatibility (graph edit distance to the input bubble diagram). Overlap was about 16% on ProcTHOR and 36 to 53% on RPLAN. — [arXiv 2407.15723](https://arxiv.org/pdf/2407.15723)
- ME2 transfer: ME2's seed record (department-to-mass assignment, floors, links) is a DS2D-like structured representation. Adopt DS2D's split between self-consistency checks (is the record internally valid?) and prompt-consistency checks (does the record match the concept text's claims?). The latter is a concrete way to measure text-to-axis alignment. A 2025 follow-up uses RL with verifiable rewards for LLM floor plans. — [arXiv 2605.14117](https://arxiv.org/pdf/2605.14117) [SR]

**CoMa: Contextual Massing Generation with VLMs** (2026) [FT]
- Massing is represented as hierarchical LoD 1.3 JSON (extrusions with bottom and top elevations and footprints). Qwen3-VL (2B to 8B) is LoRA-tuned on 12,845 Melbourne massings with 1D (JSON), 2D, or 3D context. — [arXiv 2601.08464](https://arxiv.org/pdf/2601.08464)
- Evaluation: a learned "contextual relevance" classifier over 17 hand-designed scores (orientation, FAR, coverage, height, shape) reached ROC-AUC 0.915. The best CR score was 0.435. There were no program-compliance checks and no human evaluation. — [arXiv 2601.08464](https://arxiv.org/pdf/2601.08464)
- ME2 transfer: confirms that massing-as-JSON is now standard for LLM and VLM generation. Its evaluator, a classifier over hand-coded geometric descriptors, parallels ME2's 9-axis record used as the trust layer. It is a data-hungry (12k samples) contrast to ME2's 15 seeds.

### Inferences
- In the sources found, architecture-domain systems either verbalize numeric descriptors into text (TileGPT) or let users steer within a numeric archive (UC-ME). None embed free-form design-concept text and reconcile it with the descriptor archive. ME2's joint space appears to be a novel combination: Luminate-style user-extensible semantic dimensions plus a TileGPT/UC-ME-style trusted numeric archive.

### Gaps
- "Navigating Design Spaces" (Garcia & Leitao): searches did not locate this paper. Results returned unrelated people with similar names (e.g., Carla Leitao at RPI). Not verified.
- DesignAID: not searched due to the tool-call budget. Not verified.
- house-GAN / House-GAN++ (graph-constrained layout GANs) and CLIP-guided architecture navigation: not fetched this session.

## Q3. Materials, molecules, proteins: language-conditioned generation checked against structured property spaces

### Takeaway
MolLEO is the clearest pattern: LLMs (prompted in text, or a text-molecule joint embedding) act as mutation or crossover operators, while every child is scored by structured property oracles. The authors report that LLM edits alone give modest gains and that the evolutionary loop with oracle verification is essential.

### Cited Findings
- MolLEO embeds GPT-4, BioT5, or MoleculeSTM as genetic operators in Graph-GA. GPT-4 crossover gets two parents plus their scores. MoleculeSTM mutation does gradient descent in a joint text-molecule embedding toward a text prompt, with a penalty for drifting from the original. — [arXiv 2406.16976](https://arxiv.org/pdf/2406.16976v3)
- Structured side: oracles (QED, SA, JNK3/GSK3B/DRD2 classifiers, Vina docking). A filter keeps offspring closest (Tanimoto) to the top molecule, because LLM edits tend to reduce fitness. Multi-objective selection uses Pareto front and hypervolume. — [arXiv 2406.16976](https://arxiv.org/pdf/2406.16976v3)
- Results: on 23 PMO tasks, GPT-4 MolLEO had a summed score of 17.862 vs 13.823 for Graph-GA and led on 15 tasks. Single-step LLM edits alone gave only modest gains. — [arXiv 2406.16976](https://arxiv.org/pdf/2406.16976v3)
- Survey context: "LLMs for Text-Guided Molecular Discovery: from Generation to Optimization." — [arXiv 2505.16094](https://arxiv.org/html/2505.16094v1) [SR]
- ME2 transfer: (1) Showing the LLM parent records together with their trusted 9-axis values in the prompt (MolLEO feeds parent scores) lets it reason about where to move. (2) A similarity filter to an anchor keeps LLM proposals from drifting into incoherence. (3) The paper's finding that LLM edits alone gave only modest gains while the full loop did well supports a hybrid loop: LLM proposals plus cheap code variants, with every candidate measured by code.

### Inferences
- The MoleculeSTM operator, which moves in a joint text-structure embedding and is then decoded and checked, is the most literal "joint semantic plus structured space" in this list. ME2's analogue would require a learned joint embedding of concept text and the 9-axis record, which 15 paired examples cannot support without augmentation (e.g., verbalized axes for the 1,000 variants).

### Gaps
- Protein design (text-conditioned protein generation with structure checks) was not covered this session.

## Q4. Explicit comparisons: joint vs single-space exploration

### Takeaway
No source found compares joint (semantic plus numeric) exploration against single-space exploration head-to-head. The available evidence compares descriptor types: LLM-judged semantic axes beat embedding-similarity axes (QDAIF vs QDEF, ACES vs ELM-embedding), learned projections of embeddings nearly match ground-truth descriptors (QDHF), and QD-structured data beats random data for text-conditioned generation (TileGPT).

### Cited Findings
- QDAIF vs QDEF: human QD score 0.617 vs 0.308 (LMX, seeded). — [arXiv 2310.13032](https://arxiv.org/pdf/2310.13032)
- ACES semantic archive vs ELM embedding archive: more cells beyond training coverage and higher entropy for semantic. The embedding archive produced more valid but less novel puzzles. — [arXiv 2310.10692](https://arxiv.org/html/2310.10692v1)
- QDHF learned descriptors vs AURORA unsupervised descriptors vs ground truth: 72.5 vs 53.0 vs 74.8 (robot arm QD score). — [arXiv 2310.12103](https://arxiv.org/html/2310.12103v3)
- OMNI-EPIC full system vs no-archive and vs no-interestingness ablations: significantly higher embedding-cell coverage. — [arXiv 2405.15568](https://arxiv.org/pdf/2405.15568)
- UC-ME vs unguided MAP-Elites: lower coverage but better match to user criteria. This is the bounding-by-user trade-off. — [arXiv 2304.01642](https://ar5iv.labs.arxiv.org/html/2304.01642)

### Inferences
- ME2 can contribute an evaluation the literature lacks: an ablation of (a) 9-axis-only archive, (b) embedding-only archive, and (c) joint archive, scored by coverage on both axis cells and embedding-PCA cells (OMNI-EPIC metric), plus prompt-consistency between concept text and record (DS2D-style).

### Gaps
- No direct joint-vs-single study located. This may exist in 2025–2026 GECCO or CAADRIA proceedings not reached within the tool budget.
