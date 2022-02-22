import requests
from bs4 import BeautifulSoup

SUM_STATS_CONTAINERS_COUNT = 6


def scrap_stats_page(stats_link):
    """Data:
     summary stats: watching, completed, on-hold, dropped, Plan to Watch, Total
     score stats: 10 - 1 votes
     """

    stats_page = requests.get(stats_link)
    soup = BeautifulSoup(stats_page.text, "html.parser")

    stats_page_data = {}
    stats_page_data["anime_id"] = soup.find('input', {'name': 'aid'})['value']

    # Scraping summary stats
    sum_stats_identifier = soup.find('h2', string='Summary Stats')
    sum_stats_containers = sum_stats_identifier.find_next_siblings('div', limit=SUM_STATS_CONTAINERS_COUNT)

    sum_stats = {stat[0]: int(stat[1].replace(",", "")) for stat in
                 [stat_container.text.split(": ") for stat_container in sum_stats_containers]}

    stats_page_data |= sum_stats

    # Scrapping score stats
    score_stats_table = soup.find('table', {"class": 'score-stats'})
    score_stats_containers = score_stats_table.find_all('tr')
    score_stats = {}
    for stat in score_stats_containers:
        score = stat.find('td', {"class": "score-label"}).text
        votes = int(stat.find('small').text[1:-7])
        score_stats[score] = votes

    stats_page_data['score_votes'] = score_stats

    return stats_page_data


scrap_stats_page("https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2/stats")
