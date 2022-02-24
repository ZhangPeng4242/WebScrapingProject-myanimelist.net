from Modules.archive_page import get_season_links
from Modules.season_page import get_anime_links

from Modules.stats_page import scrap_stats_page
from Modules.anime_page import scrap_anime_page
from Modules.store_stats_page_data import store_stats_page_data
import csv


def main():
    season_links = get_season_links()
    anime_links = set([])
    i = 0
    for link in season_links:
        if i > 0:
            break
        anime_links |= get_anime_links(link)
        i += 1

    # Scrap stats page
    anime_stats=[]
    for anime_link in anime_links:
       anime_stats.append(scrap_stats_page(f'{anime_link}/stats'))
    store_stats_page_data(anime_stats)

    # Scrap anime page


if __name__ == "__main__":
    main()
