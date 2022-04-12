"""
This module is to scrap imdb score.
:export: scrap_imdb_score
"""
import time
from bs4 import BeautifulSoup
import requests
from src_files.config import config
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_proxy, get_rand_headers
import numpy as np


def scrap_imdb_score(imdb_link):
    """
    This function is to scrap the score from a given imdb page.
    :param imdb_link: the link of the imdb page
    :return: tuple, (imdb_title, imdb_score,imdb_year)
    """
    with requests.Session() as res:
        while True:
            try:
                imdb = res.get(imdb_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                               timeout=config.timeout)
                break
            except Exception:
                config.logger.warning(f"scrap_anime_page: Change proxy... {imdb_link}")
                time.sleep(config.proxy_change_delay)
                continue

    imdb_soup = BeautifulSoup(imdb.text, 'html.parser')
    temp = imdb_soup.find(attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    if not temp:
        raise Exception("Anime not found on IMDB")
    imdb_score = temp.find('span')
    imdb_score = float(imdb_score.text) if imdb_score else np.nan

    imdb_title = imdb_soup.find('h1', attrs={'data-testid': "hero-title-block__title"})
    imdb_title = imdb_title.text if imdb_title else ""

    imdb_year = imdb_soup.find('li', attrs={"role": "presentation",
                                            "class": "ipc-inline-list__item"}).find_next_sibling().find('span')
    imdb_year = int(imdb_year.text.split("–")[0]) if imdb_year else 0
    config.logger.info(f"scrap_imdb_score: Success! {imdb_link}")

    return (imdb_title, imdb_score, imdb_year)
