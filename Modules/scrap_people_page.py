"""
we create a function to scrap an acotrs page on myanimelist for info.
"""
import requests
from bs4 import BeautifulSoup
from get_rand_proxy_headers import get_rand_proxy, get_rand_headers


def scrap_actor(link):
    """
    we receive a link for an actors page on mal.
     we return a dictionary containing the actors id(in the website), name, birthday, numeber of members who chose
     the actor as their favorite, and a list containing all voice acting roles of the actor.
    :param link: str
    :return: info_dict :dictionary
    """
    info_dict = {}
    # request page using random proxy and header:
    with requests.Session() as res:
        while True:
            try:
                page = res.get(link, proxies={"http": get_rand_proxy()}, headers=get_rand_headers(),
                                     timeout=100)
                break
            except Exception:
                print("Anime_page: Change proxy...")
                continue
    soup = BeautifulSoup(page.content, 'html.parser')
    # get cator id:
    id = soup.find('input', attrs={'name': 'vaid'})['value']
    info_dict['actor_id'] = id
    # get name:
    name = soup.find('h1', class_='title-name').text
    info_dict['actors_name'] = name
    # get birthday:
    birthday = soup.find('span', text='Birthday:').parent.text.replace('Birthday: ', '')
    info_dict['actors_birthday'] = birthday
    # get member favorites:
    member_favorites = soup.find('span', text='Member Favorites:').parent.text.replace('Member Favorites: ', '')
    info_dict['member_favorites'] = member_favorites
    # get anime list
    anime_tag_list = soup.find_all('tr', class_='js-people-character')
    anime_info_list = []
    for anime in anime_tag_list:
        anime_name = anime.find('a', class_='js-people-title').text
        anime_role = anime.find_all('td')[2].find('a').text
        anime_importance = anime.find_all('td')[2].find_all('div')[1].text.strip()
        anime_tuple = (anime_name, anime_role, anime_importance)
        anime_info_list.append(anime_tuple)
    info_dict['all_roles'] = anime_info_list
    return info_dict


def test():
    """
    we test our function for several links
    :return:
    """
    link1 = 'https://myanimelist.net/people/112/Hikaru_Midorikawa'
    link2 = 'https://myanimelist.net/people/185/Kana_Hanazawa'
    link3 = 'https://myanimelist.net/people/513/Yuuichi_Nakamura'
    print(scrap_actor(link1))
    print(scrap_actor(link2))
    print(scrap_actor(link3))


if __name__ == '__main__':
    test()