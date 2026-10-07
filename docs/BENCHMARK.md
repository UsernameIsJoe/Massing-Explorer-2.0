# Shared Benchmark

## Status

This document records the locked and unresolved decisions for Step 01 of the Massing Explorer 2.0 development sequence.

## Frozen benchmark inputs

The benchmark uses the existing default project material from `UsernameIsJoe/massing-explorer`:

- `test-elementary-space-summary.xlsx` (display alias for frozen source workbook)
- `test-elementary-brief.txt` (display alias for frozen source brief)
- `config/project.example.yaml`

The original frozen inputs are identified by Git blob hashes `dfd6fe15516702a8de269ebb105dd689d1cb3478` (program), `8294bb8833825de7ea97149b3ce96254ef070a7a` (brief), and `5d0133ddd7a71791dd78fac1957991cd4efaa5ac` (config). Display aliases do not change source bytes, evaluation values, or preserved SHA-256 checksums.

The current Massing Explorer reference implementation is pinned to commit `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`. This commit identifies the reproducible baseline; the complete original repository does not need to be copied into Massing Explorer 2.0.

## Step 02 prompt conditions (pilot)

The pure-LLM group contains **A0 (natural objective)** and **A1 (self-structured exploration)**. These are paired **one-response** trials, with the same frozen test-elementary program/brief, matching model settings where possible, a matching output-token ceiling, and **one best recommended proposal** in both conditions.

- **A0:** Request the best proposal, with **no search instructions** or required count of alternatives. Voluntary visible alternatives or revision count as observations; their absence proves nothing about internal reasoning.
- **A1:** Request that the LLM **choose and carry out its own exploration structure** and report the approach and evidence of alternatives considered. Do not prescribe axes, enumeration/sampling/search methods, candidate counts, predefined steps, or a shortlist. It must still recommend a single strongest proposal.
- Common evaluation measures independent feasibility and quality of the final recommended design. Comparative descriptions of visible exploration methods, breadth, novelty and limitations are **secondary**. A model's claimed approach is not conclusive evidence of internal exploration.
- The same **one model call and output-token cap** applies within each host/condition, where setting that cap is supported. Note differences in actual tokens, hidden reasoning effort, time, and cost; equal limits do not guarantee identical consumed resources.
- No benchmark taxonomy, scores, prior cases, run schema or repository links enter **either** generating model's inputs. Extract the two-layer benchmark fields **after** generation, marking model-provided, evaluator-inferred, and missing information separately.
- Repeated fresh runs are required to test stable tendencies. Longer-horizon guided experiments, if useful, must be registered as a **separate protocol** rather than quietly added to A1.

## Required experimental record

Every experimental run must retain the **complete unedited observable record** produced under its registered protocol, plus the final recommendation(s) used for comparison.

- **A0 / A1 pure-LLM pilot:** retain the complete single model response as the exploration record and exactly **one best recommended proposal** as the primary final output. Any alternatives, comparisons, revisions, or search structure voluntarily visible inside that response remain part of the raw record but are not required.
- **Later multi-candidate or agentic conditions (including systems B/C/D where applicable):** retain all observable intermediate proposals, revisions, tool calls, rejections and failures, plus a final selected set containing no more than 10 proposals.

This preserves protocol neutrality: a system is evaluated on the outputs it was actually asked to produce, while all observable search evidence remains available for later analysis.

Run-level metadata follows [`schemas/run-log.schema.json`](../schemas/run-log.schema.json). It records the system and version, input hashes, prompt and conditions, budgets, execution environment, timing, status, usage, artifact paths, and summary results. Fields that do not apply to a system are recorded as `null` rather than estimated.

## Two-layer output format

The benchmark separates the system's submitted proposal from the independent evaluation applied afterward. This avoids forcing every system to use Massing Explorer's current internal representation and preserves the possibility of discovering strategies outside that representation.

### Layer 1 — Proposal submitted by the system

Each final proposal must include:

| Field | Meaning |
| --- | --- |
| `proposal_id` | Unique identifier |
| `concept_name` | Short descriptive name |
| `strategy_summary` | Concise explanation of the organizational idea |
| `program_grouping` | Which programs belong together |
| `spatial_relationships` | Adjacency, separation, hierarchy, and shared spaces |
| `vertical_organization` | Ground/upper-floor distribution and stacking |
| `massing_organization` | Number of masses and how they relate |
| `circulation_logic` | How people move between major program areas |
| `requirement_response` | How the proposal addresses each brief requirement |
| `known_risks` | Possible violations or unresolved questions |
| `stated_rationale` | Why the system selected this strategy |
| `representation_gap` | Anything the current Massing Explorer encoding cannot express |

The submission may also include text, structured data, diagrams, or geometry, but these fields are required for comparison.

### Layer 2 — Independent benchmark evaluation

The evaluator adds:

| Field | Measurement |
| --- | --- |
| `normalized_strategy` | Mapping to the nine strategy axes where possible |
| `encoding_status` | Fully expressible, partially expressible, or outside the current representation |
| `hard_feasibility` | Pass/fail plus each violation |
| `realization_status` | Whether the strategy was successfully converted into geometry |
| `feasibility_distance` | Distance from a valid solution |
| `distinctness` | Difference from other proposals |
| `coverage_contribution` | New region or family added |
| `four_evaluation_axes` | Coherence, alignment, efficiency, and robustness |
| `runtime_and_cost` | Resources used to produce and verify the proposal |
| `expert_review` | Blinded architectural review added later |

## Interpretation rule

The universal proposal format describes architectural relationships. Mapping into Massing Explorer's internal variables happens during independent evaluation. A proposal must not be rejected solely because the current representation cannot encode it.

For A0/A1, the post-generation procedure is frozen in [`EVALUATION_PROTOCOL.md`](../benchmarks/test-elementary-v0.1/step02/EVALUATION_PROTOCOL.md): raw records may be canonicalized **unmasked** by a non-evaluative extractor; only the resulting architectural records are then stripped of metadata/process cues, randomized, and supplied for masked scoring. Scores are locked before identities are restored and behavior is analyzed separately. This is a **label-masked and style-normalized evaluation stage**, not a claim of perfect blinding.

## Pilot evaluation metrics — version 0.1

The first experiments use a deliberately simple metric set. The metrics may evolve as the experiments reveal better questions, but every experimental batch must record and retain one frozen metric version so that results within that batch remain comparable.

| Metric | Pilot calculation |
| --- | --- |
| Feasibility | Hard pass/fail, number of violations, and the existing Massing Explorer feasibility distance |
| Distinctness | Number of unique normalized strategies in the submitted set; for A0/A1's single required recommendation, within-run distinctness is **not a primary metric** and applies only to voluntarily visible alternatives |
| Coverage | Number of occupied strategy families or cells; for A0/A1's single-response pilot, treat coverage as **descriptive only where multiple alternatives are visibly present**, not as a required success criterion |
| Quality | Existing coherence, alignment, efficiency, and robustness calculations, without retuning their current formulas |
| Search efficiency | Wall-clock time, number of proposals generated, and number of model/tool calls |
| Representation expansion | Number of proposals classified as partially or fully outside the current encoding |
| Expert review | Deferred until the pilot produces sufficiently comparable visual outputs |

Metric changes must create a new version and apply only to a new experimental batch. Previous results remain attached to the metric version under which they were produced.

## Frozen baseline result

The original Massing Explorer regression runner was executed twice from the pinned commit. Both runs produced identical JSON results.

| Result | Value |
| --- | ---: |
| Attempts | 209 |
| Archived cells | 159 |
| Legal cells | 37 |
| Legal three-mass cells | 37 |
| P-pool size | 41 |
| Feasible P entries | 6 |
| Unresolved P entries | 35 |
| Wall time | 22.282 s and 24.750 s |
| Deterministic repeat | Identical output |

The archived run manifest and report are in [`benchmarks/test-elementary-v0.1/baseline/`](../benchmarks/test-elementary-v0.1/baseline/).

The legacy runner provides aggregate results but does not retain the complete candidate-level exploration log or a final set normalized to the new proposal schema. This limitation is recorded in the manifest. All new experimental runners must emit both artifacts.

## Step 01 status

The shared inputs, output contract, pilot metrics, run-log schema, and frozen baseline report are complete for benchmark version `test-elementary-v0.1`.
