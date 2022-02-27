import requests

web = requests.get("https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2",
                   proxies={"http": "181.129.43.3:8080"}, timeout=40)
print(web.text)

