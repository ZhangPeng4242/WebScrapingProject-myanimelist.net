import sys
import os
from pathlib2 import Path

src_path = Path(os.getcwd()).parent / "scraping_src_directory"
sys.path.append(str(src_path))
from store_stats_page_data import store_stats_page_data
from ..config import config

def test():
    """
    Run this program directly to test store_stats_page_data function
    :return: None
    """
    test_data = [({'watching': 15062, 'completed': 128422, 'on-hold': 9963, 'dropped': 9028, 'plan to watch': 44438,
                   'total': 206913, 'anime_id': '18179'},
                  {'10': 11259, '9': 22063, '8': 36107, '7': 22906, '6': 7308, '5': 2815, '4': 936, '3': 323, '2': 132,
                   '1': 151, 'anime_id': '18179'}),
                 ({'watching': 65017, 'completed': 1, 'on-hold': 1191, 'dropped': 4902, 'plan to watch': 35088,
                   'total': 106199, 'anime_id': '47161'},
                  {'10': 1595, '9': 1170, '8': 2465, '7': 4707, '6': 3999, '5': 2739, '4': 1580, '3': 903, '2': 438,
                   '1': 438, 'anime_id': '47161'})]
    store_stats_page_data(test_data, _test=True)


if __name__ == "__main__":
    test()
