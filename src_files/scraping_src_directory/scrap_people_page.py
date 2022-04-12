"""
This module is to scrap data from the people main page on myanimelist.net
:export: scrap_people_page
"""
import re
import time
import requests
from bs4 import BeautifulSoup
from src_files.scraping_src_directory.get_rand_proxy_headers import get_rand_proxy, get_rand_headers
from src_files.config import config
import src_files.scraping_src_directory.reformat as reformat
from src_files.scraping_src_directory.record_exists_check import is_exist
from src_files.scraping_src_directory.scrap_anime_page import scrap_anime_page


def scrap_people_page(people_page_link):
    """
    This function is to scrap all the information we need on the main info page of the people with the given link.
    Also it formats the data according to the database table requirements.
    Relavant tables: people, character, staff, voice_actor, anime_character
    :param people_page_link: the link for the main people info page
    :return: DataFrame: formatted_people_data, formatted_character_data, formatted_staff_data, formatted_voice_actor_data,
            formatted_anime_character_data
    """
    # request page using random proxy and header:
    with requests.Session() as res:
        while True:
            try:
                people_page = res.get(people_page_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                      timeout=config.timeout)
                break
            except Exception:
                config.logger.warning(f"scrap_people_page: Change proxy... {people_page_link}")
                time.sleep(config.proxy_change_delay)
                continue

    soup = BeautifulSoup(people_page.text, 'html.parser')

    ######Get people_info_dict####

    # get people id:
    people_id = int(soup.find('input', attrs={'name': 'vaid'})['value'])
    # get name:
    people_fullname = soup.find('h1', class_='title-name').text.replace(",", "")
    # get birthday:
    birthday = soup.find('span', text='Birthday:').parent.text.replace('Birthday: ', '')
    # get member favorites:
    member_favorites = int(soup.find('span', text='Member Favorites:').parent.text.replace('Member Favorites: ',
                                                                                           '').replace(',', ""))
    # get people img url
    people_img_url = soup.find('img', {'data-src': re.compile("https://cdn.myanimelist.net/images")})

    people_info_dict = {'people_id': people_id, 'people_fullname': people_fullname, 'birthday': birthday,
                        'member_favorites': member_favorites,
                        'people_img_url': people_img_url['data-src'] if people_img_url else None}

    ####Get voice_actor_info & character_info####
    anime_url_reg_pattern = "(?<=https://myanimelist.net/anime/)[0-9]*"
    character_url_reg_pattern = "(?<=https://myanimelist.net/character/)[0-9]*"

    voice_actor_info_list = []
    character_info_list = []
    voice_acting_tags_list = soup.find_all('tr', class_='js-people-character')
    for voice_acting_tag in voice_acting_tags_list:
        anime_url = voice_acting_tag.find('a', {"href": re.compile(anime_url_reg_pattern)})
        anime_id = int(re.search(anime_url_reg_pattern, anime_url['href']).group())

        character_url = voice_acting_tag.find('a', {"href": re.compile(character_url_reg_pattern)})
        character_id = int(re.search(character_url_reg_pattern, character_url['href']).group())
        character_fullname = character_url.text.replace(",", "")
        character_role = character_url.parent.find_next_sibling("div").text.strip()
        character_favorites = int(character_url.parent.find_next_sibling("small").text.strip())
        character_img_url = character_url.parent.find_next("img")

        voice_actor_info_dict = {"character_id": character_id, "people_id": people_id}
        character_info_dict = {"character_id": character_id, "anime_id": anime_id,
                               "character_fullname": character_fullname, "role": character_role,
                               "character_favorites": character_favorites,
                               "character_img_url": character_img_url['data-src'] if character_url else None}
        voice_actor_info_list.append(voice_actor_info_dict)
        character_info_list.append(character_info_dict)

    ####Get staff_info####
    staff_info_list = []
    staff_info_tags_list = soup.find_all('tr', class_="js-people-staff")
    for staff_info_tag in staff_info_tags_list:
        anime_url = staff_info_tag.find('a', {"href": re.compile(anime_url_reg_pattern)})
        anime_id = int(re.search(anime_url_reg_pattern, anime_url['href']).group())

        staff_role = staff_info_tag.find('small').text

        staff_info_dict = {"anime_id": anime_id, "people_id": people_id, "staff_role": staff_role}
        staff_info_list.append(staff_info_dict)

    for staff in staff_info_list:
        if not is_exist("id", staff["anime_id"], "anime"):
            scrap_anime_page(f"https://myanimelist.net/anime/{staff['anime_id']}")
    for character in character_info_list:
        if not is_exist("id", character["anime_id"], "anime"):
            scrap_anime_page(f"https://myanimelist.net/anime/{character['anime_id']}")

    formatted_people_data = reformat.format_people_data(people_info_dict)
    formatted_character_data = reformat.format_character_data(character_info_list)
    formatted_staff_data = reformat.format_staff_data(staff_info_list)
    formatted_voice_actor_data = reformat.format_voice_actor_data(voice_actor_info_list)
    formatted_anime_character_data = reformat.format_anime_character_data(character_info_list)

    config.logger.info(f"scrap_people_page: Success! {people_page_link}")

    return (formatted_people_data, formatted_character_data, formatted_staff_data, formatted_voice_actor_data,
            formatted_anime_character_data)
