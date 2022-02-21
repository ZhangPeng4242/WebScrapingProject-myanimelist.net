import requests
from bs4 import BeautifulSoup

main_link = 'https://myanimelist.net/anime/season/archive'
def get_main_urls():
    # get urls from archive page
    page = requests.get('https://myanimelist.net/anime/season/archive')
    soup = BeautifulSoup(page.content, 'html.parser')
    table_of_links = soup.find('table', class_="anime-seasonal-byseason mt8 mb16")
    list_of_a = table_of_links.find_all('a')
    link_list = [a['href'] for a in list_of_a]
    return link_list

seasonal_example = 'https://myanimelist.net/anime/season/2022/spring'
def get_seasonal_links(link):
    # get urls from seasonal page
    season_page = requests.get(link)
    season_soup = BeautifulSoup(season_page.content, 'html.parser')
    list_of_h2 = season_soup.find_all('h2', class_="h2_anime_title")
    seasonal_link_list = [h2.find('a')['href'] for h2 in list_of_h2]
    return seasonal_link_list


print(len(get_seasonal_links('https://myanimelist.net/anime/season')))
anime_example = 'https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2'
def get_info_from_page(link):
    #get info from anime page:
    anime_page = requests.get(link)
    anime_soup = BeautifulSoup(anime_page.content, 'html.parser')
    stat_list = []
    # appends score
    score_tag = anime_soup.find(class_='score-label')
    stat_list.append(score_tag.get_text())
    # appends rank
    rank_tag = anime_soup.find(class_='numbers ranked')
    rank = rank_tag.find('strong').get_text()
    stat_list.append(rank)
    # appends popularity
    popularity_tag = anime_soup.find(class_='numbers popularity')
    stat_list.append(popularity_tag.get_text())
    # appends members
    members_tag = anime_soup.find(class_='numbers members')
    members = members_tag.find('strong').get_text()
    stat_list.append(members)
    # appends season
    season_tag = anime_soup.find(class_='information season')
    season = season_tag.find('a').get_text()
    stat_list.append(season)
    # appends type (tv/movie/ova)
    type_tag = anime_soup.find(class_='information type')
    type = type_tag.find('a').get_text()
    stat_list.append(type)
    # appends studio
    studio_tag = anime_soup.find(class_='information studio author')
    studio = studio_tag.find('a').get_text()
    stat_list.append(studio)



    return stat_list
print(get_info_from_page(anime_example))
