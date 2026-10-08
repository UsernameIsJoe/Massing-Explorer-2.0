# Massing gallery geometry

## Correction — intended constraint mismatch (2026-10-08)

Batch 01 generation and scoring omitted the intended hard prohibition on splitting a department across masses. The original evaluator additionally allowed academic/special education in “a mass or masses.” Under the user-confirmed intended rule, R01, R03, R06, R07, R08, R10 and R12 violate cross-mass assignment; R02, R04, R05, R09 and R11 pass this check only. These are retrospective intended-rule annotations, not evidence that generators disobeyed a supplied instruction. Original scores/PASS labels remain historical judgments, not verified compliance with the intended benchmark. Matched-constraints LLM-versus-ME feasibility and quality conclusions are withdrawn. See [constraint audit](../../../CONSTRAINT_ALIGNMENT_AUDIT.md).


12 LLM final proposals and all 37 legal archive candidates from the frozen pipeline rerun. These are massing envelopes, not independently verified room layouts. OBJ units: feet; Z up. No Fable quality scores have been assigned to pipeline candidates.

LLM: envelope dimensions and program text from the original proposals. Placement is a diagrammatic reconstruction of narrative relationships. Exact rotation, joints and coordinates are not supplied for all schemes. Stepped upper floors are centered where their offset is unspecified. Heights use 14 ft per occupied floor and 28 ft hall volumes; missing heights are visualization assumptions. R09 contains an unresolved diagram/text interface conflict. No rooms or connection masses are invented.

Pipeline: pinned source commit 751ba24b0d2bcaeae5274eaffa589060c95ec0f9 in UsernameIsJoe/Massing-Explorer. Same program file and regression budgets as archived baseline. Rerun reproduced 209 attempts, 159 cells, 37 legal cells, same phase and P-pool counts. Each recovered snapshot was solved again with the frozen solver: ground dimensions match archived plates within 0.02 ft rounding; all returned solver validation checks pass. This is engine validation, not independent architectural feasibility certification. The saved baseline lacks individual geometry, so these files are recovered rerun output rather than original saved candidates.

Pipeline bars use arbitrary 24 ft presentation gaps. Heights follow the same 14 ft/28 ft convention; vertical volumes can contain double-height voids, and an envelope is not a count of occupied rooms. The engine's retained candidate is identified in data.json; the remaining candidates are archive alternatives, not 37 independently selected final designs. IDs ME01–ME37 are display identifiers in archive order, not quality ranks. The pipeline and LLM quality scores are not comparable until the pipeline receives the same independent rubric.

Open: download `massing-comparison.html` and open it in a browser. Geometry and source program summaries are embedded in the HTML. No server or API connection is required. GitHub's file viewer displays source rather than running HTML.

The separate model download contains 49 OBJ envelopes, data.json, recovered archive snapshots, solver results and export scripts. This repository directory contains the HTML gallery and these notes. Original scorer documents and hidden model reasoning are not included.


## Display consistency

Colors identify Mass A, B and C consistently; they do not classify program roles. All main and overview panels use one shared pixels-per-foot scale computed from every candidate and layout. Changing selection, rotation, elevation or view mode does not refit or resize schemes. View controls remain in a sticky dock during page scrolling. A 50 ft ruler appears in every view.



## Program split display

Display → Program split shows balanced schematic department blocks. LLM blocks indicate reported mass/floor membership; their sizes do not represent area shares. ME department areas are preserved, but positions can be reblocked for display. These are display adjustments, not revised solver results. The old Source program split option has been removed. Mass geometry, program assignments and original scores are unchanged.

## Fable rating radars

Every LLM case shows two separate radar graphs: four quality axes on 0–4 and eleven behavior axes on 0–3. Values are the unchanged locked Fable transcriptions. Unknown representation expansion (B10) is shown as a gap, never zero; the behavior plot remains unfilled with no line across that gap. Axis names and exact values are available in the UI. ME candidates are explicitly unrated by Fable; no engine scores are substituted. Quality identity exposure remains an audit limitation. The two score families are not combined.

