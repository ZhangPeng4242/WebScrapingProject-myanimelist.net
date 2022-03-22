import csv
import os
from pathlib2 import Path
from src_files.config import config


def store_studios_info_data(studios_info_list, _test=False):

    with open(Path(config.datas_dir) / f'4_studios_info{"_test" if _test else ""}.csv', "w", encoding="utf-8",
              newline="") as studios_info_file:
        field_names = [key for key in studios_info_list[0].keys()]
        writer = csv.DictWriter(studios_info_file, fieldnames=field_names)
        writer.writeheader()
        for studio_info in studios_info_list:
            writer.writerow(studio_info)

    config.logger.info("All studios info successfully stored!!")
