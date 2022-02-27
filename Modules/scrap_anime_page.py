import math
import random
import re
import time

from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers

#imge not exists problem, scrap_anime_page: https://myanimelist.net/anime/21607/Picotopia 'NoneType' object is not subscriptable
#only genre, themes prob
#add aired field
#filename should we add timestamp?

def scrap_anime_page(anime_page_link):
    """This function is to scrap all the information we need from the anime page.
    Datasets:
        anime_page_info:
    """

    with requests.Session() as res:
        while True:
            try:
                anime_page = res.get(anime_page_link, proxies={"http": "192.177.186.60:3128"}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                print("scrap_anime_page: Change proxy...")
                time.sleep(0.5)
                continue

    soup = BeautifulSoup(anime_page.text, 'html.parser')

    # Scrap anime_page_info section
    anime_page_info = {}
    anime_page_info["anime_id"] = soup.find('input', {'name': 'aid'})['value']
    anime_page_info["title"] = soup.find('h1', class_="title-name").text

    info_containers = soup.find_all('span', string=['Type:', 'Genres:', 'Genre:', 'Aired:', 'Premiered:', 'Studios:', 'Source:', 'Theme:',
                                                    'Rating:'])

    for info_container in info_containers:
        info_list = info_container.parent.text.split(":")
        # index 0: info key, index 1: info value
        key, value = info_list
        key = key.strip()

        if key in ["Genres","Genre", "Theme"]:
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
            continue

        site_stats[key.lower()] = val.replace(",", "").replace("#", "").strip()

    print(f'scrap_anime_page: {anime_page_link}  Success!')

    return (anime_page_info, alternative_titles, site_stats)


def test():
    test_pool = [
        "https://myanimelist.net/anime/246/Groove_Adventure_Rave"
    ]

    print("\n".join(str(stat) for stat in scrap_anime_page(random.choice(test_pool))))


if __name__ == "__main__":
    test()
