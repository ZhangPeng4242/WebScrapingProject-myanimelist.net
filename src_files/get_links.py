import sqlalchemy
import pandas as pd
from config import config
from bs4 import BeautifulSoup
import requests
import datetime
THIS_YEAR = datetime.date.today().year
YEAR_LINKS =[f'https://myanimelist.net/anime/season/{THIS_YEAR}/summer',
                    f'https://myanimelist.net/anime/season/{THIS_YEAR}/winter',
                    f'https://myanimelist.net/anime/season/{THIS_YEAR}/fall',
                    f'https://myanimelist.net/anime/season/{THIS_YEAR}/spring']



def get_anime_link_by_name(name):
    name = name.lower()
    name = name.strip()

    df = pd.read_sql_table("anime", config.engine)
    df['title'] = df['title'].apply(lambda x: x.lower() if x else x)
    df['english_title'] = df['english_title'].apply(lambda x: x.lower() if x else x)

    link_list =  [f'https://myanimelist.net/anime/{id}' for id in df[df['title']==name]['id']]

    if not link_list:
        link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['english_title'] == name]['id']]

    if not link_list:

        for main_link in YEAR_LINKS:
            page = requests.get(main_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            page_links = soup.find_all('a')
            relevant_links = [link['href'] for link in page_links if name in link.text]
            link_list += relevant_links
            if relevant_links:
                break

    return link_list


# print(get_anime_link_by_name('Shingeki no Kyojin'))
# print(get_anime_link_by_name('attack on titan'))


def get_anime_link_by_year(year):

    if year < THIS_YEAR:
        df = pd.read_sql_table("anime", config.engine)
        link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['start_air'].apply(lambda x: x.year) == year]['id']]

    elif year == THIS_YEAR:
        anime_link_set = set()
        for main_link in YEAR_LINKS:
            page = requests.get(main_link)
            season_soup = BeautifulSoup(page.content, 'html.parser')

            a_tag_list = season_soup.find_all('a', class_="link-title")
            anime_link_set |= {a['href'] for a in a_tag_list}

            print(f"get_anime_links: {season_link}  Success!")
        link_list = list(anime_link_set)
    else:
        return []

    return link_list


# print(get_anime_link_by_year(1998))

def get_anime_by_rank(rank):
    return get_anime_rank(rank)[:rank]