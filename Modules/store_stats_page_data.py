"""
we create a function that receives a list filled with all info scraped from anime stats pages
and store it in different csv files
"""
import csv
import os
from pathlib2 import Path


def store_stats_page_data(anime_stats_list):
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
    with open(Path(datas_dir) / '2_anime_watch_stats.csv', "w", encoding="utf-8",
              newline="") as anime_watch_stats_csv_file:
        field_names = ['anime_id', 'watching', 'completed', 'on-hold', 'dropped', 'plan to watch', 'total']
        writer = csv.DictWriter(anime_watch_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats_list:
            writer.writerow(stat[0])

    # creates file anime_score_stats.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / '2_anime_score_stats.csv', "w", encoding="utf-8",
              newline="") as anime_score_stats_csv_file:
        field_names = ["anime_id"] + [str(num) for num in range(10, 0, -1)]
        writer = csv.DictWriter(anime_score_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats_list:
            writer.writerow(stat[1])

    print("Stats data successfully stored!")


def test():
    """
    Run this program directly to test store_stats_page_data function
    :return: None
    """
    test_data = [({'Watching': 15062, 'Completed': 128422, 'On-Hold': 9963, 'Dropped': 9028, 'Plan to Watch': 44438,
                   'Total': 206913, 'anime_id': '18179'},
                  {'10': 11259, '9': 22063, '8': 36107, '7': 22906, '6': 7308, '5': 2815, '4': 936, '3': 323, '2': 132,
                   '1': 151, 'anime_id': '18179'}),
                 ({'Watching': 65017, 'Completed': 1, 'On-Hold': 1191, 'Dropped': 4902, 'Plan to Watch': 35088,
                   'Total': 106199, 'anime_id': '47161'},
                  {'10': 1595, '9': 1170, '8': 2465, '7': 4707, '6': 3999, '5': 2739, '4': 1580, '3': 903, '2': 438,
                   '1': 438, 'anime_id': '47161'})]

    store_stats_page_data(test_data)


if __name__ == "__main__":
    test()
