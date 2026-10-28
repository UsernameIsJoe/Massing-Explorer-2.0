# Seed record specification — draft v2.0

Status: **draft for review**, 2026-10-28. Replaces generator case format v1.0 for future Step 02 runs only. Existing seed records keep v1.0.

## Why this revision

Pilot 01 embedded the v1.0 `organizing_principle` and `main_tradeoff` text. Those fields mostly restated placements ("special education on floor 2, media on top"), so they duplicated the structure instead of expressing a scheme's concept. v1.0 never asked the generating LLM for the concept, its intentions, or which commitments define the scheme. This revision asks for them at generation time, from the LLM that made the strategy.

## What a seed is for

A seed is one coherent strategic response to the brief. It must serve five later uses. Every field below exists for at least one of them; a field that serves none should be cut.

| Use | Step | Needs from the seed |
|---|---|---|
| **U1 Semantic space** | 03 | the scheme's concept and intention, in words, without restating the structure |
| **U2 Structural space** | 03 | explicit, checkable decisions: grouping, floors, links |
| **U3 Linking the two** | 03 | which decisions carry which part of the concept |
| **U4 Membership and variation** | 03 | what must stay fixed for the scheme to remain itself, and what may vary |
| **U5 Checking and later realization** | 03 onward | trade-offs against the brief and what remains unresolved |

## Fields

Order matters: the LLM writes the concept **before** the structure, so the structure implements the concept rather than the concept summarizing the structure.

### 1. `name` — label
3–7 words. A recognizable handle for people. Serves: navigation only; not embedded.

### 2. `concept` — the organizing idea (U1)
40–70 words. The spatial idea of the scheme in architectural terms: the roles the parts play (civic front, learning wing, shared heart, service spine, campus pavilions), how they relate (centralized, linear, clustered, stacked, layered, detached), and the overall diagram a designer would sketch first.

- **May** name program groups when they carry the idea ("the public programs form an entrance mass").
- **Must not** enumerate departments by mass or floor. That is the structure's job.
- **Must not** argue benefits; that is `intent`.

Example register (not templates): "Public programs are isolated as an entrance mass, with focused academic wings attached to one side and a service yard behind." / "A central public space anchors the plan; every program has direct access to it and to each other through it."

### 3. `intent` — what the scheme is trying to achieve (U1, U4)
20–40 words. The purposes the concept serves: for students, staff, community use, operations or the brief's tensions. Written as intentions, not claimed outcomes ("aims to", not "achieves").

### 4. `key_moves` — the bridge from concept to decisions (U3, U4)
2–4 moves. Each move is:
- `move`: one short phrase ("lift assembly above a civic plinth").
- `serves`: which part of the concept or intent it carries.
- `decisions`: the structural facts it consists of, as references (department IDs, mass labels, links), e.g. `["D04,D06 on floors 2-3 in M1", "D07,D08,D09 on floor 1 in M1"]`.

This is the explicit many-to-many link between meaning and structure. It is what lets a later variation keep a move's purpose while changing how it is implemented.

### 5. `structure` — explicit decisions (U2, U5)
Unchanged from v1.0 in content: `masses` (`mass_id`, `role`, a short role label, not a placement list), `departments` (all nine: `department_id`, `mass_ids`, `occupied_floors`), `connections` (every pair: `direct_link` true/false/null). This is the supporting record that the grey structure line and diagrams are drawn from.

### 6. `commitments` — what defines the scheme (U4)
- `core`: 2–4 statements that must remain true for this to still be the same strategy. Each names the move it protects. Changing one yields a different strategy.
- `flexible`: 2–4 aspects that could change without changing the strategy (e.g. "which floor media occupies", "whether medical sits with administration or the support house").

This is the seed's own statement of its boundary. Step 03 membership and variation start from it instead of inventing it.

### 7. `brief_response` — trade-offs against the brief (U5)
- `main_tradeoff`: 15–35 words, the consequential sacrifice or tension.
- `preferences_given_up`: list of brief preferences the scheme does not meet (e.g. "three floors in every mass"), empty if none.

### 8. `unresolved` — open questions (U5)
Up to four items: unknowns, possible requirement conflicts, checks needed at realization. Unchanged from v1.0 `unresolved_notes`.

### Collection-level
`collection_differences` (up to 120 words): the consequential conceptual differences across the set, stated in concept terms first, structure second.

## Rules that make the fields usable

1. **Concept and structure must agree.** Every `key_moves.decisions` entry must match `structure`. A reviewer (or code, for the references) checks this; a mismatch is recorded, not silently fixed.
2. **No restating across fields.** `concept` does not list placements; `intent` does not describe the diagram; `structure` carries no prose rationale.
3. **Intentions are hypotheses.** Nothing in `intent`, `key_moves` or `commitments` is treated as a demonstrated effect.
4. **Nulls stay nulls.** Unresolved structural values remain `null` with a note; no defaults are filled in later.
5. **Hard requirements as before.** The v0.2 model input, including the whole-department-in-one-mass rule, is unchanged.

## What gets embedded (Pilot 01b and later)

- Concept embedding: `concept` alone.
- Concept-plus-intent embedding: `concept` + `intent`.
- Not embedded as semantics: `structure` (it has its own distance), `name`, `unresolved`.

## Open choices for review

1. Is `commitments` (core vs flexible) worth asking for at generation, or should Step 03 derive it? It is the most useful field for membership but the hardest for the LLM to do well.
2. Should `key_moves.decisions` reference structure strictly (IDs only), or allow short prose?
3. Word ranges for `concept` (40–70) and `intent` (20–40).
4. Seed count for the new generation round (five keeps continuity with Pilot 01).
