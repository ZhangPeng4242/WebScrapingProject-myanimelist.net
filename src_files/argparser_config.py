import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='welcome to the myanimelist webscarper! '
                                                 'fisrt choose to either init- for storing the data initially'
                                                 ' or scrap- to update the existing database.'
                                                 ' for additional help use -h after init or scarp.'
                                                 'when first running the program, please choose the init option.')

    # create  subparser to decide if we init- set up the database for the first time or scrap- update the database
    # based on some property.
    subparsers = parser.add_subparsers(help='init or scrap', dest='main')

    init_parser = subparsers.add_parser("init", help='run the program for the first time, set up data either locally '
                                                     'or globally (choose local or remote). after choosing location,'
                                                     ' provide mysql user and password (and optionally host)'
                                        , description='init sets up the database and selects wheather to store it '
                                                      'locally or globaly. after chooseing provide mysql username'
                                                      ' and password (and optionally host).')
    scrap_parser = subparsers.add_parser("scrap", help='scrap the web to update data, can choose to partially update'
                                                       '(choose anime, people, or leave empty to update the whole database). '
                                         , description='scarp allows the user to update the data either fully or '
                                                       'partially based on some category. to completely update the data'
                                                       ' enter the key "all" or simply run without any further keys. '
                                                       'to update by category look at the list of other optional flags.'
                                         )

    init_parser.add_argument('location', help='choose weather to store data locally or remotely'
                             , choices=['local', 'remote'])

    # add arguments to allow the program to take username and password for mysql account of user
    # locally or remotely

    init_parser.add_argument('username', type=str, help='username for sql connection')
    init_parser.add_argument('password', type=str, help='password for sql connection')
    init_parser.add_argument('--host', type=str, help='host for sql connection', default='localhost')
    init_parser.add_argument('--port', type=int, help='port for sql connection', default=3306)

    # create four subparsers to decide what type of info we want to update
    scrap_subparser = scrap_parser.add_subparsers(help='how to scrap (anime, people, all)', dest='type')
    anime_parser = scrap_subparser.add_parser('anime', help='updates based on anime info'
                                              , description='updates based on anime info, '
                                                            'can add more specific criteria for updates,'
                                                            ' see full description below. '
                                                            'if no other criteria specified, updates all anime.')
    people_parser = scrap_subparser.add_parser('people', help='updates based on people info'
                                               , description='updates based on people info '
                                                             'can add more specific criteria for updates,'
                                                             ' see full description below.'
                                                             'if no other criteria specified, updates all people.')

    # add arguments to parser to decide on even more specific data to update
    by_group = anime_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help='scrap all', action="store_true")
    by_group.add_argument("--name", help='scrap by name', type=str)
    by_group.add_argument("--rank", help='scrap by rank', type=int)
    by_group.add_argument("--year", help='scrap by year', type=int)
    by_group.add_argument("--genre", help='scrap by genre', type=str)
    by_group.add_argument("--studio", help='scrap by studio', type=str)

    by_group = people_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help='scrap all',action="store_true")
    by_group.add_argument("--anime", help='scrap by anime', type=str)
    by_group.add_argument("--rank", help='scrap by rank', type=int)
    by_group.add_argument("--name", help='scrap by  name', type=str)
    return parser
