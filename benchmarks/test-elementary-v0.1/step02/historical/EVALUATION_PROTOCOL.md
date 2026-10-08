# Step 02 — Evaluation protocol (v0.2)

Benchmark: `test-elementary-v0.1` | Applies to the A0/A1 pure-LLM batch after raw runs have been captured.

## Purpose

Evaluate architectural performance without letting model identity, prompt condition, prose style, or process narration unnecessarily influence the design score. Then analyze A0/A1 exploration behavior separately.

This procedure separates **generation**, **canonicalization**, and **evaluation**. Canonicalization is deliberately non-evaluative and does not need to be blinded. The later design-scoring stage is **label-masked and style-normalized, not fully blinded**. An evaluator may still infer a model or condition from architectural content or level of detail. Do not claim double-blind evaluation.

## 0. Freeze and archive the raw batch

Generation validity depends on what the generating model could see before and during the run. Host/operator metadata such as model name, reasoning setting, elapsed work time, screenshots, timestamps, or later A0/A1 file grouping does **not** contaminate an already completed run unless it was supplied back to the generator as additional design input.

Before normalization or scoring:

1. Preserve every raw model response exactly as produced.
2. Preserve available run metadata: model/version, reasoning setting, A0/A1 condition, timestamps, elapsed/visible work time, token/cost information if available, screenshots, and any host-visible process/status markers.
3. Assign each run an internal source ID and keep the source-to-condition/model mapping in a separate key.
4. Do not revise, repair, clarify, or follow up with the generating model.

The raw output remains the authoritative source. Normalized records are derived evaluation artifacts, not replacements.

## 1. Canonicalize the final design — masking not required

Canonicalization is a **non-evaluative extraction task**. The canonicalizer may see the original A0/A1 grouping, model metadata, screenshots, source ordering, and other run metadata. This is acceptable because no scoring or comparison occurs at this stage.

Convert the **single recommended design** from each run into the same terse canonical representation. Strip prose style, rhetorical framing, model-specific headings, exploration narration, and decorative concept naming from the architectural record. Keep run metadata in a separate metadata block if useful for audit.

Use the source case identifier during canonicalization. Randomized evaluation IDs are assigned only afterward. The canonical record should contain:

- `evaluation_id`
- `strategy_summary`
- `program_grouping`
- `spatial_relationships`
- `vertical_organization`
- `massing_organization`
- `circulation_logic`
- `requirement_response`
- `known_risks`
- `stated_rationale`
- `representation_gap`

For every material statement, preserve provenance using one of three statuses:

- **explicit** — directly stated or numerically given in the raw response;
- **inferred** — a minimal interpretation needed to express the design consistently, supported by the raw response;
- **unknown** — the response does not provide enough information.

### Canonicalization rules

1. Preserve architectural facts, quantities, dimensions, program assignments, floor locations, stated relationships, assumptions, and unresolved issues.
2. Do **not** improve a design, solve a missing dimension, repair a constraint violation, invent a room allocation, or reconcile conflicting statements.
3. If the response contradicts itself, retain the contradiction and flag it.
4. If a proposal uses a concept outside the Massing Explorer representation, describe it neutrally rather than forcing it into an existing category.
5. Keep model/host names, A0/A1 labels, elapsed time, screenshots, and other execution metadata **outside the architectural record** in a separate metadata block. Remove prompt references, search-process narration, stylistic language, and statements whose only purpose is to describe how the model explored from the architectural record.
6. Neutralize proposal names if they reveal writing style; the strategy itself must still be described factually.
7. Keep a traceable link from each normalized field to the corresponding raw passage so the transformation can be audited.

## 2. Mask and randomize before design scoring

This is the **principal masking boundary**. Build a new evaluation package from the completed canonical records.

For each case:

- remove the separate run-metadata block;
- remove model/host names, reasoning settings, A0/A1 labels, source-PDF names, elapsed time, screenshots, and process/status information;
- do not include the raw response or exploration narration;
- assign a newly randomized `Rxx` evaluation ID;
- randomize proposal order;
- keep the source-case ↔ randomized-ID mapping in a separate key.

The design evaluator receives only the randomized canonical architectural records and the frozen evaluation rules. The mapping key is revealed only after design scores are locked.

If the evaluator helped canonicalize the raw responses and may recognize them, record this as a limitation. The masking still reduces obvious stylistic and condition cues but does not make the evaluation fully blind.

## 3. Score hard feasibility first

Apply the frozen benchmark requirements and planning assumptions before subjective quality assessment.

Record:

- hard pass/fail;
- each specific violation;
- unverified requirements where the canonical record lacks evidence;
- realization status;
- existing feasibility distance where the current backend can validly compute it.

For this benchmark, checks include at minimum the frozen requirements concerning:

- exactly three masses;
- maximum three floors and three-floor preference;
- 60 m length cap according to the benchmark's recorded interpretation;
- gym and dining together and double height;
- art/music ground-floor preference;
- media on top floor above administration preference;
- administration on ground floor;
- 80-ft core-academic and special-education width requirement;
- mass-ratio band;
- gym/cafeteria minimum dimensions;
- department split contiguity and minimum 70 m² (~753 SF) floor portion;
- program-area conservation and relevant gross-area/tolerance logic.

Do not turn a preference into a hard failure. Preserve benchmark ambiguities rather than retroactively choosing a new interpretation because one proposal benefits from it.

## 4. Score architectural performance

After hard feasibility is recorded, evaluate the canonical proposal under the frozen Step 01 metrics:

- **program coherence**
- **preference alignment**
- **performance efficiency**
- **robustness / flexibility**
- **encoding status / representation gap**

Use the existing metric definitions without retuning them after seeing the batch. If a metric cannot be computed because required geometry or evidence is absent, mark it unavailable/unknown rather than estimating a convenient value.

For the A0/A1 one-proposal runs, within-run distinctness and coverage are not primary design-quality metrics.

## 5. Lock design scores

Before revealing identities:

1. Save the canonical records.
2. Save all feasibility outcomes.
3. Save all architectural-performance scores and evaluator notes.
4. Mark the evaluation batch as **locked**.

No score may be changed after unmasking merely because the model or condition is revealed. Corrections are allowed only for documented extraction/calculation errors and must retain the original value plus the correction reason.

## 6. Reveal model and condition, then aggregate

After score lock, restore the mapping from `Rxx` to:

- model/host;
- reasoning setting;
- A0 or A1;
- run number.

Compare first **within the same model**:

- A0 vs A1 final-design feasibility and quality.

Then compare **between models under the same condition**:

- ChatGPT vs Claude/other models for A0;
- ChatGPT vs Claude/other models for A1.

With the initial three runs per cell, report patterns and ranges rather than claiming population-level statistical significance.

## 7. Analyze exploration behavior separately and unblinded

Behavior analysis uses the **raw responses** and therefore intentionally knows A0/A1. It must not retroactively affect the locked design scores.

Record only observable behavior, such as:

- whether multiple alternatives are visibly considered;
- how many alternatives are explicitly distinguishable, if countable;
- whether an exploration framework is explicitly stated;
- what architectural variables or design dimensions the model says it varied;
- whether alternatives are compared, rejected, narrowed, or revisited;
- whether feasibility/constraints are explicitly checked during selection;
- how the final recommendation is selected;
- any visibly reported unexplored directions or representation-expanding ideas.

For **A0**, these are spontaneous behaviors and their absence is not evidence that no hidden deliberation occurred.

For **A1**, assess whether the model actually supplies a self-chosen exploration structure and observable evidence consistent with carrying it out. A reported process may still be post-hoc narration; do not treat it as privileged access to hidden chain of thought.

## 8. Batch outputs

For each run, retain:

- raw response and metadata;
- canonical `Rxx` record with explicit/inferred/unknown provenance;
- feasibility report;
- architectural-performance evaluation;
- later-unmasked model/condition metadata;
- behavior-analysis record.

For the batch, retain:

- the randomized mapping key;
- score-lock timestamp/version;
- per-cell summaries;
- cross-cell comparison;
- documented limitations.

The raw generation experiment, unmasked canonicalization record, masked design evaluation, and unblinded behavior analysis are separate artifacts and should remain separately auditable.

