"""Pilot 4 local scoring run (architect's PC, local Ollama; standard library only).

1. Embeds texts.json with three encoders (settings frozen as in Pilots 01/01b, config p01-enc-v1).
2. Extracts the trait questionnaire from items.json with llama3.1:8b (as in Experiment 1):
   prompt 1 of Experiment 1, 3 samples, temperature 0.7.
Outputs embeddings.jsonl and extraction.jsonl. Resumable: finished work is skipped.

Usage:  python run_local.py
"""
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434"
ENCODERS = {"mxbai-embed-large": "", "nomic-embed-text": "clustering: ", "bge-m3": ""}
MODEL = "llama3.1:8b"
SAMPLES = 3
TEMPERATURE = 0.7

DEFS = """Definitions. The school has exactly three masses:
- L: the mass that holds the core academic classrooms
- C: the mass that holds the gym and dining (the commons; its hall is double height)
- X: the remaining third mass
Answer only from the text. If the text does not state or clearly imply something, answer "not stated"."""
PROMPT = "Read this description of an elementary school massing strategy and fill in the questionnaire."


def post(path, body, timeout=600):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def schema(q):
    props = {}
    for d, name in q["place"].items():
        props[f"place_{d}"] = {"type": "string", "enum": ["L", "C", "X", "not stated"], "description": f"which mass holds {name}"}
    for p, desc in (("LX", "L and X"), ("LC", "L and C"), ("CX", "C and X")):
        props[f"link_{p}"] = {"type": "string", "enum": ["linked", "not linked", "not stated"], "description": f"are {desc} directly connected by a built link"}
    for r in "LCX":
        props[f"storeys_{r}"] = {"type": "string", "enum": ["1", "2", "3", "not stated"], "description": f"storeys of mass {r} (a double-height hall counts as 2)"}
    for d, name in q["level"].items():
        props[f"level_{d}"] = {"type": "string", "enum": ["ground only", "ground and upper", "upper only", "not stated"], "description": f"floors of {name}"}
    return {"type": "object", "properties": props, "required": list(props)}


def embed():
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
            print(f"  embeddings: {enc} done")


def extract():
    out_path = HERE / "extraction.jsonl"
    data = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    sch = schema(data["questions"])
    qtext = "\n".join(f"- {k}: {v['description']} ({' / '.join(v['enum'])})" for k, v in sch["properties"].items())
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            done.add(json.loads(line)["key"])
    jobs = [(it, s) for it in data["items"] for s in range(SAMPLES) if f"{it['id']}|{s}" not in done]
    print(f"  extraction: {len(jobs)} calls to go")
    t0 = time.time()
    with out_path.open("a", encoding="utf-8") as out:
        for n, (it, s) in enumerate(jobs, 1):
            msg = f"{PROMPT}\n\n{DEFS}\n\nQuestionnaire:\n{qtext}\n\nText:\n{it['text']}\n\nReturn JSON only."
            try:
                r = post("/api/chat", {"model": MODEL, "messages": [{"role": "user", "content": msg}], "format": sch,
                                       "stream": False, "options": {"temperature": TEMPERATURE, "seed": 100 + s}})
                out.write(json.dumps({"key": f"{it['id']}|{s}", "item": it["id"], "sample": s,
                                      "output": json.loads(r["message"]["content"])}) + "\n")
                out.flush()
            except Exception as e:
                print(f"  {it['id']}|{s}: failed ({e})")
            if n % 10 == 0 or n == len(jobs):
                el = time.time() - t0
                print(f"  {n}/{len(jobs)} done, about {el / n * (len(jobs) - n) / 60:.0f} min left")


if __name__ == "__main__":
    print("Step 1 of 2: embeddings")
    embed()
    print("Step 2 of 2: extraction")
    extract()
    print("finished")
