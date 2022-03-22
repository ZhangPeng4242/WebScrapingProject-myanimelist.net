"""
we create a function that scraps the people list pages of myanimelist for links to all people page links.
"""
import math
import time
from bs4 import BeautifulSoup
import requests
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
from src_files.config import config


def get_people_links(_crit=math.inf):
    """
    scraps the people list pages of myanimelist
    and returns a list of all links for people main pages on myanimelist.
    receives an optional argument set by default to infinity of how many peoples list pages to scrap.
    :param _crit: int
    :return: people_link_list: list
    """
    # loops over all people list pages up to the value of the integer _crit (which is by default infinity)
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
                                               timeout=100)
                    break
                except Exception:
                    config.logger.warning(f"scrap_people_list_page: Change proxy... {people_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        # creates beautiful soup object
        soup = BeautifulSoup(people_list_page.text, "html.parser")

        # We check we indeed reach the end of the list. Use loops to double confirm that soup not found is not caused by proxy being blocked or requested the mobile version
        if not soup.find('a', class_="fs14"):
            if loop > 3:
                break
            loop += 1
            config.logger.info(
                f"scrap_people_list_page: Search end check, attempt: {loop}, rescraping... {people_search_link}.")
            time.sleep(5)
            continue

        # reaching here means we are scraping a true people list page, and can start getting our main anime page links.
        a_tag_list = soup.find_all('a', class_="fs14")
        people_link_list += [link['href'] for link in a_tag_list]
        config.logger.info(f"scrap_people_list_page: Success! {people_search_link}")
        limit += 1
        loop = 0

    config.logger.info(
        f"Successfully get all the links of people page! Total number of people page links: {len(people_link_list)}")

    return people_link_list
