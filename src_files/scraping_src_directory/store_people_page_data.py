"""
we create a function that receives a list filled with all info scraped from people pages
and store it in different csv files
"""
import os
from pathlib2 import Path
import csv
from src_files.config import config


def store_people_page_data(people_stats_list, _test = False):
    """
    the function receives a list with all info scraped from people pages and stores it in different files.
    the first file people_info.csv holds all info in the people_info_dict dictionaries.
    the second file anime_characters_info.csv holds all info in the character_info_list lists.
    the third file voice_actors_info.csv holds all info in the voice_actor_info_list lists
    the fourth file staff_info.csv holds all info in the staff_info_list lists.
    :param people_stats_list: list of tuple of dicts, _test(only for test purpose)
    :return: None
    """

    datas_dir = config.datas_dir
    # creates file people_info.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / f'3_people_info{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as people_info_csv_file:
        field_names = ['people_id', 'people_fullname', 'birthday', 'member_favorites', 'people_img_url']
        writer = csv.DictWriter(people_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in people_stats_list:
            writer.writerow(stat[0])

    # creates file anime_character_info.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / f'3_anime_characters_info{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as characters_info_csv_file:
        field_names = ['character_id', 'anime_id', 'character_fullname', 'role', 'character_favorites',
                       'character_img_url']
        writer = csv.DictWriter(characters_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[1]:
                writer.writerow(stat)

    # creates file voice_actors_info.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / f'3_voice_actors_info{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as voice_actors_info_csv_file:
        field_names = ['character_id', 'people_id']
        writer = csv.DictWriter(voice_actors_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[2]:
                writer.writerow(stat)
    # creates file staff_info.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / f'3_staff_info{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as staff_info_csv_file:
        field_names = ['anime_id', 'people_id', 'staff_role']
        writer = csv.DictWriter(staff_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[3]:
                writer.writerow(stat)

    config.logger.info("People pages data successfully stored!")


