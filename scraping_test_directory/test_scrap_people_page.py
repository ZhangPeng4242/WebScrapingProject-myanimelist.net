"""
scraping_test_directory for the scrap_people_page library
"""
from test_pool import test_pool
import sys
import os
from pathlib2 import Path
src_path = Path(os.getcwd()).parent / "scraping_src_directory"
sys.path.append(str(src_path))

import scrap_people_page as scr


def check_keys(input_tuple):
    """
    checks if the output of scrap_people_page contains all mandatory keys.
    (we cant test for values as they constantly update).
    :param input_tuple: tuple of dicts and lists
    :return: test: boolen
    """
    input_len = len(input_tuple)
    test = True
    key_tests = [('people_id', 'people_fullname', 'birthday', 'member_favorites', 'people_img_url'),
                 ('character_id', 'anime_id', 'character_fullname', 'role', 'character_favorites', 'character_img_url'),
                 ('character_id', 'people_id'),
                 ('anime_id', 'people_id', 'staff_role')]
    for key in key_tests[0]:
        if key not in input_tuple[0].keys():
            test = False
            return test
    for i in range(1, input_len):
        for element in input_tuple[i]:
            for key in key_tests[i]:
                if key not in element.keys():
                    test = False
                    return test
    return test


def test():
    """
    we test our function for several links
    :return:
    """
    url = test_pool.get_people_page_link()

    print('\n'.join(str(item) for item in scr.scrap_people_page(url)))
    assert check_keys(scr.scrap_people_page(url))


if __name__ == '__main__':
    test()
