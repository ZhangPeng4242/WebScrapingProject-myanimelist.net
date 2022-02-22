import math

from bs4 import BeautifulSoup
import requests


# think of cases where there might have the data, theme, deal with it. Catch error.

def anime_page_information(anime_page_link):
    anime_page = requests.get(anime_page_link)
    soup = BeautifulSoup(anime_page.text, 'html.parser')

    anime_page_info = {}
    anime_page_info["anime_id"] = soup.find('input', {'name': 'aid'})['value']

    # two methods: 1.find identifier and next siblings 2. use span to find parents

    info_containers = soup.find_all('span', string=['Type:', 'Genres:', 'Premiered:', 'Studios:', 'Source:', 'Theme:',
                                                    'Rating:'])
    # print(info_containers)
    for info_container in info_containers:
        info_list = info_container.parent.text.split(":")
        #index 0: info key, index 1: info value

        info_list[0] = info_list[0].strip()

        if info_list[0] in ["Genres", "Theme"]:
            anime_page_info[info_list[0]] = [genre.strip()[:math.floor(len(genre.strip()) / 2)] for genre in
                                             info_list[1].split(",")]
            continue

        anime_page_info[info_list[0]] = info_list[1].strip()

    print(anime_page_info)


anime_page_information("https://myanimelist.net/anime/9253/Steins_Gate")
