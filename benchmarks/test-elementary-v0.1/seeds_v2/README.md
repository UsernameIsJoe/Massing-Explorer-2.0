# Seeds v2.0 — five fresh seeds with concepts

Record format and purposes: [docs/SEED_RECORD_SPEC.md](../../../docs/SEED_RECORD_SPEC.md).

## Files

- `GENERATION_MESSAGE.txt` — the complete, self-contained message to send to the generating model (instruction plus the four attachments embedded verbatim). Hashes in `SHA256.json`.
- `generation_inputs/` — the instruction and attachments the message was assembled from. `MODEL_INPUT.md` is v0.2, unchanged, including the whole-department-in-one-mass rule.
- `scripts/validate_seeds.py` — coherence and brief-rule checker (standard library only).

## Run

1. Open a fresh chat with the generating model, with no project files or memory.
2. Paste the whole of `GENERATION_MESSAGE.txt` and send it.
3. Save the JSON reply unchanged as `raw/seeds_received.txt`, and record the model, mode/effort, date and host in `raw/RUN.md`.
4. Parse it to `cases/seeds.json` and run `python scripts/validate_seeds.py cases/seeds.json`.
5. Review the report. Errors mean a record contradicts itself or the brief; do not repair it silently. Either record the defect or regenerate, and log which.
