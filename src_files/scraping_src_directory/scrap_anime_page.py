"""
we create a function that receives a url for an anime main page in myanimelist and scraps it
"""
import re
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers
from src_files.config import config


def scrap_anime_page(anime_page_link):
    """
    This function scraps all the information we need from the main page of an anime.
    it returns three dictionaries which will later be inserted into the following Datasets:
    anime_page_info: contains anime_id, title, type, anime_img_url,aired, premiered, studios, source, genres, rating and theme
    alternative titles: contains anime_id, and english_title
    site_stats: contains anime_id, score, rating_count, ranked, popularity, members, and favorites
    :param anime_page_link: str
    :return: (anime_page_info, alternative_titles, site_stats): tuple of dictionaries
    """

    with requests.Session() as res:
        while True:
            try:
                anime_page = res.get(anime_page_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                config.logger.warning(f"scrap_anime_page: Change proxy... {anime_page_link}")
                time.sleep(config.proxy_change_delay)
                continue

    soup = BeautifulSoup(anime_page.text, 'html.parser')

    # Scrap anime_page_info section
    anime_page_info = {}
    anime_page_info["anime_id"] = soup.find('input', {'name': 'aid'})['value']
    anime_page_info["title"] = soup.find('h1', class_="title-name").text

    info_containers = soup.find_all('span',
                                    string=['Type:', 'Genres:', 'Genre:', 'Aired:', 'Premiered:', 'Studios:', 'Source:',
                                            'Theme:',
                                            'Rating:'])

    for info_container in info_containers:

        info_list = info_container.parent.text.split(":\n")
        # index 0: info key, index 1: info value
        key, value = info_list
        key = key.strip()

        if key in ["Genres", "Genre", "Theme"]:
            key = "Genres" if key == "Genre" else key
            value_a_tags = info_container.parent.find_all('a')
            value = ", ".join(a_tag.text for a_tag in value_a_tags)
            anime_page_info[key.lower()] = value
            continue

        anime_page_info[key.lower()] = ", ".join(v.strip() for v in value.split(","))

        img_url = soup.find('img', {"itemprop": "image"})
        anime_page_info['anime_img_url'] = img_url['data-src'] if img_url else None

    # Scrap alternative and english titles
    alternative_titles = {}
    alternative_titles["anime_id"] = anime_page_info["anime_id"]
    en_title = soup.find("p", class_="title-english")
    alternative_titles["english_title"] = en_title.text if en_title else None

    # Scrap anime site stats
    site_stats = {}
    site_stats["anime_id"] = anime_page_info["anime_id"]

    site_stats["score"] = soup.find('span', class_="score-label").text
    site_stats["rating_count"] = soup.find('span', {"itemprop": "ratingCount"}).text if site_stats[
                                                                                            "score"] != 'N/A' else None

    stats_containers = soup.find_all('span', string=['Ranked:', 'Popularity:', 'Members:', 'Favorites:'])
    for stat_container in stats_containers:
        stat_list = stat_container.parent.text.split(":")
        key, val = stat_list
        key = key.strip()

        if key == "Ranked":
            val_find = re.findall("(?<=#)[0-9]*", val)
            val = val_find[0][:-1] if val_find else None
            site_stats['ranked'] = val
            continue

        site_stats[key.lower()] = val.replace(",", "").replace("#", "").strip()

    config.logger.info(f'scrap_anime_page: Success! {anime_page_link}')

    return (anime_page_info, alternative_titles, site_stats)