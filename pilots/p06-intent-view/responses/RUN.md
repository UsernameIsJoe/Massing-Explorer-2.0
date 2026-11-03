# Outside-model run, Pilot 6

- Host: ChatGPT, temporary chat, medium effort, run by the architect 2026-11-03.
- Prompt: `prompts/1_REWRITE_INTENT.txt`.
- Reply: `raw/1_rewrite_intent_received.txt` (SHA-256 `721eaebb4b6cbb6691c083bc4a416cbc0c8d402e9173f69b5f2dfdd213dac502`). Valid JSON as received; copied unchanged to `1_rewrite_intent.json`.
- Checks: 15/15 IDs; 30–38 words (rule 20–40); mean 6% reuse of the originals' 5+ letter words (range 0–16%). Pilot 01c's concept rewrites reused 16%, so the intent paraphrases are lexically farther from their originals, which makes Q1 harder for intent than it was for concept.
- `local/texts.json` (45 texts), built from these:
  - the 15 archive intents (seeds_v2);
  - the 15 intent rewrites;
  - 15 idea rewrites: the Pilot 01c concept rewrite + " " + the intent rewrite, matching how the archive idea view joins concept and intent.
