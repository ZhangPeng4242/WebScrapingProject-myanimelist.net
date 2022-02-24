from archive_page import get_season_links
from season_page import get_anime_links

from stats_page import scrap_stats_page
from anime_page import scrap_anime_page
from store_stats_page_data import store_stats_page_data
from store_anime_page_data import store_anime_page
from pathlib2 import Path
import os


def main():
    err_log = []

    # get list of all season links
    season_links = get_season_links()

    # get list of all anime links
    anime_links = set([])
    i = 0
    for link in season_links:
        if i > 0:
            break
        anime_links |= get_anime_links(link)
        i += 1

    # Scrap stats page
    stats_page_datas = []
    for anime_link in anime_links:
        try:
            stats_page_datas.append(scrap_stats_page(f'{anime_link}/stats'))
        except Exception as err:
            err_log.append(f"{anime_link}: {err}")

    store_stats_page_data(stats_page_datas)

    # Scrap anime page
    anime_page_datas = []
    for anime_link in anime_links:
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))
        except Exception as err:
            err_log.append(f"{anime_link}: {err}")

    store_anime_page(anime_page_datas)

    # Write err_log:
    cur_path = Path(os.getcwd())
    log_dir = cur_path.parent / "Datas" / "err_log.txt"
    with open(log_dir, "w") as err_log_file:
        err_log_file.write("\n".join(err for err in err_log))

    print("Successfully finished all the scraping!!!Good job!")

if __name__ == "__main__":
    main()
