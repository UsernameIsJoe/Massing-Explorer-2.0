# Seed record specification — draft v2.0

Status: **adopted for seeds_v2**, 2026-10-28 (review decisions recorded below). Replaces generator case format v1.0 for future Step 02 runs only. Existing seed records keep v1.0.

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
35–70 words. The spatial idea of the scheme in architectural terms: the roles the parts play (civic front, learning wing, shared heart, service spine, campus pavilions), how they relate (centralized, linear, clustered, stacked, layered, detached), and the overall diagram a designer would sketch first.

- **May** name program groups when they carry the idea ("the public programs form an entrance mass").
- **Must not** enumerate departments by mass or floor. That is the structure's job.
- **Must not** argue benefits; that is `intent`.
- **Must not** restate requirements every scheme shares (gym and dining together and double height, for example). Shared boilerplate pulls every embedding toward the others.

Example register (not templates): "Public programs are isolated as an entrance mass, with focused academic wings attached to one side and a service yard behind." / "A central public space anchors the plan; every program has direct access to it and to each other through it."

### 3. `intent` — what the scheme is trying to achieve (U1, U4)
20–40 words. The purposes the concept serves: for students, staff, community use, operations or the brief's tensions. Written as intentions, not claimed outcomes ("aims to", not "achieves").

### 4. `key_moves` — the bridge from concept to decisions (U3, U4)
2–4 moves. Each move is:
- `move`: one short phrase ("lift assembly above a civic plinth").
- `serves`: which part of the concept or intent it carries.
- `decisions`: the structural facts it consists of, as strict references that code can check: `{"type": "placement", "department_id", "mass_id", "floors"}` (floors equal the department's full occupied floors) or `{"type": "link", "mass_a", "mass_b", "direct_link"}`.

`move` and `serves` stay prose for people and for meaning; `decisions` stays strict for checking. This also separates the two kinds of lock from the Step 02–03 plan: a semantic lock keeps `serves`, an implementation lock keeps `decisions`.

This is the explicit many-to-many link between meaning and structure. It is what lets a later variation keep a move's purpose while changing how it is implemented.

### 5. `structure` — explicit decisions (U2, U5)
Unchanged from v1.0 in content: `masses` (`mass_id`, `role`, a short role label, not a placement list), `departments` (all nine: `department_id`, `mass_ids`, `occupied_floors`), `connections` (every pair: `direct_link` true/false/null). This is the supporting record that the grey structure line and diagrams are drawn from.

### 6. `commitments` — what defines the scheme (U4), optional module
- `core`: 2–4 statements that must remain true for this to still be the same strategy. Each names the move it protects. Changing one yields a different strategy.
- `flexible`: 2–4 aspects that could change without changing the strategy (e.g. "which floor media occupies", "whether medical sits with administration or the support house").

This is the seed's own statement of its boundary. Step 03 membership and variation start from it instead of inventing it.

It is a **detachable module**: no other field refers to it, the schema does not require it, and `validate_seeds.py --no-commitments` ignores it. It can be dropped later without regenerating seeds.

### 7. `brief_response` — trade-offs against the brief (U5)
- `main_tradeoff`: 15–35 words, the consequential sacrifice or tension.
- `preferences_given_up`: ids from a fixed list (`arts_ground_floor`, `media_top_above_admin`, `three_floors`), each defined in CASE_FORMAT v2.0 so code can derive it from the structure and compare.

### 8. `unresolved` — open questions (U5)
Up to four items: unknowns, possible requirement conflicts, checks needed at realization. Unchanged from v1.0 `unresolved_notes`.

### Collection-level
`collection_differences` (up to 120 words): the consequential conceptual differences across the set, stated in concept terms first, structure second.

## Rules that make the fields usable

1. **One scheme per record.** Every field must describe the same scheme. Checked in three layers:
   - **Generator self-check:** the generation instruction makes the LLM check six coherence items before returning.
   - **Code** (`seeds_v2/scripts/validate_seeds.py`): key-move references against structure, hard rules (one mass per department, admin at grade, gym with dining, floors 1–3, contiguity, 753 SF per floor portion), connections complete, commitments pointing at real moves, stated preferences against structure, concept length, enumeration, floor mentions and shared boilerplate.
   - **Reviewer:** concept, intent and moves read against the diagram, for the semantic agreement code cannot judge.
   A mismatch is recorded, never silently fixed.
2. **No restating across fields.** `concept` does not list placements; `intent` does not describe the diagram; `structure` carries no prose rationale.
3. **Intentions are hypotheses.** Nothing in `intent`, `key_moves` or `commitments` is treated as a demonstrated effect.
4. **Nulls stay nulls.** Unresolved structural values remain `null` with a note; no defaults are filled in later.
5. **Hard requirements as before.** The v0.2 model input, including the whole-department-in-one-mass rule, is unchanged.

## What gets embedded (Pilot 01b and later)

- Concept embedding: `concept` alone.
- Concept-plus-intent embedding: `concept` + `intent`.
- Not embedded as semantics: `structure` (it has its own distance), `name`, `unresolved`.

## Review decisions (2026-10-28)

1. `commitments`: kept, as a detachable module.
2. `key_moves`: prose `move`/`serves` plus strict `decisions` references.
3. Lengths: concept 35–70 words, intent 20–40. About 55–95 tokens for a concept and about 150 for concept plus intent, within every Pilot 01 encoder's limit (the tightest, mxbai, takes 512 tokens). Shorter than about 30 words drifts toward generic school language; longer than about 100 averages several ideas into one vector. A full five-seed response is about 2,000 words, one ordinary chat response.
4. Seeds: five fresh seeds under v2.0, generated by the user's advanced model from `seeds_v2/GENERATION_MESSAGE.txt`.
