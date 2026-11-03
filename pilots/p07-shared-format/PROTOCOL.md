# Pilot 7: does one shared writer and format make the map's meaning address work?

Declared 2026-11-03, before the re-expression is generated. Agreed with the architect the same day ("let's fix, so we are ready for the map").

## Why

Map v0 ([map/v0/NOTES.md](../../map/v0/NOTES.md)) found that meaning does not transfer between the archive seeds (seed format v2, earlier runs) and the Pilot 4 cases (format v3.1, ChatGPT), even after centring. The root is that the two sets of texts are not comparable. The loop will write format v3.1 with ChatGPT, so the fix is to re-express the 15 seeds in that same writer and format, then test whether the gap closes without the seeds losing their families.

**Process rule.**
- Task: Task 2 (embedding representation): the cross-batch comparability the map needs.
- Depends on: Pilots 5–6, done.
- Blocks: map v0.1.

## Inputs

1. `prompts/1_REEXPRESS_V31.txt` (built by code from the seed records). For each seed it gives:
   - name, concept, intent;
   - the key moves (move and serves);
   - the structure.

   It asks for the v3.1 text fields (concept, intent, section_intent, program_stance) of the same strategy. It runs in one ChatGPT temporary chat, medium effort, as in Pilot 4. The reply is saved raw; only formatting artefacts are removed.
2. Checks on the reply:
   - 15/15 IDs;
   - field lengths against the v3.1 rules;
   - word reuse against the originals (reported).
3. `local/RUN_P07.bat` on the architect's PC embeds the 15 new concepts and 15 new intents (30 texts) with the four installed encoders. No downloads.

## Representation

As decided for the map: concept and intent embedded separately and used together. Each is normalised; they are concatenated ÷ √2, so cosine similarity is the mean of the two.

**Encoders.** qwen3-embedding:4b is primary. A criterion passes only if it holds in qwen3 4b **and** at least one other encoder.

## Criteria

**C1: families preserved (the re-expression does not wash out differences).**
- Set: the 15 re-expressed seeds alone.
- Neighbourhoods: agglomerative clustering, average linkage, cosine; k by silhouette over 3–8.
- Pass: ARI against the idea families (`pilots/p05-neighbourhood-address/reference/families_claude_v1.json`) is at least 0.40, with permutation p < 0.05 (10,000 shuffles, seed 20261103).
- Reported: ARI against the purpose families.

**C2: the writer/format gap is closed.**
- Set: the 15 re-expressed seeds plus the 40 Pilot 4 cases, **uncentred**. If they share a writer and format, no correction should be needed.
- (a) **Nearest neighbours mix.** At least 8 of the 40 cases have a seed as their nearest neighbour. If batch played no role, about 11 would (40 × 15/54).
- (b) **Clusters do not follow the batch.** ARI between the clusters (k by silhouette over 3–12) and the seed/case label is at most 0.10.
- Both (a) and (b) must hold.

**Baseline with the original seeds, measured 2026-11-03 before this declaration (same method):**

| Encoder | Cases with a seed as nearest neighbour | ARI(clusters, batch) |
|---|---:|---:|
| qwen3 4b | 0/40 | 0.18 |
| mxbai | 0/40 | 0.81 |
| nomic | 1/40 | 0.24 |
| bge-m3 | 0/40 | 0.54 |

**Reported, not gated:**
- the keyword lean from map v0's notes (cases using a family's own words, against that family's centroid);
- each re-expressed seed's nearest original seed, which shows how far the re-expression moved in meaning across formats.

## Readings, fixed now

| Outcome | Reading | Next |
|---|---|---|
| C1 and C2 pass | One writer and format makes the address work | Map v0.1: the re-expressed seeds become the archive text; all items share one format; anchored families (fix B) |
| C1 fails | The re-expression washes out the seeds' differences | Keep the original seeds as families. Re-express with a different instruction, or rethink the archive |
| C1 passes, C2 fails | The gap is not format alone: the writer, or the directed prompts, separate the cases | Rethink before any map. Candidates: generate the archive and the loop in one prompt context, or treat batches as separate layers |

## Limits

- One re-expression batch from one model.
- 15 seeds.
- The cases were written under directed prompts that pushed them away from the archive, so some real distance is expected even with a shared format. C2's bar (8, below the 11 expected with no batch effect) allows for that.
