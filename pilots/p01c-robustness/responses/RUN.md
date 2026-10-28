# Outside-model runs, Pilot 01c

- Host: ChatGPT, temporary (non-personalized) chat, a new chat per task; thinking effort medium; model name to be recorded.
- 1 Rewrite: `raw/1_rewrite_received.txt` (SHA-256 `81e72c1f4834cafc149d1d95614c0a7068ef6c7784475a6a1603a8f91ea1f75b`). Reply contained rich-text artefacts (trailing backslashes, `&#x20;`); only those characters were removed to produce `1_rewrite.json`. 15/15 IDs; 53–68 words; mean 16% reuse of the originals' 5+ letter words.
- 2 Describe: `raw/2_describe_received.txt` (SHA-256 `13b62c85815e37882dc37b9304217f509f99c1da6a2a6c8d13f88c82f82d93f4`). Code fence removed. 35/35 IDs; 52–59 words. **Rule not followed:** the descriptions enumerate program (mean 8 program terms each) instead of stating an organizing idea, so Test 2 measures embeddings of placement-style text from an outside writer rather than concept-level text. Kept, not regenerated.
