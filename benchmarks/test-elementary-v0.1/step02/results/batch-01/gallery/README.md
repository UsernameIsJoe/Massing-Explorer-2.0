# Massing gallery geometry

12 LLM final proposals and all 37 legal archive candidates from the frozen pipeline rerun. These are massing envelopes, not independently verified room layouts. OBJ units: feet; Z up. No Fable quality scores have been assigned to pipeline candidates.

LLM: envelope dimensions and program text from the original proposals. Placement is a diagrammatic reconstruction of narrative relationships. Exact rotation, joints and coordinates are not supplied for all schemes. Stepped upper floors are centered where their offset is unspecified. Heights use 14 ft per occupied floor and 28 ft hall volumes; missing heights are visualization assumptions. R09 contains an unresolved diagram/text interface conflict. No rooms or connection masses are invented.

Pipeline: pinned source commit 751ba24b0d2bcaeae5274eaffa589060c95ec0f9 in UsernameIsJoe/Massing-Explorer. Same program file and regression budgets as archived baseline. Rerun reproduced 209 attempts, 159 cells, 37 legal cells, same phase and P-pool counts. Each recovered snapshot was solved again with the frozen solver: ground dimensions match archived plates within 0.02 ft rounding; all returned solver validation checks pass. This is engine validation, not independent architectural feasibility certification. The saved baseline lacks individual geometry, so these files are recovered rerun output rather than original saved candidates.

Pipeline bars use arbitrary 24 ft presentation gaps. Heights follow the same 14 ft/28 ft convention; vertical volumes can contain double-height voids, and an envelope is not a count of occupied rooms. The engine's retained candidate is identified in data.json; the remaining candidates are archive alternatives, not 37 independently selected final designs. IDs ME01–ME37 are display identifiers in archive order, not quality ranks. The pipeline and LLM quality scores are not comparable until the pipeline receives the same independent rubric.

Open: download `massing-comparison.html` and open it in a browser. Geometry and source program summaries are embedded in the HTML. No server or API connection is required. GitHub's file viewer displays source rather than running HTML.

The separate model download contains 49 OBJ envelopes, data.json, recovered archive snapshots, solver results and export scripts. This repository directory contains the HTML gallery and these notes. Original scorer documents and hidden model reasoning are not included.


## Display consistency

Colors identify Mass A, B and C consistently; they do not classify program roles. All main and overview panels use one shared pixels-per-foot scale computed from every candidate and layout. Changing selection, rotation, elevation or view mode does not refit or resize schemes. View controls remain in a sticky dock during page scrolling. A 50 ft ruler appears in every view.


## Program split display

Choose **Display → Program split** for all 12 LLM proposals and all 37 ME candidates. The same nine department colors apply throughout. For LLM cases, equal-width bands encode documented mass/floor membership only; they do not encode area shares or exact room placement. For ME candidates, colored pieces use the recovered solver's department footprints and gross allocations. The camera and scale are unchanged by this switch. R11 B L2 has no scheduled program; R12's medical department is shown in C L1 following area accounting, with its contradictory narrative location explicitly marked.
