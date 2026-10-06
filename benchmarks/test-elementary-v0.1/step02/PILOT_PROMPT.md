# Step 02 — Pilot instructions (pure LLM, v0.1)

## Scope

Design architectural organizations for the a test elementary school using **only** the supplied brief, complete space-program schedule, and project planning assumptions. No coding, search, external validators, CAD, CSP, geometry tools, other agents, or existing Massing Explorer documentation. Do not inspect benchmark/evaluation materials. This test concerns the proposals you can develop independently.

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

After P20, await an instruction to select **at most 10** proposals. For each selected proposal, report all fields listed above through `stated_rationale`, plus `representation_gap` (an organizational idea you could not describe with your own current terms, if any). Explain why you selected them, and mention missing directions or limitations you noticed. Do not claim exhaustive coverage.

## Project inputs

Read only these two model-facing input files, supplied identically to each tested model:
1. `MODEL_INPUT.md` (verbatim design brief, background and neutral numeric planning assumptions)
2. `ROOM_PROGRAM.csv` (complete 41-row net area and quantity schedule)

The source Excel workbook and source config are retained by the experiment operator for independent audit; they are not additional model input.

Source room names, counts, and areas must be preserved. The prompt's explicit brief requirements override generic configuration hints. The spreadsheet's displayed NFA/GFA and independent configuration's area adjustment are both source facts; note any conflict rather than silently reinterpreting the data.

## Start

Return **P01 only**. No introductory list of 20 concepts, no scoring or comparison until the final selection.
