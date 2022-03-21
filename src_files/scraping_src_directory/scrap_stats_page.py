"""
we create a function that receives a url for an anime stats page in myanimelist and scraps it
"""
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
from src_files.config import config
import reformat
from src_files.mysql_db_src_directory.update_db import update_table

SUM_STATS_CONTAINERS_COUNT = 6


def scrap_stats_page(stats_link):
    """
    this function scraps all the informations we need from an anime stats page.
    [anime_score_stats],[anime_watch_stats]
    it returns two dictionaries which will later be inserted into the following Datasets:
    sum stats: contains anime_id and num of people who rated the anime 1 - 10
    score stats: contains anime_id, watching, completed, on-hold, dropped, plan to watch and total
    :param stats_link: str
    :return: (watch_stats, score_stats): tuple of dict
    """
    with requests.Session() as res:
        while True:
            try:
                stats_page = res.get(stats_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                config.logger.warning(f"scrap_anime_stats_page: Change proxy... {stats_link}")
                time.sleep(config.proxy_change_delay)
                continue

    soup = BeautifulSoup(stats_page.text, "html.parser")

    # Get id
    anime_id = int(soup.find('input', {'name': 'aid'})['value'])

    if not soup.find('span', string="Watching:"):
        watch_stats = {"anime_id": anime_id}
    else:
        # Scraping summary stats
        sum_stats_containers = soup.find('h2', string='Summary Stats').find_next_siblings('div',
                                                                                          limit=SUM_STATS_CONTAINERS_COUNT)

        watch_stats = {stat[0].lower(): int(stat[1].replace(",", "")) for stat in
                       [stat_container.text.split(": ") for stat_container in sum_stats_containers]}

        watch_stats["anime_id"] = anime_id

    # Scrapping score stats
    score_stats_containers = soup.find('table', {"class": 'score-stats'})

    score_stats = {str(num): None for num in range(10, 0, -1)}
    score_stats["anime_id"] = anime_id

    if score_stats_containers:
        for stat in score_stats_containers.find_all('tr'):
            score = stat.find('td', {"class": "score-label"}).text
            votes = int(stat.find('small').text[1:-7])
            score_stats[score] = votes

    formatted_anime_watch_stats_data = reformat.format_anime_watch_stats_data(watch_stats)
    formatted_anime_score_stats_data = reformat.format_anime_score_stats_data(score_stats)
    update_table(formatted_anime_watch_stats_data, "anime_id", "anime_watch_stats")
    update_table(formatted_anime_score_stats_data, "anime_id", "anime_score_stats")

    config.logger.info(f"scrap_anime_stats_page: Success! {stats_link}")
    return (formatted_anime_watch_stats_data, formatted_anime_score_stats_data)

# result = scrap_stats_page(
#     "https://myanimelist.net/anime/16498/Shingeki_no_Kyojin/stats")
# # print(result[0], "\n", result[1])
