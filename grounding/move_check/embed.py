"""Embed the move-check texts with the four local encoders (standard library only).
Settings frozen as in Pilots 01/01b (config p01-enc-v1). Writes embeddings.jsonl.
Usage:  python embed.py
"""
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENCODERS = {"nomic-embed-text": "clustering: ", "mxbai-embed-large": "", "bge-m3": "", "qwen3-embedding:0.6b": ""}


def post(body):
    req = urllib.request.Request("http://localhost:11434/api/embed", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def main():
    texts = json.loads((HERE / "texts.json").read_text(encoding="utf-8"))
    with (HERE / "embeddings.jsonl").open("w", encoding="utf-8") as out:
        for enc, prefix in ENCODERS.items():
            for i in range(0, len(texts), 16):
                chunk = texts[i:i + 16]
                vecs = post({"model": enc, "input": [prefix + t["text"] for t in chunk]})["embeddings"]
                for t, v in zip(chunk, vecs):
                    out.write(json.dumps({"encoder": enc, "text_id": t["text_id"], "vector": v}) + "\n")
            print(enc, "done")
    print("finished")


if __name__ == "__main__":
    main()
