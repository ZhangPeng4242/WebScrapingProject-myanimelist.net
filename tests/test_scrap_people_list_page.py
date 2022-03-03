"""
we test the scrap_people_list_page library
"""
import scrap_people_list_page as scr


def test():
    """
    tests get_people_links by checking the number of links taken from the first three people list pages.
    also print the links of those pages.
    :return:
    """
    people_list = scr.get_people_links(3)
    assert len(people_list) == 150
    print(people_list)


if __name__ == "__main__":
    test()