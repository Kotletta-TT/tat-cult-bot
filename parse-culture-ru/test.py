import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.culture.ru/events/1189120/muzeinyi-prazdnik-kraski-sabantuya")

soup = BeautifulSoup(response.content, 'lxml')

sp = soup.find("div", class_="entity-heading_subtitle").text.split(",")[0]

print(sp)