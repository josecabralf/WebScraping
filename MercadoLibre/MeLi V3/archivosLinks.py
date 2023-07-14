from bs4 import BeautifulSoup
import requests
from config import *


def validarCantResultados(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    cant_publicaciones = int(soup.find('span', class_ = 'ui-search-search-result__quantity-results shops-custom-secondary-font').text.split()[0].replace('.',''))
    
    if cant_publicaciones > 2016:
        return formarListaLinks(URL)
    
    else: return [URL]


def formarListaLinks(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    link_zonas = soup.find('a', class_ = 'ui-search-modal__link ui-search-modal--default ui-search-link')["href"]
    response = requests.get(link_zonas)
    soup = BeautifulSoup(response.content, 'html.parser')

    zonas = [a["href"].split('#')[0] for a in soup.find_all('a', class_ = 'ui-search-search-modal-filter ui-search-link')]
    if zonas != []:
        return zonas
    else:
        formarLinksBarrios(soup)


def formarLinksBarrios(soup):
    nombres = [n.text.lower() for n in soup.find_all('span', class_ = 'andes-checkbox__label andes-checkbox__label-text')]
    URL = 'https://inmuebles.mercadolibre.com.ar/casas/venta/propiedades-individuales/cordoba/cordoba/'
    suffix = '/inmuebles'
    links = []
    for nom in nombres:
        nom = nom.replace('ñ','n').replace('ü','u')

def main():
    URLs = [URL_Meli_CASAS]
    ar = archivos_Links_CASAS

    ciudades = validarCantResultados(URLs.pop(0))
    
    for ciudad in range(len(ciudades)):
        barrios = validarCantResultados(ciudades[ciudad])
        for barrio in barrios:
            URLs.append(barrio)

    with open(ar, 'w', encoding='utf-8') as archivoLinks:
        for link in URLs:
            archivoLinks.write(link + '\n')


if __name__ == "__main__":
    main()
