# import requests
#
# web = requests.get("https://myanimelist.net/anime/48583/Shingeki_no_Kyojin__The_Final_Season_Part_2",
#                    proxies={"http": ""}, timeout=40)
# print(web.text)
#

a = [1,2,3,4]
a=iter(a)
b = next(a)
while b:
    print(b)
    b = next(a,None)