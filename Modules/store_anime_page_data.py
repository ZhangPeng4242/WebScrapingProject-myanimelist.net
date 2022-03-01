from pathlib2 import Path
import os
import csv


def store_anime_page(anime_page_data_list):
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    with open(Path(datas_dir) / '1_anime_info.csv', "w", encoding="utf-8", newline="") as anime_info_csv_file:
        field_names = ['anime_id', 'title', 'type', 'aired', 'premiered', 'studios', 'source', 'genres', 'rating',
                       'theme',
                       'anime_img_url']
        writer = csv.DictWriter(anime_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[0])

    with open(Path(datas_dir) / '1_alternative_titles.csv', "w", encoding="utf-8", newline="") as alter_title_csv_file:
        field_names = ['anime_id', 'english_title']
        writer = csv.DictWriter(alter_title_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[1])

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
