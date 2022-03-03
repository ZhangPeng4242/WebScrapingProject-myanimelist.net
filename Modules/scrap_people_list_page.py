"""
we create a function that scraps the people list pages of myanimelist for links to all people page links.
"""
import math
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import random


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
        with requests.Session() as res:
            # requests page content using random proxy and header
            while True:
                try:
                    people_list_page = res.get(f"https://myanimelist.net/people.php?limit={limit * 50}",
                                               proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                               timeout=100)
                    break
                except Exception:
                    print("scrap_people_list_page: Change proxy...")
                    time.sleep(0.5)
                    continue

        # creates beautiful soup object
        soup = BeautifulSoup(people_list_page.text, "html.parser")

        # we check our current page is indeed a people list page
        if not soup.find('a', class_="fs14"):
            if loop > 2:
                break
            loop += 1
            print(
                f"scrap_people_list_page: Failed https://myanimelist.net/people.php?limit={limit * 50} Rescraping...\nAttempt: {loop} ")
            time.sleep(60)
            continue

        # reaching here means we are scraping a true people list page, and can start getting our main anime page links.
        a_tag_list = soup.find_all('a', class_="fs14")
        people_link_list += [link['href'] for link in a_tag_list]
        print(f"scrap_people_list_page: https://myanimelist.net/people.php?limit={limit * 50}  Success!")
        limit += 1
        loop = 0
        time.sleep(round(random.random() * 4, 1))

    print(f"Successfully get all the links of people page! Length: {len(people_link_list)}")
    return people_link_list


