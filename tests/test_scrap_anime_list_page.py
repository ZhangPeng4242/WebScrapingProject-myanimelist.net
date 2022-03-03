"""
we test the scrap_anime_list_page library
"""
import scrap_anime_list_page as scr


def test():
    """
    tests get_anime_links by checking the number of links taken from the first three people list pages.
    also print the links of those pages.
    :return:
    """
    anime_list = scr.get_anime_links(3)
    assert len(anime_list) == 150
    print(anime_list)


if __name__ == "__main__":
    test()
