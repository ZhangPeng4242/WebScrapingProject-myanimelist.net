import pandas as pd

from monkeylearn import MonkeyLearn
from src_files.config import config
from src_files.scraping_src_directory.record_exists_check import is_exist
import re
from src_files.scraping_src_directory.scrap_and_update import scrap_and_update_anime


def get_synopsis_sentiment(anime_link_list):
    syn_data_list = []
    for anime_link in anime_link_list:
        # if the anime_id not existed, need to scrap and update the anime first
        anime_id = re.findall("(?<=https://myanimelist.net/anime/)[0-9]*", anime_link)
        anime_id = int(anime_id[0]) if len(anime_id) != 0 else None
        if not is_exist("anime_id", anime_id, "description"):
            scrap_and_update_anime(anime_link)

        if not config.connection.open:
            config.reconnect()
        with config.connection:
            with config.connection.cursor() as cursor:
                cursor.execute("USE db_myanimelist")
                sql = f'SELECT description from description WHERE anime_id = {anime_id}'
                cursor.execute(sql)
                result = cursor.fetchall()
                description = result[0]["description"].strip() if len(result) != 0 else ""
        syn_data_list.append((anime_id, description))

    ml = MonkeyLearn(config.monkeylearn_key)
    model_id = 'cl_pi3C7JiL'
    result = ml.classifiers.classify(model_id, [item[1] for item in syn_data_list]).body

    sentiment_info = [
        {"anime_id": int(syn_data_list[indx][0]), "synopsis_sentiment": res["classifications"][0]["tag_name"],
         "confidence": res["classifications"][0]["confidence"]} for indx, res in enumerate(result)]

    df_sentiment = pd.DataFrame(sentiment_info)
    sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df_sentiment.loc[:, "synopsis_sentiment"] = df_sentiment.apply(lambda x: sentiment_map[x["synopsis_sentiment"]],
                                                                   axis=1)
    config.logger.info(
        f"get_synopsis_sentiment: Success! anime_ids: {', '.join([str(item[0]) for item in syn_data_list])}")

    return df_sentiment
