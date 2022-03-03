"""
tests for the get_rand_proxy_and_headers library
"""
import get_rand_proxy_headers as gr
import requests
PAGE_LINK = 'https://myanimelist.net/anime/246/Groove_Adventure_Rave'


def test():
    print(gr.get_rand_proxy())
    print(gr.get_rand_headers())
    with requests.Session() as res:
        page = res.get(PAGE_LINK, proxies={"http": gr.get_rand_proxy()}, headers=gr.get_rand_headers(), timeout=100)
        assert page.url == PAGE_LINK


if __name__ == "__main__":
    test()