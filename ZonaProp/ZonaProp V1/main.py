from bs4 import BeautifulSoup
import requests
from config import *
from scraperZonaProp import scrapZonaProp

response = requests.get(URL_ZonaProp)
soup = BeautifulSoup(response.content, 'html.parser')

paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)

for i in range(1,paginas+1):
    scrapZonaProp(URL=URL_ZonaProp + f'&page={i}', archivo=archivos_ZonaProp + f'pagina{i}.json')