import os
from pathlib2 import Path
import csv


# people
# staff: id, name, member favorites, staff? voice actor?

# character id, people_id, role,(role favorites)2                                       3333333333333333333

# voice_actor: id, name, role, member favorites


# databases:
# people info: people_id , name  , birthday, member_favorites, img_url
# staff info:  anime_id, people_id, role
# voice actor info: character_id, people_id,
# character info: character_id 1, name, anime_id, role,character_favorites, img_url

def store_people_page_data(people_stats_list):
    cur_path = Path(os.getcwd())
    datas_dir = cur_path.parent / "Datas"

    with open(Path(datas_dir) / 'people_info.csv', "w", encoding="utf-8") as people_info_csv_file:
        field_names = ['people_id', 'people_fullname', 'birthday', 'member_favorites', 'people_img_url']
        writer = csv.DictWriter(people_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat in people_stats_list:
            writer.writerow(stat[0])

    with open(Path(datas_dir) / 'anime_characters_info.csv', "w", encoding="utf-8") as characters_info_csv_file:
        field_names = ['character_id', 'anime_id', 'character_fullname', 'role', 'character_favorites',
                       'character_img_url']
        writer = csv.DictWriter(characters_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[1]:
                writer.writerow(stat)

    with open(Path(datas_dir) / 'voice_actors_info.csv', "w", encoding="utf-8") as voice_actors_info_csv_file:
        field_names = ['character_id', 'people_id']
        writer = csv.DictWriter(voice_actors_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[2]:
                writer.writerow(stat)

    with open(Path(datas_dir) / 'staff_info.csv', "w", encoding="utf-8") as staff_info_csv_file:
        field_names = ['anime_id', 'people_id', 'staff_role']
        writer = csv.DictWriter(staff_info_csv_file, fieldnames=field_names)
        writer.writeheader()

        for stat_list in people_stats_list:
            for stat in stat_list[3]:
                writer.writerow(stat)

    print("People page data successfully stored!")


def test():
    store_people_page_data(
        [({'people_id': '112', 'people_fullname': 'Midorikawa Hikaru', 'birthday': 'May  2, 1968',
           'member_favorites': '3781', 'people_img_url': 'https://cdn.myanimelist.net/images/voiceactors/2/56626.jpg'},
          [{'character_id': '205064', 'anime_id': '49385', 'character_fullname': 'Fenrir', 'role': 'Supporting',
            'character_favorites': '0',
            'character_img_url': 'https://cdn.myanimelist.net/r/84x124/images/characters/13/462308.jpg?s=9f1279b261cdd7aa01d98829741458a9'},
           {'character_id': '136284', 'anime_id': '42892', 'character_fullname': 'Henry VI', 'role': 'Main',
            'character_favorites': '38',
            'character_img_url': 'https://cdn.myanimelist.net/r/84x124/images/characters/2/296117.jpg?s=f206b96e4401259b1da9f494a8f6b35a'},
           {'character_id': '4631', 'anime_id': '48775', 'character_fullname': 'Natsume Kyousuke', 'role': 'Main',
            'character_favorites': '987',
            'character_img_url': 'https://cdn.myanimelist.net/r/84x124/images/characters/9/241453.jpg?s=55ca2b1dc5736032e13f84209c9d419f'},
           {'character_id': '178349', 'anime_id': '44961', 'character_fullname': 'Balta', 'role': 'Supporting',
            'character_favorites': '10',
            'character_img_url': 'https://cdn.myanimelist.net/r/84x124/images/characters/3/400680.jpg?s=a30f06d9d02ef1a93fca97395d5e14a3'},
           {'character_id': '202838', 'anime_id': '38192', 'character_fullname': 'Rufus', 'role': 'Supporting',
            'character_favorites': '1',
            'character_img_url': 'https://cdn.myanimelist.net/r/84x124/images/characters/6/456962.jpg?s=a6b40203af7d451cb884d6994b072f4e'}],
          [{'character_id': '205064', 'people_id': '112'}, {'character_id': '136284', 'people_id': '112'},
           {'character_id': '4631', 'people_id': '112'}],
          [{'anime_id': '25839', 'people_id': '112', 'staff_role': 'Theme Song Performance'},
           {'anime_id': '17513', 'people_id': '112', 'staff_role': 'Theme Song Performance'},
           {'anime_id': '20919', 'people_id': '112', 'staff_role': 'Theme Song Performance'}]
          )
         ])

if __name__ == "__main__":
    test()
