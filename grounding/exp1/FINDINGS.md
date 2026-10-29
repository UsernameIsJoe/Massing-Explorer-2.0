# Experiment 1 findings: per-axis grounding map (pilot, 15 seeds)

Date: 2026-10-29. Protocol: `PROTOCOL.md`. Raw: `responses.jsonl` (630 calls). Scores: `results.json`.

## Result in one line

The authored concept text carries **topology** (links between masses) well. It partly carries where **culturally named programs** sit (arts, library, office). It does not carry **storeys**, **vertical organization**, or where **special education** sits. The expressibility ceiling shows that all of these *can* be written and read back, so the gap is in what the concepts choose to say, not in the vocabulary.

## Extractor check

- qwen2.5:7b answered "not stated" on most questions, 56–100% of samples for placements. It also failed the ceiling, scoring 0.13–0.33 on links that were written explicitly, so it is unusable as an extractor.
- llama3.1:8b reached the ceiling on most traits. It reads text written to state the traits at 0.67–1.00 for links, storeys and most placements. **The map below uses llama only.**
- Deviation from the protocol: the locked rule averaged both models, which marks every axis "uncarried" because of qwen's refusals. The llama-only reading is a post-hoc decision forced by the extractor check, and is labelled as such.

## Grounding map (llama3.1:8b, modal answer over 3 prompts × 5 samples)

| Axis | Questions: accuracy on authored text (κ) | Ceiling (text written to state traits) | Reading |
|---|---|---|---|
| Topology | L–X 1.00 (1.00); L–C 0.67 (0.41); C–X 0.67 (0.31) | 0.73–1.00 | **Carried** to partly carried. Matches the Mantel result: topology was the only axis tracked by all four encoders |
| Program organization | arts 0.67, library 0.53, office 0.40; special education 0.13, medical 0.20, custodial 0.07 | 0.47–0.93 | **Partial.** Named public programs carried; special education, medical and custodial mostly "not stated" (56–88%) |
| Heights (storeys per mass) | learning 0.40, commons 0.67, third 0.20; below the majority baseline | 0.73–1.00 | **Uncarried** by authored text, but expressible |
| Vertical organization (ground or upper) | 0.13–0.47 except core academic (0.87, at or below majority 0.93) | 0.27–0.93 | **Uncarried**; partly hard even to express (library level, ceiling 0.27) |
| Distribution balance (derived) | not computable: placements often "not stated" | n/a | **Uncarried** |

**Part A (Mantel, 4 encoders, concept + intent).**
- Topology: ρ 0.19–0.40, p ≤ 0.025 in all four encoders.
- Height articulation: ρ 0.37–0.43 in mxbai and nomic only.
- Program and vertical organization: weak or not significant.

## Caveats

- 15 seeds hold about 8 distinct ideas.
- κ is unstable when one answer dominates the key. Several level questions have a majority baseline of 0.93–1.00, so their κ is near 0 by construction.
- Accuracy against the majority baseline is the safer reading for those.
- One small extractor; a frontier extractor might read more inference out of the text.

## Implication for plan step 2 (generation prompt)

The semantic side already grounds topology. The traits that matter but are missing from authored concepts are:
- vertical intent: which masses are tall or low, and what is at grade or at the top;
- special education placement, a defining move in the architect's weights.

The next generation prompt should require the concept or intent to state these in words. Code then checks the stated words against the record. Medical and custodial placement stays free: low weight, and rarely meaningful to the idea.
