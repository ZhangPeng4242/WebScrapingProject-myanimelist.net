from scrap_archive_page import get_season_links
from scrap_season_page import get_anime_links

from scrap_stats_page import scrap_stats_page
from scrap_anime_page import scrap_anime_page
from store_stats_page_data import store_stats_page_data
from store_anime_page_data import store_anime_page
from pathlib2 import Path
import os


def main():
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
            err_log.append(f"scrap_stats_page: {anime_link}  {err}")
            continue

    store_stats_page_data(stats_page_datas)

    # Scrap anime page
    anime_page_datas = []
    for anime_link in anime_links:
        try:
            anime_page_datas.append(scrap_anime_page(anime_link))

        except Exception as err:
            err_log.append(f"scrap_anime_page: {anime_link} {str(err)}")
            continue

    store_anime_page(anime_page_datas)

    print("Successfully finished all the scraping!!!Good job!")


if __name__ == "__main__":
    err_log = []
    try:
        main()
    except Exception as err:
        err_log.append(str(err))
    finally:
        # Write err_log:
        cur_path = Path(os.getcwd())
        log_dir = cur_path.parent / "Datas" / "err_log.txt"
        with open(log_dir, "w", encoding="utf-8") as err_log_file:
            err_log_file.write("\n".join(err for err in err_log))
