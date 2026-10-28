# Grounding and Steering Free LLM Generation with a Trusted Structured Attribute System

Reading depth legend: [FT] = full text (or most of the HTML/PDF) read via fetch; [ABS] = abstract or landing page only; [SR] = search-result listing only (existence and title confirmed, content not read).

Project framing used throughout: the LLM writes concept text plus an explicit structured record; code computes a trusted 9-axis descriptor record (the "verifier/descriptor function"). Advanced models are reached only through manual chat batches; small local models run in Ollama.

## Generate-verify architectures (LLM-Modulo, solver/verifier loops, critics, self-consistency vs external verification)

### Takeaway
The evidence consistently says that LLM self-critique does not reliably improve, and often harms, correctness. Gains come from sound external verifiers, and much of the benefit comes from just the verifier's pass/fail signal plus re-prompting. For this project the 9-axis code is the "hard critic". The LLM should be used as generator and reformulator, never as the judge of where a proposal lands on the axes.

### Cited Findings
- [FT] LLM-Modulo is a generate-test-critique loop. An LLM proposes candidates, and a bank of critics evaluates them. **Hard critics** (sound, model-based checks such as VAL for PDDL, or causal/timeline/resource constraints) must all approve before a candidate is returned. **Soft critics** check style or preferences and may be LLM-based. — [Kambhampati et al., ICML 2024 position paper](https://arxiv.org/html/2402.01817v2)
- [FT] In LLM-Modulo, LLMs also act as **reformulators**, converting candidates into the formats that critics consume. A **meta/backprompt controller** pools critic feedback, using round-robin, LLM summaries, or prompt diversification. Verified outputs can become synthetic fine-tuning data. Humans contribute once per domain (model acquisition) and once per problem (spec refinement), not inside the loop. — [Kambhampati et al. 2024](https://arxiv.org/html/2402.01817v2)
- [FT] Evidence cited in the position paper: GPT-4 produced executable, goal-reaching plans only about 12% of the time in autonomous mode. Obfuscating names degraded this further, and fine-tuning did not change the picture much. On graph coloring, iterative self-critique was worse than the baseline because the LLM rejected correct colorings it had generated. — [Kambhampati et al. 2024](https://arxiv.org/html/2402.01817v2)
- [FT] Stated limits: the LLM's guesses carry no guarantees, and soundness comes only from the critics. LLMs cannot serve as hard critics. The approach depends on someone writing or acquiring the verifier model. — [Kambhampati et al. 2024](https://arxiv.org/html/2402.01817v2)
- [FT] An LLM-Modulo case study on TravelPlanner (180 validation queries) raised the final pass rate from 4.4% to 20.6% with GPT-4-Turbo (about 4.6x), and from 0% to 5% with GPT-3.5-Turbo. Baselines for GPT-3.5 were CoT 0%, ReAct 0.6%, and Reflexion 0%. The loop ran at most 10 iterations, or until all critics accepted. — [Gundawar et al. 2024](https://arxiv.org/pdf/2405.20625)
- [FT] Critic ablation in that study: format-only critics gave 1.1%, hard-only 1.6%, commonsense-only 2.8%, and all critics together 20.6%. Critic coverage therefore matters non-additively. A format critic (JSON validity and required keys) runs first and gates the others. — [Gundawar et al. 2024](https://arxiv.org/pdf/2405.20625)
- [FT] GPT-4-Turbo also served as a **critic extractor**, writing the code for hard and commonsense critics, which needed only minor manual fixes. The metacontroller simply concatenated critic feedback into the prompt. The authors flag that absolute pass rates remain low and that only the validation set was evaluated. — [Gundawar et al. 2024](https://arxiv.org/pdf/2405.20625)
- [SR] A follow-up generalizes this to "compound LLM architectures". — [Robust Planning with Compound LLM Architectures, arXiv 2411.14484](https://arxiv.org/html/2411.14484v1)
- [FT] Intrinsic self-correction, with no external signal, lowered accuracy on every benchmark tested:
  - GSM8K: GPT-4 went from 95.5 to 89.0 and Llama-2 from 62.0 to 36.5.
  - CommonSenseQA: GPT-3.5 went from 75.8 to 41.8.
  - HotpotQA: GPT-4 went from 49.0 to 43.0.

  Gains reported elsewhere were traced to oracle labels deciding when to stop, or to weak initial prompts. — [Huang et al., ICLR 2024, "LLMs Cannot Self-Correct Reasoning Yet"](https://arxiv.org/pdf/2310.01798)
- [FT] At equal numbers of responses on GSM8K, multi-agent debate did not beat self-consistency (majority vote): 83.2 vs 85.3 at 6 responses, and 83.0 vs 88.2 at 9. The authors recommend reliable external feedback (code execution, verifiers) and comparing methods at equal inference cost. — [Huang et al. 2024](https://arxiv.org/pdf/2310.01798)
- [ABS] On Game of 24, Graph Coloring, and STRIPS planning, GPT-4 self-critique causes a "significant performance collapse". A sound external verifier significantly improves performance. Simple re-prompting with a sound verifier keeps most of the benefit of more elaborate critique setups. — [Stechly, Valmeekam & Kambhampati, ICLR 2025](https://arxiv.org/abs/2402.08115v2)

### Inferences
- Mapping to this project:
  - Generator: the LLM, producing concept text plus a structured record.
  - Reformulator: the LLM, or a small local model, turning concept text into whatever input the axis code needs, if the structured record is not already code-ready.
  - Hard critic: the 9-axis code plus validity checks (geometry and program constraints).
  - Soft critics: text-vs-axes agreement and novelty.

  Never let the LLM's own claim about its axis position be authoritative. The finding that after-the-fact text becomes a placement inventory is consistent with "LLM as describer is unreliable".
- The Stechly result suggests that, in manual chat batches, simply returning "your proposal landed at axes X, intended Y; propose again" is likely to capture most of the value. Elaborate natural-language critiques may add little. This is cheap for a manual loop.
- The TravelPlanner ablation implies you need a gated format critic (schema validity) before computing axes, and multiple critic types together. A single check is weak.
- **Concrete small test:** take 20 targets (axis vectors). Arm A gives the LLM one shot. Arm B gives up to 3 rounds of feedback, where the feedback is only the computed axis vector vs the target. Arm C adds the LLM's own self-critique without computed axes. Measure L1/L2 distance to target per axis and the fraction within tolerance. The prediction from the literature is B > A ≥ C. Run it on a local Ollama model first (automatable), then a smaller manual batch on the advanced model.

### Gaps
- I did not find studies of LLM-Modulo-style loops in architectural or spatial design specifically.
- The precise "critique content vs bare signal" numbers in Stechly et al. were not read (abstract only).
- The original self-consistency paper (Wang et al. 2022) was not fetched. Self-consistency evidence here comes only via Huang et al.'s comparison.

## Round-trip / cycle consistency between text and structure (faithfulness metrics)

### Takeaway
There are mature methods for checking text against a record: PARENT (n-gram overlap against the source table), QAGS (question-answer agreement between source and output), and cycle training (text to data to text). All of them operationalize "text and record agree" as **recoverability**. For this project the natural metric is: extract axes from the concept text (with no access to the record), then compare them to the code-computed axes, per axis.

### Cited Findings
- [ABS] PARENT aligns n-grams of both the generated text and the reference to the source table, and computes precision and recall against both. It correlated better with human judgments than BLEU and ROUGE on WikiBio, where references diverge from tables. It performed comparably to information-extraction-based evaluation (Wiseman et al. 2017) while being easier to use. — [Dhingra et al., ACL 2019](https://arxiv.org/abs/1906.01081)
- [ABS] QAGS generates questions from the output and answers them against both the output and the source. Consistency means similar answers. It had "substantially higher correlations" with human factual-consistency judgments than other automatic metrics on CNN/DM and XSUM, and its Q/A pairs localize which spans are inconsistent. — [Wang, Cho & Lewis, ACL 2020](https://aclanthology.org/2020.acl-main.450)
- [ABS] Cycle training pairs a data-to-text model with a text-to-data model and frames faithfulness as consistency between the two representations. From only 100 supervised samples it reportedly approaches fully supervised performance on WebNLG, E2E, WTQ, and WSQL. — [Wang et al., ACL 2023 (Outstanding Paper)](https://aclanthology.org/2023.acl-long.160)

### Inferences
- **Text-to-axes recoverability score.** A blind extractor (a local model or a second chat) reads only the concept text and predicts each of the 9 axes. Compare against the code values to get per-axis agreement (κ or weighted κ for ordinal axes, MAE or Spearman for continuous ones).
  - Axes the text cannot recover are the ones where text and structure disagree.
  - Given the existing finding that semantic distance does not track heights, expect height-type axes to score lowest.
  - This is a QAGS analogue: the "questions" are the 9 axes.
- **Record-vs-claim check (PARENT analogue).** Parse explicit numeric or categorical claims in the text ("four-storey bar", "courtyard") and check each against the computed record. Report claim precision (claims supported by the record) and record recall (salient record features mentioned).
- **Round trip, reverse direction.** Code-computed axes go to an LLM, which writes concept text. A blind extractor reads that text back to axes. This measures whether the vocabulary can express each axis at all. If an axis fails even here, the problem is the vocabulary, not the generator.
- To counter the "placement inventory" failure, prompt for intent before structure: text first, then record, as in NL-to-Format (see next section). Score the text with the blind extractor, not with the LLM that wrote the record.

### Gaps
- Exact PARENT and QAGS correlation values, and the cycle-training error breakdowns, were not read (abstract-level only).
- I found no published round-trip faithfulness study for design or architectural descriptions.
- NLI-based or LLM-judge consistency checkers from 2023–2026 (e.g., AlignScore, FActScore-style claim decomposition) were not researched in this pass.

## Attribute-conditioned and constraint-guided generation (explicit targets, constrained decoding)

### Takeaway
Giving LLMs explicit numeric targets works only partially. Even on a simple, directly countable attribute (length), frontier models hit the target precisely only about 50–60% of the time, and small open models 10–25%. Hard format constraints such as JSON schemas can degrade reasoning. The robust pattern is: free text first, then conversion to the structured record, then code verification, then feedback on the target error.

### Cited Findings
- [FT] Asked for target word counts, models matched precisely at these rates (Precise Match / Flexible Match):
  - claude-3.5-sonnet 61.65 / 79.55
  - gpt-4o 57.75 / 74.30
  - Llama3-70B 46.55 / 63.75
  - Mistral-7B 15.45 / 27.70
  - Gemma-2B 12.35 / 18.45

  Long targets (700 to over 800 words) were hardest. — [Ruler, Findings of EMNLP 2024](https://arxiv.org/html/2409.18943v2)
- [FT] Training with special "meta length tokens" (Ruler) raised precise match by an average of +27.97 points. For example, Mistral-7B at Level 0 went from 20.29 to 70.18. The authors attribute the original errors to tokenization and to training data that rarely targets length. — [Ruler 2024](https://arxiv.org/html/2409.18943v2)
- [SR] Related work on iterative and zero-shot length-controllable summarization treats attribute control as a multi-round refinement problem. — [Exploring Iterative Controllable Summarization](https://arxiv.org/html/2411.12460v2); [Zero-Shot Strategies for Length-Controllable Summarization](https://arxiv.org/html/2501.00233v2)
- [FT] Format restrictions affect reasoning and classification differently:
  - Stricter format restrictions degrade reasoning tasks. GPT-3.5-Turbo on Last Letter scored 56.74 in free text vs 25.20 in JSON mode.
  - Removing the explicit schema raised Claude 3 Haiku on GSM8K from 23.44 to 86.99.
  - For classification, JSON mode was competitive or better: Gemini 1.5 Flash on DDXPlus went from 41.59 to 60.36.
  - Key order matters. Putting the answer key before the reasoning key suppressed reasoning.
  - "NL-to-Format" (answer in natural language, then convert) performed nearly identically to unrestricted text.

  — [Tam et al., "Let Me Speak Freely?", EMNLP 2024 Industry](https://arxiv.org/html/2408.02442v1)
- [FT] In-context QD showed that **explicit target feature values in the prompt** do steer generation in low-dimensional numeric domains. Archive elites were serialized as `fitness:features:params`, and the query asked for specific cell features. Feature-aware templates were critical: the fitness-only template had low coverage. This was with Mistral-7B, a small model. — [Lim et al., In-context QD, 2024](https://arxiv.org/html/2404.15794v2)

### Inferences
- Expect explicit axis targets to land only approximately, with likely per-axis differences. Axes that the LLM can "count" in text (number of bars or wings, courtyard yes/no) should be easier than derived geometric quantities (height variance, compactness). Plan on a feedback loop (previous section), not one-shot hits.
- Record order: write concept text (intent) first, then the structured record, and place any reasoning field before the axis or target fields. A JSON schema with targets-first ordering risks the "answer before reasoning" failure.
- For manual chat batches, show 3–6 archive exemplars together with their *computed* axis vectors (the in-context QD format), sorted by distance to the target cell. That paper found distance sorting the most consistent ordering. Then ask for a proposal at the target vector.
- **Concrete small test:** for each of the 9 axes, sweep a target across 5 levels while holding others at mid. Record computed vs requested values, and fit the slope and R² per axis. Slope near 1 means controllable; slope near 0 means the LLM cannot steer that axis, so steer it with code-side parameters instead. Run it in Ollama at around 10 samples per level.

### Gaps
- Grammar-constrained or JSON-schema constrained decoding in Ollama (structured outputs) was not separately evaluated for quality cost on small models.
- I found no study testing LLMs hitting multi-dimensional (more than 3) attribute targets in text or design generation. In-context QD used 2D feature grids on numeric toy domains.

## Gap-guided / coverage-guided prompting (LLM-driven MAP-Elites, QDAIF, novelty prompts)

### Takeaway
LLM-as-mutation-operator inside MAP-Elites (QDAIF, In-context QD) improves coverage and QD score over random sampling and quality-only baselines. Explicitly querying empty cells is a tested option in In-context QD. QDAIF uses an LLM to compute descriptors, which in this project are replaced by trusted code. That is a strict improvement, because QDAIF's main reported limits are reward hacking and miscalibrated AI-feedback descriptors.

### Cited Findings
- [FT] QDAIF loop: pick a random archive elite, mutate it with LMX few-shot prompting, then have an LM score quality (yes/no log-prob) and diversity (label log-probs). Keep the result if it fills an empty bin or beats the current occupant. Mutation does **not** explicitly target empty bins: parents are chosen at random. — [Bradley et al., ICLR 2024](https://arxiv.org/html/2310.13032v4)
- [FT] QDAIF results:
  - On Opinions and Stories (2000 iterations, 5 seeds) it had significantly higher QD scores than all baselines.
  - Poetry (200 iterations): QD score 130 (CI 118–145), vs Random-Poems 76 and Fixed-Seed-Rewrite 99.
  - Human-evaluated QD score: 0.772, vs Fixed-Few-Shot 0.767, Shuffling-Few-Shot 0.696, LMX-Quality-Only 0.650, and Random-Search 0.606.
  - Human quality rating was slightly lower than Fixed-Few-Shot (3.900 vs 4.133).

  — [Bradley et al. 2024](https://arxiv.org/html/2310.13032v4)
- [FT] AI-feedback descriptor reliability in QDAIF: AI and human labels agreed 73% of the time, and humans agreed with each other 73%. AI–human agreement rose to 82% where both humans agreed, and to 95% when the neutral category was excluded. Bins were made non-uniform (denser at the extremes) because LM logits do not move linearly with qualitative change. — [Bradley et al. 2024](https://arxiv.org/html/2310.13032v4)
- [FT] QDAIF's stated limits:
  - Reward hacking: the AI–human quality correlation weakens at the highest AI scores.
  - It does not discover new diversity axes.
  - The specified axes can be satisfied superficially. Their example is "hero spy vs politician" stories that ignored how the characters interacted.

  — [Bradley et al. 2024](https://arxiv.org/html/2310.13032v4)
- [FT] In-context QD details:
  - Feature queries are either "Uniform" (sample cell centroids) or "Empty" (fill empty cells first). The fitness query is set about 20% above the best fitness in context.
  - It beat MAP-Elites (iso-line operator) and random sampling on max fitness and QD score for Rastrigin and Sphere. Coverage was similar across methods. It was competitive on Arm and effective on Hexapod (D=24).
  - Larger context helped.
  - Limits: context length caps dimensionality, a predefined feature space is assumed, and it struggles when patterns are unclear.

  — [Lim et al. 2024](https://arxiv.org/html/2404.15794v2)

### Inferences
- The project's architecture (trusted code descriptors plus LLM generator) sits between QDAIF and In-context QD. Use In-context QD's empty-cell querying with QDAIF's semantic (text) generation.
- The "superficial satisfaction" limit in QDAIF maps to the project's text/axes disagreement risk. The text may claim a strategy that the record does not realize. The round-trip score from the cycle-consistency section is the guard against this.
- With 9 axes, a full grid is huge (for example 5^9, about 2M cells). Use a CVT-MAP-Elites style centroid archive, or project to 2–3 axes per batch. Gap targets should be drawn from cells *adjacent* to occupied ones (reachable) as well as from distant ones, and both arms compared.
- **Concrete small test, with three arms of equal budget (for example 60 proposals each):**
  - (a) Random-parent few-shot mutation (QDAIF-like).
  - (b) Explicit empty-cell target: exemplars sorted by distance, then "propose a strategy at axes = v*" (In-context QD-like).
  - (c) Natural-language gap description: "no proposals yet have tall, compact, low-link-density schemes", with no numbers.

  Metrics: new cells filled, coverage, validity rate, distance-to-target for arms b and c, and text–axes recoverability. Arm (c) tests whether semantic gap descriptions outperform numeric ones for a semantic generator.

### Gaps
- OMNI / OMNI-EPIC (models of interestingness), "novelty search with LLMs", LLMatic, and ELM (Evolution through Large Models) were not fetched in this pass. They are relevant for open-ended interestingness prompts and should be checked.
- Exact In-context QD coverage numbers appear only in figures and were not extracted.
- I found no measured comparison of "empty-cell numeric target" vs "natural-language gap description" prompts. This appears to be an open question, and a good project experiment.

## Language-to-attribute extraction reliability (LLM or local model extracting structured attributes)

### Takeaway
LLM attribute extraction is highly sensitive to prompt wording, option order, role framing, model choice, and sampling. Reliability must be measured per field, with repeated runs, paraphrase ensembles, and at least two models, against a small expert-labeled audit set. Do not trust single-shot extraction from one model.

### Cited Findings
- [FT] A five-source variance framework for LLM annotation:
  1. Construct and rubric specification.
  2. Interface and context (wording, option order, layout, role).
  3. Model preferences, with chain-of-thought rationale possibly mismatched to the label.
  4. Output constraining and parsing, plus poor probability calibration.
  5. System and aggregation (cross-model disagreement, version drift).

  — [Variance-Aware LLM Annotation, arXiv 2601.02370](https://arxiv.org/pdf/2601.02370)
- [FT] Measured effects in that paper:
  - Role framing shifted outcomes by 15.76–85.12 percentage points.
  - Prompt paraphrases shifted them by about 3–28 points.
  - Prestige cues shifted them by about 12–13 points.
  - Identical prompts gave P(option A) from 0.68 to 0.92 across repeated draws.
  - Average cross-model Cohen's κ was 0.026 (58.7% raw agreement), and model choice determined the outcome in 90% of annotations.

  The setting is strategy/business evaluation, not geometry. — [arXiv 2601.02370](https://arxiv.org/pdf/2601.02370)
- [FT] Recommended protocol:
  - Behaviorally anchored rubric per construct.
  - Paraphrase ensemble P≥3 (recommended 3–5), samples S≥10 (recommended 20), models M≥2.
  - Randomized option order.
  - Majority vote for labels, median or trimmed mean for numeric slots.
  - Dawid–Skene or GLAD aggregation if κ < 0.6, and human escalation or redesign if κ < 0.4.
  - Calibration via Brier score and reliability curves.
  - Slot-by-slot reliability for multi-field outputs.
  - Expert validation on about 5–10% of the corpus.

  — [arXiv 2601.02370](https://arxiv.org/pdf/2601.02370)
- [FT] Separate vs joint elicitation of multiple criteria produced significant effects for most criteria. So extracting all 9 axes in one prompt vs one prompt per axis can change results. — [arXiv 2601.02370](https://arxiv.org/pdf/2601.02370)
- [FT] QDAIF's AI–human label agreement (73%, equal to human–human agreement) gives a reference point for LLM attribute labeling of creative text. Categorical extremes are much more reliable (95%) than neutral middles. — [Bradley et al. 2024](https://arxiv.org/html/2310.13032v4)
- [SR] Open-weight LLMs have been evaluated for structured extraction from narrative medical reports across use cases and languages. This is relevant for local-model extraction, but not read. — [arXiv 2511.10658](https://arxiv.org/pdf/2511.10658)

### Inferences
- Per-axis reliability protocol for the project. The ground truth is the code-computed axes, which this project has for free, unlike most annotation settings.
  1. Write a behaviorally anchored rubric per axis, with architectural examples at low, mid, and high.
  2. Run the local Ollama model with 3 paraphrases × 10 samples per text, plus a second local model.
  3. Report per axis: (i) self-consistency across samples; (ii) cross-paraphrase stability; (iii) agreement with code values (weighted κ or Spearman); (iv) calibration if log-probs are available.

  Axes with κ < 0.4 against code should not be used as extraction targets. Treat them as "code-only" axes and do not ask the text to carry them.
- Expect mid-range values to be least reliable, following the QDAIF neutral-category finding. Consider extracting coarse ordinal bins (low/mid/high) rather than continuous values.
- Test one-prompt-all-axes vs one-prompt-per-axis, given the joint-elicitation effect.
- **Concrete small test:** use 40 existing proposals with code-computed axes. Strip the records, extract axes from text only with two Ollama models × 3 paraphrases × 10 samples, and produce a 9-row reliability table. Cross-check against the existing finding that heights are not recoverable.

### Gaps
- No source found specifically on extracting spatial or geometric attributes (heights, adjacency topology) from architectural prose.
- The medical extraction paper's per-field numbers were not read.
- No 2025–2026 benchmark comparing small local models (7–14B) vs frontier models on per-field extraction reliability was retrieved in this pass.
