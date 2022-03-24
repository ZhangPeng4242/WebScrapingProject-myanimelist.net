"""
we test the scrap_people_list_page library
"""
import sys
import os
from pathlib2 import Path
src_path = Path(os.getcwd()) / "scraping_src_directory"
sys.path.append(str(src_path))
import scrap_people_list_page as scr


def test():
    """
    scraping_test_directory get_people_links by checking the number of links taken from the first three people list pages.
    also print the links of those pages.
    :return:
    """
    people_list = scr.get_people_links(3)
    assert len(people_list) == 150
    print(people_list)


if __name__ == "__main__":
    test()