"""Embed every Pilot 01 text with local Ollama encoders.

Standard library only (Windows/macOS/Linux). Requires Ollama running locally
and each model pulled first, e.g.  ollama pull nomic-embed-text

Usage (from pilots/p01-representation):
    python scripts/run_embeddings.py                      # default encoder set
    python scripts/run_embeddings.py nomic-embed-text     # one encoder

Writes runs/<encoder>/embeddings.jsonl and runs/<encoder>/run_log.json.
Configuration is frozen in ENCODERS; change it only by bumping CONFIG_VERSION.
"""
import datetime
import hashlib
import json
import platform
import sys
import time
import urllib.request
from pathlib import Path

CONFIG_VERSION = "p01-enc-v1"  # unchanged from Pilot 01
OLLAMA = "http://localhost:11434"
HERE = Path(__file__).resolve().parent.parent

# prefix: text prepended to every input, as each model's card recommends for
# symmetric similarity/clustering. Empty means none. Record, never improvise.
ENCODERS = {
    "nomic-embed-text": {"prefix": "clustering: "},
    "mxbai-embed-large": {"prefix": ""},
    "bge-m3": {"prefix": ""},
    "qwen3-embedding:0.6b": {"prefix": ""},
}


def post(path, body):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def model_digest(name):
    try:
        tags = json.loads(urllib.request.urlopen(OLLAMA + "/api/tags", timeout=30).read())
        for m in tags.get("models", []):
            if m["name"] == name or m["name"] == name + ":latest":
                return m.get("digest")
    except Exception:
        return None
    return None


def load_texts():
    texts = []
    for line in open(HERE / "data" / "descriptions.jsonl", encoding="utf-8"):
        r = json.loads(line)
        texts.append({"text_id": r["text_id"], "text": r["text"]})
    probes = json.loads((HERE / "data" / "probes.json").read_text(encoding="utf-8"))
    for pid, t in probes["texts"].items():
        texts.append({"text_id": f"{pid}::probe", "text": t})
    return texts


def run(name):
    cfg = ENCODERS[name]
    texts = load_texts()
    out = HERE / "runs" / name.replace(":", "_")
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    vecs = []
    for k in range(0, len(texts), 16):
        chunk = texts[k:k + 16]
        res = post("/api/embed", {"model": name, "input": [cfg["prefix"] + t["text"] for t in chunk],
                                  "truncate": False})
        vecs += res["embeddings"]
    elapsed = time.time() - t0
    with open(out / "embeddings.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for t, v in zip(texts, vecs):
            f.write(json.dumps({"text_id": t["text_id"],
                                "text_sha256": hashlib.sha256(t["text"].encode()).hexdigest(),
                                "vector": v}) + "\n")
    log = {
        "config_version": CONFIG_VERSION,
        "encoder": name,
        "model_digest": model_digest(name),
        "prefix": cfg["prefix"],
        "similarity": "cosine",
        "texts": len(texts),
        "dimensions": len(vecs[0]) if vecs else None,
        "seconds": round(elapsed, 2),
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "host": {"os": platform.platform(), "python": platform.python_version()},
        "inputs_sha256": hashlib.sha256("".join(t["text"] for t in texts).encode()).hexdigest(),
    }
    (out / "run_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"{name}: {len(texts)} texts, dim {log['dimensions']}, {elapsed:.1f}s")


if __name__ == "__main__":
    names = sys.argv[1:] or list(ENCODERS)
    for n in names:
        if n not in ENCODERS:
            sys.exit(f"Unknown encoder {n}; add it to ENCODERS with its prefix first.")
        try:
            run(n)
        except Exception as e:
            print(f"{n}: FAILED ({e}). Is Ollama running and the model pulled?")
