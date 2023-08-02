from bs4 import BeautifulSoup
import requests
from time import sleep


def getSoup(URL):
    """Genera un objeto BeautifulSoup a partir de una URL

    Args:
        URL (sring): url del sitio web

    Returns:
        BeautifulSoup: objeto BeautifulSoup del sitio web
    """
    res = requests.get(URL)
    return BeautifulSoup(res.content, 'html.parser')


def getImgMapa(tag):
    return tag.name == 'img' and str(tag.get('src')).startswith('https://maps.googleapis.com/maps/')


def getUbicGeo(soup, URL):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de MercadoLibre

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina
        URL (string): url de la pagina de publicacion

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    i = 1
    while True:
        try:
            ubic = soup.find('div', class_='ui-vip-location')
            img = ubic.find('img')['src']
            print(img)
            loc = img.split('&')[4].split('=')[1]
            if loc:
                return [float(n) for n in loc.split('%2C')]
        except:
            print('ERROR ', i)
            if i == 10:
                return [None, None]
            i += 1
            soup = getSoup(URL)


URL = 'https://casa.mercadolibre.com.ar/MLA-1391749532-casa-tipo-duplex-a-estrenar-alta-gracia-financiacion-_JM'
soup = getSoup(URL)

links = getUbicGeo(soup, URL)
print(links)
