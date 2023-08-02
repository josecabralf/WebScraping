import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def formarLinksBarrios(soup, URL):
    """Forma links para filtrar por barrio.

    Args:
        soup (BeautifulSoup): contenidos de la página de filtro posibles según barrio
        tipo (string): tipo de propiedad que se está filtrando

    Returns:
        [string]: listado de links de páginas filtradas según barrios
    """
    nombres = [n.text.lower() for n in soup.find_all(
        'span', class_='andes-checkbox__label andes-checkbox__label-text')]
    url_base = '/'.join(URL.split('/')[0:-1])
    suffix = URL.split('/')[-1]
    links = []
    for i in range(len(nombres)):
        n = unidecode(nombres[i]).split()
        n = "-".join(n)
        links.append(url_base + n + suffix)
    return links

URL = 'https://inmuebles.mercadolibre.com.ar/casas/cordoba/cordoba/inmueble_NoIndex_True'
filt = 'https://inmuebles.mercadolibre.com.ar/casas/cordoba/cordoba/inmueble_NoIndex_True_FiltersAvailableSidebar?filter=neighborhood'
res = requests.get(filt)
soup = BeautifulSoup(res.content, 'html.parser')

links = formarLinksBarrios(soup, URL)
print(links)