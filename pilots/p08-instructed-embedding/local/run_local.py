"""Pilot 8 local run (architect's PC, local Ollama; standard library only).

Embeds texts.json (instruction prefixes already included) with qwen3-embedding:4b.
No downloads. Output: embeddings.jsonl. Resumable: finished work is skipped.

Usage:  python run_local.py
"""
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434"
ENCODERS = {"qwen3-embedding:4b": ""}  # the only instruction-aware encoder installed


def post(path, body, timeout=600):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def installed():
    req = urllib.request.Request(OLLAMA + "/api/tags")
    with urllib.request.urlopen(req, timeout=30) as r:
        names = {m["name"] for m in json.loads(r.read())["models"]}
    return {e for e in ENCODERS if e in names or f"{e}:latest" in names}


def main():
    have = installed()
    missing = [e for e in ENCODERS if e not in have]
    if missing:
        print(f"  Missing encoders: {', '.join(missing)}. Nothing was downloaded. Tell Claude.")
        return
    out_path = HERE / "embeddings.jsonl"
    texts = json.loads((HERE / "texts.json").read_text(encoding="utf-8"))
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["encoder"], r["text_id"]))
    with out_path.open("a", encoding="utf-8") as out:
        for enc, prefix in ENCODERS.items():
            todo = [t for t in texts if (enc, t["text_id"]) not in done]
            for i in range(0, len(todo), 16):
                chunk = todo[i:i + 16]
                vecs = post("/api/embed", {"model": enc, "input": [prefix + t["text"] for t in chunk]})["embeddings"]
                for t, v in zip(chunk, vecs):
                    out.write(json.dumps({"encoder": enc, "text_id": t["text_id"], "vector": v}) + "\n")
                out.flush()
            print(f"  {enc} done")
    print("finished")


if __name__ == "__main__":
    main()
