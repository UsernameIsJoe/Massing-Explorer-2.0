# LLM output format v3 (draft for Pilot 4)

Status: **draft for architect review**, 2026-10-29. Extends seed format v2.0 (`benchmarks/test-elementary-v0.1/seeds_v2/generation_inputs/CASE_FORMAT.md`).

## Why it changes

- Experiment 1 found that concept text carries topology, but **not**:
  - vertical organization (storeys, what sits at grade and at the top);
  - **special education's placement**, which the architect weights as a defining decision.
- The ceiling arm showed both can be written and read back, so the fix is to ask for them in words.
- The concept itself must stay an idea, not an inventory: Pilot 01 showed placement prose ruins it as a semantic signal. So the two missing traits get their own short fields instead of being forced into the concept.

## Fields per case, in writing order

Text comes before structure: decide the idea in words, then commit to the record. Forcing structure first is known to degrade LLM reasoning.

| # | Field | Rule | Changed from v2? |
|---|---|---|---|
| 1 | `case_id` | C01, C02, … | – |
| 2 | `name` | 3–7 words | – |
| 3 | `concept` | 35–70 words; the organizing spatial idea: roles of the parts and how they relate. Do not list departments by mass or floor. Do not restate requirements every scheme shares. No benefits | Same rules |
| 4 | `intent` | 20–40 words; aims, written as aims ("seeks to"), not results | – |
| 5 | `section_intent` | 20–40 words; **in words**, the vertical idea: which masses rise and which stay low, what is at grade and what is at the top, and why | **New** |
| 6 | `program_stance` | 20–40 words; **in words**, where the defining programs sit *relative to each other* and why: core academic, special education, administration, and the commons (gym and dining). Relations, not a mass-by-mass list | **New** |
| 7 | `key_moves` | 2–4 moves; each with `move_id`, `move`, `serves`, and 1–6 `decisions` that exactly reference `structure` | – |
| 8 | `structure` | masses `{mass_id, role}`, as many as the brief allows (3 in this brief); all 9 departments `{department_id, mass_ids: [one], occupied_floors}`; all 3 connections `{mass_a, mass_b, direct_link}` | – |
| 9 | `brief_response` | `main_tradeoff` (15–35 words), `preferences_given_up` from the 3 fixed ids | – |
| 10 | `unresolved` | Up to 4 short strings | – |
| 11 | `direction_response` | One sentence: how this case answers the direction it was given, or for unguided runs, how it differs from the existing cases | **New**; never embedded, hidden in any blind review |

**Removed:** the `commitments` module (detachable by design; the LLM's core commitments locked 9–12 of 12 decisions, so they did not mark a boundary) and `collection_differences` (not used).

## Output contract

- **One JSON object only:** `{"format": "v3", "cases": [ ... 5 cases ... ]}`. No prose outside it; a code fence around it is tolerated and stripped.
- **Schema:** `case.schema.json` v3, derived from v2 with the field changes above.
- **Exactly 5 cases per reply.** Each case answers its own direction when directions are given.
- **Hard rules** (MODEL_INPUT.md and the architect's added rules):
  - each department in exactly one mass;
  - administration on the ground floor;
  - gym and dining in the same mass, double height on floor 1;
  - at most 3 floors, contiguous;
  - core academic and gym in different masses;
  - custodial is never a mass of its own;
  - every mass stacks from the ground;
  - at least 753 SF per floor when a department spans floors.

## Validation (code, after every reply; no repair in the pilot)

1. Parse and schema check.
2. Word counts per field.
3. Every key-move reference matches `structure` exactly.
4. Hard rules.
5. `preferences_given_up` matches what code computes from the structure.
6. **Text–record agreement** (extractor from Experiment 1, llama3.1:8b): `section_intent` against computed storeys and levels; `program_stance` against computed placement of the defining programs; `concept` against computed topology. Each is reported as agreement per trait.

Invalid cases are kept and counted, never silently fixed: validity is a pilot outcome.

## What is embedded

See [EMBEDDING_VIEWS.md](EMBEDDING_VIEWS.md).
- **Embedded:** idea (`concept` + `intent`); moves (each `move` + `serves`); unresolved (each `unresolved` item).
- **Read by extraction, not embedded:** `section_intent` and `program_stance`.
- **Never embedded:** `direction_response` and `name`.

## Mass count

Taken from the brief. Format v3 does not fix it at 3, but axes-v1 and the gap cells still assume 3 (see EMBEDDING_VIEWS.md, last section).
