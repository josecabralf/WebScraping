from bs4 import BeautifulSoup
import requests


def getSoup(URL):
    """Genera un objeto BeautifulSoup a partir de una URL

    Args:
        URL (sring): url del sitio web

    Returns:
        BeautifulSoup: objeto BeautifulSoup del sitio web
    """
    res = requests.get(URL)
    return BeautifulSoup(res.content, 'html.parser')


def getUbicGeo(soup):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de LaVoz, si es que hay un mapa

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    try:
        img = soup.find('amp-iframe', id='map-iframe')['src']
        loc = img.split('marker=')[1]
        return [float(n) for n in loc.split('%2C')]
    except:
        return [None, None]


url = 'https://clasificados.lavoz.com.ar/avisos/casas/4742707/reserva-recibo-casa-cerro'
s = getSoup(url)
v = getUbicGeo(s)
print(v)
