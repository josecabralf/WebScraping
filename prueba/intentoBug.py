from bs4 import BeautifulSoup
import requests

URL_Meli = 'https://departamento.mercadolibre.com.ar/MLA-1375718613-departamento-en-venta-rodas-lugones-nueva-cordoba-2-dorm-_JM'

# response = requests.get(URL_Meli)
# soup = BeautifulSoup(response.content, 'html.parser')
i = "70.62 m"
j = int(round(float(i.split()[0]), 0))

print(j)
