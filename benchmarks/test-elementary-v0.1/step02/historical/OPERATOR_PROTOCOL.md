# Step 02 — Pure-LLM pilot operator protocol (v0.4)

Benchmark: `test-elementary-v0.1` | Metrics: `0.1` | Group **A (pure LLM)** is split into two distinct prompt conditions:

- **A0 — Natural objective:** `NATURAL_PROMPT.md` asks for the best proposal, leaving the design approach entirely up to the model.
- **A1 — Self-structured exploration:** `GUIDED_PROMPT.md` asks the model to invent **and carry out its own exploration structure**, without supplying sampling axes, strategies, a candidate count, search steps, or a shortlist quota.

A1 does not test whether an LLM can follow an experimenter's search instructions; it tests whether it can choose an effective approach when explicitly asked to explore. A0 tests what it does when exploration is **not** requested.

## Identical inputs and limits

Supply only `MODEL_INPUT.md` and `ROOM_PROGRAM.csv` to each model, in the same order and format. They neutrally reproduce the frozen three-mass school program, brief and planning assumptions. Audit provenance, source aliases and hashes remain in `docs/BENCHMARK.md`, **not** in model-facing prompts.

For **both A0 and A1**:
1. Start an independent **fresh chat** with no earlier architectural project context, memory or host instructions if the host permits disabling them.
2. Send the respective prompt with both files; do not provide Massing Explorer documentation, strategy taxonomies, prior proposals, reference solutions, benchmark rubrics, or evaluation results.
3. Allow **one initial model response only** and require **one best final recommendation**, not an externally determined number of alternatives. No operator follow-ups, feedback, revisions, `NEXT`, `SELECT`, or model-directed extra turns.
4. Use the same model/host configuration, reasoning effort, sampling settings and **maximum output-token cap** for both conditions within each host wherever controls permit. Record the configured cap; if one cannot be set, mark it `null` and report actual token usage separately. A0 and A1 use the same maximum calls/turns; this does **not** guarantee identical realized inference cost or invisible reasoning effort.
5. No browser, coding, CAD, validators, CSP, specialized massing tools, external agents, web resources or feedback. Ordinary reading of the provided inputs is allowed.

## Output handling

- Both conditions share the same deliverable: **one recommended design** supported by program allocation, three-mass layout, floor organization, circulation, major dimensional implications, requirement responses and trade-offs. Do not impose benchmark field names or an internal strategy ontology on the generating model.
- **A0:** Record any visible alternatives, comparisons, exploratory choices and revisions voluntarily included. Do not penalize silence about process or infer absence of internal exploration.
- **A1:** Record the model's **self-chosen exploration framework** (e.g. what was considered, how it chose to compare or prioritize) and any observable evidence it actually performed such exploration. A claimed process can be a post-hoc explanation; never equate a plausible narrative with verified internal search.
- Preserve the exact complete input, generated output, failed/partial output and host metadata as produced, **before** normalizing. Do not repair infeasible ideas interactively.
- Populate `schemas/run-log.schema.json`: prompt condition/version, input provenance, run id, host/model/version, settings, dates, elapsed wall time, output length, token and tool usage and costs when actually available; unavailable values remain `null`.
- An independent evaluator later maps claims to Layer 1 and Layer 2 of `docs/BENCHMARK.md`, tagging which statements were **explicit**, which were **inferred**, and which are **unknown**. Outside-representation concepts are retained for separate assessment.
- The post-generation sequence is frozen in `EVALUATION_PROTOCOL.md`: archive raw outputs/metadata → canonicalize in a non-evaluative stage (the canonicalizer may remain unmasked) → strip metadata/process cues and randomize IDs → masked design scoring → **lock scores** → reveal model/condition → separately analyze raw A0/A1 behavior. The canonicalization instruction is `CANONICALIZATION_PROMPT.md`.
- Primary outcome: feasibility and architectural quality of the **single best recommended design**. Secondary exploratory analysis: visible variation, method/coverage, novelty, repetitions, and missing constraints **only where observable**. Do not treat a missing alternative list from A0 as a failure.
- Keep A0 and A1 results separate. With one response and matched caps, opportunity is more comparable than the previous 20-turn setup, but prompts differ in length and actual output/tokens/compute may still differ. Report actual costs and do not make stronger causal claims without repetitions and controls.

## Pilot

Run **ChatGPT A0, ChatGPT A1, Claude A0, Claude A1**, one fresh trial per cell, with exactly the frozen input pack. Afterward repeat each cell across multiple independent runs. Do not revise one condition's prompt based on the other condition's results without changing the prompt version and rerunning both.

Record ambiguities, without coaching models to one interpretation: `mass ratio` meaning; 60-m length scope; spreadsheet 66,405 SF GFA versus separately configured adjustment 1.15 and grossing factor 1.50. Preserve the old engine's frozen C-baseline scores, metrics and input hashes.

**Future extension, not part of A0/A1:** A separately labeled longer-horizon agent experiment could grant both conditions equal multistep/tool-call budgets. Do not confuse that with the matched one-response pure-LLM pilot.

