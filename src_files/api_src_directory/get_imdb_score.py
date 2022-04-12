"""
This module is to bridge myanimelist and IMDB, find the anime in IMDB and get the scores.
:export: get_imdb_score
"""
import pandas as pd
import re
from src_files.scraping_src_directory.record_exists_check import is_exist
from src_files.scraping_src_directory.scrap_and_update import scrap_and_update_anime
from src_files.config import config
from googlesearch import get_random_user_agent, search
from src_files.scraping_src_directory.scrap_imdb import scrap_imdb_score
from src_files.scraping_src_directory.reformat import _make_data_integrity


def get_imdb_score(anime_link):
    """
    This function is to find the anime on IMDB from the given anime_link on myanimelist.
    We will scrap and format all the required data for api_imdb_table. We scrap name and year for cross-validation.
    :param anime_link:
    :return: DataFrame, for api_imdb_table
    """
    anime_id = re.findall("(?<=https://myanimelist.net/anime/)[0-9]*", anime_link)
    anime_id = int(anime_id[0]) if len(anime_id) != 0 else None

    if not is_exist("id", anime_id, "anime"):
        scrap_and_update_anime(anime_link)

    if not config.connection.open:
        config.reconnect()

    with config.connection:
        with config.connection.cursor() as cursor:
            sql = f"SELECT title FROM anime WHERE id = {anime_id} "
            cursor.execute("USE db_myanimelist")
            cursor.execute(sql)
            anime_title = cursor.fetchall()[0]["title"]

    google_search_query = 'imdb ' + anime_title
    uagent = get_random_user_agent()
    result = search(google_search_query, tld="co.in", num=10, stop=10, pause=0.5, user_agent=uagent)
    try:
        imdb_link = next(result)
    except:
        raise Exception(f"No anime search result on IMDB. {anime_link}")

    imdb_id = re.findall("(?<=https://www.imdb.com/title/tt)[0-9]*", imdb_link)
    imdb_id = int(imdb_id[0]) if len(imdb_id) != 0 else None

    imdb_title, imdb_score, imdb_year = scrap_imdb_score(imdb_link)

    df_imdb_score = pd.DataFrame([{"anime_id": anime_id, "imdb_id": imdb_id, "imdb_title": imdb_title,
                                   "score": imdb_score, "year": imdb_year, "imdb_url": imdb_link}])
    df_imdb_score = _make_data_integrity(df_imdb_score, "api_imdb")

    return df_imdb_score
