import json
import re

def remove_prefix(text):
    return re.sub(r"^([a-zA-Z][\)\.]|\d+[\)\.])\s*", "", text)

with open("pytania.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for question in data:
    for answer in question.get("answers", []):
        answer["text"] = remove_prefix(answer["text"])

with open("pytania_bez_prefiksow.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
