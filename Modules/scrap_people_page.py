"""
we create a function to scrap an acotrs page on myanimelist for info.
"""
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers


def scrap_people_page(people_page_link):
    """
    we receive a link for an actors page on mal.
     we return a dictionary containing the actors id(in the website), name, birthday, numeber of members who chose
     the actor as their favorite, and a list containing all voice acting roles of the actor.
    :param people_page_link: str
    :return: info_dict :dictionary
    """

    # request page using random proxy and header:
    with requests.Session() as res:
        while True:
            try:
                people_page = res.get(people_page_link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                      timeout=100)
                break
            except Exception:
                print("scrap_people_page: Change proxy...")
                time.sleep(0.5)
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

    print(f"scrap_people_page: {people_page_link}  Success!")
    return (people_info_dict, character_info_list, voice_actor_info_list, staff_info_list)


def test():
    """
    we test our function for several links
    :return:
    """
    test_pool = ['https://myanimelist.net/people/112/Hikaru_Midorikawa'
                 'https://myanimelist.net/people/185/Kana_Hanazawa'
                 'https://myanimelist.net/people/513/Yuuichi_Nakamura']

    print('\n'.join(str(item) for item in scrap_people_page(random.choice(test_pool))))


if __name__ == '__main__':
    test()
