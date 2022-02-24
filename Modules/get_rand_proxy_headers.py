import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
import os
from pathlib2 import Path


def proxies_pool(proxy_web_url):
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
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"
    if not Path(datas_dir).exists():
        os.mkdir(datas_dir)

    proxy_dir = cur_path.parent/ "Datas" / "proxy_list.txt"

    if not Path(proxy_dir).exists():
        proxy_webs = ['https://www.sslproxies.org/', 'https://www.us-proxy.org/']
        with open(proxy_dir, "w") as proxy_file:
            proxies = []
            for proxy_web in proxy_webs:
                proxies += proxies_pool(proxy_web)
            proxy_file.write("\n".join(proxy for proxy in proxies))
            print("Successfully import")

    with open(proxy_dir, "r") as proxy_file:
        proxies_list = proxy_file.read().split("\n")

    return random.choice(proxies_list)


def test():
    print(get_rand_proxy())
    print(get_rand_headers())

if __name__ == "__main__":
    test()