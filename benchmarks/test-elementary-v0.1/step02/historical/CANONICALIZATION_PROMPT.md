# Step 02 — Sonnet canonicalization prompt (v0.2)

## Batch 01 use

This is the canonicalization prompt used for the Step 02 Batch 01 normalization stage. The canonicalizer was run in a fresh incognito Sonnet session on the separate A0 and A1 raw-result bundles. Canonicalization was intentionally **unmasked**: source labels and run metadata could be visible because this stage performs extraction only, not scoring or comparison.

The canonicalizer was not supplied the benchmark/evaluation documents or Massing Explorer search/evaluation documentation. Those materials are reserved for the later evaluation/analysis stages.

You are the **canonicalization stage** of an architectural benchmark.

The supplied source material may contain multiple independent design runs, including two source bundles (for example A0 and A1 PDFs), screenshots, model names, reasoning settings, elapsed-work indicators, and other metadata. Treat each run as a separate case. Do not merge runs or carry information from one run into another.

Your task is only to convert each run's **single final recommended design** into a neutral, standardized architectural record for later independent evaluation.

## Role boundary

- Do **not** evaluate, score, rank, praise, criticize, compare, or judge design quality.
- Do **not** analyze which model or experimental condition performs better.
- Do **not** infer hidden reasoning.
- Do **not** improve, repair, optimize, redesign, or complete any proposal.
- Do **not** resolve ambiguities or contradictions on the model's behalf.
- Do **not** use one response to fill gaps in another.
- Do **not** apply an external search taxonomy or scoring system.
- Ignore prose style, rhetorical framing, formatting quality, and exploration/process narration when constructing the architectural record.

Visible model names, A0/A1 labels, screenshots, elapsed work time, and other metadata are acceptable at this stage. Keep them separate from the design record and do not let them change how architectural facts are extracted.

## Provenance

For every material architectural fact, assign one provenance category:

- **explicit** — directly stated in the raw response;
- **inferred** — a minimal interpretation directly supported by the raw response;
- **unknown** — insufficient information.

If a response contradicts itself, preserve both statements and flag the contradiction.

Use terse, neutral architectural language. Remove stylistic adjectives and persuasive language unless necessary to preserve the design itself.

## Output for each source run

# [source case ID]

## strategy_summary
- value:
- provenance:
- evidence:

## program_grouping
Record how the nine departments are distributed across the three masses.
- value:
- provenance:
- evidence:

## spatial_relationships
Record adjacency, separation, hierarchy, connections, shared spaces, and relative placement.
- value:
- provenance:
- evidence:

## vertical_organization
Record floor-by-floor program distribution, stacking, double-height conditions, and departments spanning multiple levels.
- value:
- provenance:
- evidence:

## massing_organization
Record mass count, mass identities, dimensions, floor counts, proportions/ratios, and physical relationship/topology where provided.
- value:
- provenance:
- evidence:

## circulation_logic
Record primary entry, public/student/staff/service movement, vertical circulation, and connections between masses where stated.
- value:
- provenance:
- evidence:

## requirement_response
For each supplied project requirement, report only what the proposal states or clearly shows. Do not independently judge whether compliance is correct.

Include:
- exactly 3 masses
- max 3 floors
- preference for 3 floors
- max 60 m length
- gym and dining together
- gym and dining double height
- art and music preferred on ground floor
- media preferred on top floor above administration
- administration required on ground floor
- core academic width 80 ft
- special education width 80 ft
- mass ratio 2:5 to 5:8
- gym minimum 60 × 100 ft
- cafeteria minimum 40 × 60 ft
- daylight preferred maximum width 90 ft
- department split rule: contiguous floors and at least 70 m² / ~753 SF per floor portion
- program-area conservation
- gross-area / tolerance interpretation if stated

For each item:
- stated response:
- provenance:
- evidence:

## known_risks
Record uncertainties, unresolved requirements, assumptions, or feasibility concerns explicitly acknowledged by the response.
- value:
- provenance:
- evidence:

## stated_rationale
Reduce the proposal's stated architectural justification to neutral factual language.
- value:
- provenance:
- evidence:

## representation_gap
Only include something if the raw response explicitly describes an architectural relationship or idea that may not fit a conventional/simple representation. Otherwise:
- value: unknown
- provenance: unknown

Do not independently decide whether an external system can encode it.

## contradictions_or_missing_information
List contradictions, unclear dimensions, missing program assignments, unclear floor relationships, unspecified requirements, or anything that cannot be normalized without invention.

## run_metadata
Record only directly visible metadata if available:
- source run label
- model
- reasoning setting
- A0/A1 condition
- elapsed / visible work time
- screenshot present: yes/no
- other directly visible execution metadata

This metadata is for archiving only and will be removed before masked evaluation.

## Final rules

- Do not produce feasibility scores.
- Do not produce architectural-quality scores.
- Do not produce coverage, novelty, coherence, alignment, efficiency, or robustness scores.
- Do not rank cases.
- Do not summarize which cases appear strongest.
- Preserve traceability with short evidence pointers to the relevant section/table/sentence.
- Process every run with exactly the same standard.
- Output only the canonicalized case records and optional run-metadata blocks. No cross-run interpretation or conclusions.

