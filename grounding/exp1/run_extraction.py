"""Experiment 1 runner (runs on the architect's PC against local Ollama; standard library only).

Arms
  text     blind extraction of the trait questionnaire from each seed's concept + intent
           (key moves withheld): models x 3 prompt paraphrases x SAMPLES samples
  express  expressibility ceiling: a model writes a concept from the code record in words,
           then the other model extracts from it (1 paraphrase x SAMPLES samples)
Output: responses.jsonl (one line per call; resumable: finished calls are skipped).

Usage:  python run_extraction.py
"""
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434"
MODELS = ["qwen2.5:7b", "llama3.1:8b"]
SAMPLES = 5
TEMPERATURE = 0.7
OUT = HERE / "responses.jsonl"

DEFS = """Definitions. The school has exactly three masses:
- L: the mass that holds the core academic classrooms
- C: the mass that holds the gym and dining (the commons; its hall is double height)
- X: the remaining third mass
Answer only from the text. If the text does not state or clearly imply something, answer "not stated"."""

PROMPTS = [
    "Read this description of an elementary school massing strategy and fill in the questionnaire.",
    "Below is an architect's concept statement for a three-mass elementary school. Extract the arrangement it describes into the questionnaire.",
    "You are checking what a design statement commits to. From the statement alone, record the school's arrangement in the questionnaire.",
]
WRITE = ("You are an architect. Write a concept statement of 60 to 100 words for the elementary school massing "
         "strategy below, as you would present it to a client. Convey the arrangement so that a careful reader could "
         "reconstruct it. Return only the statement.\n\nArrangement: ")


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


def questionnaire_text(sch):
    return "\n".join(f"- {k}: {v['description']} ({' / '.join(v['enum'])})" for k, v in sch["properties"].items())


def extract(model, prompt, text, sch, seed):
    msg = f"{prompt}\n\n{DEFS}\n\nQuestionnaire:\n{questionnaire_text(sch)}\n\nText:\n{text}\n\nReturn JSON only."
    r = post("/api/chat", {"model": model, "messages": [{"role": "user", "content": msg}], "format": sch, "stream": False,
                           "options": {"temperature": TEMPERATURE, "seed": seed}})
    return json.loads(r["message"]["content"])


def main():
    data = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    sch = schema(data["questions"])
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add(r["key"])
    out = OUT.open("a", encoding="utf-8")
    jobs = []
    for it in data["items"]:
        for m in MODELS:
            for pi in range(len(PROMPTS)):
                for s in range(SAMPLES):
                    jobs.append(("text", m, it, pi, s))
    for it in data["items"]:
        for wi, writer in enumerate(MODELS):
            jobs.append(("write", writer, it, 0, 0))
            for s in range(SAMPLES):
                jobs.append(("express", MODELS[1 - wi], it, 0, s))
    todo = [j for j in jobs if "|".join(map(str, (j[0], j[1], j[2]["id"], j[3], j[4]))) not in done]
    print(f"{len(jobs)} calls in total, {len(todo)} to go")
    written = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["arm"] == "write":
                written[(r["model"], r["item"])] = r["output"]
    t0 = time.time()
    for n, (arm, model, it, pi, s) in enumerate(todo, 1):
        key = "|".join(map(str, (arm, model, it["id"], pi, s)))
        try:
            if arm == "write":
                r = post("/api/chat", {"model": model, "messages": [{"role": "user", "content": WRITE + it["record_words"]}],
                                       "stream": False, "options": {"temperature": TEMPERATURE, "seed": 1}})
                outp = r["message"]["content"].strip()
                written[(model, it["id"])] = outp
            elif arm == "express":
                writer = MODELS[1 - MODELS.index(model)]
                outp = extract(model, PROMPTS[0], written[(writer, it["id"])], sch, 100 + s)
            else:
                outp = extract(model, PROMPTS[pi], it["text"], sch, 100 + s)
            out.write(json.dumps({"key": key, "arm": arm, "model": model, "item": it["id"], "prompt": pi, "sample": s, "output": outp}) + "\n")
            out.flush()
        except Exception as e:
            print(f"  {key}: failed ({e})")
        if n % 10 == 0 or n == len(todo):
            el = time.time() - t0
            print(f"  {n}/{len(todo)} done, about {el / n * (len(todo) - n) / 60:.0f} min left")
    print("finished")


if __name__ == "__main__":
    main()
