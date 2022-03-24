"""
Test store_anime_page_data store the date in the correct format.
"""
import sys
import os
from pathlib2 import Path

src_path = Path(os.getcwd()) / "scraping_src_directory"
sys.path.append(str(src_path))
from store_anime_page_data import store_anime_page_data


def test():
    """
    Run this program directly to test store_anime_page_data function
    :return: None
    """
    test_data = [({'anime_id': '25607', 'title': 'Sekai no Fushigi Tanken Series', 'type': 'TV',
                  'anime_img_url': 'https://cdn.myanimelist.net/images/anime/10/65129.jpg', 'aired': '1978',
                  'premiered': '?', 'studios': 'None found, add some', 'source': 'Unknown',
                  'genres': 'Adventure, Fantasy', 'theme': 'Historical', 'rating': 'G - All Ages'},
                 {'anime_id': '25607', 'english_title': None},
                 {'anime_id': '25607', 'score': 'N/A', 'rating_count': None, 'ranked': '13486', 'popularity': '17056',
                  'members': '163', 'favorites': '0'})]

    store_anime_page_data(test_data, _test=True)


if __name__ == "__main__":
    test()
