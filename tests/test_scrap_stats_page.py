"""
tests for the scrap_stats_page library
"""
import scrap_stats_page as scr


def check_keys(input_tuple):
    """
    checks if the output of scrap_stats_page contains all mandatory keys.
    (we cant test for values as they constantly update).
    :param input_tuple: tuple of dicts
    :return: test: boolen
    """
    input_len = len(input_tuple)
    test = True
    sec_keys = [str(i) for i in range(10, 0, -1)]
    sec_keys.append('anime_id')
    key_tests = [('watching', 'completed', 'on-hold', 'dropped', 'plan to watch', 'total', 'anime_id'),
                 sec_keys]

    for i in range(input_len):
        for key in key_tests[i]:
            if key not in input_tuple[i].keys():
                test = False
                return test
    return test


def test():
    test_pool = [
        "https://myanimelist.net/anime/19815/No_Game_No_Life/stats",
        'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood/stats',
        'https://myanimelist.net/anime/9253/Steins_Gate/stats']
    for url in test_pool:
        print(scr.scrap_stats_page(url))
        assert check_keys(scr.scrap_stats_page(url))


if __name__ == "__main__":
    test()
