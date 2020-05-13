# -*- coding: utf-8 -*-
import time
from datetime import date

from crud import session
from models import Subscribers, Tracking, Manga

from parser.manga_parser import get_chapters_value, get_html, \
                                get_random_sleep_time

s = session()


def get_active_tracking_manga():
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


def check_manga_in_tracking(manga_id):
    """returns True if manga in Tracking table"""
    manga_exist = s.query(Tracking).filter_by(manga_id=manga_id).count()
    s.close()
    if manga_exist == 0:
        return False
    return True


def insert_manga_in_tracking(manga_id):
    """Inserts manga in Tracking table"""
    time.sleep(get_random_sleep_time())
    manga_url = s.query(Manga).filter_by(id=manga_id).first().url
    html = get_html(manga_url)
    chapters = get_chapters_value(html)
    new_manga = Tracking(
        manga_id=manga_id,
        update_date=date.today(),
        chapters=chapters,
        number_of_chapters=len(chapters)
    )
    s.add(new_manga)
    s.commit()
    s.close()
    return True


def search_manga_titles(title):
    manga_list = s.query(Manga).all()
    s.close()
    result = []
    for manga in manga_list:
        if title.strip().lower() in manga.title.lower():
            result.append({
                'title': manga.title,
                'id': manga.id
                })
    return result


def get_manga_title(manga_id):
    manga_title = s.query(Manga).filter_by(id=manga_id).first().title
    s.close()
    return manga_title


def get_manga_chapters_value(manga_id):
    chapters = s.query(Tracking).filter_by(manga_id=manga_id).first()
    s.close()
    return chapters.number_of_chapters
