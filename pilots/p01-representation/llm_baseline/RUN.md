# LLM baseline run

- Date: 2026-10-28
- Model: Claude Opus (claude-opus-5-5), run as a separate subagent with a fresh context
- Input: `data/labeling_set.json` only (SHA-256 `6d183eb34eb79cc236145e7f9bdcb16fa6dd83684605319248a47fa6b9af2f30`), copied to an isolated folder; the agent was instructed to read no other file and not to use the web
- Prompt: `PROMPT.md`, with the note that some items carry a structure line
- Output: `labels/llm_labels.json`, 31 answers (18 option_2, 11 option_1, 2 about_equal)

Limitations: the baseline is the same model family that wrote the probes and built the pilot, so it is not an independent rater; on the probes in particular it can recognise its own construction. Unlike the labeler, it saw structure lines but no diagrams.
