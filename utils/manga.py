# -*- coding: utf-8 -*-
import time
from datetime import date

from db.base import s
from db.models import Readmanga, Mintmanga

from parser.manga_parser import get_chapters_value, get_html, \
                                get_random_sleep_time


def update_manga(manga_site, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    returns False if manga has no chapters
    or returns True
    """
    time.sleep(get_random_sleep_time())
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
    elif manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()

    if manga.update_date != date.today() or manga.update_date is None:
        html = get_html(manga.url)
        chapters = get_chapters_value(html)
        if chapters == "no chapters":
            return False
        manga.chapters = chapters
        manga.update_date = date.today()
        manga.number_of_chapters = len(chapters)
        s.commit()
    return True


def search_manga_titles(manga_site, title):
    """
    manga_site - 'readmanga' or 'mintmanga'
    returns list of titles
    """
    if manga_site == 'readmanga':
        manga_list = s.query(Readmanga).all()
    elif manga_site == 'mintmanga':
        manga_list = s.query(Mintmanga).all()
    result = []
    for manga in manga_list:
        if title.strip().lower() in manga.title.lower():
            result.append({
                'title': manga.title,
                'id': manga.id
                })
    return result


def get_manga_title(manga_site, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    returns manga title
    """
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
    if manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
    return manga.title


def get_manga_chapters_value(manga_site, manga_id):
    """
    manga_site - 'readmanga' or 'mintmanga'
    """
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
    if manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
    return manga.number_of_chapters


def delete_manga(manga_site, manga_id):
    """
    deletes manga from readmanga or mintmanga tables
    """
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
    if manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
    s.delete(manga)
    s.commit()


def get_manga_chapters(manga_site, manga_id):
    if manga_site == 'readmanga':
        manga = s.query(Readmanga).filter_by(id=manga_id).first()
    if manga_site == 'mintmanga':
        manga = s.query(Mintmanga).filter_by(id=manga_id).first()
    return manga.chapters


def check_exists_manga_id(manga_id):
    pass


class MangaInfo():
    def __init__(self, manga_id, session):
        self.id = manga_id
        self.info = session.query(Manga).filter_by(id=manga_id).first()
        session.close()

    def delete(self):
        pass
