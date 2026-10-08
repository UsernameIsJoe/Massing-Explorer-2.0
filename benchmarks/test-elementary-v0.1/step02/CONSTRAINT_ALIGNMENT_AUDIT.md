# Constraint alignment and leakage audit — 2026-10-08

## Status and correction

- **Confirmed:** cross-mass department splitting is prohibited by the user-confirmed intended hard requirement.
- **Confirmed omission:** historical MODEL_INPUT.md, A0/A1 prompts and evaluator rubric did not state that prohibition. The evaluator instead used “mass or masses” for academic/special education.
- **Backend mechanism:** frozen ME partitions assign each whole department to one mass. This is distinct from the solver's `program_split` failures, which concern within-mass contiguous floors/minimum floor portions. Do not interpret that failure label as a cross-mass check.
- **Consequence:** seven LLM recommendations fail the intended rule, but their generators were not given it. Original Fable PASS labels are judgments under the historical incomplete rubric. They cannot establish intended-rule compliance or matched LLM-versus-ME feasibility.
- **Action:** current protocols/input v0.2+ explicitly state the rule; original bytes are retained under historical/. No historical score or raw answer is rewritten. Revised rules are forward-only; a corrected batch requires new generation and evaluation.

## Requirement comparison

| Requirement/policy | Historical LLM input / scorer | Frozen ME | Correction/status |
|---|---|---|---|
| Whole department in exactly one mass | Omitted; scorer allowed “mass or masses” | Whole-department partition representation | Explicit hard rule in input, both prompts, extractor, rubric and operator gate |
| Floor splits within assigned mass | Contiguous floors, ≥70 m² per portion | Awkward-split hard gate | Keep separate from cross-mass prohibition |
| GFA target | 66,405 display and 76,365.75 calculation; scorer permitted either stated basis | 76,365.75 ±3% fixed configuration | Revised input/rubric fix adjusted band; R04/R08 historical basis differs |
| Length | 60 m with scope not explicit | Per-mass length check | Revised input states per mass; does not impose a 60-m whole-building cap |
| Mass ratio | Meaning ambiguous; scorer accepted explicit proposal interpretation | Ground footprint, transposable aspect | Revised input uses ground footprint short/long; not every upper plate or inter-mass ratio |
| Ratio tolerance | Not supplied explicitly | Absolute 0.00675 from 0.03 × max(0.625−0.4, 0.15) | Disclosed in revised input/rubric; future common validator required |
| Academic/special-ed width | 80 ft; scorer allowed multiple masses | Department-width constraint | Whole department in one 80-ft bar; width means bar depth |
| Gym/dining double height | Explicit brief requirement | Brief-derived double-height state | Verify parsed runtime state; cafeteria config default is false and brief must override it |
| Daylight width | Generic instructional/daylit preference | Named configured academic/SPED/art/music/classroom/science set | Do not automatically penalize gym-only halls; applicability recorded in existing rationale audit |
| Prefer three floors / top media / ground arts | Soft preferences | Floor pins and preferred-story scoring | Keep soft status; distinguish satisfaction in one mass versus every mass, and above-admin level versus true vertical overlap |
| Department allocation priors | Not fully spelled out | Config ground/upper biases, modified by brief | Backend priors are not extra hard requirements; disclose them in comparisons |
| Quality/behavior/ME scores | Reviewer 0–4; behavior 0–3 | Computational 0–1 proxies | Separate constructs; preserve original scales and anchors |
| Design tools | Operator prohibited use | Solver/search permitted | Raw Rhino-session remarks are availability cues, not proof of tool use; actual tool-log compliance remains unverified |
| Budget and coverage | One final recommendation per response | 209 attempts / 159 archived cells | Unequal denominators/resources; no direct success-rate or compute ranking |

## Intended-rule overlay (not replacement scores)

| Cases | Cross-mass assignment finding |
|---|---|
| R01 | Core academic; special education; custodial |
| R03 | Core academic; custodial |
| R06 | Core academic; custodial |
| R07 | Core academic |
| R08 | Custodial (network/telecom separated) |
| R10 | Core academic |
| R12 | Custodial (network/telecom separated); medical placement independently ambiguous |
| R02, R04, R05, R09, R11 | No cross-mass department split found; passes this check only, not full feasibility |

- Intended-rule pass counts: ChatGPT A0 2/3; ChatGPT A1 1/3; Opus A0 1/3; Opus A1 0/3. These are retrospective checks, **not** comparative instruction-following scores under matched inputs.
- R02's whole-department grouping was in the initial ME pool and 16 archive cells, none legal. Its ME variants flagged length 10 times, ratio 10 and within-mass program split 8, with overlap. The original R02 geometry was not itself injected and tested.
- R04/R09 and R05/R11 groupings were absent from the recorded pool/archive. Their grouping syntax is representable; geometric realizability is untested. No evidence establishes precisely why pool selection omitted them.

## Leakage findings and packet corrections

- **Direct identity leak, already established:** the original quality scoring DOCX retained source metadata. Cleaning a later derivative does not change original evaluation provenance.
- **Newly found residual provenance cue:** the current canonical masked Markdown retained source-document page comments. Removed from current derivative and delivery packet; archived unmasked sources/git history retain traceability.
- **Newly found process cue:** canonical `stated_rationale` sections included rejected-option comparisons, staged-family labels and search narratives. Removed those sections from the quality derivative, plus explicit F1/E2/P4 labels and alternative-scheme area references. Architectural risks and area-policy sensitivities are retained; they may remain indirect condition cues.
- **Newly found host-session cue:** masked behavior records retained Rhino offers/session availability remarks. Removed the two identified tails from the masked derivative only; raw response files remain byte-identical. This does not establish whether tools were used during generation.
- **Packaging cue:** existing operator introductions mention A0/A1 and the shuffle key. New `results/batch-01/delivery/QUALITY_PACKET.md` and `BEHAVIOR_PACKET.md` contain only R01–R12 records. Never send the repository folder, raw/unmasked files, shuffle key, gallery, scored results or this audit with a masked packet.
- **Not metadata:** A1/F1/F2 used as architectural mass/floor labels are retained. Blind global removal would corrupt geometry/program evidence.
- **Current cleaned DOCX check:** direct identity markers were not found by the scoped XML scan, but process-rationale sections remain. Use the corrected Markdown quality delivery packet for fresh review; the DOCX was not rewritten in this Markdown correction. Historical unmasked documents remain operator archives and must never accompany evaluator delivery.
- **Residual limits:** architectural detail, style and visible exploration can reveal a likely condition. No text sanitizer proves perfect blinding. Embedded images and the exact historical delivered bytes remain unverified; prior DOCX exposure remains documented.

## Checks and release gate

- Run `python3 verify_audit.py` from this folder. It checks clean-packet record counts/order, direct metadata/session/page markers, required no-cross-mass rule, original raw/key bytes and preserved historical instruction hashes. A clean scanner result is scoped evidence, not a guarantee of full anonymity or architectural feasibility.
- Before a new run: compare the complete input payload, evaluator rubric and parsed backend hard/soft constraints; hash exact sent files; record model/host/settings and actual tool actions separately; validate packet content and metadata before delivery.
- Do not mix revised generation rules with historical scoring or silently rescore Batch 01. Do not count forbidden splits as valid representation expansion.

## Source evidence

- Repository state before correction: `e420f46d346563e5ca5bc1b0306f4c5a04356c15`.
- Historical instruction hashes: `AUDIT_VERIFICATION.json`.
- Cross-mass assignments: raw R01–R12 responses and canonical program_grouping/vertical_organization records; R12 medical discrepancy remains unresolved.
- Frozen ME source commit: `751ba24b0d2bcaeae5274eaffa589060c95ec0f9`; `explore/axes.py` pairwise owner encoding, `solver.py` check_program_splits/check_ratio_band, `explore/descriptors.py` awkward splits and project configuration.
- Frozen rerun archive: existing local candidate_geometry.json; grouping overlap checked in PARTITION_OVERLAP_CHECK.json. No geometry or numeric score was modified by this audit.
