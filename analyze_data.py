import json

with open(
    "data/website_pages.json",
    "r",
    encoding="utf-8"
) as f:
    pages = json.load(f)

print("Total Pages:", len(pages))

for page in pages[:10]:
    print("\n")
    print(page["title"])
    print(page["url"])