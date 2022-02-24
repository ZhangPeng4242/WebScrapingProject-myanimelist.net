import requests
from bs4 import BeautifulSoup
import random
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy

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
                                     timeout=40)
                break
            except Exception:
                print("Stats_page: Change proxy...")
                continue

    soup = BeautifulSoup(stats_page.text, "html.parser")

    # Get id
    anime_id = soup.find('input', {'name': 'aid'})['value']

    # Scraping summary stats
    sum_stats_containers = soup.find('h2', string='Summary Stats').find_next_siblings('div',
                                                                                      limit=SUM_STATS_CONTAINERS_COUNT)

    sum_stats = {stat[0]: int(stat[1].replace(",", "")) for stat in
                 [stat_container.text.split(": ") for stat_container in sum_stats_containers]}

    sum_stats["anime_id"] = anime_id

    # Scrapping score stats
    score_stats_containers = soup.find('table', {"class": 'score-stats'}).find_all('tr')
    score_stats = {}

    for stat in score_stats_containers:
        score = stat.find('td', {"class": "score-label"}).text
        votes = int(stat.find('small').text[1:-7])
        score_stats[score] = votes

    score_stats["anime_id"] = anime_id

    print(f"scrap_stats_page: {stats_link}  Success!")
    # store data
    return (sum_stats, score_stats)


def test():
    test_pool = ["https://myanimelist.net/anime/47161/Shikkakumon_no_Saikyou_Kenja/stats",
                 "https://myanimelist.net/anime/44961/Platinum_End/stats",
                 "https://myanimelist.net/anime/18179/Yowamushi_Pedal/stats",
                 "https://myanimelist.net/anime/37987/Violet_Evergarden_Movie/stats"]

    print(scrap_stats_page(random.choice(test_pool)))


if __name__ == "__main__":
    test()
