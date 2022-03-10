"""
we create a function to scrap an acotr's page on myanimelist for info.
"""
import re
import time
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers
from src_files.config import config


def scrap_people_page(people_page_link):
    """
    This function scraps all the information we need from the main page of a person in the anime industry.
    it returns four dictionaries which will later be inserted into the following Datasets:
    people_info_dict: contains people_id, people_full_name, birthday, member_favorites and people_img_url

    anime_characters_info_list: contains a list of info about characters the actor voices. Each list entry is a dict
    containing: character_id, anime_id, character_fullname, role, character_favorites
    and character_img_url

    voice_actors_info_list: contains a list of info about each voice acting job in the persons career. Each entry in the list  is a dict
    containing: character_id , people_id.

    staff_info_list: contains a list of info about all anime related jobs in the persons career. Each entry in the list is a dict
    containing: anime_id, people_id and staff role

    :param people_page_link: str
    :return: (people_info_dict, character_info_list, voice_actor_info_list, staff_info_list) touple
    """

    # request page using random proxy and header:
    with requests.Session() as res:
        while True:
            try:
                people_page = res.get(people_page_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                      timeout=100)
                break
            except Exception:
                config.logger.warning(f"scrap_people_page: Change proxy... {people_page_link}")
                time.sleep(config.proxy_change_delay)
                continue

    soup = BeautifulSoup(people_page.text, 'html.parser')

    ######Get people_info_dict####

    # get people id:
    people_id = soup.find('input', attrs={'name': 'vaid'})['value']
    # get name:
    people_fullname = soup.find('h1', class_='title-name').text.replace(",", "")
    # get birthday:
    birthday = soup.find('span', text='Birthday:').parent.text.replace('Birthday: ', '')
    # get member favorites:
    member_favorites = soup.find('span', text='Member Favorites:').parent.text.replace('Member Favorites: ',
                                                                                       '').replace(',', "")
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
        anime_id = re.search(anime_url_reg_pattern, anime_url['href']).group()

        character_url = voice_acting_tag.find('a', {"href": re.compile(character_url_reg_pattern)})
        character_id = re.search(character_url_reg_pattern, character_url['href']).group()
        character_fullname = character_url.text.replace(",", "")
        character_role = character_url.parent.find_next_sibling("div").text.strip()
        character_favorites = character_url.parent.find_next_sibling("small").text.strip()
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
        anime_id = re.search(anime_url_reg_pattern, anime_url['href']).group()

        staff_role = staff_info_tag.find('small').text

        staff_info_dict = {"anime_id": anime_id, "people_id": people_id, "staff_role": staff_role}
        staff_info_list.append(staff_info_dict)

    config.logger.info(f"scrap_people_page: Success! {people_page_link}")
    return (people_info_dict, character_info_list, voice_actor_info_list, staff_info_list)
