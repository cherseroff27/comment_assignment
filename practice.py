from pathlib import Path
import json


data = {"ключ": "значение", "список": [1, 2, 3]}


p = Path("~/test_dir").expanduser()
print(p.resolve())
p.mkdir(parents=True, exist_ok=True)

path_to_json = p / "myfile.json"

with open(path_to_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

with open(path_to_json, "r", encoding="utf-8") as f:
    print(json.load(f))