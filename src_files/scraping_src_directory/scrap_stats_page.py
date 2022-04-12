"""
This module is to scrap data from the anime stats page on myanimelist.net
:export: scrap_stats_page
"""
import requests
from bs4 import BeautifulSoup
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
from src_files.config import config
import src_files.scraping_src_directory.reformat as reformat

SUM_STATS_CONTAINERS_COUNT = 6


def scrap_stats_page(stats_link):
    """
    This function is to scrap all the information we need on the stats page of the anime with the given link.
    Also it formats the data according to the database table requirements.
    Relavant tables: anime_watch_stats, anime_score_stats
    :param stats_link: the link for the anime stats page
    :return: DataFrame: formatted_anime_watch_stats_data, formatted_anime_score_stats_data
    """
    with requests.Session() as res:
        while True:
            try:
                stats_page = res.get(stats_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=config.timeout)
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

    config.logger.info(f"scrap_anime_stats_page: Success! {stats_link}")
    return (formatted_anime_watch_stats_data, formatted_anime_score_stats_data)
