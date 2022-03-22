"""
we create functions that return a random proxy and a random header
in order to implements the scraping process without being blocked.
"""

import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
from pathlib2 import Path
from src_files.config import config


def proxies_pool(proxy_web_url):
    """
    receives a url of a proxy table website and returns a list containing all proxies in the table.
    :param proxy_web_url: str
    :return: proxies: list
    """
    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    with requests.Session() as res:
        proxies_page = res.get(proxy_web_url)

    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find('table', class_='table table-striped table-bordered')
    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append(f"{row.find_all('td')[0].text}:{row.find_all('td')[1].text}")
    return proxies


def get_rand_headers():
    """
    returns a random header using the fake_useragent module.
    :return: headers: dict
    """
    accepts = {"firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "safari": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5",
               "chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5",
               "edge": "text/html, application/xhtml+xml, image/jxr, */*"}
    ua = UserAgent()
    user_list = [('safari', ua.safari), ('firefox', ua.firefox), ('chrome', ua.chrome), ('edge', ua.edge)]
    rand_user = random.choice(user_list)
    headers = {"User-Agent": rand_user[1],
               "Accept": accepts[rand_user[0]]}

    return headers


def get_rand_proxy():
    """
    scraps four different proxy tables and stores their ip and port in a text file.
    the function then returns a random proxy out of the proxies it scraped.
    the file is stored in a new directory called datas created inside the parent directory of our current location.
    the file is only created if it didn't exist before running, saving time for multiple uses.
    :return: random.choice(proxies_list): str
    """
    proxy_dir = Path(config.datas_dir) / "proxy_list.txt"

    if not Path(proxy_dir).exists():
        proxy_webs = ['https://www.sslproxies.org/', 'https://www.us-proxy.org/', 'https://free-proxy-list.net/',
                      'https://free-proxy-list.net/uk-proxy.html']
        with open(proxy_dir, "w", encoding="utf-8") as proxy_file:
            proxies = []
            for proxy_web in proxy_webs:
                proxies += proxies_pool(proxy_web)
            proxy_file.write("\n".join(proxy for proxy in proxies))
            config.logger.info("Successfully get all the proxies!!")

    with open(proxy_dir, "r") as proxy_file:
        proxies_list = proxy_file.read().split("\n")

    random.shuffle(proxies_list)
    return random.choice(proxies_list)
