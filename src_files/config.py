"""This module is to build the configuration for the project to use,  a global config instance from the Configuration class
:export: config"""

import logging
import os
import sys
from pathlib2 import Path
import pymysql
from pymysql import cursors
import json
import sqlalchemy


class Configuration:
    """
    A class of Configuration
    """

    def __init__(self, config_dict):
        """Init the config instance, reading and setting the properties from config_dict
        :return: None
        """
        self.project_dir = get_project_folder_dir()
        self.datas_dir = config_dict['datas_dir']
        self.logs_dir = config_dict['logs_dir']
        self.logger = get_logger()
        self.proxy_change_delay = config_dict['proxy_change_delay']
        self.delay_after_request = config_dict['delay_after_request']
        self.rescrap_delay = config_dict['rescrap_delay']
        self.mysql_connection = config_dict['mysql_connection']
        self.connection = self._get_connection()
        self.engine = self._get_engine()
        self.timeout = config_dict['request_timeout']
        self.monkeylearn_key = config_dict['monkeylearn_key']
        self._initiated = False

    def _get_connection(self):
        """
        Configure and build pymysql connection
        :return: pymysql.connect
        """
        try:
            if self.mysql_connection["password"] and self.mysql_connection["user"]:
                return pymysql.connect(host=self.mysql_connection["host"], user=self.mysql_connection["user"],
                                       password=self.mysql_connection["password"], port=self.mysql_connection["port"],db=None if not self._initiated else self.mysql_connection["database"],
                                       cursorclass=pymysql.cursors.DictCursor)

        except Exception:
            self.logger.error("Error: Database connection error! Please check your connection/username/password is correct!")
            os._exit(0)

    def _get_engine(self):
        """
        Create engine for sqlalchemy connection
        :return: sqlalchemy engine
        """
        return sqlalchemy.create_engine(
            f'mysql+pymysql://{self.mysql_connection["user"]}:{self.mysql_connection["password"]}@{self.mysql_connection["host"]}:{self.mysql_connection["port"]}/{self.mysql_connection["database"]}?charset=utf8')

    def is_connected(self):
        """
        Check if mysql connection is closed.
        :return: boolean, True: connected, False: closed
        """
        self.get_params()
        self.reconnect()
        return self.connection.open

    def reconnect(self):
        """
        Reconnect to mysql
        :return: None
        """
        self.connection = self._get_connection()

    def set_sql_connection(self, name, password, host='127.0.0.1', port=3306, db="db_myanimelist"):
        """
        Set the sql connection parameters
        :param name: mysql username
        :param password: mysql passsword
        :param host: mysql host
        :param port: mysql host
        :return: None
        """
        self.mysql_connection["user"] = name
        self.mysql_connection["password"] = password
        self.mysql_connection["host"] = host
        self.mysql_connection["port"] = port
        self.mysql_connection["database"] = db
        self.reconnect()

    def get_params(self):
        """
        Read the config.json and set the config properties according to the json file.
        :return: None
        """
        config_path = Path(get_project_folder_dir()) / 'config.json'
        if Path(config_path).exists():
            with open(config_path, "r") as config_file:
                config_json = json.load(config_file)

            self.datas_dir = config_json["datas_dir"]
            self.logs_dir = config_json["logs_dir"]
            self.delay_after_request = config_json["delay_after_request"]
            self.proxy_change_delay = config_json['proxy_change_delay']
            self.rescrap_delay = config_json['rescrap_delay']
            self.timeout = config_json['request_timeout']
            self.monkeylearn_key=config_json["monkeylearn_key"]
            self.mysql_connection["user"] = config_json["mysql_connection"]["user"]
            self.mysql_connection["password"] = config_json["mysql_connection"]["password"]
            self.mysql_connection["host"] = config_json["mysql_connection"]["host"]
            self.mysql_connection["port"] = config_json["mysql_connection"]["port"]
            self.mysql_connection["database"] = config_json["mysql_connection"]["database"]

            self.engine = self._get_engine()

    def get_json(self):
        """
        Format the user adjustable configuration parameter into dictionary (json format)
        :return: configuration dictionary
        """
        return {
            "datas_dir": str(get_datas_dir()),
            "logs_dir": str(get_logs_dir()),
            "delay_after_request": self.delay_after_request,
            "proxy_change_delay": self.proxy_change_delay,
            "rescrap_delay": self.rescrap_delay,
            "request_timeout": self.timeout,
            "monkeylearn_key": self.monkeylearn_key,
            "mysql_connection": {
                "host": self.mysql_connection["host"],
                "port": self.mysql_connection["port"],
                "user": self.mysql_connection["user"],
                "password": self.mysql_connection["password"],
                "database": self.mysql_connection["database"]
            }
        }


def get_project_folder_dir():
    """
    This is to handle the situation when user run part of the program at different directory level, and the paths are not correct.
    This is to find the highest parent directory no matter where the folder is or the program is run at.
    :return: folder_dir, the absolute path of the ITC-DataMining-Project directory
    """
    cur_dir = os.getcwd()
    folder_dir = cur_dir[:cur_dir.index("ITC-DataMining-Project")] + "ITC-DataMining-Project/"
    return folder_dir


def get_datas_dir():
    """
    This is to get the absolute path of the _init_datas_ folder
    :return: datas_dir, the absolute path of the _init_datas_
    """
    datas_dir = Path(get_project_folder_dir()) / "_init_datas_"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)
    return datas_dir


def get_logs_dir():
    """
    This is to get the absolute path of the logs folder
    :return: logs_dir, the absolute path of the logs
    """
    logs_dir = Path(get_project_folder_dir()) / "logs"
    if not Path(logs_dir).exists():
        os.mkdir(logs_dir)

    return logs_dir


def get_logger():
    """
    This is to initiate and configure the logging.
    :return: logger, instance
    """
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
    "datas_dir": str(get_datas_dir()),
    "logs_dir": str(get_logs_dir()),
    "delay_after_request": 0,
    "request_timeout": 100,
    "proxy_change_delay": 10,
    "rescrap_delay": 5,
    "monkeylearn_key": "c58353a32c5c93159197ff32f47b3b521744f795",
    "mysql_connection": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": None,
        "password": None,
        "database": None
    }
}

config = Configuration(config_dict)
config.get_params()