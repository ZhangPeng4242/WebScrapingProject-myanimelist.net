"""This module is to build functions that check if a record already existed in the database"""

from src_files.config import config


def is_exist(crit_name, crit_value, tb_name):
    """
    This function check if a record already existed in the database, with single field identifier.
    :param crit_name: str, the field name for identification
    :param crit_value: str/int, the value for identification
    :param tb_name: str, the name of the table
    :return: Boolean, True: record exist, False: record not exist
    """

    sql = f"""SELECT EXISTS( SELECT * FROM {tb_name} WHERE {crit_name} = {f"'{crit_value}'" if type(crit_value) != int else crit_value}) AS result"""
    if not config.is_connected():
        config.reconnect()

    with config.connection as connection:
        with connection.cursor() as cursor:
            # cursor.execute("USE db_myanimelist")
            cursor.execute(sql)
            if not int(cursor.fetchall()[0]["result"]):
                return False
            else:
                return True


def is_exist_double(crit1, crit2, tb_name):
    """
    This function check if a record already existed in the database, with double field identifiers.
    :param crit1: tuple, First identifier, position 0: str, the field name for identification, position 1: str, the value for identification
    :param crit2: tuple, Second identifier, position 0: str, the field name for identification, position 1: str, the value for identification
    :param tb_name: str, the name of the table
    :return: Boolean: True: record exist, False: record not exist
    """
    sql = f"""SELECT EXISTS( SELECT * FROM {tb_name} WHERE {crit1[0]} = {f"'{crit1[1]}'" if type(crit1[1]) != int else crit1[1]} AND {crit2[0]} = {f"'{crit2[1]}'" if type(crit2[1]) != int else crit2[1]}) AS result"""
    if not config.connection.open:
        config.reconnect()

    with config.connection as connection:
        with connection.cursor() as cursor:
            # cursor.execute("USE db_myanimelist")
            cursor.execute(sql)
            res = cursor.fetchall()[0]["result"]
            if not int(res):
                return False
            else:
                return True
