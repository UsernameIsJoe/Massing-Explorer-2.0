# LLM baseline run, Pilot 01b

- Date: 2026-10-28
- Model: Claude Opus (claude-opus-5-5), separate subagent with a fresh context
- Input (v1): `data/labeling_set.json` only (SHA-256 `1a5e415925257a36129de3f8b03d04969b5e99462bae21eed0ed4523c693d7d2`), copied to an isolated folder; instructed to read no other file and not to use the web
- Output: `labels/llm_labels.json`, 16 answers
- Limitation: same model family as the seed generator; saw concept, intent and structure lines but no diagrams.

## v1.1 re-run

Re-run on `data/labeling_set_full.json` (Pass B display) so the baseline sees the same information as the labeler's Pass B; the earlier answers are kept as `labels/llm_labels_v1_partial.json`.
- v1.1 output: `labels/llm_labels.json`, 16 answers, input `data/labeling_set_full.json` (SHA-256 `51205d45b2660153ce96a035163754eed6d4548d6425025f1cab3a12c8c8d82e`).
