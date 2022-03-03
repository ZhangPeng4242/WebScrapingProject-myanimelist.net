"""
we create a function to scrap all people list paages in myanimelist and get all links for specific people pages.
"""
import math
import time
from bs4 import BeautifulSoup
# import grequests
import requests
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import random
from config import config


def get_anime_links(_crit=math.inf):
    """
    scraps the anime list pages of myanimelist
    and returns a list of all links for anime main pages on myanimelist.
    receives an optional argument set by default to infinity of how many peoples list pages to scrap.
    :param _crit: int
    :return: anime_link_list: list
    """
    # loops over all people list pages up to the value of the integer _crit (which is by default infinity)
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
                                              timeout=100)
                    break
                except Exception:
                    config.logger.warning(f"scrap_anime_list_page: Change proxy... {anime_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        # creates beautiful soup object
        soup = BeautifulSoup(anime_list_page.text, "html.parser")

        # we check our current page is indeed an anime list page
        if not soup.find('tr', class_="ranking-list"):
            # If not found, it might be we reached the end, or it might be due to the proxy is blocked, or the proxy activates the mobile version of the web,

            if soup.find('h1', string="404 Not Found"):
                break
            config.logger.error(f"scrap_anime_list_page: Failed, re-scraping... {anime_search_link} ")
            continue

        # reaching here means we are scraping a true people list page, and can start getting our main anime page links.
        a_tag_list = soup.find_all('a', class_="fl-l")
        anime_link_list += [link['href'] for link in a_tag_list]
        config.logger.info(f"scrap_anime_list_page: Success! {anime_search_link} ")
        limit += 1

    config.logger.info(
        f"Successfully get all the links of anime page! Total number of anime links: {len(anime_link_list)}")

    return anime_link_list


def test():
    people_list = get_anime_links(2)
    print(len(people_list))
    print(people_list)


if __name__ == "__main__":
    test()
