"""
scraping_test_directory for the get_rand_proxy_and_headers library
"""
from .pool_for_test import test_pool
import sys
import os
from pathlib2 import Path

src_path = Path(os.getcwd()) / "scraping_src_directory"
sys.path.append(str(src_path))
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers
import requests


def test():
    print(get_rand_proxy())
    print(get_rand_headers())

    with requests.Session() as res:
        link = test_pool.get_anime_page_link()
        page = res.get(test_pool.get_anime_page_link(), proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                       timeout=100)
        print(page)


if __name__ == "__main__":
    test()
