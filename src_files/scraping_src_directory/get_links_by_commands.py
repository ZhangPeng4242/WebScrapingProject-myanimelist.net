import sqlalchemy
import pandas as pd
from src_files.config import config
from bs4 import BeautifulSoup
import requests
import datetime
from src_files.scraping_src_directory.scrap_anime_list_page import get_anime_links
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import math
from src_files.scraping_src_directory.scrap_people_list_page import get_people_links

THIS_YEAR = datetime.date.today().year
YEAR_LINKS = [f'https://myanimelist.net/anime/season/{THIS_YEAR}/summer',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/winter',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/fall',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/spring']


def get_anime_link_by_name(name):
    config.logger.info(f'Start scraping anime links: {name}')

    name = name.lower().strip()
    df = pd.read_sql_table("anime", config.engine)
    df['title'] = df['title'].apply(lambda x: x.lower() if x else x)
    df['english_title'] = df['english_title'].apply(lambda x: x.lower() if x else x)

    anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['title'] == name]['id']]

    if not anime_link_list:
        anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['english_title'] == name]['id']]

    if not anime_link_list:

        for main_link in YEAR_LINKS:
            page = requests.get(main_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            page_links = soup.find_all('a')
            relevant_links = [link['href'] for link in page_links if name in link.text]
            anime_link_list += relevant_links
            if relevant_links:
                break
    config.logger.info(f'Successfully retreived all {name} links, total number: {len(anime_link_list)}')
    return anime_link_list


# print(get_anime_link_by_name('Shingeki no Kyojin'))
# print(get_anime_link_by_name('attack on titan'))


def get_anime_link_by_year(year):
    config.logger.info(f'Start scraping anime links at year {year}...')
    if year < THIS_YEAR:
        df = pd.read_sql_table("anime", config.engine)
        anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in
                           df[df['start_air'].apply(lambda x: x.year) == year]['id']]

    elif year == THIS_YEAR:
        anime_link_set = set()
        for main_link in YEAR_LINKS:
            page = requests.get(main_link)
            season_soup = BeautifulSoup(page.content, 'html.parser')

            a_tag_list = season_soup.find_all('a', class_="link-title")
            anime_link_set |= {a['href'] for a in a_tag_list}

            print(f"get_anime_links: {main_link}  Success!")
        anime_link_list = list(anime_link_set)
    else:
        return []
    config.logger.info(f'Successfully retreived all anime links at year {year}, total number: {len(anime_link_list)}')
    return anime_link_list


# print(get_anime_link_by_year(1998))

def get_anime_link_by_rank(rank):
    config.logger.info(f'Start scraping top {rank} anime links...')
    if rank < 0:
        return []
    page_num = 1 + rank // 50
    anime_link_list = get_anime_links(page_num)

    config.logger.info(f'Successfully retreived all the top {rank} anime links.')
    return anime_link_list[:rank]


# result = get_anime_link_by_rank(80)
# print(len(result), result)


def get_anime_link_by_genre(genre):
    # genre_links_dict = {}
    # genre_list = list(pd.read_sql_table("genre", config.engine)['name'])
    # genre_list.sort()
    # index = 1
    # for g in genre_list:
    #     genre_links_dict[g] = f'https://myanimelist.net/anime/genre/{index}/{g}'
    #     index += 1
    # genre_link = genre_links_dict[genre]
    genre = genre.title()
    config.logger.info(f'Start scraping {genre} anime links...')
    df = pd.read_sql_table("genre", config.engine)
    id_list = list(df[df['name'] == genre]['id'])
    if id_list:
        genre_id = id_list[0]
    else:
        return []
    df = pd.read_sql_table("anime_genre", config.engine)
    anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['genre_id'] == genre_id]['anime_id']]
    config.logger.info(f'Successfully retreived all the {genre} anime links. Total number: {len(anime_link_list)}')
    return anime_link_list


def get_anime_link_by_studio(studio):
    config.logger.info(f'Start scraping anime links produced by {studio}...')
    df = pd.read_sql_table("studio", config.engine)
    id_list = list(df[df['name'] == studio]['id'])
    if id_list:
        studio_id = id_list[0]
    else:
        return []
    df = pd.read_sql_table("studio_anime", config.engine)
    anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['studio_id'] == studio_id]['anime_id']]
    config.logger.info(f'Successfully retreived all the anime links produced by {studio}. Total number: {len(anime_link_list)}')
    return anime_link_list


def run_sql(sql):
    if not config.connection.open:
        config.reconnect()
    with config.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("USE db_myanimelist;")
            cursor.execute(sql)
            return cursor.fetchall()


def get_people_link_by_name(people_name):
    config.logger.info(f'Start scraping people links...')
    sql = f"SELECT id, full_name FROM people WHERE full_name = '{people_name}'"
    result = run_sql(sql)
    if not len(result):
        config.logger.warn("People name not found, please input a valid full name!")
        return []
    people_link_list = ["https://myanimelist.net/people/" + str(res["id"]) for res in result]
    config.logger.info(f'Successfully retreived all the people links. Total number: {len(people_link_list)}')
    return people_link_list


def get_people_link_by_anime_name(anime_name):
    config.logger.info(f'Start scraping people links that has participated in {anime_name}')
    sql1 = f"SELECT id, title FROM anime WHERE title = '{anime_name}' OR english_title = '{anime_name}'"
    result = run_sql(sql1)
    if not len(result):
        config.logger.warn("Anime name not found, please input a valid full name!")
        return []
    anime_id = result[0]["id"]

    people_id_list = []
    sql2 = f"SELECT people_id FROM staff WHERE anime_id = {anime_id}"
    result = run_sql(sql2)
    if len(result):
        people_id_list += [res["people_id"] for res in result]
    sql3 = f"""SELECT p.id AS people_id FROM people p LEFT JOIN voice_actor v ON p.id = v.people_id LEFT JOIN anime_character a ON a.character_id = v.character_id WHERE a.anime_id = {anime_id} GROUP BY p.id;"""
    result = run_sql(sql3)
    if len(result):
        people_id_list += [res["people_id"] for res in result]

    if not len(people_id_list):
        return []
        config.logger.info("Anime staff and voice actors unknown")

    people_link_list = [f"https://myanimelist.net/people/{people_id}" for people_id in people_id_list]
    config.logger.info(f'Successfully retreived all the people links that has participated in {anime_name}. Total number: {len(people_link_list)}')
    return people_link_list


# print(get_people_link_by_anime_name("Attack on Titan"))


def get_people_link_by_rank(rank_num):
    config.logger.info(f'Start scraping all the links for each person...')
    page_num = rank_num // 50 + 1
    people_link_list = get_people_links(page_num)
    config.logger.info(f'Successfully retreived all the top {rank_num} people links')
    return people_link_list[:rank_num]
