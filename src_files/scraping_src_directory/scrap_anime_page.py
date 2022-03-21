"""
we create a function that receives a url for an anime main page in myanimelist and scraps it
"""
import re
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers
from src_files.config import config
import reformat
from src_files.mysql_db_src_directory.update_db import update_anime_page_data
from scrap_stats_page import scrap_stats_page
import numpy as np


def scrap_anime_page(anime_page_link):
    """
    This function scraps all the information we need from the main page of an anime.
    From this page, we can scrap information for the database tables: [anime],[genre],[anime_genre],[studio_anime],[anime_general_info]

    it returns three dictionaries which will later be inserted into the following Datasets:
    anime_page_info: contains anime_id, title, type, anime_img_url,aired, premiered, studios, source, genres, rating and theme
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
    anime_page_info["id"] = int(soup.find('input', {'name': 'aid'})['value'])
    anime_page_info["title"] = soup.find('h1', class_="title-name").text
    en_title = soup.find("p", class_="title-english")
    anime_page_info["english_title"] = en_title.text if en_title else None

    studio_containers = soup.find('span', string="Studios:").find_next_siblings('a', {
        "href": re.compile("/anime/producer/")})
    studio_ids = [int(re.findall("(?<=/anime/producer/)[0-9]*", studio['href'])[0]) for studio in
                  studio_containers] if len(
        studio_containers) > 0 else []
    anime_page_info["studios"] = studio_ids

    info_containers = soup.find_all('span',
                                    string=['Type:', 'Genres:', 'Genre:', 'Aired:', 'Premiered:', 'Source:',
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
        anime_page_info['img_url'] = img_url['data-src'] if img_url else None

    # Scrap anime site stats
    site_stats = {}
    site_stats["id"] = anime_page_info["id"]

    site_stats["score"] = soup.find('span', class_="score-label").text
    site_stats["rating_count"] = soup.find('span', {"itemprop": "ratingCount"}).text if site_stats[
                                                                                            "score"] != 'N/A' else np.nan
    site_stats["score"] = np.nan if site_stats["score"] == "N/A" else site_stats["score"]

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

    # Now, we have all the information we need.
    # The next step is to format all the datas into the database format.

    formatted_anime_data = reformat.format_anime_data(anime_page_info)
    formatted_anime_general_stats_data = reformat.format_anime_general_stats_data(site_stats)
    formatted_anime_genre_data = reformat.format_anime_genre_data(anime_page_info)
    formatted_studio_anime_data = reformat.format_studio_anime_data(anime_page_info)
    # if not exists then
    update_anime_page_data(formatted_anime_data, formatted_anime_general_stats_data, formatted_anime_genre_data,
                           formatted_studio_anime_data)

    config.logger.info(f'scrap_anime_page: Success! {anime_page_link}')

    #update stats link as well
    scrap_stats_page(anime_page_link + '/stats')

    return (
        formatted_anime_data, formatted_anime_general_stats_data, formatted_anime_genre_data,
        formatted_studio_anime_data)


result = scrap_anime_page("https://myanimelist.net/anime/40834/Ousama_Ranking")

# print(result[0])
