# Step 02 — Pilot instructions (pure LLM, v0.1)

## Scope

Design architectural organizations for the Underwood Elementary School using **only** the supplied brief, complete space-program schedule, and project planning assumptions. No coding, search, external validators, CAD, CSP, geometry tools, other agents, or existing Massing Explorer documentation. Do not inspect benchmark/evaluation materials. This test concerns the proposals you can develop independently.

## Task

Develop **20 architectural organizations**, one at a time. Explore credible alternatives rather than small dimensional variants. Think about educational adjacencies, program grouping, circulation, stacking, architectural form, and feasibility. You may propose an unusual architectural organization if it is defensible. Do not invent new rooms or modify room areas/quantities without explicitly acknowledging the change.

For each of proposals **01–20**, produce exactly these fields:

- `proposal_id` (P01–P20)
- `concept_name`
- `strategy_summary` (the architectural organizational principle)
- `program_grouping` (all nine program departments distributed across exactly three masses; include any spanning masses or shared facilities explicitly)
- `spatial_relationships` (relative placement, adjacency, shared connections)
- `vertical_organization` (ground, second, and third levels; stacking and double-height voids)
- `massing_organization` (three mass identities, their spatial/physical relationship and approximate widths/lengths if justifiable)
- `circulation_logic` (entry, student/staff flow, accessible connections)
- `requirement_response` (response to each hard condition and preference; distinguish evidence from assumptions)
- `known_risks` (what may fail or remains uncertain)
- `stated_rationale` (the design reasoning you report, not a claimed record of internal computation)
- `difference_from_previous` (the significant difference from preceding proposals)
- `next_exploration_direction` (the next architectural principle you intend to test)

Only emit **one proposal at a time**. After each proposal, the experiment operator sends the fixed message `NEXT` until all 20 are complete. Do not use operator feedback or revise earlier proposals. If some requirement cannot be verified from available evidence, mark it **unverified** rather than assert compliance.

After P20, select **at most 10** proposals and return the selected proposals with the fields required in `docs/BENCHMARK.md` (plus `difference_from_previous` and `next_exploration_direction` in the exploration log only). Explain why you selected them, and mention missing directions or limitations you noticed. Do not claim exhaustive coverage.

## Project inputs

Read only the three attachments/inputs supplied with this prompt:
1. `Underwood_Elementary_Space_Summary_GSF_Tweaked.xlsx` (original room schedule; use the supplied plain-text transcription as an accessibility aid, not a replacement)
2. `underwood_3mass_brief.txt` (verbatim requirements)
3. `project.example.yaml` (planning assumptions, dimensions, tolerances)

Source room names, counts, and areas must be preserved. The prompt's explicit brief requirements override generic configuration hints. The spreadsheet's displayed NFA/GFA and independent configuration's area adjustment are both source facts; note any conflict rather than silently reinterpreting the data.

## Start

Return **P01 only**. No introductory list of 20 concepts, no scoring or comparison until the final selection.
