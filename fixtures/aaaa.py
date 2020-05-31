import csv
import json

r = []


def manga_list():
    with open('manga_list.csv', 'r', newline='') as f:
        fields = ['manga_title', 'manga_url', 'manga_img', 'genre_list']
        manga_list = csv.DictReader(f, fields, delimiter=';')
        for manga in manga_list:
            yield manga


for i in manga_list():
    if i not in r:
        r.append(i)


with open('manga.json', 'a', encoding='utf-8') as f:
    result = []
    for manga in r:
        result.append({
            "title": manga["manga_title"],
            "url": manga["manga_url"],
            "img": manga["manga_img"],
            })
    json.dump(result, f, ensure_ascii=False)
