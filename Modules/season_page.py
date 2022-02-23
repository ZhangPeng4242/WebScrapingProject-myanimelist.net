import requests
from bs4 import BeautifulSoup


def get_anime_links(season_link):
    # get urls from seasonal page
    season_page = requests.get(season_link)
    season_soup = BeautifulSoup(season_page.content, 'html.parser')

    a_tag_list = season_soup.find_all('a', class_="link-title")
    anime_link_set = {a['href'] for a in a_tag_list}

    print(f"get_anime_links: {season_link}  Success!")
    return anime_link_set
