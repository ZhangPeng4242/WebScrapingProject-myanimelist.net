"""This is the main function for the project, and the only python file the user should run."""
import json
import os
from src_files.mysql_db_src_directory.init_db import init_db
from pathlib2 import Path
from src_files.argparser_config import get_parser
from src_files.scraping_src_directory.get_links_by_commands import *
from src_files.mysql_db_src_directory.export_db_to_csv import export_db_to_csv
from src_files.scraping_src_directory.scrap_and_update import scrap_and_update_people, scrap_and_update_anime
from src_files.api_src_directory.get_imdb_score import get_imdb_score
from src_files.mysql_db_src_directory.update_db import update_table
from src_files.api_src_directory.get_synopsis_sentiment import get_synopsis_sentiment


def get_anime_link_list(args):
    """
    This function is to assign different get_anime_link functions according to different args
    :param args:
    :return: anime_link_list: list
    """
    if args.name:
        anime_link_list = get_anime_link_by_name(args.name)
    elif args.rank:
        anime_link_list = get_anime_link_by_rank(args.rank)
    elif args.year:
        anime_link_list = get_anime_link_by_year(args.year)
    elif args.genre:
        anime_link_list = get_anime_link_by_genre(args.genre)
    elif args.studio:
        anime_link_list = get_anime_link_by_studio(args.studio)
    else:
        config.logger.warning(
            "Start scraping all anime pages, this process might take over 15 hours to complete.")
        anime_link_list = get_anime_links()
    return anime_link_list


def get_people_link_list(args):
    """
    This function is to assign different get_people_link functions according to different args
    :param args:
    :return: people_link_list: list
    """
    if args.anime:
        people_link_list = get_people_link_by_anime_name(args.anime)
    elif args.name:
        people_link_list = get_people_link_by_name(args.name)
    elif args.rank:
        people_link_list = get_people_link_by_rank(args.rank)
    else:
        config.logger.warning(
            "Start scraping all people pages, this process might take over 12 hours to complete.")
        people_link_list = get_people_links()
    return people_link_list


def main(parser=None):
    """
    Main function for the project, handle different kind of commands.
    :return: None
    """
    if not parser:
        parser = get_parser()

    args = parser.parse_args()

    # init
    if args.main == 'init':
        config.logger.info("Start initiating the project...")

        if Path(Path(config.project_dir) / "config.json").exists():
            os.remove(Path(config.project_dir) / "config.json")

        # 1. Setting up config
        config.set_sql_connection(args.username, args.password, host = args.host, port = args.port, db=args.db)

        with open(Path(config.project_dir) / "config.json", "w") as write_file:
            json.dump(config.get_json(), write_file, indent=4)
        config.logger.info(f"Successfully created config.json at {config.project_dir}config.json")
        config.get_params()

        # 2. Init Database
        init_db()

        if not config.connection:
            parser.error('Could not log in to mysql with the given parameters. Please confirm and try it again.')

        config.logger.info(
            "Congratulations! You have successfully initiated the project. Run it again for other commands.")

    # scrap
    elif args.main == 'scrap':
        if not Path(Path(config.project_dir) / "config.json").exists():
            parser.error(
                'Please initiate the project first. Using: init local|remote db_username db_password [--host] [--port]')

        config.logger.info("Start scraping...")

        if args.type == 'anime':
            anime_link_list = get_anime_link_list(args)
            for anime_link in anime_link_list:
                try:
                    scrap_and_update_anime(anime_link)
                except Exception as exc1:
                    config.logger.error(f"{exc1}: {args.main} {args.type} {anime_link}")

        elif args.type == 'people':
            people_link_list = get_people_link_list(args)
            for people_link in people_link_list:
                try:
                    scrap_and_update_people(people_link)
                except Exception as exc1:
                    config.logger.error(f"{exc1}: {args.main} {args.type} {people_link}")

        else:
            config.logger.warning("Start scraping all the pages, this process might take over 30 hours to complete.")
            anime_link_list = get_anime_links()
            for anime_link in anime_link_list:
                try:
                    scrap_and_update_anime(anime_link)
                except Exception as exc1:
                    config.logger.error(f"{exc1}: {args.main} {args.type} {anime_link}")

            people_link_list = get_people_links()
            for people_link in people_link_list:
                try:
                    scrap_and_update_people(people_link)
                except Exception as exc1:
                    config.logger.error(f"{exc1}: {args.main} {args.type} {people_link}")
    # api
    elif args.main == 'api':
        if args.type == 'imdb':
            anime_link_list = get_anime_link_list(args)
            for anime_link in anime_link_list:
                try:
                    df_imdb_score = get_imdb_score(anime_link)
                    update_table(df_imdb_score, "anime_id", "api_imdb")
                except Exception as exc1:
                    config.logger.error(f"{exc1}: {args.main} {args.type} {anime_link}")

        elif args.type == 'sentiment_analysis':
            anime_link_list = get_anime_link_list(args)
            try:
                df_synopsis_sentiment = get_synopsis_sentiment(anime_link_list)
                update_table(df_synopsis_sentiment, "anime_id", "api_description_sentiment_analysis")
            except Exception as exc1:
                config.logger.error(f"{exc1}: {args.main} {args.type}")

        else:
            config.logger.error(f"Api commands incorrect")

    # export
    elif args.main == 'export':
        export_db_to_csv()

    else:
        parser.error('please choose scrap or init (choose init if this is your first time running)')


if __name__ == "__main__":
    try:
        main()
        config.logger.info(
            "Program has ended! Run the main.py again for another action.")
    except KeyboardInterrupt:
        config.logger.warning(
            "You have manually stopped the program, all the scrapping process conducted has been updated in the database.")
    except Exception as exc:
        config.logger.error(exc)
