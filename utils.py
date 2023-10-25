import json

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(name, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(name, indent=4, ensure_ascii=False))