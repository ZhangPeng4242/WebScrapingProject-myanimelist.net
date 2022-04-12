"""
This module is to create functions that will return the links of webpages according to the commands given.
:export: get_anime_link_by_name(name), get_anime_link_by_year(year), get_anime_link_by_rank(rank), get_anime_link_by_genre(genre),
         get_anime_link_by_studio(studio), get_people_link_by_name(people_name), get_people_link_by_anime_name(anime_name), get_people_link_by_rank(rank_num)
"""
import pandas as pd
from src_files.config import config
from bs4 import BeautifulSoup
import requests
import datetime
from src_files.scraping_src_directory.scrap_anime_list_page import get_anime_links
from src_files.scraping_src_directory.scrap_people_list_page import get_people_links

THIS_YEAR = datetime.date.today().year
YEAR_LINKS = [f'https://myanimelist.net/anime/season/{THIS_YEAR}/summer',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/winter',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/fall',
              f'https://myanimelist.net/anime/season/{THIS_YEAR}/spring']


def _run_sql(sql):
    """
    This function will run the given sql query and return all the result
    :param sql: sql query
    :return: dict: cursor.fetchall() result
    """
    if not config.is_connected():
        config.reconnect()
    with config.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("USE db_myanimelist;")
            cursor.execute(sql)
            return cursor.fetchall()


def get_anime_link_by_name(name):
    """
    This function will find the anime links with the exact same name given.
    This name match is case sensitive, and search for match to either original or english names in the database.
    :param name: str, anime_name
    :return: anime_link_list: list of str, a list of anime full links
    """
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


def get_anime_link_by_year(year):
    """
    This function will find the links of the animes released in the year given.
    :param year: int, year of release
    :return: anime_link_list: list of str, a list of anime full links
    """
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

            config.logger.info(f"get_anime_links: {main_link}  Success!")
        anime_link_list = list(anime_link_set)
    else:
        config.logger.warn(f"Animes released in year {year} not exist.")
        return []
    config.logger.info(f'Successfully retreived all anime links at year {year}, total number: {len(anime_link_list)}')
    return anime_link_list


def get_anime_link_by_rank(rank):
    """
    This function will find the links of all the animes before(include) the rank given.
    :param rank: int, the rank we want to scrap until
    :return: anime_link_list: list of str, a list of anime full links
    """
    config.logger.info(f'Start scraping top {rank} anime links...')
    if rank < 0:
        return []
    page_num = 1 + rank // 50
    anime_link_list = get_anime_links(page_num)

    config.logger.info(f'Successfully retreived all the top {rank} anime links.')
    return anime_link_list[:rank]


def get_anime_link_by_genre(genre):
    """
    This function will find the links of all the animes of the genre given.
    :param genre: str, the genre of the anime we want to scrap.
    :return: anime_link_list: list of str, a list of anime full links
    """
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
    """
    This function will find the links of all the animes from the studio given.
    :param studio: str, the name of the studio.
    :return: anime_link_list: list of str, a list of anime full links
    """

    config.logger.info(f'Start scraping anime links produced by {studio}...')
    df = pd.read_sql_table("studio", config.engine)
    id_list = list(df[df['name'] == studio]['id'])
    if id_list:
        studio_id = id_list[0]
    else:
        return []
    df = pd.read_sql_table("studio_anime", config.engine)
    anime_link_list = [f'https://myanimelist.net/anime/{id}' for id in df[df['studio_id'] == studio_id]['anime_id']]
    config.logger.info(
        f'Successfully retreived all the anime links produced by {studio}. Total number: {len(anime_link_list)}')
    return anime_link_list


def get_people_link_by_name(people_name):
    """
    This function will find the links of all the people that matches the full name given.
    The match is case sensitive.
    :param people_name: str, the full name of the people
    :return: people_link_list: list of str, a list of people full links
    """
    config.logger.info(f'Start scraping people links...')
    sql = f"SELECT id, full_name FROM people WHERE full_name = '{people_name}'"
    result = _run_sql(sql)
    if not len(result):
        config.logger.warn("People name not found, please input a valid full name!")
        return []
    people_link_list = ["https://myanimelist.net/people/" + str(res["id"]) for res in result]
    config.logger.info(f'Successfully retreived all the people links. Total number: {len(people_link_list)}')
    return people_link_list


def get_people_link_by_anime_name(anime_name):
    """
    This function will find the links of all the people that have participated in a certain anime.
    The match of the anime name is case sensitive, and also search for the match of either original or english names.
    :param anime_name: str, the name of the anime
    :return: people_link_list: list of str, a list of people full links
    """
    config.logger.info(f'Start scraping people links that has participated in {anime_name}')
    sql1 = f"SELECT id, title FROM anime WHERE title = '{anime_name}' OR english_title = '{anime_name}'"
    result = _run_sql(sql1)

    if not len(result):
        config.logger.warn("Anime name not found, please input a valid full name!")
        return []
    anime_id = result[0]["id"]

    people_id_list = []
    sql2 = f"SELECT people_id FROM staff WHERE anime_id = {anime_id}"
    result = _run_sql(sql2)
    if len(result):
        people_id_list += [res["people_id"] for res in result]
    sql3 = f"""SELECT p.id AS people_id FROM people p LEFT JOIN voice_actor v ON p.id = v.people_id LEFT JOIN anime_character a ON a.character_id = v.character_id WHERE a.anime_id = {anime_id} GROUP BY p.id;"""
    result = _run_sql(sql3)

    if len(result):
        people_id_list += [res["people_id"] for res in result]

    if not len(people_id_list):
        config.logger.info("Anime staff and voice actors unknown")
        return []

    people_link_list = [f"https://myanimelist.net/people/{people_id}" for people_id in people_id_list]
    config.logger.info(
        f'Successfully retreived all the people links that has participated in {anime_name}. Total number: {len(people_link_list)}')
    return people_link_list


def get_people_link_by_rank(rank_num):
    """
    This function will find the links of all the people before(include) the rank given.
    :param rank_num: int, the rank of the people we want to scrap until.
    :return: people_link_list: list of str, a list of people full links
    """
    config.logger.info(f'Start scraping all the links for each person...')
    page_num = rank_num // 50 + 1
    people_link_list = get_people_links(page_num)
    config.logger.info(f'Successfully retreived all the top {rank_num} people links')
    return people_link_list[:rank_num]
