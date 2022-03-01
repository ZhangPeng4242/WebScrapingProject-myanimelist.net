from pathlib2 import Path
import os
import random
from scrap_anime_page import scrap_anime_page
import time
import csv

DELAY_AFTER_ONE_REQUEST = 2


def scrap_err_data():
    datas_dir = Path(os.getcwd()).parent / "Datas"
    anime_links = []
    with open(datas_dir / "err_log_people_page.txt", "r") as err_file:
        err_txt = err_file.read().split("\n")
        for err in err_txt:
            anime_links.append(err.split()[1])

    anime_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping anime_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.2, 1)} hours.")

    while anime_link:
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                print(f"Scrap Error: continue with next... ({scrap_count}/{total_count})")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            print(f"scrap_anime_page: Failed {anime_link}  Rescraping...\nAttempt: {loop}")
            time.sleep(10)
            continue

    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    with open(Path(datas_dir) / '1_anime_info.csv', "a", encoding="utf-8") as anime_info_csv_file:
        field_names = ['anime_id', 'title', 'type', 'aired', 'premiered', 'studios', 'source', 'genres', 'rating',
                       'theme',
                       'anime_img_url']
        writer = csv.DictWriter(anime_info_csv_file, fieldnames=field_names)

        for stat in anime_page_datas:
            writer.writerow(stat[0])

    with open(Path(datas_dir) / '1_alternative_titles.csv', "a", encoding="utf-8") as alter_title_csv_file:
        field_names = ['anime_id', 'english_title']
        writer = csv.DictWriter(alter_title_csv_file, fieldnames=field_names)

        for stat in anime_page_datas:
            writer.writerow(stat[1])

    with open(Path(datas_dir) / '1_anime_site_stats.csv', "a", encoding="utf-8") as site_stats_csv_file:
        field_names = ['anime_id', 'score', 'rating_count', 'ranked', 'popularity', 'members', 'favorites']
        writer = csv.DictWriter(site_stats_csv_file, fieldnames=field_names)

        for stat in anime_page_datas:
            writer.writerow(stat[2])

    print("Anime page data successfully stored!")


scrap_err_data()
