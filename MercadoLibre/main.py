from bs4 import BeautifulSoup
import requests
from scraperMercadoLibre import scrapMeLi
from config import *

response = requests.get(URL_Meli)
soup = BeautifulSoup(response.content, 'html.parser')

paginas = int(soup.find('li', class_ = 'andes-pagination__page-count').text.split()[-1])

for i in range(1,paginas+1):
    scrapMeLi(URL=URL_Meli + f'&page={i}', archivo=archivos_Meli + f'pagina{i}.json')
