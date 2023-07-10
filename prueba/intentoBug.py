from bs4 import BeautifulSoup
import requests

URL_Meli = 'https://casa.mercadolibre.com.ar/MLA-1443569504-casa-en-zona-sur-carrara-de-horizonte-_JM'

response = requests.get(URL_Meli)
soup = BeautifulSoup(response.content, 'html.parser')

