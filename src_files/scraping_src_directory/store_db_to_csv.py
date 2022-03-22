import pandas as pd
from src_files.config import config
from pathlib2 import Path
from src_files.mysql_db_src_directory.db_info import db_info
import os


def store_db_to_csv():
    outpath = Path(config.project_dir) / "db_datas"

    if not Path(outpath).exists():
        os.mkdir(outpath)

    for db_name in db_info.keys():
        df = pd.read_sql_table(db_name, config.engine)
        df.to_csv(outpath)

    config.logger.info(f"Successfully export database into csv at {outpath}")

store_db_to_csv()