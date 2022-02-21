import requests
from bs4 import BeautifulSoup
page = requests.get(' https://dataquestio.github.io/web-scraping-pages/ids_and_classes.html')
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.find_all('p', class_= 'outer-text'))