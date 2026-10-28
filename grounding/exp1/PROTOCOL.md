# Experiment 1: per-axis grounding map (pilot on 15 seeds)

Locked 2026-10-28, before any extraction result. Plan step 1 (`docs/STEP02_03_STATUS.md`). Design: `reports/Joint semantic axis search space.md`, Experiment 1.

**Question.** Which concrete traits does an LLM seed's concept text carry? For each axis, can the trait be recovered from the concept and intent alone? Key moves are withheld, because they name departments and links directly.

**Inputs.** 15 seeds, runs 01–03 (`items.json`). The answer key is computed by code from each seed's structure.

**Questionnaire.** Masses are named by role:
- L: the mass with the core academic classrooms;
- C: the mass with gym and dining;
- X: the third mass.

| Questions | Axis |
|---|---|
| Which mass holds each of 6 departments | Program organization; distribution balance is derived from these |
| Three links between masses | Topology |
| Storeys of each mass | Mean height and height articulation |
| Ground / upper levels of 7 departments | Vertical organization |

Every question allows "not stated".

**Arms.**
- **text:** two local models (qwen2.5:7b, llama3.1:8b) × 3 prompt paraphrases × 5 samples, temperature 0.7, with a JSON schema. The report suggested 10 samples; this uses 5 because of local compute.
- **express (ceiling):** each model writes a concept statement from the code record, and the other model extracts from it.
- **Controls, at scoring:** a shuffled control (answers scored against other seeds' keys) and a majority-class baseline.
- **Part A:** Mantel item-permutation test of semantic distance against each axis distance, for 4 encoders.

**Classes, per axis, text arm.**
- Carried: mean κ ≥ 0.6 and beats the shuffled control on most questions.
- Partial: κ 0.4–0.6.
- Uncarried: κ < 0.4.

**Falsifying results.**
- **No axis beats the shuffled control:** the two spaces are independent.
- **Every axis is carried:** the text adds no grounding information.
- **The express arm fails on an axis:** the vocabulary cannot carry it, and the fault is not the generator's.

**Limits.** 15 seeds hold about 8 distinct ideas, so this is a pilot. Its purpose is to decide whether the generation prompt must require traits the text leaves out, before generating 100–150 cases.
