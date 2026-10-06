# Step 02 — Pure-LLM pilot operator protocol (v0.2)

Benchmark: `test-elementary-v0.1` | Pilot metrics: `0.1` | Overall comparison group **A (pure LLM)** contains two **prompt conditions**, not two new groups of software:

- **A0 — Natural goal**: `NATURAL_PROMPT.md`. Does the model independently choose visible comparison, revision or exploration when simply asked for the strongest proposal?
- **A1 — Guided exploration**: `GUIDED_PROMPT.md`. How well can the same model explore alternatives when explicitly instructed to do so?

The main research distinction is between **unprompted behavior** and **capability under explicit prompting**. Neither is inherently superior. A1 is a legitimate and useful way to use an LLM, not an artificial advantage.

## Fixed model-facing data

Use exactly `MODEL_INPUT.md` and `ROOM_PROGRAM.csv` for both conditions, in the same order and format. Both are a neutral presentation of the three inputs pinned in `docs/BENCHMARK.md` (original version of the program workbook, brief, and project config at `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`). Source hashes and historical source paths are recorded in the *operator's* benchmark files, not shown to the models.

Do not give either model repository/benchmark documents, Massing Explorer's search/strategy axes, examples of candidate designs, validation scores, or results from other runs. No web search, code, massing tools, CSP, CAD, independent validators, or agents. Reading the two provided input files is allowed. Avoid prior memory, project context, or app-specific user instructions that contain Massing Explorer background where the host allows a clean session.

## A0 natural-goal pilot

1. Begin an independent new session. Provide `NATURAL_PROMPT.md` and the fixed inputs. Ask for **one strongest recommendation**. Do not request an option count, intermediate alternatives, a search plan, a table of explored regions, a self-critique, an internal reasoning trace, or 20 iterations.
2. Let the model decide its own process and presentation. Record its **entire visible response** without intervention or follow-up. No operator-issued `NEXT` or selection turn.
3. Extract the final recommended design (typically one); retain voluntarily supplied alternatives, comparisons, refinements and omissions as **observations** rather than mandating them.
4. Do not infer the absence of internal exploration from an absence of visible alternatives; hidden reasoning is **not observable**. Report spontaneous *visible* systematic exploration only, not the model's internal cognitive mechanism.

## A1 guided pilot

1. Begin a **separate fresh** session with `GUIDED_PROMPT.md` and the exact same fixed inputs.
2. Record P01 and send precisely `NEXT` after each proposal, through P20; provide no critique, corrections, feedback, examples or custom instructions.
3. After P20, send precisely: `SELECT: Choose no more than 10 of your 20 proposals. Rank the set with your strongest proposal first, clearly identify the single best proposal, explain your choices and important directions not explored.`
4. Retain the full sequence and final shortlist as originally returned. Failed, incomplete, repeated, or infeasible designs are evidence, not grounds for on-the-fly repairs.

## Logging and evaluation

- Run each condition independently on ChatGPT and Claude, starting with **one run per model per condition**. Keep exact host, model identifier/version, available reasoning setting, system instructions (if known), prompt version, run start/end timestamps, wall time, output length, model call count, token usage and cost (nullable if not reported), status, and complete transcript.
- Save run metadata consistent with `schemas/run-log.schema.json`; unknown fields are `null`. Preserve original unedited outputs and note any missing fields without fabricating answers.
- The **common quality endpoint is the single best final recommendation** per run, evaluated independently; the secondary guided endpoint is the selected set of **up to 10**. Treat spontaneous alternatives and number of candidates as descriptive, not as mandatory A0 failures.
- The benchmark's Layer 1 fields are normalized or annotated **after generation** by the evaluator if a model did not supply them. Distinguish an explicit claim, evaluator inference, and missing information. Do **not** force A0 to use Massing Explorer's schema during generation.
- After transcript capture, score feasibility, distinctness, occupied families, evaluation composites, representation gaps, time and resource cost using `docs/BENCHMARK.md`; only then compare results.
- A0 is not given 20 calls, while A1 is explicitly allowed 20 candidate turns. Their **raw search counts, elapsed times and total costs are not controlled comparisons**; report these costs and do not infer an inherent quality advantage from an unequal budget. For controlled **later** comparisons, pre-register equal token/inference budget and matching final-output scope or analyze quality per cost.
- Keep results separated by prompt condition. Do not pool A0 and A1 into one pure-LLM score or modify the frozen C-baseline values.
- **Pilot ambiguities**: meaning of 'mass ratio' and length cap scope; displayed program GFA versus independent area adjustment. Record interpretations without coaching or retroactively changing constraints. If model-facing instructions change materially, version the prompts and rerun both hosts under the changed version.

## Interpretation

A0 primarily tests **how the model visibly responds to the objective alone**. A1 tests **performance when asked to explore deliberately**. Explanations, visible drafts, and plans are model outputs, not privileged access to internal deliberation. Both are meaningful when assessing whether a standalone Massing Explorer search policy is worth its complexity.
