import random
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
def get_anime_links(season_link):
    # get urls from seasonal page
    with requests.Session() as res:
        while True:
            try:
                season_page = res.get(season_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                      timeout=100)
                break
            except Exception:
                print("scrap_season_page: Change proxy...")
                time.sleep(0.5)
                continue

    season_soup = BeautifulSoup(season_page.content, 'html.parser')

    a_tag_list = season_soup.find_all('a', class_="link-title")
    anime_link_set = {a['href'] for a in a_tag_list}

    print(f"get_anime_links: {season_link}  Success!")
    return anime_link_set


def test():
    test_pool = ["https://myanimelist.net/anime/season/2010/summer", "https://myanimelist.net/anime/season/1986/spring",
                 "https://myanimelist.net/anime/season/2000/fall", "https://myanimelist.net/anime/season/1996/winter"]
    print(get_anime_links(random.choice(test_pool)))


if __name__ == "__main__":
    test()
