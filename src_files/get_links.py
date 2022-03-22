import sqlalchemy
import pandas as pd
from src_files.config import config
from bs4 import BeautifulSoup
import requests
import datetime
from src_files.scraping_src_directory.scrap_anime_list_page import get_anime_links
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy

THIS_YEAR = datetime.date.today().year
YEAR_LINKS = [f'https://myanimelist.net/anime/season/{THIS_YEAR}/summer',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/winter',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/fall',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/spring']


def get_anime_link_by_name(name):
    name = name.lower()
    name = name.strip()

    df = pd.read_sql_table("anime", config.engine)
    df['title'] = df['title'].apply(lambda x: x.lower() if x else x)
    df['english_title'] = df['english_title'].apply(lambda x: x.lower() if x else x)

    link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['title'] == name]['id']]

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
        link_list = [f'https://myanimelist.net/anime/{id}' for id in
                     df[df['start_air'].apply(lambda x: x.year) == year]['id']]

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
    anime_link_list = []
    limit = 0
    _crit = 1 + rank // 50
    while limit < _crit:
        anime_search_link = f"https://myanimelist.net/topanime.php?limit={limit * 50}"
        with requests.Session() as res:
            # requests page content using random proxy and header
            while True:
                try:
                    anime_list_page = res.get(anime_search_link,
                                              proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                              timeout=100)
                    break
                except Exception:
                    config.logger.warning(f"scrap_anime_list_page: Change proxy... {anime_search_link}")
                    time.sleep(config.proxy_change_delay)
                    continue

        # creates beautiful soup object
        soup = BeautifulSoup(anime_list_page.text, "html.parser")

        # we check our current page is indeed an anime list page
        if not soup.find('tr', class_="ranking-list"):
            # If not found, it might be we reached the end, or it might be due to the proxy is blocked, or the proxy activates the mobile version of the web,

            if soup.find('h1', string="404 Not Found"):
                break
            config.logger.error(f"scrap_anime_list_page: Failed, re-scraping... {anime_search_link} ")
            continue

        # reaching here means we are scraping a true people list page, and can start getting our main anime page links.
        a_tag_list = soup.find_all('a', class_="fl-l")
        anime_link_list += [link['href'] for link in a_tag_list]
        # config.logger.info(f"scrap_anime_list_page: Success! {anime_search_link} ")
        limit += 1
    config.logger.info(f'retreived top {rank} anime links')
    return anime_link_list[:rank]


def get_anime_by_genre(genre):
    # genre_links_dict = {}
    # genre_list = list(pd.read_sql_table("genre", config.engine)['name'])
    # genre_list.sort()
    # index = 1
    # for g in genre_list:
    #     genre_links_dict[g] = f'https://myanimelist.net/anime/genre/{index}/{g}'
    #     index += 1
    # genre_link = genre_links_dict[genre]

    df = pd.read_sql_table("genre", config.engine)
    genre_id = list(df[df['name'] == genre]['id'])[0]
    df = pd.read_sql_table("anime_genre", config.engine)
    genre_links = [f'https://myanimelist.net/anime/{id}' for id in  df[df['genre_id'] == genre_id]['anime_id']]
    return genre_links


def get_anime_by_studio(studio):
    df = pd.read_sql_table("studio", config.engine)
    studio_id = list(df[df['name'] == studio]['id'])[0]
    df = pd.read_sql_table("studio_anime", config.engine)
    studio_links = [f'https://myanimelist.net/anime/{id}' for id in df[df['studio_id'] == studio_id]['anime_id']]
    return studio_links

print(get_anime_by_studio('A-1 Pictures'))