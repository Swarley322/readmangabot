import json
import sys

sys.path = ['.', '..'] + sys.path[1:]

from db.base import s
from db.models import Readmanga, Mintmanga


def import_manga(filename, table):
    with open(filename, 'r') as f:
        data = json.load(f)
        for manga in data:
            manga_exists = s.query(table).filter_by(title=manga['title']).count()
            if manga_exists == 0:
                new_manga = table(
                    title=manga['title'],
                    url=manga['url'],
                    img_url=manga['img_url']
                )
                s.add(new_manga)
                s.commit()
            else:
                continue
# def import_manga(filename, table):
#     with open(filename, 'r') as f:
#         data = json.load(f)
#         for manga in data:
#             new_manga = table(
#                 title=manga['title'],
#                 url=manga['url'],
#                 img_url=manga['img_url']
#             )
#             s.add(new_manga)
#             s.commit()



if __name__ == "__main__":
    import_manga('fixtures/mintmanga.json', Mintmanga)
    import_manga('fixtures/readmanga.json', Readmanga)
