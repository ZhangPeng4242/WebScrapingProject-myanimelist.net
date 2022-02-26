import math
import time
from bs4 import BeautifulSoup
import requests
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import random

def get_people_links(_crit=math.inf):
    people_link_list = []
    limit = 0
    while limit < _crit:
        with requests.Session() as res:
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

        soup = BeautifulSoup(people_list_page.text, "html.parser")

        if not soup.find('td', class_="people"):
            break

        a_tag_list = soup.find_all('a', class_="fs14")
        people_link_list += [link['href'] for link in a_tag_list]
        limit += 1
        print(f"scrap_people_list_page: https://myanimelist.net/people.php?limit={limit * 50}  Success!")
        time.sleep(round(random.random() * 4, 1))

    print("Successfully get all the links of people page!")
    return people_link_list


def test():
    people_list = scrap_people_list_page(3)
    print(len(people_list))
    print(people_list)


if __name__ == "__main__":
    test()
