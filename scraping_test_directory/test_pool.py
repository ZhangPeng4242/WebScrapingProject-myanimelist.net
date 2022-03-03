import random


class Testpool:
    def __init__(self):
        self._anime_links_pool = [
            "https://myanimelist.net/anime/50051/Abandon__100_Nuki_Shinai_to_Derarenai_Fushigi_na_Kyoushitsu",
            "https://myanimelist.net/anime/51088/Eroriman",
            "https://myanimelist.net/anime/20261/W-Tails_Cat__A_Strange_Presence",
            "https://myanimelist.net/anime/1487/hack__Unison",
            "https://myanimelist.net/anime/49457/Otome_Game_no_Hametsu_Flag_shika_Nai_Akuyaku_Reijou_ni_Tensei_shiteshimatta_OVA",
            "https://myanimelist.net/anime/36587/Granblue_Fantasy_The_Animation_Season_2",
            "https://myanimelist.net/anime/34754/Rilu_Rilu_Fairilu__Yousei_no_Door",
            "https://myanimelist.net/anime/45612/Shu_Ling_Ji_2nd_Season",
            "https://myanimelist.net/anime/25607/Sekai_no_Fushigi_Tanken_Series",
            "https://myanimelist.net/anime/38451/Reizouko_no_Tsukenosuke",
            "https://myanimelist.net/anime/820/Ginga_Eiyuu_Densetsu"]
        self._people_links_pool = [
            "https://myanimelist.net/people/8509/Hiroyuki_Sawano",
            "https://myanimelist.net/people/5251/Asian_Kung-Fu_Generation",
            "https://myanimelist.net/people/44304/Cara_Duncan",
            "https://myanimelist.net/people/4482/Johann_Wolfgang_von_Goethe",
            "https://myanimelist.net/people/6306/Nobutaka_Nishizawa",
            "https://myanimelist.net/people/33353/Kendall_McClellan",
            "https://myanimelist.net/people/33053/Masanori_Katsuragi",
            "https://myanimelist.net/people/11533/Shiro_Yamada",
            "https://myanimelist.net/people/1250/Reiko_Mutou",
            "https://myanimelist.net/people/48105/Taikang_Chenzhang",
            "https://myanimelist.net/people/50962/Kulou_Jingling"
        ]

    def get_anime_page_link(self):
        return random.choice(self._anime_links_pool)

    def get_anime_stats_page_link(self):
        return random.choice(self._anime_links_pool) + '/stats'

    def get_people_page_link(self):
        return random.choice(self._people_links_pool)

test_pool = Testpool()