import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
import itertools


def proxies_pool():
    url = 'https://www.sslproxies.org/'
    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    with requests.Session() as res:
        proxies_page = res.get(url)

    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find('table', class_='table table-striped table-bordered')
    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append(f"{row.find_all('td')[0].text}:{row.find_all('td')[1].text}")
    return proxies


def rand_header():
    accepts = {"firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "safari":  "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5",
               "chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5",
               "edge": "text/html, application/xhtml+xml, image/jxr, */*"}
    ua = UserAgent()
    user_list = [('safari', ua.safari), ('firefox', ua.firefox), ('chrome', ua.chrome), ('edge', ua.edge)]
    rand_user = random.choice(user_list)
    headers = {"User-Agent": rand_user[1],
          "Accept": accepts[rand_user[0]]}
    return headers

proxies = proxies_pool()
link_list = ['https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2',
             'https://myanimelist.net/anime/44516/Koroshi_Ai',
             'https://myanimelist.net/anime/48556/Takt_Op_Destiny']
# for link in link_list:
#     proxy = random.choice(proxies)
#     header = rand_header()
#     page = requests.get(link, proxies={'http': proxy, 'https': proxy}, headers=header, timeout=30)
link = 'https://www.itc.tech/web-scraping-with-python-a-to-z/'
proxy = random.choice(proxies)
header = rand_header()
print(proxy)
print(header)
# page = requests.get(link, proxies={'http': proxy, 'https': proxy}, headers=header, timeout=30)
# print(page.content)
page = requests.get(link, proxies={'http': proxy, 'https': proxy})
print(page.content)