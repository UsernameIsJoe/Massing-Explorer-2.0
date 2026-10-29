"""Style-normalised meaning test (see YARDSTICK.md, attempt 2). Local Ollama; standard library only.

1. llama3.1:8b restates each of the 85 concept texts in one fixed plain template (temperature 0, fixed seed).
2. The restatements are embedded with the three judges.
Outputs normalized.jsonl and embeddings_norm.jsonl. Resumable.

Usage:  python run_normalize.py
"""
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434"
MODEL = "llama3.1:8b"
JUDGES = {"mxbai-embed-large": "", "nomic-embed-text": "clustering: ", "qwen3-embedding:4b": ""}
TEMPLATE = """Restate the school massing concept below in exactly three plain sentences, in this order:
1. The organizing idea, in one sentence.
2. How the building masses relate to each other.
3. What the arrangement brings together or keeps apart, and why.
Rules: at most 70 words in total; plain everyday words; no names, no metaphors, no stylistic adjectives; do not add anything the text does not say; do not leave out the arrangement. Return only the three sentences.

Concept:
"""


def post(path, body, timeout=600):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def main():
    texts = json.loads((HERE / "texts.json").read_text(encoding="utf-8"))
    norm_path, emb_path = HERE / "normalized.jsonl", HERE / "embeddings_norm.jsonl"
    done = {}
    if norm_path.exists():
        for line in norm_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done[r["text_id"]] = r["text"]
    todo = [t for t in texts if t["text_id"] not in done]
    print(f"Step 1 of 2: restating {len(todo)} texts")
    t0 = time.time()
    with norm_path.open("a", encoding="utf-8") as out:
        for n, t in enumerate(todo, 1):
            r = post("/api/chat", {"model": MODEL, "messages": [{"role": "user", "content": TEMPLATE + t["text"]}],
                                   "stream": False, "options": {"temperature": 0, "seed": 1}})
            done[t["text_id"]] = r["message"]["content"].strip()
            out.write(json.dumps({"text_id": t["text_id"], "text": done[t["text_id"]]}, ensure_ascii=False) + "\n")
            out.flush()
            if n % 10 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} done, about {(time.time() - t0) / n * (len(todo) - n) / 60:.0f} min left")
    print("Step 2 of 2: embeddings")
    have = set()
    if emb_path.exists():
        for line in emb_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            have.add((r["encoder"], r["text_id"]))
    ids = [t["text_id"] for t in texts]
    with emb_path.open("a", encoding="utf-8") as out:
        for enc, prefix in JUDGES.items():
            need = [i for i in ids if (enc, i) not in have]
            for k in range(0, len(need), 16):
                chunk = need[k:k + 16]
                vecs = post("/api/embed", {"model": enc, "input": [prefix + done[i] for i in chunk]})["embeddings"]
                for i, v in zip(chunk, vecs):
                    out.write(json.dumps({"encoder": enc, "text_id": i, "vector": v}) + "\n")
            print(f"  {enc} done")
    print("finished")


if __name__ == "__main__":
    main()
