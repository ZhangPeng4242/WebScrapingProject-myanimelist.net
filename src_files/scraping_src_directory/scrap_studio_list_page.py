"""
This module is to scrap the page that contains the list of studios and get the studio info.
:export: get_studio_info(_crit=math.inf)
"""
import math
import time
from bs4 import BeautifulSoup
import requests
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
from src_files.config import config
import re
import src_files.scraping_src_directory.reformat as reformat

# The numer is the number of chances we give for a failed scrap which might be resulted in proxy being blocked, different versions returned.
# We give these chances to confirm that the failure is indeed failed other than the problems mentioned above or we have reached till the end.
CONFIRMATION_LOOP_NUMBER = 3


def scrap_studio_info(_crit=math.inf):
    """
    This function scraps the myanimelist company webpages which contain lists of studio links. Each page contain 50 links.
    But instead of scraping the links, there's already enough studio info we want from the list, therefore we directly scrap the info.
    Relavant tables: studio.
    :param _crit: int, the critical point for the scraping indicating when we want to stop. 2 means we scrap two pages, 100 anime links.
    :return: DataFrame: formatted_studio_data
    """
    # loops over all studio list pages up to the value of the integer _crit (which is by default infinity)
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
                                               timeout=config.timeout)
                    break
                except Exception:
                    config.logger.warning(f"scrap_anime_list_page: Change proxy... {studio_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        soup = BeautifulSoup(studio_list_page.text, "html.parser")

        # Check if we have reached to the end.
        if not soup.find('tr', class_="ranking-list"):
            # If not found, it might be we reached the end, or it might be due to the proxy is blocked, or the proxy activates the mobile version of the web,
            if loop > CONFIRMATION_LOOP_NUMBER:
                break
            loop += 1
            config.logger.info(
                f"scrap_studios_info: Search end check, attempt {loop}, rescraping... {studio_search_link}.")
            time.sleep(config.rescrap_delay)
            continue

        # reaching here means we are scraping a valid studio list page, and we scrap the information we need from this page.
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
