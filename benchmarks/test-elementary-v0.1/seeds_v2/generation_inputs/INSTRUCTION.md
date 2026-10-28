Attachments required: MODEL_INPUT.md, ROOM_PROGRAM.csv, CASE_FORMAT.md, case.schema.json.

Use only these supplied inputs and this instruction. Do not browse, run code or request external tools.

Propose exactly 5 architectural strategies for the supplied school brief. Each strategy starts from an organizing concept: the spatial idea a designer would sketch first. Develop the concept, then make the program, floor and connection decisions that implement it.

The five strategies should differ in their organizing concepts and in the consequential commitments that follow from them, not only in names, wording or renumbered masses. Use your own architectural reasoning to choose the concepts; no family list is prescribed. Do not rank the cases or select a winner.

Coherence matters more than variety. Within each case, the concept, intent, key moves, structure, commitments and trade-offs must all describe the same scheme. Before returning, check every case against this list and fix the scheme if any item fails:
1. Every key move's decisions match the structure exactly.
2. The concept does not mention a relationship the structure contradicts (for example a "central heart" that is not linked to the parts it is said to connect).
3. The intent follows from the concept and is not a generic benefit any scheme could claim.
4. Each core commitment protects a key move, and changing it would make a different scheme.
5. preferences_given_up matches what the structure actually does.
6. The concept names program groups only where they carry the idea and does not list departments by floor.

Follow the hard requirements as design intentions and do not relax them to create variety. A seed is not guaranteed feasible: if a commitment is unresolved or conflicts with the brief, keep it visible in `unresolved` rather than claiming compliance.

Stay at strategy level. Do not produce dimensions, floor areas by mass, geometry, preference scores or a claim that dimensional feasibility has been verified. Preserve the given program. No site geometry, orientation or access arrangement is supplied; do not invent it.

Return only one JSON object conforming to the attached CASE_FORMAT.md and case.schema.json, with case IDs S01 to S05 and a collection_differences summary.
