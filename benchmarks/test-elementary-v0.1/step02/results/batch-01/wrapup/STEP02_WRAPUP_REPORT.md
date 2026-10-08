# Step 02 pilot wrap-up: LLM proposals versus Massing Explorer

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../CONSTRAINT_ALIGNMENT_AUDIT.md).

**Status: corrected exploratory record, not a final matched-constraints performance verdict.** The numerical summaries below describe original ratings only. The earlier interpretation of cross-mass splitting as a permissible representation extension was wrong.


- **Main conclusion:** LLMs supplied architectural organization, operational explanations and interpretations of an ambiguous brief. ME supplied a reproducible search archive and solver-checked realizations within a restricted representation. Asking LLMs to explore changed their observable process much more consistently than it improved their final proposals.
- **What this pilot supports:** specific strengths, weaknesses and design-process hypotheses. It does not establish a single overall winner: ME has no Fable ratings under the same rubric. The comparison below uses the scores, raw answers, arithmetic audit and frozen ME execution records together.
- **Scope:** 12 independent LLM responses, three per model/prompt cell; one frozen ME baseline recovered by rerun. A0 asks for the strongest proposal with a freely chosen approach. A1 additionally asks the model to devise and carry out systematic exploration, without prescribing axes, candidate counts or a sequence. Both permit one response and prohibit design tools/feedback. “Reasoning” below means observable decisions and explanations, not access to hidden internal thought.

## 1. What prompting changed

Quality scores below are **group medians, 0–4**; each group has three runs. Keep the four axes separate.

| Group | Cases | Coherence | Alignment | Efficiency | Robustness |
|---|---|---:|---:|---:|---:|
| ChatGPT A0 | R02, R05, R10 | 3 | 4 | 2 | 2 |
| ChatGPT A1 | R01, R07, R11 | 2 | 4 | 1 | 1 |
| Opus 5.5 A0 | R04, R08, R12 | 3 | 3 | 3 | 2 |
| Opus 5.5 A1 | R03, R06, R09 | 3 | 3 | 2 | 2 |

Behavior scores below are **group medians, 0–3**.

| Observable behavior | ChatGPT A0 | ChatGPT A1 | Opus A0 | Opus A1 |
|---|---:|---:|---:|---:|
| Search-space framing | 0 | 2 | 1 | 3 |
| Exploration breadth | 0 | 2 | 1 | 3 |
| Exploration diversity | 0 | 1 | 1 | 3 |
| Comparative evaluation | 0 | 2 | 1 | 3 |
| Constraint verification | 2 | 3 | 3 | 3 |
| Revision / backtracking | 0 | 0 | 0 | 1 |
| Tradeoff reasoning | 1 | 3 | 2 | 3 |
| Selection / stopping logic | 1 | 2 | 1 | 2 |

- **A1 successfully elicited observable exploration from both models.** ChatGPT breadth rose 0→2 and comparison 0→2; Opus breadth, diversity and comparison each rose 1→3. Raw support: ChatGPT A0 supplies one recommended scheme without a documented alternative comparison; ChatGPT A1 supplies option tables. Opus A1 supplies staged screening of allocations, sections and arrangements. [S1–S3]
- **A1 did not improve any of the four group-median quality axes.** ChatGPT coherence, efficiency and robustness each fell one point; Opus efficiency fell one point and its other medians stayed unchanged. This is the observed result of these runs, not proof that exploration harms design. [S1]
- **There were useful exceptions within A1.** ChatGPT R11 scored 3/4/2/3, versus R01 and R07 at 2/4/1/1. Opus R06 scored 3/3/2/3, while R03 scored 3/4/1/2. An exploration prompt can produce a stronger individual result without raising the group median. [S1]
- **Medians conceal some smaller shifts.** Opus A1 mean coherence rose 2.67→3.00, alignment 2.67→3.33 and robustness 2.00→2.33; mean efficiency fell 2.67→1.67. ChatGPT A1 mean alignment rose 3.67→4.00, but its other means fell. The defensible statement is “no median quality improvement,” not “no quality benefit whatsoever.” [S1, S7]
- **More process also meant more reporting.** Extracted response text averaged about 1,823→2,211 words for ChatGPT (+21%) and 1,712→1,864 for Opus (+9%). Displayed duration medians rose 7m50s→10m27s and 5m35s→7m11s respectively. These are text-length/host-duration observations, not token-cost measurements or comparable compute benchmarks. [S2, S3]

## 2. How the LLMs approached the problem

- **ChatGPT A0: propose an organization, allocate the program, then demonstrate compliance.** R02 and R05 use an academic bar, separate commons and stepped civic/media mass. R10 redistributes classrooms into the civic mass and progressively reduces its upper plates. Their strongest recurring content is the secure entry, independent after-hours zone, separate service route and explicit room accounting. Their weakness is limited evidence of testing competing organizations before committing. [S2: R02, R05, R10]
- **ChatGPT A1: mostly test variants around a favored organizational idea.** R07 varies bar stories, bar length and commons size; R11 varies commons packing and full versus stepped civic plates. R01 names broader topology alternatives but gives only qualitative rejection statements and dimensions only the selected option. This supports a pattern of local refinement more than a demonstrated broad search. [S2: R01 §10, R07 §7, R11 §2]
- **Opus A0: develop one scheme, but test local architectural consequences voluntarily.** R04 checks room frontage and compares classroom sections and narrow/wide halls. R08 checks the crowded ground-floor frontage and rejects a 30/20/30 section. R12 discusses a two- versus three-floor hub. Thus A0 process scores of 1 reflect visible local comparisons; ChatGPT's zeros reflect missing comparison evidence, not proof of absent internal exploration. [S2: R04 §§3,7; R08; R12]
- **Opus A1: use a hierarchy of decisions.** R03 reports five passes: derive envelopes → consider area targets → compare allocations → test hall/composition variants → check section/floor allocation. R06 uses a similar four-step screen. R09 explicitly orders partition → section → dimensions → topology. The partition decision determines which later geometric choices are worth investigating. [S2: R03 §§1–2, R06 exploration account, R09 §2]
- **The strongest strategic insight was the “empty middle floor” problem.** Ground-floor admin plus top-floor media plus a three-floor preference can leave an isolated civic mass with no useful scheduled program on floor 2. R09 identifies this as the decisive partition issue and embeds admin/media in the academic bar; R04/R08 independently use that integration. R11 instead accepts an unprogrammed civic floor. This is direct evidence that program organization changes the quality of the realized form. [S2]
- **The weak point is the revision loop.** Only R03 and R09 received nonzero revision scores: R03 changes hall geometry to increase its area margin; R09 lengthens its academic bar after an initial area check. Most other responses compare options but show no subsequent correction of the selected scheme. Only R09 received the top selection/stopping score, with a local dimensional stopping condition; none demonstrates exhaustive exploration. [S1–S3]

## 3. What relates to final-design performance

- **The clearest numerical association is area versus efficiency.** Across the 12 runs, Spearman rank correlation between GFA and Fable efficiency is **−0.89**. Among the ten runs using the same approximately 76,366-SF basis it remains **−0.80**. Smaller proposals generally received higher efficiency ratings in this batch. This partly overlaps what the efficiency rubric assesses; it is not an independent measure of design merit. [S1, S4, S7]
- **Exploration scores did not closely track quality.** Breadth versus efficiency is **−0.41**, versus coherence **−0.09**, and versus robustness **+0.11**. Comparison versus coherence is **0.00**. These are descriptive associations across only 12 cases with model/prompt differences mixed together; they do not identify causes. [S7]
- **The area-basis choice matters.** R04 and R08 select the 66,405-SF reference, yielding approximately **66% net-to-gross** and efficiency 3. Most other proposals select the 76,366-SF reference and yield roughly **56–60%**. Two of Opus A0's three runs therefore had a materially different area target. Its efficiency advantage cannot be attributed entirely to model ability or prompt style. [S2, S4]
- **Preference satisfaction can coexist with weak utilization.** R01 and R07 score alignment 4 but efficiency/robustness 1. They repeat two minimum-length three-floor academic bars, producing sparse upper floors and totals near the upper area limit. R07 has just approximately **117 SF** of upper-band margin. [S1, S2, S4]
- **Eight of twelve proposals have at least one plate below 40% scheduled NFA/GFA.** There are ten such plates among 76. R05's civic floor 2 is about **16%** scheduled net; R11's is **0%**. These are programmed-utilization diagnostics: the residual also includes legitimate circulation, walls, services and planning allowance, so it is not automatically all wasted space. [S4, S7]
- **A good narrative can leave a structural issue unresolved.** R07 attaches both academic bars through the ground-floor commons; it does not establish a connection between their upper floors. R03 explicitly rejects a similar hall-between-bars arrangement because upper levels are disconnected. Different runs apply different depths of scrutiny to similar design problems. [S2: R07 §§1,5; R03 §2]
- **Dimensional explanation is useful but can be wrong.** R12 claims the gym's 100-ft dimension makes a hall narrower than 90 ft impossible; other responses orient that dimension along the hall, including R03's 80-ft-wide hall. R12 also has inconsistent medical placement. R09's diagram/narrative interface and several room-size/schedule differences remain unresolved. These examples explain why articulate checking is weaker evidence than a reproducible layout test. Cross-mass department assignments must additionally pass the intended hard gate. [S2, S4]

## 4. What ME actually achieved

- **ME explored a recorded finite space:** 209 realization attempts, 159 distinct archived cells, 37 legal cells and 122 infeasible cells. That is **23.3% legal archived cells**, or **17.7 legal distinct cells per 100 attempts**. The latter is an archive-yield ratio, not an attempt-by-attempt success probability. [S5, S7]
- **The 37 legal cells represent six distinct program partitions**, with 9, 7, 6, 6, 5 and 4 variants. The full archive contains 26 partitions. There is more organizational diversity than “two schemes,” but substantially less than “37 different architectural strategies.” All legal cells use **independent bars**. [S5, S7]
- **Do not compare 12/12 LLM evaluator passes with 37/159 ME legal cells as competing success rates.** The LLM dataset contains only final recommendations; the ME archive includes failed search candidates. All 12 LLM totals reconcile arithmetically, but their full room layouts were not independently realized. [S1, S4–S5]
- **ME's advantage is traceability within its rules.** Candidates preserve partition, stories, loading, envelope, plates, solver results and failure categories. Recovered geometries match archived ground dimensions within 0.02 ft rounding and all 37 return passing frozen-solver checks. This is stronger computational evidence than an LLM's self-reported compliance, while still not certifying complete room plans or code compliance. [S5–S6]
- **Its representation is narrower than the LLM proposals.** Courtyard, perpendicular wings and podium are explicitly unsupported; paired bars require missing site-frontage information. LLM answers can discuss shared hinges, courts, security sequences, stage/music connections and stepped civic forms without that restriction. A named topology in prose still needs geometric realization. [S2, S5]
- **Search completion is not established.** COVER is explicitly marked incomplete; it searched a pool of 31 organizations against an upstream CSP landscape of 966 feasible partitions. CSP feasibility is an upstream screen, not proof that 966 complete buildings can be realized. Local MCTS/refinement saturation therefore does not show global coverage or optimality. [S5]
- **Repair and refinement contributed little in this run.** Repair made 14 projections on eight ideas, legalized zero and recorded no feasibility-distance improvement. Refinement recorded eight tries and no improvement. The logs also show no pairwise taste-learning comparisons and no active planner in the saved state. These mechanisms exist in the pipeline, but this run does not demonstrate their added value. [S5]
- **The selected scheme was not robust to all tested changes.** Under six ±15% department-area probes with partition/stories fixed and dimensions allowed to adapt, it survived **2/6** and collapsed **4/6**. All three growth probes failed the length cap; shrinking PE failed the ratio band. This is a concrete coupling between program size, ratio rules and geometry. [S5]
- **ME's internal scores cannot be treated as Fable equivalents.** Legal-cell median coherence is 1.00 and efficiency 0.956 on ME's 0–1 scale. But coherence uses contiguous stacks/public-on-grade, while efficiency uses leftover area and footprint likeness—not Fable's whole-design judgment. The common 0.75 robustness values are untested proxies; the selected scheme's measured probe is 0.333. Rescaling would not make these scores comparable. [S5, S8]

## 5. LLM versus ME: supported comparison

| Capability | LLM evidence | ME evidence | Pilot takeaway |
|---|---|---|---|
| Interpret ambiguity | All answers identify area/ratio questions; some carry alternative policies | Runs execute a configured interpretation | LLM useful for framing choices; interpretation must be explicit before computational comparison |
| Organizational reasoning | Opus A1 screens allocations; ChatGPT explains operational zoning | Six legal partitions preserved in archive | Both explore strategy, with different evidence and limits |
| Spatial/operational synthesis | Secure entry, after-hours separation, service routes, courts and interfaces described | Independent-bar realizations; topology exclusions explicit | LLM proposes richer relationships; ME realizes a narrower space |
| Constraint evidence | Arithmetic and frontage checks; some assertions and contradictions | Repeated solver checks and failure classifications | ME offers stronger auditability within its implemented rules |
| Revision | Nonzero visible revision in 2/12 responses | Recorded actions/probes, but repair/refine gains weak | Neither demonstrates a consistently effective correction loop here |
| Robustness | Fable judgments and qualitative contingencies | Explicit selected-scheme probe: 2/6 survived | ME supplies measurable sensitivity, but its selected strategy is fragile |
| Overall quality | Four Fable axes for each final proposal | No matched Fable ratings | No numerical overall LLM-versus-ME quality ranking is supported |

## 6. Conclusive takeaways for the project

- **Keep strategy first.** The empty-middle-floor examples show that partition/stacking decisions cause later utilization problems. Optimize organization before spending effort polishing dimensions.
- **Use LLMs to frame and propose, then use realization feedback to revise.** Opus A1's partition-first funnel is the strongest observed template. Require each proposed alternative to identify a changed decision, the expected benefit and a test that could reject it.
- **Do not use longer explanations as a proxy for better outcomes.** A1 raised process ratings substantially but delivered no median quality gain. The missing ingredient appears to be reliable feedback on the chosen proposal; that is a hypothesis to test next, not a result already demonstrated.
- **Make floor utilization and connections explicit objectives.** Check scheduled net/gross by floor, empty intermediate plates, upper-level connections and ground-floor frontage—not only total area and preference checklists.
- **Expand ME where the architectural reasoning exceeds its representation.** Respect the hard prohibition on cross-mass department splitting. Investigate legal vertical civic/academic integration and connected L/U/hinge arrangements with explicit circulation joints. Retain unsupported concepts for review rather than translating them into independent bars and losing their intent.
- **Make robustness consequential in selection.** A scheme that passes nominal conditions but fails all tested growth scenarios should carry that evidence into the shortlist; untested proxy values should not compete as measured robustness.
- **Demonstrate each search mechanism's contribution.** Compare COVER-only with MCTS/BO/repair/refine additions under fixed budgets, tracking new legal partitions and improved outcomes. This run cannot establish that pipeline complexity bought better architecture.
- **Step 02 remains an exploratory pilot requiring a corrected matched-input run before performance comparison.** LLMs show richer architectural synthesis and self-chosen search structures; ME shows explicit computational search and bounded validation. A tool-assisted revision experiment is the direct next test of whether combining those strengths improves the final result.

## Evidence and reproducibility

- **S1:** `evaluator/QUALITY_FABLE_LOCKED.csv`, `BEHAVIOR_FABLE_LOCKED.csv`, `GROUP_SUMMARIES.json`, `MASTER_RESULTS.json`; original ratings unchanged.
- **S2:** `behavior/MASKED_SHUFFLED_RAW_RESPONSES.md`; the R01–R12 identifiers above reference these raw answers. Local reviewed copy: `source/masked_raw.md`.
- **S3:** Step 02 `NATURAL_PROMPT.md`, `GUIDED_PROMPT.md`, `MODEL_INPUT.md`, `OPERATOR_PROTOCOL.md`.
- **S4:** `evaluator/validation/VALIDATION_REPORT.md` and `NUMERIC_CHECKS.json`; local copies in `validation_work/`. Arithmetic checks establish necessary conditions, not complete room-fit feasibility.
- **S5:** Frozen archive/trace in `gallery_engine/candidate_geometry.json`, original engine commit `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`; rerun regression report in `gallery_engine/studies/_underwood_3mass_regress_report.json`.
- **S6:** Recovered floor geometry in `gallery_engine/realized_gallery.json`; provenance in gallery README. Gallery placements and balanced program blocks are presentation reconstructions, not additional experimental designs.
- **S7:** `QUANTITATIVE_FINDINGS.json`, calculated from locked scores, audited arithmetic and frozen archive; the local calculation script is `step02_wrapup/analyze_step02.py`. Spearman coefficients use average ranks for ties. No hypothesis tests or quality totals are used.
- **S8:** Frozen `src/massing_explorer/explore/performance.py`, especially `evaluate_descriptors` and `_robustness_score`.
- **Pilot interpretation:** three independent runs per cell, one quality rater, ambiguous area policy and unequal realized search/compute budgets. Treat numerical findings as batch descriptions; do not generalize model rankings or claim a causal search benefit. No blinding claim is needed for this pilot synthesis.

