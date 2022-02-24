import math
import random
import re
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers


# think of cases where there might have the data, theme, deal with it. Catch error.s

def scrap_anime_page(anime_page_link):
    """This function is to scrap all the information we need from the anime page.
    Datasets:
        anime_page_info:
    """
    with requests.Session() as res:
        while True:
            try:
                anime_page = res.get(anime_page_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                print("Anime_page: Change proxy...")
                continue

    soup = BeautifulSoup(anime_page.text, 'html.parser')

    # Scrap anime_page_info section
    anime_page_info = {}
    anime_page_info["anime_id"] = soup.find('input', {'name': 'aid'})['value']
    anime_page_info["Title"] = soup.find('h1', class_="title-name").text

    info_containers = soup.find_all('span', string=['Type:', 'Genres:', 'Premiered:', 'Studios:', 'Source:', 'Theme:',
                                                    'Rating:'])

    for info_container in info_containers:
        info_list = info_container.parent.text.split(":")
        # index 0: info key, index 1: info value
        key, value = info_list
        key = key.strip()

        if key in ["Genres", "Theme"]:
            anime_page_info[key] = ", ".join([genre.strip()[:math.floor(len(genre.strip()) / 2)] for genre in
                                              value.split(",")])
            continue

        anime_page_info[key] = ", ".join(v.strip() for v in value.split(","))

    # Scrap alternative and english titles
    alternative_titles = {}
    alternative_titles["anime_id"] = anime_page_info["anime_id"]
    alternative_titles["Title"] = anime_page_info["Title"]
    en_title = soup.find("p", class_="title-english")
    alternative_titles["English_title"] = en_title.text if en_title else None

    # Scrap anime site stats
    site_stats = {}
    site_stats["anime_id"] = anime_page_info["anime_id"]

    site_stats["Score"] = soup.find('span', class_="score-label").text
    site_stats["Rating_count"] = soup.find('span', {"itemprop": "ratingCount"}).text if site_stats[
                                                                                            "Score"] != 'N/A' else None

    stats_containers = soup.find_all('span', string=['Ranked:', 'Popularity:', 'Members:', 'Favorites:'])
    for stat_container in stats_containers:
        stat_list = stat_container.parent.text.split(":")
        key, val = stat_list
        key = key.strip()

        if key == "Ranked":
            val_find = re.findall("(?<=#)[0-9]*", val)
            val = val_find[0][:-1] if val_find else None
            continue

        site_stats[key] = val.replace(",", "").replace("#", "").strip()

    print(f'scrap_anime_page: {anime_page_link}  Success!')
    return (anime_page_info, alternative_titles, site_stats)


def test():
    test_pool = [
        "https://myanimelist.net/anime/11757/Sword_Art_Online",
        "https://myanimelist.net/anime/25063/Anime_Roukyoku_Kikou_Shimizu_no_Jirochouden",
        "https://myanimelist.net/anime/111/Corrector_Yui",
        "https://myanimelist.net/anime/38690/Si_Hai_Jing_Qi",
        "https://myanimelist.net/anime/38469/Hanasaku_Kizuna_no_Romantan"
    ]

    print("\n".join(str(stat) for stat in scrap_anime_page(random.choice(test_pool))))


if __name__ == "__main__":
    test()
