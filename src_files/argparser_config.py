"""This module is to build and configure the argparser instance for the project.
:export: argparse"""
import argparse


def get_parser():
    """
    Configure and build the system arguments parser for the project.
    :return: parser, instance
    """
    parser = argparse.ArgumentParser(description='Welcome to myanimelist webscarper!'
                                                 'If you are running the program for the first time, please initiate the database using init.'
                                                 'You can either, init the program, scrap webpages or export the database.'
                                                 'For additional help use -h after init or scarp.'
                                     )

    # Add subparser: init, scrap, or export
    subparsers = parser.add_subparsers(help='init, scrap,  export or api', dest='main')

    init_parser = subparsers.add_parser("init", help='Usage example: init root 123456'
                                        ,
                                        description='If you are running the program for the first time, you need to first initiate the program.'
                                                    'This will 1. Create the database in your local mysql server. 2.Insert all the initial data the developers have scrapped in advance.'
                                                    "3. Create a config.json file where you can adjust settings for the scrapper. "
                                                    'You need to provide the username and password of the mysql database for this command.')

    scrap_parser = subparsers.add_parser("scrap",
                                         help="Usage Example: scrap anime --rank 50, scrap people --anime 'Fullmetal Alchemist', scrap anime --all, scrap --all "
                                         ,
                                         description='Scrap command will scrap all the relevant pages on myanimelist website, and update the data scrapped in the database.'
                                                     'Scrap anime will scrap the anime main page and stats page. '
                                                     'Eg. scrap anime --year 2018, will scrap main pages and stats pages of all the animes that were released in 2018'
                                                     'Scrap people will scrap the people main page'
                                                     'Eg. scrap people --anime "Fullmetal Alchemist", will scrap main pages of all the people that have participated in the anime Fullmetal Alchemist.'
                                                     "Scrap --all will scrap the entire website of all the animes and people."
                                                     'If you decide to scrap and update all the data, bear in mind that this might take over 36 hours to be done.'
                                         )
    export_parser = subparsers.add_parser("export", help='Usage example: export'
                                          ,
                                          description='This will export all the data for each table in the database into csv format in the current direcotry under data/.')

    # add username, password, [--host], [--port] arguments to the init subparser

    api_parser = subparsers.add_parser('api', help="usage example: api imdb", description="call api's to either get a sentiment analysis of anime synopsis "
                                                          "or use google to get imdb information on the anime ")

    init_parser.add_argument('username', type=str, help='username for mysql connection, mandatory')
    init_parser.add_argument('password', type=str, help='password for mysql connection, mandatory')
    init_parser.add_argument('--host', type=str, help='host for mysql connection', default='localhost')
    init_parser.add_argument('--port', type=int, help='port for mysql connection', default=3306)

    # create four subparsers to decide what type of info we want to update
    scrap_subparser = scrap_parser.add_subparsers(help='scrap target: anime, people, all', dest='type')

    anime_parser = scrap_subparser.add_parser('anime',
                                              help="Usage example: scrap anime, scrap anime --genre 'Adventure', scrap anime --rank 250"
                                              , description="""Scrap anime related pages and update related tables in the database.\n
                                                            Updated tables: anime, anime_general_stats, anime_score_stats, anime_watch_stats, genre, anime_genre, studio_anime, studio\n
                                                            Can specify what anime to scrap: by name, year, rank, genre and studio\n
                                                            Default: scrap and update all the animes""")
    people_parser = scrap_subparser.add_parser('people',
                                               help="Usage example: scrap people, scrap people --anime 'Fullmetal Alchemist', scrap people --rank 250 "
                                               , description="""Scrap people related pages and update related tables in the database.\n
                                                             Updated tables: people, character, staff, voice_actor, anime_character\n
                                                             Can specify what people to scrap: by name, rank, anime_name\n
                                                             Default: scrap and update all the people.""")
    all_parser = scrap_subparser.add_parser("all", help="Usage example: scrap, scrap all "
                                            , description="""
                                               Scrap and update the entire website. (All the people and animes)
                                               This would take more than 36 hours to finish.
                                               """)

    # add arguments to subparser for further specificity
    by_group = anime_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help='scrap all', action="store_true")
    by_group.add_argument("--name", help='scrap by anime name', type=str)
    by_group.add_argument("--rank", help='scrap by rank number', type=int)
    by_group.add_argument("--year", help='scrap by year', type=int)
    by_group.add_argument("--genre", help='scrap by genre name', type=str)
    by_group.add_argument("--studio", help='scrap by studio name', type=str)

    by_group = people_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help='scrap all', action="store_true")
    by_group.add_argument("--anime", help='scrap by anime', type=str)
    by_group.add_argument("--rank", help='scrap by rank', type=int)
    by_group.add_argument("--name", help='scrap by  name', type=str)

    # create two subparsers to decide the type of api to use
    api_subparser = api_parser.add_subparsers(help='choose type: imdb, sentiment_analysis', dest='type')

    imdb_parser = api_subparser.add_parser('imdb', help="Usage example: api imdb --name dragon ball, api imdb year 1997",
                                           description="get imdb information on anime using google api"
                                                       "Updated tables: api_imdb"
                                                       "Can specify what criterion to get information on by: name, year, genre, rank and studio_name"
                                                       "Default: get imdb info of all anime"
                                           )

    # add arguments to subparser for further specificity
    by_group = imdb_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help="get all imdb info", type=str)
    by_group.add_argument("--name", help="get imdb info by name", type=str)
    by_group.add_argument("--year", help="get imdb info by year", type=int)
    by_group.add_argument("--genre", help="get imdb info by genre", type=str)
    by_group.add_argument("--rank", help="get imdb info by rank", type=int)
    by_group.add_argument("--studio", help="get imdb info by studio_name", type=str)

    sentiment_analysis_parser = api_subparser.add_parser('sentiment_analysis',
                                           help="Usage example: api sentiment_analysis --name 'dragon ball', api sentiment_analysis --year 1997",
                                           description="get sentiment analysis of anime synopsis using MonkeyLearn api"
                                                       "Updated tables: api_sentiment_analysis"
                                                       "Can specify what criterion to get sentiment analysis on by: name, year, genre, rank and studio_name"
                                                       "Default: get synopsis sentiment analysis of all anime"
                                           )

    # add arguments to subparser for further specificity
    by_group = sentiment_analysis_parser.add_mutually_exclusive_group()
    by_group.add_argument("--all", help="get synopsis sentiment analysis of all anime", type=str)
    by_group.add_argument("--name", help="get synopsis sentiment analysis of anime by name", type=str)
    by_group.add_argument("--year", help="get synopsis sentiment analysis of anime by year", type=int)
    by_group.add_argument("--genre", help="get synopsis sentiment analysis of anime by genre", type=str)
    by_group.add_argument("--rank", help="get synopsis sentiment analysis of anime by rank", type=int)
    by_group.add_argument("--studio", help="get synopsis sentiment analysis of anime by studio_name", type=str)

    return parser
