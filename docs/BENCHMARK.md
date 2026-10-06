# Shared Benchmark

## Status

This document records the locked and unresolved decisions for Step 01 of the Massing Explorer 2.0 development sequence.

## Frozen benchmark inputs

The benchmark uses the existing default project material from `UsernameIsJoe/massing-explorer`:

- `examples/Underwood_Elementary_Space_Summary_GSF_Tweaked.xlsx`
- `examples/underwood_3mass_brief.txt`
- `config/project.example.yaml`

The current Massing Explorer reference implementation is pinned to commit `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`. This commit identifies the reproducible baseline; the complete original repository does not need to be copied into Massing Explorer 2.0.

## Required experimental record

Every experimental run must retain:

1. The complete exploration log, including intermediate proposals, revisions, tool calls, rejections, and failures.
2. A final selected set containing no more than 10 proposals.

The exploration log supports analysis of how each system searched. The final set supports comparison of what each system ultimately recommended.

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

## Pilot evaluation metrics — version 0.1

The first experiments use a deliberately simple metric set. The metrics may evolve as the experiments reveal better questions, but every experimental batch must record and retain one frozen metric version so that results within that batch remain comparable.

| Metric | Pilot calculation |
| --- | --- |
| Feasibility | Hard pass/fail, number of violations, and the existing Massing Explorer feasibility distance |
| Distinctness | Number of unique normalized strategies in the submitted set |
| Coverage | Number of occupied strategy families or cells |
| Quality | Existing coherence, alignment, efficiency, and robustness calculations, without retuning their current formulas |
| Search efficiency | Wall-clock time, number of proposals generated, and number of model/tool calls |
| Representation expansion | Number of proposals classified as partially or fully outside the current encoding |
| Expert review | Deferred until the pilot produces sufficiently comparable visual outputs |

Metric changes must create a new version and apply only to a new experimental batch. Previous results remain attached to the metric version under which they were produced.

## Remaining Step 01 decisions

- Define the run-level metadata and logging schema.
- Run and archive the frozen Massing Explorer baseline.
