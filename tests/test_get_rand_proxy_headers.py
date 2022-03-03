"""
tests for get_rand_proxy_And_headers module
"""
import sys
sys.path.insert(1, 'D:\Pangzhang\Pycharm\Project\webscraping\ITC WebScraping\ITC-WebScraping-Project-Peng-Yam-\Modules\get_rand_proxy_headers.py')
from get_rand_proxy_headers.py import get_rand_proxy(), get_rand_headers()
def test():
    print(get_rand_proxy())
    print(get_rand_headers())


if __name__ == "__main__":
    test()