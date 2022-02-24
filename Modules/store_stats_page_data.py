import csv
import os
from pathlib2 import Path


def store_stats_page_data(anime_stats):
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)

    with open(Path(datas_dir) / 'anime_sum_stats.csv', "w") as anime_sum_stats_csv_file:
        field_names = ['anime_id', 'Watching', 'Completed', 'On-Hold', 'Dropped', 'Plan to Watch', 'Total']
        writer = csv.DictWriter(anime_sum_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats:
            writer.writerow(stat[0])

    with open(Path(datas_dir) / 'anime_score_stats.csv', "w") as anime_score_stats_csv_file:
        field_names = ["anime_id"] + [str(num) for num in range(10, 0, -1)]
        writer = csv.DictWriter(anime_score_stats_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in anime_stats:
            writer.writerow(stat[1])

    print("Stats data successfully stored!")


def test():
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
