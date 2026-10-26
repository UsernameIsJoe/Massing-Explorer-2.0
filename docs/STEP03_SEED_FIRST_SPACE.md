# Step 03 — seed-first construction of a semantic possibility space

Date: 2026-10-26 (America/New_York).
Status: user-selected starting approach; construction/expansion mechanisms remain research questions. No new implementation or experiment is claimed.
Authority: the user's proposal, four reasons, boundary-expansion clarification, and decision to start with this approach.

## Decision and continuity

Start by asking an existing advanced LLM to propose a small set of distinct strategies against the active brief. Five is an initial example, not a locked sample count. Use those proposals to construct an initial semantic exploration space, then grow and revise it through further reasoning, user briefs and realization evidence.

This is the current candidate construction method within ME 2.0. It changes the entry into the space, not the strategy-first backbone or the value of prior work. Earlier ideas for constructing concepts and relationships before any scheme are retained as alternatives/background rather than the immediate starting route. No graph/tree/embedding/latent format, algorithm, or dimensional-realization budget policy is selected by this decision.

## User's reasons

1. **Reasoning from the start.** Use the LLM's architectural reasoning immediately instead of first feeding it an externally constructed space that it must interpret.
2. **Semantic connections originate with the proposals.** Their meanings and relationships draw on the same model/context that generated them.
3. **Avoid comprehensive representation design upfront.** Begin with understandable strategic proposals instead of enumerating a whole space or inventing a complete new case format first.
4. **Brief-conditioned focus.** The active brief shapes the initial strategies and region of attention.

Qualifications: potentially meaningful relationships still need to be made explicit enough to preserve and test. A minimal comparable account of strategic commitments will be needed for reliable exchanges. Neither a new comprehensive schema nor universal causal rules follow from five examples. The initial brief can focus exploration while also creating framing bias.

## Accepted pipeline baseline

The user accepted the [eight-step pipeline in the current backbone](CURRENT_BACKBONE.md#accepted-eight-step-pipeline-baseline) as the baseline to develop. It refines the initial working sequence here without changing the seed-first entry.

1. Interpret and confirm the brief.
2. Generate X clear, strategically distinctive cases; seek stable coverage across runs.
3. Construct their initial semantic space and boundary.
4. Explore with repeated user input and deliberate boundary-expansion probes.
5. Assess maturity using stability, diminishing useful discoveries, expansion attempts and user concerns before narrowing.
6. Realize and test shortlisted strategies, with cheap earlier probes where useful.
7. Revise, focus, archive or re-search; return to strategic exploration when realization or feedback warrants it.
8. Present the selected case with trade-offs and uncertainty.

Record lineage, brief changes, boundary updates, checks and decisions throughout. Boundary stability alone cannot distinguish maturity from stagnation. Narrowing stays reversible. The detailed mechanisms and thresholds remain research questions.

Seeds are hypotheses, not automatically compliant designs. Preserve the active school's whole-department/no-cross-mass-split rule. Cheap feasibility probes and strategic confidence before full realization remain important research topics.

## Current focus — analytical axes for Steps 02 and 03

The user approved the [axis-based evaluation and expansion research plan](STEP02_03_AXIS_EVALUATION_AND_EXPANSION.md). Treat Step 01's confirmed brief as available; resolve Steps 02 and 03 before developing Step 04 onward in detail.

Step 02 will compare prompt style and initial count using mixed-type **descriptive strategic axes**, separate quality/compliance checks, and deterministic separation, redundancy, reference/combination coverage, stability and cost measurements. Gower-style dissimilarity is the starting candidate; exact axes, encodings, weights, prompts, counts and thresholds remain to be specified. Coordinates are conditional on explicit modelling choices, not interpretation-free architectural truth.

Step 03 continues those axes: populate relevant within-axis alternatives, coupled changes and opposing commitments around each seed, retaining semantic meanings, dependencies and transformation history. Preserve reframing beyond shared seed assumptions. Seeds and related cases anchor an explored region; they do not certify all intermediate combinations or architectural completeness. A node/link account and constraint-based construction are candidate supports; the exact implicit boundary/membership rule is unresolved.

Freeze evaluation axes across compared runs while versioning working-space extensions. Begin with a controlled independent reference benchmark, then test transfer; preserve the existing program, whole-department rule and audit qualifications. Quality-diversity, In-context QD, mixed-data distance, combinatorial coverage, morphological analysis and attribute exploration supply component precedents, not proof of the full method. Manual chat remains the operating constraint. No implementation or experiment has been executed for this plan.

## Central research problem: moving beyond the seeds

The core question is:

> Can a small set of LLM-generated strategies grow into a semantic exploration space that helps subsequent reasoning escape its initial limitations?

The seed set is an entry point, not a boundary of admissible architecture. Different initial outputs are expected. The mechanism should be assessed by whether useful exploration remains possible across different starts and can recover from narrow or poor seeds.

Candidate expansion modes discussed with the user:

- **Develop:** vary or deepen a strategy and investigate its unresolved possibilities.
- **Connect:** propose combinations or transformations between strategies; check joint compatibility rather than assuming composition works.
- **Reframe:** introduce a strategic distinction or possibility absent from every initial seed.

These are a conceptual scaffold, not implemented operators or a frozen taxonomy. Reframing is particularly important: interpolation and recombination alone could preserve the common omissions of all seeds.

Research must establish how to notice an inadequate boundary, obtain outside-seed possibilities, retain useful alternatives, and update the space after a changed brief or contradictory realization. Do not silently convert initially absent possibilities into exclusions.

## Manual chat constraint

The user currently has chat access and cannot automatically call advanced LLMs whenever the pipeline runs. Design the first experiments around manual interaction:

- A script prepares the current brief, relevant alternatives/relationships and evidence.
- The user supplies that material to an advanced LLM through chat.
- The model returns proposals, exploration decisions or requests for checks.
- The script records the exchange and performs selected computations/realizations.
- Feedback and further user input return through chat.

The LLM remains responsible for architectural reasoning, the script provides persistent state and computations, and the user directs the process and transfers context/results. API integration is optional later work, not a prerequisite. The exact exchange format is still to be designed. Record user interventions and transfer effort so they are not mistaken for gains from the semantic space.

## Proposed first comparison — not yet executed

Use identical initial strategies, active brief, model, information access, evaluation and comparable total effort:

- **Baseline:** seed strategies plus ordinary chat/history.
- **Semantic-space condition:** the same seeds plus the reconstructed, navigable semantic account.

Then introduce the same user brief updates and compare valid strategic alternatives, adaptation, useful outcomes, continuity and total cost. Match underlying informational content where possible so extra descriptions are not confused with benefits of relational organization.

Repeat across different seed sets, including deliberately narrow ones. This is necessary to assess boundary expansion and sensitivity to initialization; success from one favorable set is insufficient. Five and all experimental settings remain provisional.

## Open decisions

- What counts as a distinct strategic seed, and how to detect shared hidden assumptions.
- Which minimum commitments must be recorded without premature comprehensive schema design.
- How relationships are inferred, grounded, retrieved and revised.
- How expansion and reframing are triggered and tested.
- How strategic confidence and user interest affect probing/realization effort.
- How renewed context preserves the exploration when long chat becomes stiff.
- What evidence supports stopping at a contextual local optimum.

The user retains authorship of the conceptual spine. Explain mechanisms and mathematics before implementation, and proceed through baselines and small tests.
