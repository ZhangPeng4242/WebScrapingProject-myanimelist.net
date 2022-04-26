"""
This module is to scrap the page that contains the people main page links and get the links.
:export: get_people_links(_crit=math.inf)
"""
import math
import time
from bs4 import BeautifulSoup
import requests
import random
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
from src_files.config import config

# The numer is the number of chances we give for a failed scrap which might be resulted in proxy being blocked, different versions returned.
# We give these chances to confirm that the failure is indeed failed other than the problems mentioned above or we have reached till the end.
CONFIRMATION_LOOP_NUMBER = 3

def get_people_links(_crit=math.inf):
    """
    This function scraps the myanimelist people list webpages which contain lists of people main page links. Each page contain 50 links.
    :param _crit: int, the critical point for the scraping indicating when we want to stop. 2 means we scrap two pages, 100 anime links.
    :return: people_link_list: list, the list of people main page links
    """
    config.logger.info("Start scraping and retrieving the people links...")

    # loops over the people list pages up to the value of the integer _crit (which is by default infinity), so that we can get all the links of the people.
    people_link_list = []
    limit = 0
    loop = 0
    while limit < _crit:
        people_search_link = f"https://myanimelist.net/people.php?limit={limit * 50}"
        with requests.Session() as res:
            # requests page content using random proxy and header
            while True:
                try:
                    people_list_page = res.get(people_search_link,
                                               proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                               timeout=config.timeout)
                    break
                except Exception:
                    config.logger.warning(f"scrap_people_list_page: Change proxy... {people_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        soup = BeautifulSoup(people_list_page.text, "html.parser")

        # We check we indeed reach the end of the list. Use loops to double confirm that soup not found is not caused by proxy being blocked or requested the mobile version
        if not soup.find('a', class_="fs14"):
            if loop > CONFIRMATION_LOOP_NUMBER:
                break
            loop += 1
            config.logger.info(
                f"scrap_people_list_page: Search end check, attempt: {loop}, rescraping... {people_search_link}.")
            time.sleep(config.rescrap_delay)
            continue

        # reaching here means we have the valid people list page
        a_tag_list = soup.find_all('a', class_="fs14")
        people_link_list += [link['href'] for link in a_tag_list]
        config.logger.info(f"scrap_people_list_page: Success! {people_search_link}")
        limit += 1
        loop = 0
        time.sleep(config.delay_after_request * random.random())
    config.logger.info(
        f"Successfully get all the links of people page! Total number of people page links: {len(people_link_list)}")

    return people_link_list
