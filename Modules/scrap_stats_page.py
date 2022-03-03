import requests
from bs4 import BeautifulSoup
import random
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
SUM_STATS_CONTAINERS_COUNT = 6


def scrap_stats_page(stats_link):
    """Data:
     summary stats: watching, completed, on-hold, dropped, Plan to Watch, Total
     score stats: 10 - 1 votes
     """
    with requests.Session() as res:
        while True:
            try:
                stats_page = res.get(stats_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                print("scrap_stats_page: Change proxy...")
                time.sleep(0.5)
                continue

    soup = BeautifulSoup(stats_page.text, "html.parser")

    # Get id
    anime_id = soup.find('input', {'name': 'aid'})['value']

    # Scraping summary stats
    sum_stats_containers = soup.find('h2', string='Summary Stats').find_next_siblings('div',
                                                                                      limit=SUM_STATS_CONTAINERS_COUNT)

    sum_stats = {stat[0].lower(): int(stat[1].replace(",", "")) for stat in
                 [stat_container.text.split(": ") for stat_container in sum_stats_containers]}

    sum_stats["anime_id"] = anime_id

    # Scrapping score stats
    score_stats_containers = soup.find('table', {"class": 'score-stats'})

    score_stats = {"anime_id":anime_id}|{str(num):None for num in range(10,0,-1)}

    if score_stats_containers:
        for stat in score_stats_containers.find_all('tr'):
            score = stat.find('td', {"class": "score-label"}).text
            votes = int(stat.find('small').text[1:-7])
            score_stats[score] = votes
    print(f"scrap_stats_page: {stats_link}  Success!")


    # store data
    return (sum_stats, score_stats)


def test():
    test_pool = [
                 "https://myanimelist.net/anime/19815/No_Game_No_Life/stats"]

    print(scrap_stats_page(random.choice(test_pool)))


if __name__ == "__main__":
    test()
