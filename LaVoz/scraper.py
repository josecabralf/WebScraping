from bs4 import BeautifulSoup
import requests
from config import URL

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

box_casas_contenido = soup.find_all('div', class_="col col-9 px2") 
# Estas son todas las casas listadas incluida la featured

featured_casa = box_casas_contenido.find()