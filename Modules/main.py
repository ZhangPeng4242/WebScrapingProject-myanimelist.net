"""
we make use of all of our libraries to scrap myanimelist and store the data in several csv files
"""
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

DELAY_AFTER_ONE_REQUEST = 1


def main_get_and_store_anime_links(datas_dir):
    """
    receives as input the path of a data directory.
    checks if a file called anime_links.txt already exists and if not creates that file
    and uses get_anime_links to store all main anime page links inside of it.
    the function then returns all anime main page links as a list.
    :param datas_dir: str
    :return: anime_links: list
    """
    # creates file path
    anime_links_path = datas_dir / "anime_links.txt"

    # if file exists, we get its content as a list
    if anime_links_path.exists():
        with open(anime_links_path, "r", encoding="utf-8") as anime_links_file:
            anime_links = anime_links_file.read().split("\n")
    # if not, we fill the file with the links
    else:
        anime_links = get_anime_links()
        with open(anime_links_path, "w", encoding="utf-8") as anime_links_file:
            anime_links_file.write("\n".join(anime_links))

    # return list of all anime main page links
    print("Successfully get all the anime links!!")
    random.shuffle(anime_links)
    return anime_links


def main_get_and_store_people_links(datas_dir):
    """
    receives as input the path of a data directory.
    checks if a file called people_links.txt already exists and if not creates that file
    and uses get_people_links to store all main anime page links inside of it.
    the function then returns all people page links as a list.
    :param datas_dir: str
    :return: people_links: list
    """
    # creates file path
    people_links_path = datas_dir / "people_links.txt"

    # if file exists, we get its content as a list
    if people_links_path.exists():
        with open(people_links_path, "r", encoding="utf-8") as people_links_file:
            people_links = people_links_file.read().split("\n")

    # if not, we fill the file with the links
    else:
        people_links = get_people_links()
        with open(people_links_path, "w", encoding="utf-8") as people_links_file:
            people_links_file.write("\n".join(people_links))

    # return list of all anime main page links
    print("Successfully get all the people links")
    random.shuffle(people_links)
    return people_links


def main_scrap_and_store_anime_pages(anime_links):
    """
    receives as input a list of anime main page links, scrapes them for info using scrap_anime_page
    and stores them in a csv file with store_anime_page_data.
    it handles proxies being blocked by re-running with a different proxy when detecting errors during requests
    :param anime_links: list
    :return: None
    """
    # creates a list to store all scraped data from links and iterates over the anime_links list.
    anime_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping anime_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.5, 1)} hours.")

    while anime_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        # in case of n error, it tries running with a different proxy 5 times before giving up and logging the error
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

    # stores all extracted data in csv files.
    store_anime_page(anime_page_datas)


def main_scrap_and_store_anime_stats_pages(anime_links):
    """
    receives as input a list of anime main page links, changes them into stats page format,
    scrapes them for info using scrap_stats_page and stores them in a csv file with store_stats_page_data.
    it handles proxies being blocked by re-running with a different proxy when detecting errors during requests
    :param anime_links: list
    :return: None
    """
    # creates a list to store all scraped data from links and iterates over the anime_links list.
    stats_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping anime_stats_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.5, 1)} hours.")

    while anime_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            stats_page_datas.append(scrap_stats_page(f'{anime_link}/stats'))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        # in case of an error, it tries running with a different proxy 5 times before giving up and logging the error
        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                print(f"Scrap Error: continue with next...({scrap_count}/{total_count})")
                err_log.append(f"scrap_anime_stats_page: {anime_link}/stats {str(err)}")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            time.sleep(10)
            print(f"scrap_anime_stats_page: Failed {anime_link}/stats  Rescraping...\nAttempt: {loop}")
            continue

    # stores all extracted data in csv files.
    store_stats_page_data(stats_page_datas)


def main_scrap_and_store_people_pages(people_links):
    """
    receives as input the path of a data directory.
    checks if a file called people_links.txt already exists and if not creates that file
    and uses get_people_links to store all main anime page links inside of it.
    the function then returns all people page links as a list.
    :param people_links: list
    :return: None
    """
    # creates a list to store all scraped data from links and iterates over the people_links list.
    people_page_datas = []
    total_count = len(people_links)
    people_links = iter(people_links)
    people_link = next(people_links, None)
    loop = 0
    scrap_count = 0
    print(
        f"Scraping people_pages starts! Time estimation: {round(DELAY_AFTER_ONE_REQUEST / 2 * total_count / 3600 * 1.5, 1)} hours.")

    while people_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            people_page_datas.append(scrap_people_page(people_link))
            people_link = next(people_links, None)
            loop = 0
            scrap_count += 1
            print(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * DELAY_AFTER_ONE_REQUEST, 1))

        # in case of an error, it tries running with a different proxy 5 times before giving up and logging the error
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

    # stores all extracted data in csv files.
    store_people_page_data(people_page_datas)


def main():
    """
    creates the data directory to hold all files (if it doesn't exist).
    uses all previous functons to scrap and store all data
    :return:
    """
    # creates Datas directory if it doesn't exist
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)

    # gets a list of all anime page links , scraps and stores the info in csv files
    anime_links = main_get_and_store_anime_links(datas_dir)

    # main_scrap_and_store_anime_pages(anime_links)
    #
    main_scrap_and_store_anime_stats_pages(anime_links)
    #

    # gets a list of all people pages links, scraps and stores the info in csv files.
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
