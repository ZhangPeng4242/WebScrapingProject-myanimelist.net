import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
import os
import csv
URL_LIST = ['https://www.sslproxies.org/', 'https://www.us-proxy.org/']


def proxies_pool(url):
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


def rand_proxy():
    try:
        with open('url_list.csv', 'r') as url_list:
            csv_reader = csv.reader(url_list, delimiter=',')
            proxy_short_list = [random.choice(row) for row in csv_reader if row != []]
            return random.choice(proxy_short_list)
    except FileNotFoundError:
        with open('url_list.csv', 'w') as url_list:
            new_writer = csv.writer(url_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for url in URL_LIST:
                new_writer.writerow(proxies_pool(url))
        proxy_short_list = [random.choice(proxies_pool(url)) for url in URL_LIST]
        return random.choice(proxy_short_list)





