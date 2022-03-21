class Queries():
    def __init__(self):
        self.sql_anime = f"INSERT INTO anime_info (id, title, english_title, type, source, start_air, end_air, season_premier, theme, img_ur) VALUES ({'%s, ' * 9 + '%s'})"
        self.sql_anime_general_stats = f"INSERT INTO anime_general_stats (anime_info_id, rating_count, ranked, popularity, members, favorites) VALUES ({'%s, ' * 6 + '%s'})"
        self.sql_anime_watch_stats = f"NSERT INTO anime_watch_stats (anime_info_id, watching, completed, on-hold, dropped, plan_to_watch, total) VALUES ({'%s, ' * 6 + '%s'})"
        self.sql_anime_score_stats = f"INSERT INTO anime_score_stats (anime_info_id, {', '.join([str(i) for i in range(10, 0, -1)])}) VALUES({'%s, ' * 10 + '%s'})"
        self.sql_character_info = f"INSERT INTO character_info (id, full_name, role, favorites, img_url) VALUES({'%s, ' * 4 + '%s'})"
        self.sql_people_info = f"INSERT INTO people_info (id, full_name, birthday, member_favorites, img_url) VALUES({'%s, ' * 4 + '%s'})"
        self.sql_genres = f"INSERT INTO genres (id, name) VALUES({'%s, ' * 1 + '%s'})"
        self.sql_anime_genres = f"INSERT INTO anime_genres (id,genres_id, anime_info_id) VALUES({'%s, ' * 2 + '%s'})"
        self.sql_anime_staff = f"INSERT INTO character_info (id,staff_role, anime_info_id, people_info_id) VALUES({'%s, ' * 3 + '%s'})"
        self.sql_character_voice_actor = f"INSERT INTO character_voice_actor (id,people_info_id, character_info_id) VALUES({'%s, ' * 2 + '%s'})"
        self.sql_character_anime = f"INSERT INTO character_info (id,staff_role, character_info_id, anime_info_id) VALUES({'%s, ' * 2 + '%s'})"


insert_queries = {
    "anime": f"INSERT INTO anime (id, title, english_title, type, source, start_air, end_air, season_premier, theme, img_url) VALUES ({'%s, ' * 9 + '%s'})",
    "anime_general_stats": f"INSERT INTO anime_general_stats (anime_id, score, rating_count, ranked, popularity, members, favorites) VALUES ({'%s, ' * 6 + '%s'})",
    "anime_watch_stats": f"NSERT INTO anime_watch_stats (anime_id, watching, completed, on_hold, dropped, plan_to_watch, total) VALUES ({'%s, ' * 6 + '%s'})",
    "anime_score_stats": f"INSERT INTO anime_score_stats (anime_id, {', '.join([str(i) for i in range(10, 0, -1)])}) VALUES({'%s, ' * 10 + '%s'})",
    "people": f"INSERT INTO people (id, full_name, birthday, favorites, img_url) VALUES({'%s, ' * 4 + '%s'})",
    "character": f"INSERT INTO character (id, full_name, favorites, img_url) VALUES({'%s, ' * 3 + '%s'})",
    "genre": f"INSERT INTO genre (id, name) VALUES({'%s, ' * 1 + '%s'})",
    "studio": f"INSERT INTO studio (id, name, rank, favorites, img_url) VALUES({'%s, ' * 4 + '%s'})",
    "studio_anime": f"INSERT INTO studio_anime (match_id, studio_id, anime_id) VALUES({'%s, ' * 2 + '%s'})",
    "anime_genre": f"INSERT INTO anime_genre (match_id, anime_id, genre_id) VALUES({'%s, ' * 2 + '%s'})",
    "staff": f"INSERT INTO staff (match_id, people_id, anime_id, role) VALUES({'%s, ' * 3 + '%s'})",
    "voice_actor": f"INSERT INTO voice_actor (match_id, character_id, people_id) VALUES({'%s, ' * 2 + '%s'})",
    "anime_character": f"INSERT INTO anime_character (match_id, anime_id, character_id, role) VALUES({'%s, ' * 3 + '%s'})",
}
