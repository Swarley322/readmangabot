import csv

from crud import session
from models import Manga

s = session()

with open('fixtures/manga_list.csv', 'r', encoding='utf-8', newline='') as f:
    fields = ['manga_title', 'manga_url', 'manga_img', 'genre_list']
    manga_list = csv.DictReader(f, fields, delimiter=';')
    for manga in manga_list:
        manga_exists = s.query(Manga).filter_by(title=manga['manga_title']).count()
        if manga_exists == 0:
            new_manga = Manga(
                title=manga['manga_title'],
                url=manga['manga_url'],
                img_url=manga['manga_img']
            )
            s.add(new_manga)
            s.commit()
            s.close()
        else:
            continue
