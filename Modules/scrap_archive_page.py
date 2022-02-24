import requests
from bs4 import BeautifulSoup


def get_season_links():
    # get urls from archive page
    page = requests.get('https://myanimelist.net/anime/season/archive')
    soup = BeautifulSoup(page.content, 'html.parser')

    a_tag_list = soup.find('table', class_="anime-seasonal-byseason").find_all('a')
    season_link_set = {a['href'] for a in a_tag_list}

    return season_link_set


def test():
    print(get_season_links())


if __name__ == "__main__":
    test()
