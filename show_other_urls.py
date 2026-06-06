import json

with open("data/others.json", "r", encoding="utf-8") as f:
    others = json.load(f)

for page in others[:50]:
    print(page["title"])
    print(page["url"])
    print("-" * 50)