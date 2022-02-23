from Webscraping.Modules.archive_page import get_season_links
from Webscraping.Modules.season_page import get_anime_links

from Webscraping.Modules.stats_page import scrap_stats_page
from Webscraping.Modules.anime_page import scrap_anime_page
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
    anime_stats = []

    for anime_link in anime_links:
        anime_stats.append(scrap_stats_page(f'{anime_link}/stats'))

    with open("Datas/anime_sum_stats.csv", "w") as anime_sum_stats_csv_file:
        field_names = ['anime_id', 'Watching', 'Completed', 'On-Hold', 'Dropped', 'Plan to Watch', 'Total']
        writer = csv.DictWriter(anime_sum_stats_csv_file, fieldnames=field_names)
        writer.writeheader()
        for stat in anime_stats:
            writer.writerow(stat[0])

    with open("Datas/anime_score_stats.csv", "w") as anime_score_stats_csv_file:
        field_names = ["anime_id"] + [str(num) for num in range(10, 0, -1)]
        writer = csv.DictWriter(anime_score_stats_csv_file, fieldnames=field_names)
        writer.writeheader()
        for stat in anime_stats:
            writer.writerow(stat[1])

    # Scrap anime page


if __name__ == "__main__":
    main()
