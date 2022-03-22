import argparse
import json
import logging

import pymysql
from src_files.config import config
from src_files.mysql_db_src_directory.init_db import init_db
from pathlib2 import Path
from src_files.argparser_config import get_parser
from src_files.scraping_src_directory.get_links_by_commands import *
from src_files.scraping_src_directory.scrap_anime_page import scrap_anime_page
from src_files.scraping_src_directory.scrap_people_page import scrap_people_page


def main():
    """
    We wrap our code using argparse and execute it using all the modules we created thus far.
    :return: None
    """
    parser = get_parser()
    args = parser.parse_args()
    # print(args)

    if args.main == 'init':
        config.logger.info("Start initiating the project...")

        # 1. Setting up config
        config.set_sql_connection(args.username, args.password, args.host, args.port)

        with open(Path(config.project_dir) / "config.json", "w") as write_file:
            json.dump(config.get_json(), write_file, indent=4)
        config.logger.info(f"Successfully created config.json at {config.project_dir}/config.json")
        config.get_params()

        # 2. Init Database
        init_db()

        if not config.connection:
            parser.error('Could not log in to mysql with the given parameters. Please confirm and try it again.')

        config.logger.info(
            "Congratulations! You have successfully initiated the project. Run it again for other commands.")
        # print(config.connection)
        # if args.location == 'remote':
        #     pass
        #     print('remote')
        #
        # elif args.location == 'local':
        #     pass
        # print('local')
        #
        # else:
        #     if not args.help:
        #         parser.error('please choose where to store data')

    elif args.main == 'scrap':
        config.logger.info("Start scraping...")
        if not config.connection:
            parser.error(
                'Please initiate the project first. Using: init local|remote db_username db_password [--host] [--port]')

        if args.type == 'anime':
            # print('anime')
            if args.name:
                anime_link_list = get_anime_link_by_name(args.name)
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)
            elif args.rank:
                anime_link_list = get_anime_link_by_rank(args.rank)
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)
            elif args.year:
                anime_link_list = get_anime_link_by_year(args.year)
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)
            elif args.genre:
                anime_link_list = get_anime_link_by_genre(args.genre)
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)
            elif args.studio:
                anime_link_list = get_anime_link_by_studio(args.studio)
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)
            else:
                config.logger.warning("Start scraping all anime pages, this process might take over 15 hours to complete.")

                anime_link_list = get_anime_links()
                for anime_link in anime_link_list:
                    scrap_anime_page(anime_link)

        elif args.type == 'people':
            # print('people')
            if args.anime:
                people_link_list = get_people_link_by_anime_name(args.anime)
                for people_link in people_link_list:
                    scrap_people_page(people_link)
            elif args.name:
                people_link_list = get_people_link_by_name(args.name)
                for people_link in people_link_list:
                    scrap_people_page(people_link)
            elif args.rank:
                people_link_list = get_people_link_by_rank(args.rank)
                for people_link in people_link_list:
                    scrap_people_page(people_link)
            else:
                config.logger.warning("Start scraping all people pages, this process might take over 12 hours to complete.")

                people_link_list = get_people_links()
                for people_link in people_link_list:
                    scrap_people_page(people_link)

        else:
            config.logger.warning("Start scraping all the pages, this process might take over 30 hours to complete.")

            anime_link_list = get_anime_links()
            for anime_link in anime_link_list:
                scrap_anime_page(anime_link)
            people_link_list = get_people_links()
            for people_link in people_link_list:
                scrap_people_page(people_link)

    else:
        parser.error('please choose scrap or init (choose init if this is your first time running)')


if __name__ == "__main__":
    try:
        main()
        config.logger.info(
            "You have successfully scrap and updated everything! Run the program again for another action.")
    except KeyboardInterrupt:
        config.logger.warning(
            "You have manually stopped the program, all the scrapping process conducted has been updated in the database.")
