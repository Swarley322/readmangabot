import random
import re
import time
import json

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


readmanga_url = "https://readmanga.me/list?sortType=rate&offset={page}"
mintmanga_url = "https://mintmanga.live/list?sortType=rate&offset={page}"
mintmanga = "https://mintmanga.live"
readmanga = "https://readmanga.me"


def get_mangas_from_page(html, site):
    soup = BS(html, "html.parser")
    manga_list = soup.find_all('div', class_="tile col-sm-6")
    for manga in manga_list:
        try:
            name = manga.find('div', class_="desc").find("h3").find('a')["title"]
            url = site + manga.find('div', class_="desc").find("h3").find('a')["href"]
            img = manga.find('div', class_="img").find('img')["data-original"]
            # eng_name = manga.find('div', class_="desc").find("h4")['title']
            yield {
                "title": name,
                "url": url,
                "img": img,
            }
        except (KeyError, AttributeError):
            continue


def parse_all_pages(url, pages, site):
    result = []
    for page in range(0, pages, 70):
        my_url = url.format(page=page)
        html = get_html(my_url)
        for manga in get_mangas_from_page(html, site):
            result.append(manga)
        print(len(result))
        with open('manga_list.json', 'w') as f:
            json.dump(result, f, ensure_ascii=False)
        time.sleep(get_random_sleep_time())


def get_chapters_value(html):
    '''returns list of chapters or "no chapters"'''
    soup = BS(html, "html.parser")
    try:
        chapters = soup.find('table', class_="table table-hover").find_all('tr')[1:]
    except AttributeError:
        return "no chapters"
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


if __name__ == "__main__":
    # parse_all_pages(mintmanga_url, 12600, mintmanga)
    g = "https://mintmanga.live/vtorjenie_gigantov"
    html = get_html(g)
    print(get_chapters_value(html))
