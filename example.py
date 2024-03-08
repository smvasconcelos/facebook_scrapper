import requests
from bs4 import BeautifulSoup

URL = "https://pt.wikipedia.org/wiki/Raspagem_de_dados"

page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")

with open('result.txt', "w+", encoding="utf-8") as f:

    div = soup.find("main")

    for child in div:
        print(child.text)
