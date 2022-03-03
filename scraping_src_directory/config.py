import logging
import os
import sys
from pathlib2 import Path


class Configuration:
    def __init__(self, config_dict):
        self.datas_dir = config_dict['datas_dir']
        self.logger = config_dict['logger']
        self.proxy_change_delay = config_dict['proxy_change_delay']
        self.rescrap_delay = config_dict['rescrap_delay']


def get_datas_dir():
    datas_dir = Path(os.getcwd()).parent / "Datas"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)
    return Path(os.getcwd()).parent / "Datas"


def get_logger():
    logger = logging.getLogger("web_scraping")
    logger.setLevel(logging.DEBUG)
    formatter_info = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    formatter_error = logging.Formatter(
        '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

    file_handler1 = logging.FileHandler(Path(get_datas_dir()) / "scraping.log")
    file_handler1.setLevel(logging.DEBUG)
    file_handler1.setFormatter(formatter_info)
    logger.addHandler(file_handler1)

    file_handler2 = logging.FileHandler(Path(get_datas_dir()) / "error.log")
    file_handler2.setLevel(logging.ERROR)
    file_handler2.setFormatter(formatter_error)
    logger.addHandler(file_handler2)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter_info)
    logger.addHandler(stream_handler)

    return logger


config_dict = {
    "datas_dir": get_datas_dir(),
    "logger": get_logger(),
    "delay_after_a_request": 0,
    "proxy_change_delay": 2,
    "rescrap_delay": 5,

}

config = Configuration(config_dict)
