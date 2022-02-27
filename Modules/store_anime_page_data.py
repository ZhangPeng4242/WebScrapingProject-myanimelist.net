from pathlib2 import Path
import os
import csv


def store_anime_page(anime_page_data_list):
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    with open(Path(datas_dir) / 'anime_info.csv', "w", encoding="utf-8") as anime_info_csv_file:
        field_names = ['anime_id', 'Title', 'Type', 'Premiered', 'Studios', 'Source', 'Genres', 'Rating', 'Theme',
                       'anime_img_url']
        writer = csv.DictWriter(anime_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[0])

    with open(Path(datas_dir) / 'alternative_titles.csv', "w", encoding="utf-8") as alter_title_csv_file:
        field_names = ['anime_id', 'English_title']
        writer = csv.DictWriter(alter_title_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[1])

    with open(Path(datas_dir) / 'anime_site_stats.csv', "w", encoding="utf-8") as site_stats_csv_file:
        field_names = ['anime_id', 'Score', 'Rating_count', 'Ranked', 'Popularity', 'Members', 'Favorites']
        writer = csv.DictWriter(site_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_page_data_list:
            writer.writerow(stat[2])

    print("Anime page data successfully stored!")




def test():
    test_data = [({'anime_id': '11757', 'Title': 'Sword Art Online', 'Type': 'TV', 'Premiered': 'Summer 2012',
                   'Studios': 'A-1 Pictures', 'Source': 'Light novel',
                   'Genres': ['Action', 'Adventure', 'Fantasy', 'Romance'], 'Theme': ['Game'],
                   'Rating': 'PG-13 - Teens 13 or older'},
                  {'anime_id': '11757', 'Title': 'Sword Art Online', 'English_title': None},
                  {'anime_id': '11757', 'Score': '7.20', 'Rating_count': '1850653', 'Ranked': '2900', 'Popularity': '5',
                   'Members': '2677417', 'Favorites': '62815'}),
                 ({'anime_id': '111', 'Title': 'Corrector Yui', 'Type': 'TV', 'Premiered': 'Spring 1999',
                   'Studios': 'Nippon Animation', 'Source': 'Original', 'Genres': ['Adventure', 'Comedy', 'Sci-Fi'],
                   'Rating': 'PG - Children'},
                  {'anime_id': '111', 'Title': 'Corrector Yui', 'English_title': None},
                  {'anime_id': '111', 'Score': '6.85', 'Rating_count': '5364', 'Ranked': '4416', 'Popularity': '4756',
                   'Members': '13957', 'Favorites': '47'})]
    store_anime_page(test_data)


if __name__ == "__main__":
    test()
