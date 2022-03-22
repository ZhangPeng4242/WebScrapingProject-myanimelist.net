from src_files.mysql_db_src_directory.db_info import db_info
import pandas as pd
import numpy as np
from src_files.config import config


def make_data_integrity(df, db_name):
    cols = df.columns.tolist()
    db_cols = db_info[db_name]["order"]
    for db_col in db_cols:
        if db_col not in cols:
            df[db_col] = np.nan

    df = df[db_cols]
    return df


def format_anime_general_stats_data(site_stats):
    df_anime_general_stats = pd.DataFrame([site_stats])
    df_anime_general_stats.rename(columns={"id": "anime_id"}, inplace=True)
    df_anime_general_stats = make_data_integrity(df_anime_general_stats, "anime_general_stats")
    df_anime_general_stats["anime_id"] = df_anime_general_stats["anime_id"].astype("int64")
    # print(df_anime_general_stats)
    return df_anime_general_stats


def format_anime_genre_data(anime_page_info):
    if "genres" not in anime_page_info.keys():
        df_anime_genre = make_data_integrity(pd.DataFrame(), "anime_genre")
        return df_anime_genre
    df_genre = pd.read_sql_table("genre", config.engine)
    genre_names = anime_page_info["genres"].split(", ")
    genre_ids = []
    for g_name in genre_names:
        genre_ids.append(df_genre[df_genre["name"] == g_name]["id"].values.tolist()[0])
    df_anime_genre = pd.DataFrame(
        [{"anime_id": anime_page_info["id"], "genre_id": int(genre_id)} for genre_id in genre_ids])
    df_anime_genre = make_data_integrity(df_anime_genre, "anime_genre")
    return df_anime_genre


# print(format_anime_genre_data({"id": 123, "genres": "Adventure, Samsung"}))


def format_studio_anime_data(anime_page_info):
    df_studio_anime = pd.DataFrame(
        [{"anime_id": anime_page_info["id"], "studio_id": int(studio_id)} for studio_id in anime_page_info["studios"]])
    df_studio_anime = make_data_integrity(df_studio_anime, "studio_anime")
    return df_studio_anime


def format_anime_data(anime_page_info):
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
    df_anime = make_data_integrity(df_anime_page_info, "anime")
    # df_anime_page_info = df_anime_page_info[["id", "title", "english_title", "type", "source", "start_air", "end_air", "season_premier", "theme",
    #      "img_url"]]
    return df_anime


def format_anime_watch_stats_data(watch_stats):
    df_anime_watch_stats = pd.DataFrame([watch_stats])
    df_anime_watch_stats.rename(columns={"on-hold": "on_hold", "plan to watch": "plan_to_watch"}, inplace=True)
    df_anime_watch_stats = make_data_integrity(df_anime_watch_stats, "anime_watch_stats")
    # print(df_anime_watch_stats)
    return df_anime_watch_stats


def format_anime_score_stats_data(score_stats):
    df_anime_score_stats = pd.DataFrame([score_stats])
    df_anime_score_stats = make_data_integrity(df_anime_score_stats, "anime_score_stats")
    # print(df_anime_score_stats["4"].isna())
    # print(df_anime_score_stats)
    return df_anime_score_stats


def format_people_data(people_info_dict):
    df_people = pd.DataFrame([people_info_dict])
    df_people.rename(columns={"people_id": "id", "people_fullname": "full_name", "member_favorites": "favorites",
                              "people_img_url": "img_url"}, inplace=True)
    df_people = make_data_integrity(df_people, "people")
    # print(df_people)
    return df_people


def format_character_data(character_info_list):
    df_character = pd.DataFrame(character_info_list)
    df_character.rename(
        columns={"character_id": "id", "character_fullname": "full_name", "character_favorites": "favorites",
                 "character_img_url": "img_url"}, inplace=True)
    df_character = make_data_integrity(df_character, "character")
    # print(df_character)
    return df_character


def format_staff_data(staff_info_list):
    # should consider if anime not existed
    df_staff = pd.DataFrame(staff_info_list)
    df_staff.rename(columns={"staff_role": "role"}, inplace=True)
    df_staff = make_data_integrity(df_staff, "staff")
    # print(df_staff)
    return df_staff


def format_voice_actor_data(voice_actor_info_list):
    df_voice_actor = pd.DataFrame(voice_actor_info_list)
    df_voice_actor = make_data_integrity(df_voice_actor, "voice_actor")
    # print(df_voice_actor)
    return df_voice_actor


def format_anime_character_data(character_info_list):
    df_anime_character = pd.DataFrame(character_info_list)
    df_anime_character = make_data_integrity(df_anime_character, "anime_character")
    # print(df_anime_character)
    return df_anime_character


def format_studio_data(studio_info_list):
    df_studio = pd.DataFrame(studio_info_list)
    df_studio.rename(
        columns={"studio_id": "id", "studio_name": "name", "studio_rank": "rank", "studio_favorites": "favorites",
                 "studio_img_url": "img_url"}, inplace=True)
    df_studio = make_data_integrity(df_studio, "studio")
    # print(df_studio)
    return df_studio
