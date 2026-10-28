# Pilot 01 — representation

Tests whether embeddings of strategy descriptions rank strategic similarity the way an architect does. Protocol, gate and frozen settings: [PILOT_01_PROTOCOL.md](PILOT_01_PROTOCOL.md).

## Folder

- `scripts/render_descriptions.py` — builds `data/descriptions.jsonl` from the 15 frozen cases (deterministic, no LLM).
- `scripts/build_triplets.py` — builds `data/triplets_SEALED.json` and the blind `data/labeling_set.json`.
- `scripts/run_embeddings.py` — embeds all texts with local Ollama encoders into `runs/`.
- `scripts/score_triplets.py` — scores encoders, proxies and the LLM baseline against the labels into `results/scores.json`.
- `scripts/build_diagram_data.py` — builds `data/diagram_data.json`, the schematic diagram specs for real cases.
- `scripts/build_labeling_page.py` — assembles `labeling/labeling_page.html` from the template and data files.
- `labeling/` — the labeling page (published as a private artifact).
- `llm_baseline/PROMPT.md` — the one-batch LLM comparison.

All scripts use the Python standard library only.

## Rebuild the inputs

```
cd pilots/p01-representation
python scripts/render_descriptions.py ../../benchmarks/test-elementary-v0.1/seed_scope_cases_2026-10-27/cases/all_15_cases.json data
python scripts/build_triplets.py ../../benchmarks/test-elementary-v0.1/seed_scope_cases_2026-10-27/cases/all_15_cases.json data/descriptions.jsonl data/probes.json data
```

Both are deterministic; a rebuild must reproduce the committed hashes in `data/descriptions_manifest.json` and the labeling-set hash in the protocol log.

## Run the embeddings (Windows)

```
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
ollama pull bge-m3
ollama pull qwen3-embedding:0.6b
cd pilots\p01-representation
python scripts\run_embeddings.py
```

Do not open `data/triplets_SEALED.json` before labeling is complete.

## One-click run (Windows)

Double-click `RUN_PILOT_01.bat`. It checks for Ollama and Python, pulls the four models, runs the embeddings and writes `runs/` plus `runs_console.txt`.
