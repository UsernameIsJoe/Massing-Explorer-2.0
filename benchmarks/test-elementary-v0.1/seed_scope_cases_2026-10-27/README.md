# Five parent seeds and ten A/B additions

These are the existing October 27 proof-check records, not newly generated or repaired cases.

## Open these files
- cases/parents_05.json: five original parents, S01–S05 (analysis IDs 05-S01–05-S05).
- cases/additions_A.json: five ordinary LLM-broadening additions, E01–E05 (analysis IDs A-E01–A-E05).
- cases/additions_B.json: five code-gap-guided LLM additions, E01–E05 (analysis IDs B-E01–B-E05).
- cases/all_15_cases.json: combined records with collection labels.

Both expansion arms used the same five parents. B did not use A as its parent set. B still used LLM generation.

## Were these before or after the no-cross-mass correction?
These belong to the corrected proof-check protocol, not the earlier Batch 01 with the omitted rule. All three saved, self-contained generation messages include MODEL_INPUT v0.2 and explicitly say:

> Each of the nine departments must be assigned entirely to exactly one principal mass. Splitting any department across masses is prohibited, including custodial/maintenance and individual support rooms.

The full messages, including embedded attachments, are in generation_inputs/. Their MODEL_INPUT blocks match the frozen protocol. All 135 department entries in these 15 records assign exactly one mass. This does not prove geometric feasibility, floor-area compliance or room-level realization. The preserved messages verify the prepared generation inputs; an independent export of the Claude sessions is unavailable.

## Where they lived
The originals were returned as uploaded Pasted text(2).txt (parents), Pasted text(4).txt (A), and Pasted text(5).txt (B). They were retained in project handoff/report packages. The GitHub findings update published analytical findings rather than these underlying raw responses. The documentation cleanup did not delete or move these case records.

raw/ preserves received text as supplied by the current original-file read, including Markdown fences for A/B. cases/ parses the JSON and reformats whitespace only; it was checked against the existing normalized run_05/run_A/run_B records. No semantic, axis or geometric supplementation was added.

Department IDs: D01 academic; D02 special education; D03 art/music; D04 physical education; D05 media; D06 dining/food service; D07 medical; D08 administration/guidance; D09 custodial/maintenance.
