import time
from db.base import s
# from db.models import Tracking, Subscribers
from utils.manga import check_manga_in_tracking, update_manga_in_tracking, \
                        get_chapters_value
from parser.manga_parser import get_random_sleep_time


def get_active_tracking_manga_id():
    """returns set of active tracking manga or False"""
    active_users_list = [user for user in s.query(Subscribers).all() if user.active and user.tracking_list]
    s.close()
    if active_users_list:
        set_manga_id = set()
        for user in active_users_list:
            for manga_id in user.tracking_list:
                set_manga_id.add(manga_id)
        return set_manga_id
    return False


def update_all_active_mangas(context):
    manga_id_list = get_active_tracking_manga_id()
    if manga_id_list:
        for manga_id in manga_id_list:
            chapters_before = get_chapters_value(manga_id)
            updated_manga = check_manga_in_tracking(manga_id)
            if updated_manga == "not up to date":
                update_manga_in_tracking(manga_id)
                manga = s.query(Tracking).filter_by(manga_id=manga_id).first()
                if chapters_before < manga.chapters:
                    manga.new_chapters = True
                s.close()
                time.sleep(get_random_sleep_time())
        print("all active manga were updated")
    else:
        print("no active manga")


# print(update_all_active_mangas())

def erase_new_chapters(context):
    manga_list = s.query(Tracking).all()
    for manga in manga_list:
        manga.new_chapters = None
        s.commit()
    s.close()
    print("new chapters erased")
