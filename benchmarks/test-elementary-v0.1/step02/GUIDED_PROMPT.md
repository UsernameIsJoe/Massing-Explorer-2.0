# Step 02 — Guided architectural exploration prompt (A1, v0.1)

You are designing **a test elementary school**. Use the supplied design brief, space program, and planning assumptions. No external tools or additional information will be provided.

**Goal: Find the strongest architectural proposals you can**, while deliberately examining a broad range of substantially different program and massing organizations.

Develop **20 distinct architectural proposals sequentially**, one per response. Consider alternative program groupings, spatial relationships, stacking patterns, massing forms, circulation, and feasible dimensional arrangements rather than producing superficial variants. Do not change room quantities or floor areas; flag any uncertainty rather than claiming unverified compliance.

For each proposal P01–P20, report:
- `proposal_id` (P01 to P20)
- `concept_name` and `strategy_summary`
- `program_grouping`: distribute the nine departments across three masses, noting any split department
- `spatial_relationships` and `circulation_logic`
- `vertical_organization`: levels and double-height spaces
- `massing_organization`: the three masses, their arrangement, and approximate dimensions if justified
- `requirement_response`: hard constraints versus preferences; what has and has not been demonstrated
- `known_risks`
- `stated_rationale`: your stated design justification, not a claimed transcript of hidden reasoning
- `difference_from_previous`: why this differs materially from earlier proposals
- `next_exploration_direction`: which alternative organizational principle you plan to test next

Return **P01 only** now. On each subsequent `NEXT` message, return the next proposal without revising or repeating earlier proposals or requesting feedback.

After P20, await the operator's `SELECT` message. Select **no more than 10** of the P01–P20 proposals, rank your strongest recommendation first, identify it as the single **best proposal**, explain trade-offs and any important design alternatives you left unexplored. The complete transcript preserves all intermediate proposals.
