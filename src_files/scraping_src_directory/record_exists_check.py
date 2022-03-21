import pandas as pd
import sqlalchemy
from src_files.config import config



def is_exist(crit_name, crit_value, db_name):
    sql = f"""SELECT EXISTS( SELECT * FROM {db_name} WHERE {crit_name} = {f"'{crit_value}'" if type(crit_value) != int else crit_value}) AS result"""
    if not config.connection.open:
        config.reconnect()

    with config.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("USE db_myanimelist")
            cursor.execute(sql)
            if not int(cursor.fetchall()[0]["result"]):
                return False
            else:
                return True

    config.reconnect()


def is_exist_double(crit1, crit2, db_name):
    sql = f"""SELECT EXISTS( SELECT * FROM {db_name} WHERE {crit1[0]} = {f"'{crit1[1]}'" if type(crit1[1]) != int else crit1[1]} AND {crit2[0]} = {f"'{crit2[1]}'" if type(crit2[1]) != int else crit2[1]}) AS result"""
    if not config.connection.open:
        config.reconnect()

    with config.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("USE db_myanimelist")
            cursor.execute(sql)
            if not int(cursor.fetchall()[0]["result"]):
                return False
            else:
                return True

    config.reconnect()

# def is_anime_exist(anime_id):
#     df_anime = pd.read_sql_table("anime", ENGINE)
#     if not (df_anime["id"] == anime_id).any():
#         return False
#     return True
#
#
# def is_genre_exist(name):
#     with config.connection as connection:
#         with connection.cusor() as cursor:
#
#
# def is_studio_exist(studio_id):
#     df_studio = pd.read_sql_table('studio', ENGINE)
#     if not (df_studio["id"] == studio_id).any():
#         return False
#         # todo: change this when updaye scrap studio
#     return True
#
#
# def is_people_exist(people_id):
#     df_people = pd.read_sql_table("genre", ENGINE)
#     if not (df_people["id"] == people_id).any():
#         scrap_studio_page(f"https://myanimelist.net/people/{people_id}")
