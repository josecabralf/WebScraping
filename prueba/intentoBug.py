from bs4 import BeautifulSoup
import requests

URL_Meli = 'https://inmuebles.mercadolibre.com.ar/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'

"""
response = requests.get(URL_Meli)
soup = BeautifulSoup(response.content, 'html.parser')
"""
paginas = 42

for i in range(paginas):
    if i == 0:
        link = URL_Meli
    else:
        link = URL_Meli.split('_')
        link.insert(1, f"Desde_{i*48+1}")
        link = '_'.join(link)
    print(link + "\n")
    # link = '_'.join(link)
"""for i in range(paginas):
  if i == 0:
    link = URL_Meli
  else:"""
