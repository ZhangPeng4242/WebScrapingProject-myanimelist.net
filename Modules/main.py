import random
from scrap_people_list_page import get_people_links
from scrap_people_page import scrap_people_page
from scrap_stats_page import scrap_stats_page
from scrap_anime_page import scrap_anime_page
from store_stats_page_data import store_stats_page_data
from store_anime_page_data import store_anime_page
from store_people_page_data import store_people_page_data
from scrap_anime_list_page import get_anime_links
from pathlib2 import Path
import os
import time

DELAY_AFTER_ONE_REQUEST = 2


def main_get_and_store_anime_links(datas_dir):
    anime_links_path = datas_dir / "anime_links.txt"

    if anime_links_path.exists():
        with open(anime_links_path, "r", encoding="utf-8") as anime_links_file:
            anime_links = anime_links_file.read().split("\n")
    else:
        anime_links = get_anime_links()
        with open(anime_links_path, "w", encoding="utf-8") as anime_links_file:
            anime_links_file.write("\n".join(anime_links))
    print("Successfully get all the anime links!!")

    random.shuffle(anime_links)
    return anime_links


def main_get_and_store_people_links(datas_dir):
    people_links_path = datas_dir / "people_links.txt"
    if people_links_path.exists():
        with open(people_links_path, "r", encoding="utf-8") as people_links_file:
            people_links = people_links_file.read().split("\n")

    else:
        people_links = get_people_links()
        with open(people_links_path, "w", encoding="utf-8") as people_links_file:
            people_links_file.write("\n".join(people_links))

    print("Successfully get all the people links")
    random.shuffle(people_links)

    return people_links


def main_scrap_and_store_anime_pages(anime_links):
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
                err_log.append(f"scrap_anime_page: {anime_link} {str(err)}")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            print(f"scrap_anime_page: Failed {anime_link}  Rescraping...\nAttempt: {loop}")
            time.sleep(10)
            continue

    store_anime_page(anime_page_datas)


def main_scrap_and_store_anime_stats_pages(anime_links):
    stats_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping anime_stats_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.2, 1)} hours.")

    while anime_link:
        try:
            stats_page_datas.append(scrap_stats_page(f'{anime_link}/stats'))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                print(f"Scrap Error: continue with next...({scrap_count}/{total_count})")
                err_log.append(f"scrap_anime_stats_page: {anime_link} {str(err)}")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            time.sleep(10)
            print(f"scrap_anime_stats_page: Failed {anime_link}  Rescraping...\nAttempt: {loop}")
            continue

    store_stats_page_data(stats_page_datas)


def main_scrap_and_store_people_pages(people_links):
    people_page_datas = []
    total_count = len(people_links)
    people_links = iter(people_links)
    people_link = next(people_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping people_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.2, 1)} hours.")

    while people_link:
        try:
            people_page_datas.append(scrap_people_page(people_link))
            people_link = next(people_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                print(f"Scrap Error: continue with next...({scrap_count}/{total_count})")
                err_log.append(f"scrap_people_page: {people_link}  {err}")
                people_link = next(people_links, None)
                loop = 0
                continue

            loop += 1
            print(f"scrap_people_page: Failed {people_link}  Rescraping...\nAttempt: {loop}")
            time.sleep(10)
            continue

    store_people_page_data(people_page_datas)


def main():
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)

    anime_links = main_get_and_store_anime_links(datas_dir)

    # main_scrap_and_store_anime_pages(anime_links)
    #
    main_scrap_and_store_anime_stats_pages(anime_links)
    #
    # people_links = main_get_and_store_people_links(datas_dir)
    #
    # main_scrap_and_store_people_pages(people_links)

    print("Successfully finished all the scraping!!!Good job!")


if __name__ == "__main__":
    err_log = []
    try:
        main()
    except Exception as err:
        print(f"Main() error: {err}")
        err_log.append(str(err))
    finally:
        # Write error log:
        cur_path = Path(os.getcwd())
        log_dir = cur_path.parent / "Datas" / "err_log_people_page.txt"
        with open(log_dir, "w", encoding="utf-8") as err_log_file:
            err_log_file.write("\n".join(err for err in err_log))
