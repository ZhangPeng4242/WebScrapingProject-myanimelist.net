"""
we make use of all of our libraries to scrap myanimelist and store the data in several csv files
"""
import random
from scrap_people_list_page import get_people_links
from scrap_people_page import scrap_people_page
from scrap_stats_page import scrap_stats_page
from scrap_anime_page import scrap_anime_page
from store_stats_page_data import store_stats_page_data
from store_anime_page_data import store_anime_page_data
from store_people_page_data import store_people_page_data
from scrap_anime_list_page import get_anime_links
import time
from config import config

config.delay_after_a_request = 1


def main_get_and_store_anime_links():
    """
    Get and store all the individual anime page links.
    checks if a file called anime_links.txt already exists and if not creates that file
    and uses get_anime_links to store all main anime page links inside of it.
    the function then returns all anime main page links as a list.
    :return: anime_links: list
    """
    # creates file path
    anime_links_path = config.datas_dir / "anime_links.txt"

    # if file exists, we get its content as a list
    if anime_links_path.exists():
        with open(anime_links_path, "r", encoding="utf-8") as anime_links_file:
            anime_links = anime_links_file.read().split("\n")

    # if not, we will scrap and get all the anime links and store them in anime_links.txt
    else:
        anime_links = get_anime_links()
        with open(anime_links_path, "w", encoding="utf-8") as anime_links_file:
            anime_links_file.write("\n".join(anime_links))

    # return list of all anime main page links
    config.logger.info("Successfully get all the anime links!")

    random.shuffle(anime_links)
    return anime_links


def main_get_and_store_people_links():
    """
    Get and store all the individual people page links.
    checks if a file called people_links.txt already exists and if not creates that file
    and uses get_people_links to store all main anime page links inside of it.
    the function then returns all people page links as a list.
    :return: people_links: list
    """
    # creates file path
    people_links_path = config.datas_dir / "people_links.txt"

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
    config.logger.info("Successfully get all the people links")
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
    config.logger.info("Starting to scrap anime pages.")
    # creates a list to store all scraped data from links and iterates over the anime_links list.
    anime_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0

    while anime_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            config.logger.info(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * config.delay_after_a_request, 1))

        # in case of n error, it tries running with a different proxy 5 times before giving up and logging the error
        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                config.logger.error(
                    f"scrap_anime_page: Error {anime_link} {str(err)}.\nContinue with next... ({scrap_count}/{total_count})")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            config.logger.error(f"scrap_anime_page: Failed attempt {loop}, rescraping... {anime_link}")
            time.sleep(config.rescrap_delay)
            continue

    # stores all extracted data in csv files.
    store_anime_page_data(anime_page_datas)


def main_scrap_and_store_anime_stats_pages(anime_links):
    """
    receives as input a list of anime main page links, changes them into stats page format,
    scrapes them for info using scrap_stats_page and stores them in a csv file with store_stats_page_data.
    it handles proxies being blocked by re-running with a different proxy when detecting errors during requests
    :param anime_links: list
    :return: None
    """
    config.logger.info("Start scraping anime stats pages.")

    # creates a list to store all scraped data from links and iterates over the anime_links list.
    stats_page_datas = []
    total_count = len(anime_links)
    anime_links = iter(anime_links)
    anime_link = next(anime_links, None)
    loop = 0
    scrap_count = 0

    while anime_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            stats_page_datas.append(scrap_stats_page(f'{anime_link}/stats'))
            anime_link = next(anime_links, None)
            loop = 0
            scrap_count += 1
            config.logger.info(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * config.delay_after_a_request , 1))

        # in case of an error, it tries running with a different proxy 5 times before giving up and logging the error
        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                config.logger.error(
                    f"scrap_anime_page: Error {anime_link}/stats {str(err)}.\nContinue with next... ({scrap_count}/{total_count})")
                anime_link = next(anime_links, None)
                loop = 0
                continue

            loop += 1
            config.logger.error(f"scrap_anime_page: Failed attempt {loop}, rescraping... {anime_link}/stats")
            time.sleep(config.rescrap_delay)
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
    config.logger.info("Start scraping people pages.")
    # creates a list to store all scraped data from links and iterates over the people_links list.
    people_page_datas = []
    total_count = len(people_links)
    people_links = iter(people_links)
    people_link = next(people_links, None)
    loop = 0
    scrap_count = 0

    while people_link:
        # in case of no errors, it appends the scraped info from current list
        try:
            people_page_datas.append(scrap_people_page(people_link))
            people_link = next(people_links, None)
            loop = 0
            scrap_count += 1
            config.logger.info(f"scraping_progress: ({scrap_count}/{total_count})")
            time.sleep(round(random.random() * config.delay_after_a_request, 1))

        # in case of an error, it tries running with a different proxy 5 times before giving up and logging the error
        except Exception as err:
            if loop >= 4:
                scrap_count += 1
                config.logger.error(
                    f"scrap_anime_page: Error {people_link} {str(err)}.\nContinue with next... ({scrap_count}/{total_count})")
                people_link = next(people_links, None)
                loop = 0
                continue

            loop += 1
            config.logger.error(f"scrap_anime_page: Failed attempt {loop}, rescraping... {people_link}")
            time.sleep(config.rescrap_delay)
            continue

    # stores all extracted data in csv files.
    store_people_page_data(people_page_datas)


def main():
    """
    creates the data directory to hold all files (if it doesn't exist).
    uses all previous functons to scrap and store all data
    :return:
    """
    # Step 1: get and store all the anime links
    anime_links = main_get_and_store_anime_links()

    # Step 2: scrap and store all the anime pages data
    # main_scrap_and_store_anime_pages(anime_links)

    # Step 3: scrap and store all the anime stats pages data
    main_scrap_and_store_anime_stats_pages(anime_links)

    # Step 4: get and store all the people links
    # people_links = main_get_and_store_people_links()

    # Step 5: scrap and store all the people pages data
    # main_scrap_and_store_people_pages(people_links)

    config.logger("Successfully finished all the scraping!!! Good job!")


if __name__ == "__main__":
    err_log = []
    try:
        main()
    except Exception as err:
        config.logger.error(err)
