# Step 02 — Observable search / reasoning behavior protocol (v0.1)

Benchmark: `test-elementary-v0.1`

## Purpose

This protocol standardizes how the raw A0/A1 LLM responses are read for **observable search and reasoning behavior**.

It does **not** claim access to hidden chain of thought. It records only what the response itself demonstrates: how the problem is structured, what alternatives are visibly considered, what is checked, revised, compared, and selected.

This analysis is separate from masked design-quality scoring. It may be performed unblinded, but it must never be used to revise the locked Fable design scores.

The purpose is to answer a different question:

> What capabilities and failure modes are visible in the way each system searches for and selects an architectural strategy?

## General coding rules

1. Score only observable evidence in the raw response.
2. Do not infer hidden deliberation from fluent prose.
3. A statement such as “I systematically explored the space” is not evidence of systematic search unless the response shows the structure, alternatives, comparisons, or checks.
4. Distinguish **claimed process** from **evidenced process**.
5. Do not penalize A0 for failing to perform a behavior it was never explicitly asked to show. The axes are descriptive, not prompt-compliance grades.
6. Apply the same anchors to every run.
7. Keep evidence excerpts / locations with every coded judgment.
8. Do not compute a single overall “reasoning score.” Preserve the multidimensional profile.
9. With three runs per cell, aggregate descriptively only: ranges, medians/means where useful, and recurring patterns. Do not claim population significance.
10. A0/A1 and model identities may be known during this analysis. This stage is intentionally unblinded.

## Per-run evidence record

Before assigning axis scores, extract the following observable evidence:

- visible number of distinguishable alternatives;
- named or clearly varied design variables;
- explicitly stated exploration framework, if any;
- alternatives explicitly compared;
- alternatives explicitly rejected or narrowed;
- hard requirements explicitly checked;
- checks supported by calculations/dimensions versus merely asserted;
- quantitative checks performed;
- visible revisions, backtracking, or re-checks;
- explicit trade-offs used in decision-making;
- final selection rationale;
- stated stopping rule, if any;
- unresolved assumptions / unknowns acknowledged;
- representation-expanding architectural ideas;
- contradictions between claimed process and demonstrated process.

Where useful, separate:

- **asserted compliance** — the response says a requirement is satisfied;
- **demonstrated verification** — the response provides enough dimensions, arithmetic, or relational evidence to show why it is satisfied.

## Behavioral axes

Each axis is scored on an integer **0–3** scale. These scores describe observable behavior only.

### 1. Problem structuring

Does the response convert the brief into a usable design / decision problem?

- **0 — absent:** little or no explicit structuring beyond immediately proposing a scheme.
- **1 — limited:** restates or groups some brief items but does not clearly distinguish their roles.
- **2 — structured:** organizes major requirements, preferences, assumptions, and/or unknowns sufficiently to guide design decisions.
- **3 — explicit decision structure:** clearly separates hard requirements, soft preferences, assumptions, unresolved information, and important dependencies, and visibly uses that structure.

### 2. Search-space framing

Does the response identify meaningful variables or dimensions that could be varied?

- **0 — absent:** no visible search dimensions.
- **1 — implicit:** a few variables are changed or mentioned without a clear search-space structure.
- **2 — explicit:** several architectural variables are named or deliberately varied.
- **3 — structured:** an explicit multidimensional search space, branching structure, option matrix, or equivalent is established and used.

Typical variables may include program partition, mass count/role, topology, loading, floor distribution, stacking, width, length, plate profile, adjacency, circulation, or envelope.

### 3. Exploration breadth

How much of the visible option space is actually explored?

- **0 — single-path:** jumps directly to one proposal with no distinguishable alternatives.
- **1 — narrow:** one proposal plus minor alternatives or local variations.
- **2 — multiple:** several distinguishable alternatives are visibly considered.
- **3 — broad:** a deliberately broad set of alternatives or branches is explored before narrowing.

Record the visible alternative count separately whenever countable.

### 4. Exploration diversity

How strategically different are the visible alternatives?

- **0 — none:** no alternatives, or all are effectively the same strategy.
- **1 — shallow:** mostly dimensional tweaks or cosmetic/local changes.
- **2 — meaningful:** alternatives vary multiple strategic dimensions or program/massing relationships.
- **3 — qualitatively diverse:** alternatives represent substantially different organizational or architectural strategies.

### 5. Comparative evaluation

Are alternatives compared under common criteria?

- **0 — absent:** no comparison.
- **1 — informal:** one option is preferred with mostly intuitive or ad hoc reasoning.
- **2 — explicit:** alternatives are compared against multiple shared criteria.
- **3 — systematic:** the same criteria are applied consistently across alternatives, and the comparison visibly drives narrowing/selection.

### 6. Constraint verification

Does the response test feasibility rather than merely claim it?

- **0 — mostly asserted:** compliance is largely stated without supporting checks.
- **1 — partial:** a few important constraints are checked or calculated.
- **2 — substantial:** most critical hard constraints are explicitly checked with relevant evidence.
- **3 — systematic:** hard requirements are checked in a deliberate, near-complete manner, with dimensions/arithmetic/relations where needed and unresolved items clearly separated.

Record both:
- number of hard requirements explicitly addressed;
- number supported by demonstrated verification rather than assertion only.

### 7. Revision / backtracking

Does new information cause prior decisions to be reconsidered?

- **0 — none visible:** one-way progression.
- **1 — local correction:** a small adjustment is made after noticing an issue.
- **2 — meaningful revision:** a prior organizational/dimensional decision is revised because of a discovered conflict or comparison.
- **3 — iterative:** repeated detect → revise → re-check behavior is visible.

### 8. Trade-off reasoning

Does the response recognize and use competing objectives?

- **0 — absent:** little or no meaningful trade-off discussion.
- **1 — acknowledged:** trade-offs are mentioned but do not clearly influence decisions.
- **2 — decision-relevant:** competing benefits/costs explicitly affect selection.
- **3 — structured:** alternatives are intentionally preserved or compared because they occupy different trade-off positions, and the final choice is justified through those trade-offs.

### 9. Selection and stopping logic

How is the final proposal selected, and why does exploration stop?

- **0 — unexplained:** final choice appears without visible selection logic.
- **1 — intuitive:** some rationale is given, but no clear comparative basis or stopping logic.
- **2 — explicit selection:** the final choice follows from stated criteria/comparison, though stopping remains mostly implicit.
- **3 — explicit selection + stopping:** both the choice and a credible reason to stop exploring are stated or demonstrated.

### 10. Representation expansion

Does the response introduce architectural ideas beyond the currently predefined Massing Explorer representation?

- **0 — none visible:** stays within already supported strategy types/relationships.
- **1 — minor extension:** adds a modest relationship or nuance not explicitly encoded.
- **2 — meaningful expansion:** proposes a useful architectural relationship, organizational device, or geometry the current representation cannot fully capture.
- **3 — substantial expansion:** introduces a qualitatively important strategy family or reasoning construct outside the current representation that would require a meaningful extension.

This score must be supported by an explicit comparison to the current Massing Explorer representation. If that comparison cannot be established, record **unknown** rather than guessing.

### 11. Uncertainty handling

Does the response distinguish known facts from assumptions and unresolved information?

- **0 — poor:** missing information is silently invented, ignored, or presented as certain.
- **1 — limited:** some uncertainty is acknowledged, inconsistently.
- **2 — clear:** important assumptions and unknowns are generally identified and separated from facts.
- **3 — active:** uncertainty is explicitly tracked and materially shapes the proposal, verification, or robustness of the strategy.

## Claimed process vs evidenced process

For every run, record both when applicable:

- **claimed process:** what the model says it explored or checked;
- **evidenced process:** what the response contains enough observable evidence to support.

A mismatch is itself a useful result. Example:

- claimed: “systematically explored multiple massing options”;
- evidenced: one final scheme, no distinguishable alternatives, no comparison table, no rejection trace.

The behavioral score follows **evidenced process**, not the claim.

## Required per-run output

Use this structure:

### [source run ID]

**Run metadata:** model / condition / run number

**Observable evidence**
- visible alternatives:
- variables varied:
- stated exploration framework:
- explicit comparisons:
- explicit rejections/narrowing:
- hard requirements addressed:
- demonstrated constraint checks:
- quantitative checks:
- visible revisions/backtracks:
- trade-offs used:
- selection rationale:
- stopping rule:
- assumptions/unknowns acknowledged:
- representation-expanding moves:
- claimed-vs-evidenced mismatches:

**Behavior scores**

| Axis | Score | Evidence-based note |
|---|---:|---|
| Problem structuring | 0–3 | |
| Search-space framing | 0–3 | |
| Exploration breadth | 0–3 | |
| Exploration diversity | 0–3 | |
| Comparative evaluation | 0–3 | |
| Constraint verification | 0–3 | |
| Revision / backtracking | 0–3 | |
| Trade-off reasoning | 0–3 | |
| Selection + stopping logic | 0–3 | |
| Representation expansion | 0–3 / unknown | |
| Uncertainty handling | 0–3 | |

**Key observed strength:**  
**Key observed limitation:**

Do not calculate a total score.

## Batch comparison

After all 12 runs are coded:

1. Compare **A0 vs A1 within ChatGPT**.
2. Compare **A0 vs A1 within Opus**.
3. Compare **ChatGPT vs Opus under A0**.
4. Compare **ChatGPT vs Opus under A1**.
5. Report per-axis patterns, ranges, and repeated qualitative behaviors.
6. Keep the Fable outcome scores separate until behavior coding is complete.
7. Only afterward relate behavior to outcome, for example:
   - did more systematic verification correspond to fewer feasibility failures?
   - did broader/diverse exploration correspond to better architectural review?
   - did A1 increase visible search structure without improving outcomes?
   - did representation-expanding behavior produce ideas outside the Massing Explorer search space?

Do not infer causality from this small batch.

## Later Massing Explorer comparison

The same conceptual capabilities can later be mapped to Massing Explorer using its actual logs and pipeline trace, but do not force identical evidence where the system mechanisms differ.

Useful analogues include:

- problem structuring → brief parsing / constraint-preference representation;
- search-space framing → encoded strategy variables and admissible families;
- exploration breadth/diversity → sampled/visited strategies and occupied cells;
- comparative evaluation → shortlist/evaluation logic;
- constraint verification → deterministic realization and hard gates;
- revision/backtracking → repair/refinement/re-exploration;
- trade-off reasoning → multi-axis evaluation / preserved Pareto-like alternatives;
- stopping logic → search budget, convergence, coverage or exhaustion criteria;
- representation expansion → ability/inability to propose strategies outside the encoded grammar;
- uncertainty handling → explicit unknown/unsupported/unresolved states.

The goal is not to make the LLM and pipeline look artificially identical. The goal is to compare **which search capabilities each system actually possesses, how reliably they are executed, and what design outcomes result**.

