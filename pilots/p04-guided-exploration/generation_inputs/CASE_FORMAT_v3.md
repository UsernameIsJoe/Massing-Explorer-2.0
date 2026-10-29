# Case format v3.0

Each case is one coherent architectural strategy for the supplied brief, at strategy level: no dimensions, areas by mass, geometry or scores. MODEL_INPUT.md and ROOM_PROGRAM.csv are the authority for the brief and program.

**Write each case in the field order below: decide the idea in words first, then commit to the structure.** Every field must describe the same scheme.

Department codes:
- D01 core academic
- D02 special education
- D03 art and music
- D04 health and physical education (gym)
- D05 media center
- D06 dining and food service
- D07 medical
- D08 administration and guidance
- D09 custodial and maintenance

## Fields per case

1. **case_id**: C01 to C05.
2. **name**: 3–7 words.
3. **concept**: 35–70 words. The organizing spatial idea a designer would sketch first: the roles the parts play and how they relate (for example centralized, linear, clustered, stacked, layered, detached).
   - Name program groups only where they carry the idea.
   - Do **not** list departments by mass or floor.
   - Do **not** restate requirements every scheme shares.
   - Do not argue benefits.
4. **intent**: 20–40 words. What the scheme aims to achieve for students, staff, community use or operations, written as aims ("seeks to"), not results.
5. **section_intent**: 20–40 words, in words. The vertical idea: which masses rise and which stay low, what sits at grade and what sits at the top, and why.
6. **program_stance**: 20–40 words, in words. Where core academic, special education, administration and the commons (gym and dining) sit **relative to each other**, and why. State relations; do not list mass by mass.
7. **key_moves**: 2–4 moves. Each move has:
   - `move_id` (K1, …);
   - `move`: a short phrase;
   - `serves`: one sentence on what part of the concept or intent it carries;
   - `decisions`: 1–6 exact references to `structure`. Each is either `{"type": "placement", "department_id", "mass_id", "floors"}`, with `floors` equal to that department's full `occupied_floors`, or `{"type": "link", "mass_a", "mass_b", "direct_link"}`.
8. **structure**:
   - `masses`: `{mass_id, role}` for as many masses as the brief requires (this brief: three). IDs (M1, M2, M3) are arbitrary. `role` is 2–6 words naming what the mass is in the concept.
   - `departments`: all nine `{department_id, mass_ids: [one mass], occupied_floors}`. Ground = 1; floors contiguous.
   - `connections`: every pair of masses `{mass_a, mass_b, direct_link}`. `true` means a built connection (bridge, connecting passage, shared enclosed edge); shared grounds do not count.
9. **brief_response**:
   - `main_tradeoff`: 15–35 words.
   - `preferences_given_up`: from exactly these ids:
     - `arts_ground_floor`: art and music do not occupy floor 1;
     - `media_top_above_admin`: media is not on the top occupied floor of administration's mass, above it;
     - `three_floors`: at least one mass does not reach floor 3 (a double-height gym/dining volume on floor 1 counts as floors 1–2).
10. **unresolved**: up to four short strings. Name real unknowns or possible conflicts specific to this case, not generic checks.
11. **direction_response**: one sentence on how this case answers the direction it was given.

## Hard rules

These come from the brief, plus two rules the architect added.

- Each department is entirely in exactly one mass.
- Administration is on the ground floor.
- Gym and dining are in the same mass, double height from the ground floor.
- At most three floors.
- A department spans floors only on contiguous floors, with at least 753 SF of its program on each.
- Every mass stands from the ground.
- **Core academic and gym/dining are in different masses.**
- **Custodial is never a mass of its own.**

Intentions are hypotheses. Do not claim anything is verified or feasible. If a requirement cannot be met by the idea, keep the conflict visible in `unresolved`.

## Output

Return **only** one JSON object, `{"format": "v3", "cases": [five cases]}`, conforming to case.schema.v3.json. Write no text outside the JSON.
