# -*- coding: utf-8 -*-
import time
from datetime import date

from crud import s
from models import Tracking, Manga

from parser.manga_parser import get_chapters_value, get_html, \
                                get_random_sleep_time


def check_manga_in_tracking(manga_id):
    """returns True if manga in Tracking table"""
    manga = s.query(Tracking).filter_by(manga_id=manga_id)
    s.close()
    if manga.count() == 0:
        return False
    elif manga.first().update_date != date.today():
        return "not up to date"
    return True


def add_manga_in_tracking(manga_id):
    """adds manga in Tracking table"""
    time.sleep(get_random_sleep_time())
    manga_url = s.query(Manga).filter_by(id=manga_id).first().url
    html = get_html(manga_url)
    chapters = get_chapters_value(html)
    if chapters == "no chapters":
        return False
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


def update_manga_in_tracking(manga_id):
    time.sleep(get_random_sleep_time())
    manga_url = s.query(Manga).filter_by(id=manga_id).first().url
    s.close()
    html = get_html(manga_url)
    chapters = get_chapters_value(html)
    if chapters == "no chapters":
        return False
    manga = s.query(Tracking).filter_by(manga_id=manga_id).first()
    manga.chapters = chapters
    manga.update_date = date.today()
    manga.number_of_chapters = len(chapters)
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


def delete_manga(manga_id):
    manga = s.query(Manga).filter_by(id=manga_id).first()
    s.delete(manga)
    s.commit()
    s.close()


def get_manga_chapters(manga_id):
    manga = s.query(Tracking).filter_by(manga_id=manga_id).first()
    s.close()
    return manga.chapters
