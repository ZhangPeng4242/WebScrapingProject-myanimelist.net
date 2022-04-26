"""
This module is to scrap the page that contains the anime_links and get the links.
:export: get_anime_links(_crit=math.inf)
"""
import math
import time
from bs4 import BeautifulSoup
import requests
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
from src_files.config import config
import random



def get_anime_links(_crit=math.inf):
    """
    This function scraps the myanimelist topanime webpages which contain lists of anime links. Each page contain 50 links.
    :param _crit: int, the critical point for the scraping indicating when we want to stop. 2 means we scrap two pages, 100 anime links.
    :return: anime_link_list: list, the list of anime links
    """
    # loops over all anime list pages up to the value of the integer _crit (which is by default infinity)
    config.logger.info("Start scraping and retrieving the anime links...")
    anime_link_list = []
    limit = 0
    while limit < _crit:
        anime_search_link = f"https://myanimelist.net/topanime.php?limit={limit * 50}"
        with requests.Session() as res:
            # requests page content using random proxy and header
            while True:
                try:
                    anime_list_page = res.get(anime_search_link,
                                              proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                              timeout=config.timeout)
                    break
                except Exception:
                    config.logger.warning(f"scrap_anime_list_page: Change proxy... {anime_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        soup = BeautifulSoup(anime_list_page.text, "html.parser")

        # we check our current page is indeed an anime list page
        if not soup.find('tr', class_="ranking-list"):
            # If not found, it might be we reached the end, or it might be due to the proxy is blocked, or the proxy activates the mobile version of the web,

            if soup.find('h1', string="404 Not Found"):
                break

            config.logger.error(f"scrap_anime_list_page: Failed, re-scraping... {anime_search_link} ")
            continue

        # reaching here means we have the valid anime list page
        a_tag_list = soup.find_all('a', class_="fl-l")
        anime_link_list += [link['href'] for link in a_tag_list]
        config.logger.info(f"scrap_anime_list_page: Success! {anime_search_link} ")
        limit += 1
        time.sleep(config.delay_after_request * random.random())

    config.logger.info(
        f"Successfully get all the links of anime page! Total number of anime links: {len(anime_link_list)}")

    return anime_link_list
