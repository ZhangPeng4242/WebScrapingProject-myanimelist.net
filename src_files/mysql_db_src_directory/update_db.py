"""This module is to update the table in the database.
:export: update_table()"""

from src_files.config import config
from .db_info import db_info
from src_files.scraping_src_directory.record_exists_check import is_exist, is_exist_double
import pandas as pd


def update_table(df, crit_name, tb_name, double=False, insert_only=False, update_logging=True):
    """
    This function is to update/insert record in the database. If exists update, else insert the new record.
    :param df: dataframe of the data needed to be updatted,
    :param crit_name: the column name for identification of a record.
    :param tb_name: the name of the table
    :param double: Some record is identified by double columns, if exists do nothing, else insert.
    :param insert_only: Some tables don't need update but only insert.
            Therefore, if it is True, it will only insert the new record.
    :param update_logging: Decide if the update will be recorded in the logging.
    :return:
    """

    tb_name = f"`{tb_name}`" if tb_name == 'character' else tb_name

    sql_keywords = ['name', 'rank']
    # Check if the record already exisits.
    for indx, row in df.iterrows():
        exists = is_exist(crit_name, row[crit_name], tb_name) if not double else is_exist_double(
            (crit_name[0], row[crit_name[0]]), (crit_name[1], row[crit_name[1]]), tb_name)

        if not config.connection.open:
            config.reconnect()

        if exists:
            if insert_only or double:
                continue
            # Update
            with config.connection:
                with config.connection.cursor() as cursor:
                    sql = f"""UPDATE {tb_name} SET {', '.join([f"{f'`{col}`' if col.isnumeric() else col} = %s" for col in db_info[tb_name.strip("`")]['order']])} WHERE {crit_name} = {row[crit_name]}"""
                    sql_value = [None if pd.isna(val) else val for val in row]
                    cursor.execute(f"USE {config.mysql_connection['database']}")
                    cursor.execute(sql, sql_value)
                    config.connection.commit()
                    if update_logging:
                        config.logger.info(f"Record update success! Table: {tb_name}, ID: {row[0]}")
        else:
            # Insert
            with config.connection:
                with config.connection.cursor() as cursor:
                    sql = f"""INSERT INTO {tb_name} ({', '.join([f"{f'`{col}`' if col.isnumeric() or col in sql_keywords else col}" for col in db_info[tb_name.strip("`")]['order']])}) VALUES ({', '.join(['%s' for i in range(len(db_info[tb_name.strip("`")]['order']))])})"""
                    sql_value = [None if pd.isna(val) else val for val in row]
                    cursor.execute(f"USE {config.mysql_connection['database']}")
                    cursor.execute(sql, sql_value)
                    config.connection.commit()
                    config.logger.info(f"Insert new record! Table: {tb_name}, ID: {row[0]}")