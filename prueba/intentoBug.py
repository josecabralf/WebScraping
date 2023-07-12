from bs4 import BeautifulSoup
import requests

URL_Meli = 'https://inmuebles.mercadolibre.com.ar/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'


dato = ['Terreno', '52.54m2']
t = int(round(float(dato[1].split('m')[0]), 0))
print(t)
