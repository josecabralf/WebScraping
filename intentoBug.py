from bs4 import BeautifulSoup
import requests


def getSoup(URL):
    res = requests.get(URL)
    return BeautifulSoup(res.content, 'html.parser')


def getImgUbic(tag):
    return tag.name == 'img' and str(tag.get('src')).startswith('https://maps.googleapis.com/maps/')


def getUbicGeo(soup, URL):
    i = 1
    while True:
        try:
            img = soup.find(getImgUbic)['src']
            loc = img.split('&')[4].split('=')[1]
            if loc:
                return [float(n) for n in loc.split('%2C')]
        except:
            i += 1
            if i == 10:
                return [None, None]
            getSoup(URL)


url = 'https://casa.mercadolibre.com.ar/MLA-1138937605-casa-sierras-de-cordoba-valle-de-punilla-_JM'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

ubic = getUbicGeo(soup, url)
print(ubic)
