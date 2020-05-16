import csv
import random
import re
import time

import requests

from bs4 import BeautifulSoup as BS


def get_random_sleep_time():
    return random.randint(1, 7)


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    try:
        result = requests.get(url, headers=headers)
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


page = "https://readmanga.me/list?sortType=rate&offset={}"
manga_url = "https://readmanga.me/klinok__rassekaiuchii_demonov"


def get_mangas_from_page(html):
    soup = BS(html, "html.parser")
    manga_list = soup.find_all('div', class_="tile col-sm-6")
    for manga in manga_list:
        try:
            name = manga.find('div', class_="desc").find("h3").find('a')["title"]
            url = "https://readmanga.me" + manga.find('div', class_="desc").find("h3").find('a')["href"]
            img = manga.find('div', class_="img").find('img')["data-original"]
            # eng_name = manga.find('div', class_="desc").find("h4")['title']
            genre_list = [genre.text for genre in manga.find('div', class_="tile-info").find_all('a')]
            yield {
                "manga_title": name,
                "manga_url": url,
                "manga_img": img,
                "genre_list": genre_list
            }
        except (KeyError, AttributeError):
            continue


def parse_all_pages():
    page_url = "https://readmanga.me/list?sortType=rate&offset={page}"
    for page in range(0, 18340, 70):
        url = page_url.format(page=page)
        html = get_html(url)
        with open('manga_list.csv', 'a+', encoding='utf-8', newline='') as f:
            fields = ['manga_title', 'manga_url', 'manga_img', 'genre_list']
            writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
            for manga in get_mangas_from_page(html):
                writer.writerow(manga)
        time.sleep(get_random_sleep_time())


def get_chapters_value(html):
    soup = BS(html, "html.parser")
    chapters = soup.find('table', class_="table table-hover").find_all('tr')[1:]
    result = []
    for chapter in chapters:
        chapter_name = re.sub(r'\s{2,}', " | ", chapter.text.strip().replace('\n', ''))
        try:
            chapter_url = "https://readmanga.me" + chapter.a['href']
        except TypeError:
            continue
        result.append({
            "chapter_name": chapter_name,
            "chapter_url": chapter_url
        })
    return result
