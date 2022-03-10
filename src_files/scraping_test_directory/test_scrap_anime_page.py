"""
scraping_test_directory for the scrap_anime_page library
"""
from .pool_for_test import test_pool
import sys
import os
from pathlib2 import Path

src_path = Path(os.getcwd()).parent / "scraping_src_directory"
sys.path.append(str(src_path))
import scrap_anime_page as scr


def check_keys(input_tuple):
    """
    checks if the output of scrap_anime_page contains all mandatory keys.
    (we cant test for values as they constantly update).
    :param input_tuple: tuple of dicts
    :return: test: boolen
    """
    input_len = len(input_tuple)
    test = True

    key_tests = [
        ('anime_id', 'title', 'type', 'anime_img_url', 'aired', 'premiered', 'studios', 'source', 'genres', 'rating'),
        ('anime_id', 'english_title'),
        ('anime_id', 'score', 'rating_count', 'ranked', 'popularity', 'members', 'favorites')]

    for i in range(input_len):
        for key in key_tests[i]:
            if key not in input_tuple[i].keys():
                test = False
                return test
    return test


def test():
    """
    we test the scrap_anime_page function for several sample links.
    :return: None
    """
    url = test_pool.get_anime_page_link()
    result = scr.scrap_anime_page(url)
    assert check_keys(result)
    print("\n".join(str(stat) for stat in result))


if __name__ == "__main__":
    test()
