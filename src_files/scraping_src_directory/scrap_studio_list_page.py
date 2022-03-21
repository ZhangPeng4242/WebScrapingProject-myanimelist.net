"""
we create a function to scrap all people list paages in myanimelist and get all links for specific people pages.
"""
import math
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
from src_files.config import config
import re
import reformat


def scrap_studio_info(_crit=math.inf):
    """
    scraps the anime list pages of myanimelist
    and returns a list of all links for anime main pages on myanimelist.
    receives an optional argument set by default to infinity of how many peoples list pages to scrap.
    :param _crit: int
    :return: anime_link_list: list
    """
    # loops over all people list pages up to the value of the integer _crit (which is by default infinity)
    studios_info = []
    limit = 0
    loop = 0
    while limit < _crit:
        studio_search_link = f"https://myanimelist.net/company?limit={limit * 50}"
        with requests.Session() as res:
            # requests page content using random proxy and header
            while True:
                try:
                    studio_list_page = res.get(studio_search_link,
                                               proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                               timeout=100)
                    break
                except Exception:
                    config.logger.warning(f"scrap_anime_list_page: Change proxy... {studio_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        # creates beautiful soup object
        soup = BeautifulSoup(studio_list_page.text, "html.parser")

        # Check if we have reached to the end.
        if not soup.find('tr', class_="ranking-list"):
            # If not found, it might be we reached the end, or it might be due to the proxy is blocked, or the proxy activates the mobile version of the web,
            if loop > 3:
                break
            loop += 1
            config.logger.info(
                f"scrap_studios_info: Search end check, attempt {loop}, rescraping... {studio_search_link}.")
            time.sleep(5)
            continue

        # reaching here means we are scraping a true people list page, and can start getting our main anime page links.
        studio_table_list = soup.find_all('tr', class_="ranking-list")
        for studio_table in studio_table_list:
            studio_id = int(re.findall("(?<=/anime/producer/)[0-9]*", studio_table.a['href'])[0])
            studio_name = studio_table.div.a.text.strip()
            studio_rank = int(studio_table.find('span', class_="top-anime-rank-text").text.strip())
            studio_favorites = int(studio_table.find('td', class_="favorites").text.strip().replace(",", ""))
            studio_img_url = studio_table.a.img["data-src"]
            studios_info.append({"studio_id": studio_id, "studio_name": studio_name, "studio_rank": studio_rank,
                                 "studio_favorites": studio_favorites, "studio_img_url": studio_img_url})
        limit += 1
        loop = 0
        config.logger.info(f"Successfully get all the info of studios on this page: {studio_search_link}")

    formatted_studio_data = reformat.format_studio_data(studios_info)
    return formatted_studio_data

