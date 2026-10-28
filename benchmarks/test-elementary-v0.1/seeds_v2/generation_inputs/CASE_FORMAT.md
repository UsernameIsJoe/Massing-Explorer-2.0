# Generator case format v2.0

Each case is one coherent architectural strategy for the supplied brief, recorded at strategy level: no dimensions, areas by mass, geometry or scores. MODEL_INPUT.md and ROOM_PROGRAM.csv are the authority for the brief and program.

Write each case in the field order below. **Decide the concept first, then derive the structure from it.** Every field must describe the same scheme: a reader comparing any two fields must find them consistent.

Department codes: D01 CORE ACADEMIC · D02 SPECIAL EDUCATION · D03 ART & MUSIC · D04 HEALTH & PHYSICAL EDUCATION · D05 MEDIA CENTER · D06 DINING & FOOD SERVICE · D07 MEDICAL · D08 ADMINISTRATION & GUIDANCE · D09 CUSTODIAL & MAINTENANCE.

## Fields per case

1. **case_id**: S01, S02, …
2. **name**: 3–7 words.
3. **concept**: 35–70 words. The organizing spatial idea a designer would sketch first: the roles the parts play (for example a civic front, learning wings, a shared heart, a service spine, separate pavilions) and how they relate (centralized, linear, clustered, stacked, layered, detached). You may name program groups when they carry the idea. Do **not** list departments by mass or floor; the structure does that. Do **not** restate requirements every scheme shares (for example that gym and dining are together and double height). Do not argue benefits here.
4. **intent**: 20–40 words. What the scheme is trying to achieve for students, staff, community use or operations, written as aims ("aims to", "seeks to"), not as achieved results.
5. **key_moves**: 2–4 moves. Each move:
   - `move_id`: K1, K2, …
   - `move`: a short phrase naming the design move.
   - `serves`: which part of the concept or intent the move carries (one sentence).
   - `decisions`: 1–6 references to facts in `structure`, each either
     - `{"type": "placement", "department_id": "D04", "mass_id": "M1", "floors": [2, 3]}`, where `floors` equals that department's full `occupied_floors`, or
     - `{"type": "link", "mass_a": "M1", "mass_b": "M2", "direct_link": true}`, matching that pair's connection.
   Every reference must match `structure` exactly. Together the moves should account for the decisions that make this scheme different from the others.
6. **structure**:
   - `masses`: exactly three `{mass_id, role}`. IDs (M1, M2, M3) are arbitrary local labels. `role` is 2–6 words naming what the mass is in the concept (for example "civic front"), not a list of its contents.
   - `departments`: all nine `{department_id, mass_ids, occupied_floors}`. `mass_ids` lists exactly one mass. `occupied_floors` lists every occupied level (ground = 1), contiguous.
   - `connections`: every pair of masses `{mass_a, mass_b, direct_link}`: true for a proposed built connection (bridge, connecting passage, shared enclosed edge), false for none (shared grounds or outdoor walking do not count), null only if genuinely unresolved.
7. **commitments** (separate module):
   - `core`: 2–4 items `{statement, protects}`. `statement` says what must stay true for this to remain the same strategy; `protects` lists the move_ids it protects. Changing a core commitment produces a different strategy.
   - `flexible`: 2–4 short strings naming aspects that could change without changing the strategy.
   Nothing outside this block may refer to it.
8. **brief_response**:
   - `main_tradeoff`: 15–35 words naming the consequential sacrifice or tension.
   - `preferences_given_up`: the brief preferences this scheme does not meet, from exactly these ids (empty list if none):
     - `arts_ground_floor`: art and music do not occupy floor 1.
     - `media_top_above_admin`: media is not on the top occupied floor of the same mass as administration, above it.
     - `three_floors`: at least one mass does not reach floor 3 (a double-height gym/dining volume starting on floor 1 counts as floors 1–2).
9. **unresolved**: up to four short strings: unknowns, possible requirement conflicts, checks needed at dimensional realization. Empty list permitted.

## Collection

- `collection_differences`: up to 120 words on the consequential differences across the cases, in concept terms first, then structure.

## Rules

- All hard requirements in MODEL_INPUT.md apply, including: each department entirely in exactly one mass; administration on the ground floor; gym and dining in the same mass; at most three floors.
- Use null only for genuinely unresolved structure values, and explain each in `unresolved`. Do not use null to avoid deciding.
- Intentions and expected benefits are hypotheses. Do not claim that anything is verified or feasible.
- If you find an inconsistency between fields while writing, fix the scheme so all fields agree. If a requirement cannot be met by the concept, keep the conflict visible in `unresolved`.
- The attached case.schema.json specifies the syntax. Schema validity is not a feasibility certificate.
