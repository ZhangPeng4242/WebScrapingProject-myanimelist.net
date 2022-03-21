import logging
import os
import sys
from pathlib2 import Path
import pymysql
from pymysql import cursors
import json
import sqlalchemy


class Configuration:
    def __init__(self, config_dict):
        self.project_dir = get_project_folder_dir()
        self.datas_dir = config_dict['datas_dir']
        self.logs_dir = config_dict['logs_dir']
        self.logger = config_dict['logger']
        self.proxy_change_delay = config_dict['proxy_change_delay']
        self.rescrap_delay = config_dict['rescrap_delay']
        self.mysql_connection = config_dict['mysql_connection']
        self.connection = self._get_connection()
        self.engine = self._get_engine()

    def _get_connection(self):
        return pymysql.connect(host=self.mysql_connection["host"], user=self.mysql_connection["user"],
                               password=self.mysql_connection["password"],
                               cursorclass=pymysql.cursors.DictCursor)

    def _get_engine(self):
        return sqlalchemy.create_engine(
            f'mysql+pymysql://{self.mysql_connection["user"]}:{self.mysql_connection["password"]}@{self.mysql_connection["host"]}/db_myanimelist?charset=utf8')

    def is_connected(self):
        return self.connection.open

    def reconnect(self):
        self.connection = self._get_connection()

    def set_sql_connection(self, name, password):
        self.mysql_connection["user"] = name
        self.mysql_connection["password"] = password
        self.reconnect()

    def get_params(self):
        config_path = Path(os.getcwd()) / 'config.json'
        if Path(config_path).exists():
            with open(config_path, "r") as config_file:
                config_json = json.load(config_file)
            self.datas_dir = config_json["datas_dir"]
            self.logs_dir = config_json["logs_dir"]
            self.proxy_change_delay = config_json['proxy_change_delay']
            self.rescrap_delay = config_json['rescrap_delay']
            self.mysql_connection["user"] = config_json["mysql_connection"]["user"]
            self.mysql_connection["password"] = config_json["mysql_connection"]["password"]
            self.engine = self._get_engine()
            self.reconnect()

    def get_json(self):
        return {
            "datas_dir": str(get_datas_dir()),
            "logs_dir": str(get_logs_dir()),
            "delay_after_a_request": 0,
            "proxy_change_delay": 2,
            "rescrap_delay": 5,
            "mysql_connection": {
                "host": "127.0.0.1",
                "user": self.mysql_connection["user"],
                "password": self.mysql_connection["password"]
            }
        }


def get_project_folder_dir():
    cur_dir = os.getcwd()
    folder_dir = cur_dir[:cur_dir.index("ITC-DataMining-Project")] + "ITC-DataMining-Project/"
    return folder_dir


def get_datas_dir():
    datas_dir = Path(get_project_folder_dir()) / "_init_datas_"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)
    return datas_dir


def get_logs_dir():
    logs_dir = Path(get_project_folder_dir()) / "logs"
    if not Path(logs_dir).exists():
        os.mkdir(logs_dir)
    return logs_dir


def get_logger():
    logger = logging.getLogger("web_scraping")
    logger.setLevel(logging.DEBUG)
    formatter_info = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    formatter_error = logging.Formatter(
        '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

    file_handler1 = logging.FileHandler(Path(get_logs_dir()) / "scraping.log")
    file_handler1.setLevel(logging.DEBUG)
    file_handler1.setFormatter(formatter_info)
    logger.addHandler(file_handler1)

    file_handler2 = logging.FileHandler(Path(get_logs_dir()) / "error.log")
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
    "logs_dir": get_logs_dir(),
    "logger": get_logger(),
    "delay_after_a_request": 0,
    "proxy_change_delay": 2,
    "rescrap_delay": 5,
    "mysql_connection": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "zp2543765"
    }
}

config = Configuration(config_dict)
config.get_params()
