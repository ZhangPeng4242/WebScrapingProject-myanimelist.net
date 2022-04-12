"""This module is to export all the data in database into csv files.
 :export: export_db_to_csv()"""
import pandas as pd
from src_files.config import config
from pathlib2 import Path
from src_files.mysql_db_src_directory.db_info import db_info
import os


def export_db_to_csv():
    """
    A function of action which export the tables in database into multiple csv files.
    :return: None
    """
    outpath = Path(config.project_dir) / "db_data"

    if not Path(outpath).exists():
        os.mkdir(outpath)

    config.logger.info(f"Exporting data from db_myanimelist...")
    for db_name in db_info.keys():
        df = pd.read_sql_table(db_name, config.engine)
        df.to_csv(str(outpath) + f"/{db_name}.csv")

    config.logger.info(f"Successfully exported database into csv at {outpath}/")
