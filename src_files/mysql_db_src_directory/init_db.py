import pymysql
from pymysql import cursors
from src_files.config import config
import sqlparse


def init_db():
    connection = pymysql.connect(host=config.mysql_connection["host"], user=config.mysql_connection["user"],
                                 password=config.mysql_connection["password"], cursorclass=pymysql.cursors.DictCursor)

    with open("myanimelist_init_db.sql", "r") as sql_file:
        sql_script = sql_file.read()

    sql_list = sqlparse.split(sql_script)
    with connection:
        with connection.cursor() as cursor:
            for sql in sql_list:
                cursor.execute(sql)

    config.logger.info("Database successfully created!")


def insert_init_data():
    with open()
init_db()
