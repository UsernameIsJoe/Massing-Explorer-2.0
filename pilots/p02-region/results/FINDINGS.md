# Pilot 2 findings — membership rule

Date: 2026-10-28. Protocol: p02-v1.1 (graded 1–5 rating). Scores: `results/scores.json`.

## Result in one line

None of the three pre-registered rules reached the 75% bar. A rule found from the ratings, **"a candidate is a different strategy when special education changes mass"**, explains 19 of 20 decisive ratings, but because it was found after seeing the answers it must be confirmed on a fresh sample before use.

## Ratings

26 items: ratings 1 ×7, 2 ×7, 3 ×4, 4 ×5, 5 ×1. Both repeats were rated identically (4/4 and 1/1). 20 decisive items (1–2 vs 4–5).

## Pre-registered rules (binary agreement on 20 decisive items)

| Rule | Agreement | Admits (of 962) |
|---|---:|---:|
| Strict lock | 10/20 | 18 |
| Tolerant lock (≤ 1 protected decision broken) | **14/20** (70%) | 295 |
| Radius ≤ 0.10 | 13/20 | 669 |

Graded agreement (Spearman with the 1–5 rating): locked decisions broken 0.55, structure distance 0.38. No rule meets the gate; by the protocol, the ratings are used to fit a better rule that must be confirmed on a fresh sample.

## What drives the ratings

| Change | Ratings given |
|---|---|
| Special education changes mass | 4, 4, 4, 4, 5, 3, 3 |
| Special education changes floors only | 3 |
| Custodial moves or shifts floor | 1, 1, 1, 1, 1 (and 4 once, when combined with a link loss below) |
| Medical, media, art and music move or shift | 1, 1, 2, 2, 2, 2, 2 |
| Administration moves | 2, 3 |
| A link is cut or added | mostly 1–2; 4 when the commons "heart" lost its link to the learning wing |

**Post-hoc rule:** different iff special education changes mass. 19/20 decisive. The one miss is the heart-link loss, a link that is itself the scheme's organizing idea.

Under this rule, 780 of the 962 candidates stay inside the region of their nearest seed.

## Interpretation

- The architect's sense of "different strategy" is not proportional to how much changes. It hinges on a few **defining decisions**. In this brief, special education's placement carries the inclusion question, which is the scheme-level tension the seeds themselves name in their trade-offs. Supporting program (custodial, medical, media floors) can move freely.
- Structure distance treats every department equally, so it cannot see this; the lock rules fail because the generated commitments lock everything.
- This favours a **weighted decision space**: some decisions define the strategy, others do not. Which decisions are defining is partly brief-specific (special education here) and partly scheme-specific (the heart link in a heart scheme).

## Caveats

- The rule was fitted to the same 20 items it explains; 19/20 is an upper bound.
- The generator never moves core academic, gym or dining, so their weight is untested.
- Link edits were few and mixed; whether a link is defining seems to depend on the scheme.
- One labeler, though with fully consistent repeats in this round.

## Next — Pilot 2b (confirmation, about 6 minutes)

A fresh sample of about 20 candidates not seen before, enriched for the cases this round under-tested: special education moving mass versus only floors, link changes in hub schemes (hinge, heart) versus others, and administration moves. Pre-registered rule: **different iff special education changes mass, or the scheme's hub link is cut** (hub link: a link whose loss removes the only route through the mass the concept names as the connector). It is adopted for Pilot 3 if it agrees on ≥ 75% of decisive items.

## Update — decision weights stated by the architect (2026-10-28)

Instead of a confirmation round, the labeler stated which decisions matter: core academic, special education, administration, dining and gym move the strategy most; media and art and music are mild; custodial barely matters. Recorded in `data/decision_weights.json` (medical mild, floor-only changes at half weight, links mild except a hub link, which is defining: proposed as defaults and confirmed by the labeler).

Against the ratings already collected (a consistency check, not a fit; the weights were stated after the labeler had seen these items):

- Spearman of weighted change with the 1–5 rating: **0.85** (structure distance 0.38, locks broken 0.55).
- "Different if weighted change ≥ 1.0", i.e. one defining change: **19/20** decisive.

This replaces the post-hoc special-education rule and the planned confirmation round. The weighted change is the Pilot 3 membership measure.
