"""
we create a function that receives a list filled with all info scraped from anime stats pages
and store it in different csv files
"""
import csv
import os
from pathlib2 import Path
from config import config


def store_stats_page_data(anime_stats_list, _test=False):
    """
    the function receives a list with all info scraped from anime stats pages and stores it in different files.
    the first file anime_watch_stats.csv holds all info in the sum_stats dictionaries.
    the second file anime_score_stats.csv holds all info in the score_stats dictionaries.
    :param anime_stats_list: list of tuples of ticts
    :return: None
    """

    # gets Datas directory's path
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    # creates file anime_watch_stats.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / '2_anime_watch_stats{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as anime_watch_stats_csv_file:
        field_names = ['anime_id', 'watching', 'completed', 'on-hold', 'dropped', 'plan to watch', 'total']
        writer = csv.DictWriter(anime_watch_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats_list:
            writer.writerow(stat[0])

    # creates file anime_score_stats.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / '2_anime_score_stats{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as anime_score_stats_csv_file:
        field_names = ["anime_id"] + [str(num) for num in range(10, 0, -1)]
        writer = csv.DictWriter(anime_score_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats_list:
            writer.writerow(stat[1])

    config.logger.info("Anime stats pages data successfully stored!")


