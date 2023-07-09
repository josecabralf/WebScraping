from bs4 import BeautifulSoup
import requests
from scraper import scrapLaVoz
from config import *

response = requests.get(URL_LaVoz)
soup = BeautifulSoup(response.content, 'html.parser')

paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)

for i in range(1,paginas+1):
    scrapLaVoz(URL=URL_LaVoz + f'&page={i}', archivo=archivos_LaVoz + f'pagina{i}.json')