# Step 02 — Pure LLM pilot operator protocol

Benchmark ID: `test-elementary-v0.1` | Metrics: `0.1` | Condition: `A/pure-LLM`.

## Frozen model-facing inputs

Provide **only** `PILOT_PROMPT.md`, `MODEL_INPUT.md`, and `ROOM_PROGRAM.csv` to a *fresh* ChatGPT or Claude session. These files are identical across hosts. `MODEL_INPUT.md` transcribes the brief and neutral numerical assumptions; `ROOM_PROGRAM.csv` gives all 41 room rows. Both derive from the same three frozen files in the original repo (source commit `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`). Original source workbooks and config remain reference documents for audit; do not supply the old README, search taxonomy, evaluation metrics, prior results, or existing design solutions to the tested models. Do not provide the full original config as a model-facing file because its generic grouping and floor-allocation hints would influence search.

## Execution

1. Start a brand-new chat for each trial, with no earlier architectural planning context; use the same model configuration and reasoning-effort setting across the trial where each host permits.
2. Send the frozen prompt and model-facing inputs as one initial message or attachments, with no extra examples. Record host, exact model/version as reported, date, settings and exposed capabilities.
3. Collect P01 exactly as produced. Send exactly `NEXT` after each proposal. Repeat through P20; do not steer, critique, correct errors, use tools, or provide performance feedback.
4. After P20, send exactly: `SELECT: Choose at most 10 of your 20 proposals as your recommended final set. Output the complete required fields for each selected proposal, with IDs referring to the original candidates. Explain your selections and identify architectural ideas you did not explore.`
5. Save the **complete unedited transcript**, including prompts, every proposal, failed formatting and retries. Do not rewrite a proposal to make it legal. Separately save the final set as produced.
6. Extract `run.json` using `schemas/run-log.schema.json`. Keep model/cost/tokens null if unavailable; record actual elapsed time and message counts, not estimates. Archive logs before any independent scoring.
7. Evaluate afterward, externally, using `docs/BENCHMARK.md`. Mark missing evidence unverified. Do not exclude or penalize a new architectural principle merely because existing Massing Explorer cannot encode it.

## Pilot design

Start with one independent run each in ChatGPT and Claude on **the original three-mass brief**. Pilot budget: 20 sequential candidates and up to 10 selections. Assess whether the output structure is stable. If the prompt changes materially, bump its version and restart both runs. Do not adapt it between the two model runs. Later use multiple independent trials; never present an already generated proposal to a different model.

## Risks / record explicitly

- No specialized massing tools are available during generation. Ordinary text/file reading of the supplied input pack is allowed; browsing/search/coding and external validation are prohibited.
- Stated rationales and next-direction statements are *observable text outputs*, not verified internal reasoning traces.
- No geometry backend checks compliance during the pure-LLM run; model claims of dimensional feasibility are not proof.
- Brief ambiguity: definitions of 'mass ratio' and 60-meter length scope are not further specified by the brief. Save each interpretation verbatim rather than coaching the model.
- Worksheet displays 44,270 SF NFA and 66,405 SF GFA (1.50 grossing); config also states a separate 1.15 area adjustment and 1.50 factor. Retain this ambiguity; do not silently recalibrate evaluations.
