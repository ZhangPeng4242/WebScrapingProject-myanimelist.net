"""
This module is to build functions that bridges scraping and updating
:export: scrap_and_update_studio, scrap_and_update_anime, scrap_and_update_people
"""
from src_files.mysql_db_src_directory.update_db import update_table
from src_files.scraping_src_directory.record_exists_check import is_exist
from src_files.scraping_src_directory.scrap_people_page import scrap_people_page
from src_files.scraping_src_directory.scrap_anime_page import scrap_anime_page
from src_files.scraping_src_directory.scrap_studio_page import scrap_studio_page
from src_files.scraping_src_directory.scrap_stats_page import scrap_stats_page


def scrap_and_update_studio(studio_link):
    """
    This function is to scrap the studio page data and update the data in the database
    :param studio_link: str
    :return: None
    """
    formatted_studio_data = scrap_studio_page(studio_link)
    update_table(formatted_studio_data, "id", "studio")


def scrap_and_update_anime(anime_link):
    """
    This function is to scrap the ainme relavant pages data and update the data into different tables in the database
    :param anime_link: str
    :return:
    """
    anime_full_link, formatted_anime_data, formatted_anime_general_stats_data, formatted_anime_genre_data, formatted_studio_anime_data, formatted_description_data = scrap_anime_page(
        anime_link)

    # Check data integrity, foreign key constraint.
    # Check every studio_id exists in the studio table, if not scrap and update
    for studio_id in formatted_studio_anime_data["studio_id"].unique().tolist():
        if not is_exist("id", studio_id, "studio"):
            scrap_and_update_studio(f"https://myanimelist.net/anime/producer/{studio_id}")

    update_table(formatted_anime_data, "id", "anime")
    update_table(formatted_anime_general_stats_data, "anime_id", "anime_general_stats")
    update_table(formatted_anime_genre_data, "anime_id", "anime_genre", insert_only=True)
    update_table(formatted_studio_anime_data, "anime_id", "studio_anime", insert_only=True)
    update_table(formatted_description_data, "anime_id", "description")

    formatted_anime_watch_stats_data, formatted_anime_score_stats_data = scrap_stats_page(
        anime_full_link + '/stats')
    update_table(formatted_anime_watch_stats_data, "anime_id", "anime_watch_stats")
    update_table(formatted_anime_score_stats_data, "anime_id", "anime_score_stats")


def scrap_and_update_people(people_link):
    """
     This function is to scrap the ainme relavant pages data and update the data into different tables in the database
    :param people_link: str
    :return: None
    """
    formatted_people_data, formatted_character_data, formatted_staff_data, formatted_voice_actor_data, formatted_anime_character_data = scrap_people_page(
        people_link)

    # Check integrity, foreign key constraint.
    # Check every anime_id exists in the anime table, if not scrap and update
    anime_ids = set(formatted_anime_character_data["anime_id"].tolist()) | set(
        formatted_staff_data["anime_id"].tolist())
    for anime_id in list(anime_ids):
        if not is_exist("id", anime_id, "anime"):
            scrap_and_update_anime(f"https://myanimelist.net/anime/{anime_id}")

    update_table(formatted_people_data, "id", "people")
    update_table(formatted_character_data, "id", "`character`", update_logging=False)
    update_table(formatted_staff_data, ("people_id", "anime_id"), "staff", double=True)
    update_table(formatted_voice_actor_data, ("character_id", "people_id"), "voice_actor", double=True)
    update_table(formatted_anime_character_data, ("anime_id", "character_id"), "anime_character",
                 double=True)
