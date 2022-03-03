"""
we create a function that receives a url for an anime stats page in myanimelist and scraps it
"""
import requests
from bs4 import BeautifulSoup
import random
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
SUM_STATS_CONTAINERS_COUNT = 6


def scrap_stats_page(stats_link):
    """
    this function scraps all the informations we need from an anime stats page.
    it returns two dictionaries which will later be inserted into the following Datasets:
    sum stats: contains anime_id and num of people who rated the anime 1 - 10
    score stats: contains anime_id, watching, completed, on-hold, dropped, plan to watch and total
    :param stats_link: str
    :return: (sum_stats, score_stats): tuple of dict
    """
    with requests.Session() as res:
        while True:
            try:
                stats_page = res.get(stats_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                print("scrap_stats_page: Change proxy...")
                time.sleep(0.5)
                continue

    soup = BeautifulSoup(stats_page.text, "html.parser")

    # Get id
    anime_id = soup.find('input', {'name': 'aid'})['value']

    # Scraping summary stats
    sum_stats_containers = soup.find('h2', string='Summary Stats').find_next_siblings('div',
                                                                                      limit=SUM_STATS_CONTAINERS_COUNT)

    sum_stats = {stat[0].lower(): int(stat[1].replace(",", "")) for stat in
                 [stat_container.text.split(": ") for stat_container in sum_stats_containers]}

    sum_stats["anime_id"] = anime_id

    # Scrapping score stats
    score_stats_containers = soup.find('table', {"class": 'score-stats'})

    score_stats = {str(num): None for num in range(10, 0, -1)}
    score_stats["anime_id"] = anime_id

    if score_stats_containers:
        for stat in score_stats_containers.find_all('tr'):
            score = stat.find('td', {"class": "score-label"}).text
            votes = int(stat.find('small').text[1:-7])
            score_stats[score] = votes
    print(f"scrap_stats_page: {stats_link}  Success!")


    # store data
    return (sum_stats, score_stats)
