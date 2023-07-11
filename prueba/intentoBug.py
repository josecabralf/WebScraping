from bs4 import BeautifulSoup
import requests

URL_Meli = 'https://inmuebles.mercadolibre.com.ar/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'


paginas = 44

for i in range(0, paginas-2, 3):
    print(i)
    print(i+1)
    print(i+2)

if paginas % 3 == 1:
    print(paginas-1)
if paginas % 3 == 2:
    print(paginas-2)
    print(paginas-1)
