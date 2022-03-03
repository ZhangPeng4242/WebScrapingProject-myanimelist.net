"""
we create a function that receives a list filled with all info scraped from anime pages
and stores it in different csv files
"""
from pathlib2 import Path
import os
import csv


def store_anime_page(anime_page_data_list):
    """
    the function receives a list with all info scraped from anime pages and stores it in different files.
    the first file anime_info.csv holds all info in the anime_page_info dictionary.
    the second file alternative_titles.csv holds all info in the  alternative_titles dictionary
    the third file anime_site_stats.csv holds all info in the site_stats dictionary
    :param anime_page_data_list: list of tuple of dicts
    :return: None
    """

    # gets Datas directory's path
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    # creates file anime_info.csv if it doesn't exits, and fills it with all matching scraped info
    with open(Path(datas_dir) / '1_anime_info.csv', "w", encoding="utf-8", newline="") as anime_info_csv_file:
        field_names = ['anime_id', 'title', 'type', 'aired', 'premiered', 'studios', 'source', 'genres', 'rating',
                       'theme',
                       'anime_img_url']
        writer = csv.DictWriter(anime_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[0])

    # creates alternative_titles.csv if it doesn't exists and fills it with  all matching scraped info
    with open(Path(datas_dir) / '1_alternative_titles.csv', "w", encoding="utf-8", newline="") as alter_title_csv_file:
        field_names = ['anime_id', 'english_title']
        writer = csv.DictWriter(alter_title_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[1])

    # creates anime_site_stats.csv if it doesn't exists and fills it with  all matching scraped info
    with open(Path(datas_dir) / '1_anime_site_stats.csv', "w", encoding="utf-8", newline="") as site_stats_csv_file:
        field_names = ['anime_id', 'score', 'rating_count', 'ranked', 'popularity', 'members', 'favorites']
        writer = csv.DictWriter(site_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[2])

    print("Anime page data successfully stored!")


def test():
    test_data = []
    store_anime_page(test_data)


if __name__ == "__main__":
    test()
