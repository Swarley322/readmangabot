import json

with open('mintmanga.json', 'r') as f:
    raw = json.load(f)

print(len(raw))
result = []
for manga in raw:
    new_manga = {
        'title': manga['title'],
        'url': manga['url'],
        'img_url': manga['img']
    }
    if new_manga in result:
        continue
    result.append(new_manga)

with open('mintmanga_new.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(len(result))
