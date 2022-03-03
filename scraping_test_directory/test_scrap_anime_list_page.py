"""
we test the scrap_anime_list_page library
"""
import sys
import os
from pathlib2 import Path
src_path = Path(os.getcwd()).parent / "scraping_src_directory"
sys.path.append(str(src_path))
from scrap_anime_list_page import get_anime_links


def test():
    """
    scraping_test_directory get_anime_links by checking the number of links taken from the first three people list pages.
    also print the links of those pages.
    :return:
    """
    anime_list = get_anime_links(3)
    assert len(anime_list) == 150

    print(anime_list)


if __name__ == "__main__":
    test()
