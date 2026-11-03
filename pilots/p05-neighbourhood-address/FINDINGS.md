# Pilot 5 findings: is a meaning neighbourhood a reliable address?

Date: 2026-11-03.
- Protocol: [PROTOCOL.md](PROTOCOL.md), declared and committed before computing.
- Results: `results/neighbourhoods_claude_v1.json`, from `scripts/neighbourhoods.py`.
- Reference families: `reference/families_claude_v1.json` (Claude's grouping; **architect reviewed 2026-11-03: generally agrees, no changes**).

## In one line

**Yes, with batch centring.** At the neighbourhood level the embedding is a usable address. It is stable to rewording, and once the writer/format offset is removed, it matches idea families closely. qwen3-embedding:4b reproduces the reference families almost exactly. Telling the LLM "do not rephrase these" did **not** keep it out of those ideas' neighbourhoods.

## Declared result: pass

By the declared choice rule (the first correction at which any encoder passes), the chosen correction is **raw**, and **mxbai** passes:
- 12 of 15 rewrites stay home;
- ARI 0.48 with the reference, p 0.0002.

That pass is at the bar. The same declared computation under centring is much stronger (below).

## Criteria 1 and 2, all encoders (silhouette k)

| Correction | Encoder | k | Rewrites staying home (bar 12) | ARI vs reference (bar 0.40) | Pass |
|---|---|---:|---:|---:|---|
| raw | mxbai | 4 | 12 | 0.48 | **yes** |
| raw | nomic | 3 | 12 | 0.05 | no |
| raw | qwen3 4b | 7 | 10 | 0.51 | no |
| raw | bge-m3 | 7 | 11 | 0.45 | no |
| centred | mxbai | 4 | 13 | 0.64 | **yes** |
| centred | nomic | 6 | 10 | 0.56 | no |
| centred | qwen3 4b | 6 | **14** | **0.88** | **yes** |
| centred | bge-m3 | 4 | 14 | 0.57 | **yes** |

All permutation p values for the passing rows are ≤ 0.0002. At k = 6 (the number of reference families), centred bge-m3 keeps all 15 rewrites home (ARI 0.72).

**Centred qwen3 4b, neighbourhoods against the reference:**

| Neighbourhood | Members | Reference family |
|---|---|---|
| 0 | E02, E05, E09, E15 | F3 linked cluster around a court: exact |
| 1 | E03, E11, E12 | F2 civic hinge chain: exact |
| 3 | E06, E07, E13 | F1 commons heart: exact |
| 4 | E04 | F5 one block, service hinge: exact |
| 5 | E08, E14 | F4 detached campus, without E10 |
| 2 | E01, E10 | F6 low learning beside civic tower, plus E10 |

The only disagreement is E10 ("twin bars and freestanding hall"), which the reference had already flagged as borderline.

## Criterion 3: encoders agree once centred

| Pair | Raw ARI | Centred ARI |
|---|---:|---:|
| mxbai · nomic | 0.30 | 0.74 |
| mxbai · qwen3 | 0.35 | 0.67 |
| mxbai · bge-m3 | 0.49 | 0.59 |
| nomic · qwen3 | 0.09 | 0.59 |
| nomic · bge-m3 | 0.07 | 0.54 |
| qwen3 · bge-m3 | 0.59 | 0.54 |

Raw neighbourhoods depend on the encoder; centred neighbourhoods largely agree. Centring removes the same writer/format offset that broke the Pilot 4 yardstick.

## Criterion 4: preview of J vs A (no decision)

For each of the 10 axis gaps shared by A and J: did the case land in the neighbourhood of a seed that J was told "do not rephrase"?

| Correction | Encoder | A in the avoided neighbourhood | J in the avoided neighbourhood |
|---|---|---:|---:|
| raw (declared) | mxbai | 5 | 5 |
| raw (declared) | nomic | 9 | 9 |
| raw (declared) | qwen3 4b | 3 | 4 |
| centred (post hoc) | mxbai | 3 | 6 |
| centred (post hoc) | nomic | 2 | 3 |
| centred (post hoc) | qwen3 4b | 5 | 3 |

- The raw preview is degenerate: without centring, the 40 cases collapse into one or two neighbourhoods (nomic puts all 40 in one), because they come from a different writer and format than the archive.
- Centred (post hoc, labelled as such): **no sign that J avoided the named ideas better than A.** The direction even flips between encoders.
- **Reading:** a one-shot "do not rephrase X" note does not move the LLM away from X's idea. This is the "J = A" risk in the key highlights, observed. The guidance has to do more than name ideas to avoid. The obvious next step is feedback: tell the LLM which neighbourhood it actually landed in, as LLM-Modulo does with its critics. 10 pairs only.

## What this means for the joint map

1. **The meaning address works at neighbourhood level,** so the map's meaning coordinate is viable. Proposed encoder: **qwen3-embedding:4b with batch centring.** It is the best on both criteria and is already installed. bge-m3 is the alternative. Since novelty is now judged on the axes, the steering and mapping encoder no longer needs to be kept separate from a meaning judge.
2. **Centring is required, and it needs a design decision.** Here each batch was centred on its own mean (15 rewrites, 40 cases). In the loop, a round brings only about 5 cases, too few to estimate the offset. The offset has to be estimated per writer and format from a calibration set (for example, the existing rewrites and cases), not from each small round. This must be settled before map v0.
3. **Guidance by naming is too weak.** The map's "avoid" signal must reach the LLM with feedback, not as a one-time note.

## Limits

- The reference is Claude's grouping, reviewed and accepted by the architect without changes.
- 15 seeds in 6 families: ARI rests on a few groups. The silhouette k varies by encoder (3–7).
- The choice rule picked raw because it comes first. Recommending centred for the map is a reading, not the declared choice, and needs the architect's agreement.
- The preview is post hoc under centring, covers 10 pairs, and decides nothing.
