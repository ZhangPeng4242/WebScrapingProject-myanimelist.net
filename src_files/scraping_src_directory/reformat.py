"""This module is to build functions that reformat the data we scrapped from the website into the format subjects to the database.
:export: format_anime_general_stats_data(site_stats),format_anime_genre_data(anime_page_info), format_studio_anime_data(anime_page_info),
format_studio_anime_data(anime_page_info), format_anime_data(anime_page_info), format_anime_watch_stats_data(watch_stats), format_anime_score_stats_data(score_stats),
format_people_data(people_info_dict), format_character_data(character_info_list), format_staff_data(staff_info_list), format_voice_actor_data(voice_actor_info_list),
format_anime_character_data(character_info_list), format_studio_data(studio_info_list)
"""

from src_files.mysql_db_src_directory.db_info import db_info
import pandas as pd
import numpy as np
from src_files.config import config


def _make_data_integrity(df, tb_name):
    """
    This is the make the dataframe columns integrate to the fields of the database
    :param df: dataframe of the formatted page data
    :param tb_name: the name of the table
    :return: DataFrame, formatted according to the corresponding table
    """
    cols = df.columns.tolist()
    db_cols = db_info[tb_name]["order"]
    for db_col in db_cols:
        if db_col not in cols:
            df[db_col] = np.nan

    df = df[db_cols]
    return df


def format_anime_general_stats_data(site_stats):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param site_stats: tuple of dicts and list
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_anime_general_stats = pd.DataFrame([site_stats])
    df_anime_general_stats.rename(columns={"id": "anime_id"}, inplace=True)
    df_anime_general_stats = _make_data_integrity(df_anime_general_stats, "anime_general_stats")
    df_anime_general_stats["anime_id"] = df_anime_general_stats["anime_id"].astype("int64")
    return df_anime_general_stats


def format_anime_genre_data(anime_page_info):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param anime_page_info: tuple of dicts and list, data to be formatted
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    if "genres" not in anime_page_info.keys():
        df_anime_genre = _make_data_integrity(pd.DataFrame(), "anime_genre")
        return df_anime_genre
    df_genre = pd.read_sql_table("genre", config.engine)
    genre_names = anime_page_info["genres"].split(", ")
    genre_ids = []
    for g_name in genre_names:
        genre_ids.append(df_genre[df_genre["name"] == g_name]["id"].values.tolist()[0])
    df_anime_genre = pd.DataFrame(
        [{"anime_id": anime_page_info["id"], "genre_id": int(genre_id)} for genre_id in genre_ids])
    df_anime_genre = _make_data_integrity(df_anime_genre, "anime_genre")
    return df_anime_genre


def format_studio_anime_data(anime_page_info):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param anime_page_info: tuple of dicts and list, data to be formatted
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_studio_anime = pd.DataFrame(
        [{"anime_id": anime_page_info["id"], "studio_id": int(studio_id)} for studio_id in anime_page_info["studios"]])
    df_studio_anime = _make_data_integrity(df_studio_anime, "studio_anime")
    return df_studio_anime


def format_anime_data(anime_page_info):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param anime_page_info: tuple of dicts and list, data to be formatted
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_anime_page_info = pd.DataFrame([anime_page_info])
    df_anime_page_info.rename(columns={"premiered": "season_premier"}, inplace=True)
    air_date = df_anime_page_info["aired"].str.split(" to ").map(
        lambda x: [x[0] if x[0] != "Not available" else np.nan, np.nan] if len(x) == 1 else [x[0], x[1] if x[
                                                                                                               1] != '?' else np.nan])[
        0]
    df_anime_page_info["start_air"] = air_date[0]
    df_anime_page_info["start_air"] = df_anime_page_info["start_air"].map(lambda x: pd.to_datetime(x)).astype("object")
    df_anime_page_info["start_air"].replace({np.nan: None}, inplace=True)
    df_anime_page_info["end_air"] = air_date[1]
    df_anime_page_info["end_air"] = df_anime_page_info["end_air"].map(lambda x: pd.to_datetime(x)).astype("object")
    df_anime_page_info["end_air"].replace({np.nan: None}, inplace=True)
    df_anime_page_info["id"] = df_anime_page_info["id"].astype("int64")
    df_anime = _make_data_integrity(df_anime_page_info, "anime")
    return df_anime


def format_anime_watch_stats_data(watch_stats):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param watch_stats: tuple of dicts and list, data to be formatted
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_anime_watch_stats = pd.DataFrame([watch_stats])
    df_anime_watch_stats.rename(columns={"on-hold": "on_hold", "plan to watch": "plan_to_watch"}, inplace=True)
    df_anime_watch_stats = _make_data_integrity(df_anime_watch_stats, "anime_watch_stats")
    return df_anime_watch_stats


def format_anime_score_stats_data(score_stats):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param score_stats: tuple of dicts and list, data to be formatted
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_anime_score_stats = pd.DataFrame([score_stats])
    df_anime_score_stats = _make_data_integrity(df_anime_score_stats, "anime_score_stats")
    return df_anime_score_stats


def format_people_data(people_info_dict):
    """
    Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
    :param people_info_dict: dictionary
    :return: DataFrame, formatted dataframe that can be directly inserted in the db.
    """
    df_people = pd.DataFrame([people_info_dict])
    df_people.rename(columns={"people_id": "id", "people_fullname": "full_name", "member_favorites": "favorites",
                              "people_img_url": "img_url"}, inplace=True)
    df_people = _make_data_integrity(df_people, "people")
    return df_people


def format_character_data(character_info_list):
    """
     Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
     :param character_info_list: list of dictionaries and list
     :return: DataFrame, formatted dataframe that can be directly inserted in the db.
     """
    df_character = pd.DataFrame(character_info_list)
    df_character.rename(
        columns={"character_id": "id", "character_fullname": "full_name", "character_favorites": "favorites",
                 "character_img_url": "img_url"}, inplace=True)
    df_character = _make_data_integrity(df_character, "character")
    return df_character


def format_staff_data(staff_info_list):
    """
      Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
      :param staff_info_list: list of dictionaries and list
      :return: DataFrame, formatted dataframe that can be directly inserted in the db.
      """
    df_staff = pd.DataFrame(staff_info_list)
    df_staff.rename(columns={"staff_role": "role"}, inplace=True)
    df_staff = _make_data_integrity(df_staff, "staff")
    return df_staff


def format_voice_actor_data(voice_actor_info_list):
    """
      Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
      :param voice_actor_info_list: list of dictionaries and list
      :return: DataFrame, formatted dataframe that can be directly inserted in the db.
      """
    df_voice_actor = pd.DataFrame(voice_actor_info_list)
    df_voice_actor = _make_data_integrity(df_voice_actor, "voice_actor")
    return df_voice_actor


def format_anime_character_data(character_info_list):
    """
      Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
      :param character_info_list: list of dictionaries and list
      :return: DataFrame, formatted dataframe that can be directly inserted in the db.
      """
    df_anime_character = pd.DataFrame(character_info_list)
    df_anime_character = _make_data_integrity(df_anime_character, "anime_character")
    return df_anime_character


def format_studio_data(studio_info_list):
    """
      Format data from in accordance to the requirements of the table in the database: column names, order, datatypes, etc.
      :param studio_info_list: list of dictionaries and list
      :return: DataFrame: formatted dataframe that can be directly inserted in the db.
      """

    df_studio = pd.DataFrame(studio_info_list)
    df_studio.rename(
        columns={"studio_id": "id", "studio_name": "name", "studio_rank": "rank", "studio_favorites": "favorites",
                 "studio_img_url": "img_url"}, inplace=True)
    df_studio = _make_data_integrity(df_studio, "studio")

    return df_studio

def format_description_data(description_dict):
    df_description = pd.DataFrame([description_dict])
    df_description = _make_data_integrity(df_description,"description")

    return df_description