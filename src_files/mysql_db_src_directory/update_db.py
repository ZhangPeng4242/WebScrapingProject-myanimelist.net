import pandas as pd
import sqlalchemy
from src_files.config import config
from .db_info import db_info

# from db_info import db_info
ENGINE = sqlalchemy.create_engine('mysql+pymysql://root:zp2543765@localhost/db_myanimelist?charset=utf8')


def update_table(df, db_name, cursor):
    sql = f"""UPDATE {db_name} SET {', '.join([f"{f'`{col}`' if col.isnumeric() else col} = %s" for col in db_info[db_name]['order']])} WHERE {df.columns[0]} = {df.iloc[:, 0][0]}""";
    sql_value = [val for val in df.iloc[0]]
    cursor.execute("USE db_myanimelist")
    cursor.execute(sql, sql_value)
    config.connection.commit()
    config.logger.info(f"Database update success! Table: {db_name}, ID: {df.iloc[:, 0][0]}")


def update_anime_page_data(df_anime, df_anime_general_stats, df_anime_genre, df_studio_anime):
    df_db = pd.read_sql_table("anime", ENGINE)
    if not (df_db["id"] == df_anime["id"][0]).any():
        df_anime.to_sql("anime", ENGINE, if_exists="append", index=False)
        df_anime_general_stats.to_sql("anime_general_stats", ENGINE, if_exists="append", index=False)
        df_anime_genre.to_sql("anime_genre", ENGINE, if_exists="append", index=False)
        df_studio_anime.to_sql("studio_anime", ENGINE, if_exists="append", index=False)
        config.logger.info(f"Database insert new record success! ID: {df_anime['id'][0]}")
    else:
        if not config.connection.open:
            config.reconnect()
        with config.connection:
            with config.connection.cursor() as cursor:
                update_table(df_anime, 'anime', cursor)
                update_table(df_anime_general_stats, "anime_general_stats", cursor)
                # studios & anime_genre don't change, so no need to update
                # update_mid_table(df_anime_genre, 'anime_genre', cursor)
                # update_mid_table(df_studio_anime, 'studio_anime', cursor)


def update_anime_stats_page_data(df_anime_watch_stats, df_anime_score_stats):
    df_db = pd.read_sql_table("anime_watch_stats", ENGINE)
    if not (df_db["anime_id"] == df_anime_watch_stats["anime_id"][0]).any():
        df_anime_watch_stats.to_sql("anime_watch_stats", ENGINE, if_exists="append", index=False)
        df_anime_score_stats.to_sql("anime_score_stats", ENGINE, if_exists="append", index=False)
        config.logger.info(f"Database insert new record success! ID: {df_anime_watch_stats['anime_id'][0]}")
    else:
        if not config.connection.open:
            config.reconnect()
        with config.connection:
            with config.connection.cursor() as cursor:
                update_table(df_anime_watch_stats, 'anime_watch_stats', cursor)
                update_table(df_anime_score_stats, "anime_score_stats", cursor)


def update_people_page_data(df_people,df_character,df_staff):

    df_db = pd.read_sql_table("people", ENGINE)
    if not (df_db["id"] == df_people["id"][0]).any():
        df_people.to_sql("people", ENGINE, if_exists="append", index=False)
    else:
        if not config.connection.open:
            config.reconnect()
        with config.connection:
            with config.connection.cursor() as cursor:
                update_table(df_people, "people", cursor)
