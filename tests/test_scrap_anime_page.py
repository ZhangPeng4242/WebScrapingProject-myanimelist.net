"""
tests for the scrap_anime_page library
"""
import scrap_anime_page as scr


def check_keys(input_tuple):
    """
    checks if the output of scrap_anime_page contains all mandatory keys.
    (we cant test for values as they constantly update).
    :param input_tuple: tuple of dicts
    :return: test: boolen
    """
    input_len = len(input_tuple)
    test = True
    key_tests = [('anime_id', 'title', 'type','anime_img_url','aired'  , 'premiered', 'studios', 'source', 'genres', 'rating'),
                 ('anime_id', 'english_title'),
                 ('anime_id', 'score', 'rating_count', 'ranked', 'popularity', 'members', 'favorites')]

    for i in range(input_len):
        for key in key_tests[i]:
            if key not in input_tuple[i].keys():
                test = False
                return test
    return test



def test():
    """
    we test the scrap_anime_page function for several sample links.
    :return: None
    """
    test_pool = [
        "https://myanimelist.net/anime/246/Groove_Adventure_Rave",
        "https://myanimelist.net/anime/47778/Kimetsu_no_Yaiba__Yuukaku-hen",
        'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood'
    ]
    for url in test_pool:
        assert check_keys(scr.scrap_anime_page(url))
        print("\n".join(str(stat) for stat in scr.scrap_anime_page(url)))


if __name__ == "__main__":
    test()
