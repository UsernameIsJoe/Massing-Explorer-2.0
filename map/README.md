# Joint map

The connecting space of the core contribution ([CORE_CONTRIBUTION § Key highlights](../docs/CORE_CONTRIBUTION.md#key-highlights-the-joint-map-and-the-exploration-loop-architect-2026-11-03)). Every idea has two addresses:
- a **meaning neighbourhood**;
- an **axis cell**.

The two are linked case by case. The map is versioned: each loop round (one LLM batch of about 5 proposals, located and added) makes a new version.

## v0 definitions (agreed with the architect, 2026-11-03)

**Items**
- 15 archive seeds and 40 Pilot 4 cases: text and structure, so both addresses.
- 1,050 Pilot 3 variants: structure only, so an axis address and no meaning address. A meaning address for text-free variants (anchor profiles) is untested and not in v0.

**Axis address** (computed by code, exact)
- The **cell** is link pattern (8) × which mass holds special education (learning L, commons C, third X) × height profile (all three-storey / mixed / mostly low), 72 cells in all. It is the Pilot 4 coarse cell, `pilots/p04-guided-exploration/scripts/directions.py`.
- The full structural state is stored too.

**Meaning coordinates** (qwen3-embedding:4b; the other encoders are stored for checks)

| Coordinate | Definition | Use |
|---|---|---|
| **Neighbourhood** (main address) | Cluster label on the combined vector. Concept and intent are each centred by their writer/format batch mean and normalised, then concatenated ÷ √2, so cosine similarity is the mean of the concept and intent similarities. Agglomerative clustering, average linkage, cosine; k by best silhouette over 3–12 | Map rows; journey record; saturation |
| **Concept similarity** | Continuous, centred concept vectors | "Same idea" |
| **Intent similarity** | Continuous, centred intent vectors | "Same purpose" |
| Joint vector (concept + intent as one text) | Stored | Cross-check only |

- **Batch centring.** Each writer/format batch uses its own stored mean: archive (seed format v2) and Pilot 4 cases (format v3.1). A future small round is centred with its format's stored mean, not its own.
- **"Same idea, different purpose":** concept similarity in the top 10% of all pairs and intent similarity at or below the median. The reverse is "same purpose, different idea".
- **Versions.** Neighbourhoods are re-clustered at every version. Labels carry forward by matching each new cluster to the old one with the largest overlap.

**How the two spaces are connected in v0**
1. **Co-location:** the table of neighbourhoods against cells, filled by real items.
2. **Consistency:** per case, extractor agreement between text and record (Pilot 4, format v3.1). Not available for seeds.
3. **Neighbourhood footprints:** for each neighbourhood and trait, whether its members **fix** the trait (the modal value holds for ≥ 80% of at least 4 members) or leave it **free**. Fewer than 4 members means "too few". Traits:
   - link pattern;
   - special education's mass;
   - height profile;
   - the masses of administration, art and music, and media.
4. The key-move bridge (move types) is the next test after v0, not part of it.

**Checks built into v0**
- Archive items keep matching both reference families (ARI ≥ 0.40).
- Neighbourhoods mix seeds and cases rather than splitting by batch, which shows that centring removed the format offset.

## Files
- `build_map.py`: builds `v0/map_v0.json`.
- `render_view.py`: builds `v0/map_v0_view.html`, a readable view for review.
