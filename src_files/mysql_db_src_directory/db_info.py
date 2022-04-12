"""This module is to create a dictionary which marks the table names, column names and orders in the database.
This will be handy to check the data integrity when inserting / updating the database.
:export: db_info"""

db_info = {
    "anime": {
        "order": ["id", "title", "english_title", "type", "source", "start_air", "end_air", "season_premier", "theme",
                  "rating",
                  "img_url"]
    },
    "studio_anime": {
        "order": ["studio_id", "anime_id"]
    },
    "anime_genre": {
        "order": ["anime_id", "genre_id"]
    },
    "anime_general_stats": {
        "order": ["anime_id", "score", "rating_count", "ranked", "popularity", "members", "favorites"]
    },
    "anime_watch_stats": {
        "order": ["anime_id", "watching", "completed", "on_hold", "dropped", "plan_to_watch", "total"]
    },
    "anime_score_stats": {
        "order": ["anime_id"] + [str(i) for i in range(10, 0, -1)]
    },
    "people": {
        "order": ["id", "full_name", "birthday", "favorites", "img_url"]
    },
    "character": {
        "order": ["id", "full_name", "favorites", "img_url"]
    },
    "staff": {
        "order": ["people_id", "anime_id", "role"]
    },
    "voice_actor": {
        "order": ["character_id", "people_id"]
    },
    "anime_character": {
        "order": ["anime_id", "character_id", "role"]
    },
    "studio": {
        "order": ["id", "name", "rank", "favorites", "img_url"]
    },
    "api_imdb": {
        "order": ["anime_id", "imdb_id", "imdb_title", "score", "year","imdb_url"]
    },
    "api_description_sentiment_analysis": {
        "order": ["anime_id", "synopsis_sentiment", "confidence"]
    },
    "description": {
        "order": ["anime_id", "description"]
    }
}
