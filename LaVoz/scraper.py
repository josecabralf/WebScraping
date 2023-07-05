from bs4 import BeautifulSoup
import requests
from config import URL

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

#listado_casas_venta = soup.find_all('div', class_="col-6 flex flex-wrap content-start sm-col-3 md-col-3 align-top")
#print(listado_casas_venta)

descripciones_casas = soup.find_all('div', class_ = 'card-body md-mh sm-py1 md-py0 px1 px-md-1 flex flex-column flex-auto relative justify-top pb0 border-silver border rounded-bottom')

casa1 = descripciones_casas[0]
nombre = casa1.find('h2').text.strip()
ubicacion = casa1.find('div', class_="h5 mx0 mt0 mb1 col-12 font-light title-1lines").text.strip()
precio = casa1.find('span', class_="price").text.strip()

#datos_interes = casa1.find('span', class_="pr1")
datos_interes = casa1.find('div', class_='gray mt0 mb2 col-12 flex items-center ')

print(datos_interes)