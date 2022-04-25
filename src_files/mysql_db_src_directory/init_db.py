"""This module is to initialize the database.
:export: init_db()"""

from src_files.config import config
import sqlparse
from pathlib2 import Path
import pandas as pd


def create_db():
    """
    Create the database on the localhost, make sure there's init_db_myanimelist.sql in the directory.
    :return: None
    """
    with open(Path(config.project_dir) / "src_files" / "mysql_db_src_directory" / "init_db_myanimelist.sql",
              "r") as sql_file:
        sql_script = sql_file.read()

    sql_list = sqlparse.split(sql_script)
    with config.connection:
        with config.connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {config.mysql_connection['database']}")
            for sql in sql_list:
                sql = sql.replace('db_myanimelist', config.mysql_connection["database"])
                cursor.execute(sql)
            config._initiated = True
    config.logger.info("Database successfully created!")


def insert_init_data():
    """
    This is to insert all the init_data in the _init_datas_ into the database.
    :return: None
    """
    file_list = ['anime.csv', 'people.csv', 'character.csv', 'genre.csv', 'studio.csv', 'voice_actor.csv',
                 'anime_genre.csv', 'studio_anime.csv', 'anime_character.csv', 'anime_watch_stats.csv',
                 'anime_score_stats.csv', 'anime_general_stats.csv', 'staff.csv', 'description.csv', 'api_imdb.csv',
                 'api_description_sentiment_analysis.csv']

    for file_name in file_list:
        df = pd.read_csv(Path(config.datas_dir) / file_name)
        df.to_sql(file_name[:-4], config.engine, if_exists="append", index=False)

        config.logger.info(f"Successfully initiated table: {file_name[:-4]}")


def init_db():
    """
    A function of action which initiates the db_myanimelist database on your localhost.
    :return: None
    """
    create_db()
    insert_init_data()
    config.logger.info(f"Successfully initiated database: {config.mysql_connection['database']}!")
