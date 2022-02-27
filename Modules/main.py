import random
from scrap_archive_page import get_season_links
# from scrap_season_page import get_anime_links
from scrap_people_list_page import get_people_links
from scrap_people_page import scrap_people_page
from scrap_stats_page import scrap_stats_page
from scrap_anime_page import scrap_anime_page
from store_stats_page_data import store_stats_page_data
from store_anime_page_data import store_anime_page
from store_people_page_data import store_people_page_data
from new_scrap_anime_list_page import get_anime_links
from pathlib2 import Path
import os
import time

DELAY_AFTER_ONE_REQUEST = 2


def main():
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)

    # season_links_path = datas_dir / "season_links.txt"
    anime_links_path = datas_dir / "anime_links.txt"
    #
    # #### Get a set of all season links ####
    # if season_links_path.exists():
    #     with open(season_links_path, "r", encoding="utf-8") as season_links_file:
    #         season_links = season_links_file.read().split("\n")
    # else:
    #     season_links = get_season_links()
    #     with open(season_links_path, "w", encoding="utf-8") as season_links_file:
    #         season_links_file.write("\n".join(season_links))
    #
    #### Get a set of all anime links ####
    # anime_links = set([])
    # if anime_links_path.exists():
    #     with open(anime_links_path, "r", encoding="utf-8") as anime_links_file:
    #         anime_links = anime_links_file.read().split("\n")
    # else:
    #     for link in list(season_links):
    #         anime_links |= get_anime_links(link)
    #         # Reducing the request frequency, so that the website would not limit access.
    #         time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))
    #
    #     with open(anime_links_path, "w", encoding="utf-8") as anime_links_file:
    #         anime_links_file.write("\n".join(anime_links))
    # print("Successfully get all the anime links!!")
    #
    #### Get a list of all anime links ####

    if anime_links_path.exists():
        with open(anime_links_path, "r", encoding="utf-8") as anime_links_file:
            anime_links = anime_links_file.read().split("\n")
    else:
        anime_links = get_anime_links()
        with open(anime_links_path, "w", encoding="utf-8") as anime_links_file:
            anime_links_file.write("\n".join(anime_links))
    print("Successfully get all the anime links!!")

    #### Scrap anime page #####
    anime_page_datas = []
    random.shuffle(list(anime_links))

    for anime_link in anime_links:
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        except Exception as err:
            err_log.append(f"scrap_anime_page: {anime_link} {str(err)}")
            continue

    store_anime_page(anime_page_datas)
    anime_page_datas = []  # release memory

    #### Scrap stats page ####
    stats_page_datas = []
    random.shuffle(anime_links)
    for anime_link in anime_links:
        try:
            stats_page_datas.append(scrap_stats_page(f'{anime_link}/stats'))
        except Exception as err:
            err_log.append(f"scrap_stats_page: {anime_link}  {err}")
            continue

    store_stats_page_data(stats_page_datas)
    stats_page_datas = []  # release memory

    #### Get a list of people page links ####

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

    #### Scrap people page ####
    people_page_datas = []
    for people_link in people_links:
        try:
            people_page_datas.append(scrap_people_page(people_link))
        except Exception as err:
            err_log.append(f"scrap_people_page: {anime_link}  {err}")
            continue

    store_people_page_data(people_page_datas)
    people_page_datas = []  # release memory

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
        log_dir = cur_path.parent / "Datas" / "err_log.txt"
        with open(log_dir, "w", encoding="utf-8") as err_log_file:
            err_log_file.write("\n".join(err for err in err_log))
