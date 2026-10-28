# LLM baseline prompt (Pilot 01, p01-v1)

Use a **fresh chat** with no project files, memory or earlier context. Paste the prompt below, then attach or paste `data/labeling_set.json` unchanged. Record the model, mode/effort setting, date and host in `llm_baseline/RUN.md`. Save the reply's JSON as `labels/llm_labels.json`.

---

You are an experienced school architect. Below are 31 items, each with an anchor strategy and two options for a three-mass elementary school on one brief. For each item, judge which option is the closer **architectural strategy** to the anchor: program organization, relationships between parts, and strategic intentions. Do not judge by wording overlap or writing style. Judge each item independently.

Answer with JSON only, in exactly this shape, one entry per item, keyed by `triplet_id`:

```json
{"T10": {"answer": "option_1"}, "T05": {"answer": "about_equal"}}
```

Allowed answers: `option_1`, `option_2`, `about_equal`, `cannot_judge`. Give no explanations.

[paste data/labeling_set.json here]
