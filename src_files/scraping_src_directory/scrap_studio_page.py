import re
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_headers, get_rand_proxy
import time
from src_files.config import config
import reformat


def scrap_studio_page(studio_link):
    with requests.Session() as res:
        while True:
            try:
                studio_page = res.get(studio_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                      timeout=100)
                break
            except Exception:
                config.logger.warning(f"scrap_anime_page: Change proxy... {studio_link}")
                time.sleep(config.proxy_change_delay)
                continue

    soup = BeautifulSoup(studio_page.text, 'html.parser')
    studio_info = {}
    studio_info["studio_id"] = int(re.findall("(?<=https://myanimelist.net/anime/producer/)[0-9]*", studio_link)[0])
    studio_info["studio_name"] = soup.find('h1', class_='h1').text
    studio_info["rank"] = None
    studio_info["studio_favorites"] = int(soup.find('span', string="Member Favorites:").parent.text.split(": ")[1].strip().replace(",",""))
    studio_info["studio_img_url"] = soup.find('img',{"data-src": re.compile("https://cdn.myanimelist.net/img")})['data-src']

    formatted_studio_data = reformat.format_studio_data([studio_info])
    return formatted_studio_data

