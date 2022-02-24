import requests

page = requests.get("https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2",
                    proxies={'http': '177.47.181.142:8080', 'https': "177.47.181.142:8080"}, timeout=40)
print(page.text)
