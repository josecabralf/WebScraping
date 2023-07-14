from bs4 import BeautifulSoup
import requests
from config import archivos_Links, URL_Meli_CASAS, URL_Meli_DPTOS, URL_Meli_TERS
from unidecode import unidecode


def validarCantResultados(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    cant_publicaciones = int(soup.find(
        'span', class_='ui-search-search-result__quantity-results shops-custom-secondary-font').text.split()[0].replace('.', ''))

    if cant_publicaciones > 2016:
        return formarListaLinks(URL)

    else:
        return [URL]


def formarListaLinks(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    link_zonas = soup.find(
        'a', class_='ui-search-modal__link ui-search-modal--default ui-search-link')["href"]
    response = requests.get(link_zonas)
    soup = BeautifulSoup(response.content, 'html.parser')

    zonas = [a["href"].split('#')[0] for a in soup.find_all(
        'a', class_='ui-search-search-modal-filter ui-search-link')]
    if zonas != []:
        return zonas
    else:
        return formarLinksBarrios(soup)


def formarLinksBarrios(soup):
    nombres = [n.text.lower() for n in soup.find_all(
        'span', class_='andes-checkbox__label andes-checkbox__label-text')]
    URL = 'https://inmuebles.mercadolibre.com.ar/casas/venta/propiedades-individuales/cordoba/cordoba/'
    suffix = '/inmuebles'
    links = []
    for i in range(len(nombres)):
        n = unidecode(nombres[i]).split()
        n = "-".join(n)
        links.append(URL + n + suffix)
    return links


def agregarLinksArchivo(url):
    URLs = url
    archivo = open(archivos_Links, 'a', encoding='utf-8')

    ciudades = validarCantResultados(URLs)
    for i in range(len(ciudades)):
        barrios = validarCantResultados(ciudades[i])
        for barrio in barrios:
            archivo.write(barrio + '\n')
    archivo.close()


def crearArchivoLinksSiNoExiste():
    agregarLinksArchivo(URL_Meli_CASAS)
    agregarLinksArchivo(URL_Meli_DPTOS)
    agregarLinksArchivo(URL_Meli_TERS)
