"""
scraping_test_directory for the scrap_stats_page library
"""
from .pool_for_test import test_pool
import sys
import os
from pathlib2 import Path
src_path = Path(os.getcwd()).parent / "scraping_src_directory"
sys.path.append(str(src_path))
import scrap_stats_page as scr
# import pytest

def check_keys(input_tuple):
    """
    checks if the output of scrap_stats_page contains all mandatory keys.
    (we cant test for values as they constantly update).
    :param input_tuple: tuple of dicts
    :return: test: boolen
    """
    input_len = len(input_tuple)
    test = True
    sec_keys = [str(i) for i in range(10, 0, -1)]
    sec_keys.append('anime_id')
    key_tests = [('watching', 'completed', 'on-hold', 'dropped', 'plan to watch', 'total', 'anime_id'),
                 sec_keys]

    for i in range(input_len):
        for key in key_tests[i]:
            if key not in input_tuple[i].keys():
                test = False
                return test
    return test


def test():
    url = test_pool.get_anime_stats_page_link()
    print(scr.scrap_stats_page(url))

    assert check_keys(scr.scrap_stats_page(url))


if __name__ == "__main__":
    test()
