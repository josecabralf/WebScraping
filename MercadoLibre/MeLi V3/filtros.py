from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from MeLiConfig import archivos_Links, URL_Meli_CASAS, URL_Meli_DPTOS, URL_Meli_TERS


def validarCantResultados(URL):
    """Chequea si una busqueda filtrada posee más de 2016 resultados de búsqueda. Si es así, realiza un filtrado más profundo.

        Args:
        URL (string): link de la búsqueda filtrada.

        Returns:
        [string]: arreglo de urls filtradas con menos de 2016 resultados de búsqueda cada uno.
    """
    cant_publicaciones = getCantPublicaciones(URL)
    if cant_publicaciones > 2016:
        return formarListaLinks(URL)
    return [URL]


def getCantPublicaciones(URL):
    """Obtiene la cantidad de resultados de busqueda (publicaciones) de una pagina filtrada de MercadoLibre

    Args:
        URL (string): link de pagina de busqueda filtrada

    Returns:
        int: cantidad de resultados de busqueda
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    cant_publicaciones = int(soup.find(
        'span', class_='ui-search-search-result__quantity-results shops-custom-secondary-font').text.split()[0].replace('.', ''))

    return cant_publicaciones


def formarListaLinks(URL):
    """Forma una lista de links filtrados a partir de una URL que contiene los posibles filtros por zona geográfica.

    Args:
        URL (string): url de filtos geográficos posibles

    Returns:
        [string]: listado de links de páginas filtradas según zona geográfica
    """
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
        tipo = URL.split('/')[3]
        return formarLinksBarrios(soup, tipo)


def formarLinksBarrios(soup, tipo):
    """Forma links para filtrar por barrio.

    Args:
        soup (BeautifulSoup): contenidos de la página de filtro posibles según barrio
        tipo (string): tipo de propiedad que se está filtrando

    Returns:
        [string]: listado de links de páginas filtradas según barrios
    """
    nombres = [n.text.lower() for n in soup.find_all(
        'span', class_='andes-checkbox__label andes-checkbox__label-text')]
    URL = f'https://inmuebles.mercadolibre.com.ar/{tipo}/venta/propiedades-individuales/cordoba/cordoba/'
    suffix = '/inmuebles'
    links = []
    for i in range(len(nombres)):
        n = unidecode(nombres[i]).split()
        n = "-".join(n)
        links.append(URL + n + suffix)
    return links


def agregarLinksArchivo(url):
    """Agrega al final de un archivo una serie de links de páginas filtradas obtenidos a partir de una URL inicial

    Args:
        url (string): url inicial
    """
    archivo = open(archivos_Links, 'a', encoding='utf-8')

    ciudades = validarCantResultados(url)
    for i in range(len(ciudades)):
        barrios = validarCantResultados(ciudades[i])
        for barrio in barrios:
            archivo.write(barrio + '\n')
    archivo.close()


def crearArchivoLinksSiNoExiste():
    """Crea un archivo de links filtrados en caso de que no exista
    """
    agregarLinksArchivo(URL_Meli_CASAS)
    print('Casas Listo')
    agregarLinksArchivo(URL_Meli_DPTOS)
    print('Departamentos Listo')
    agregarLinksArchivo(URL_Meli_TERS)
    print('Terrenos Listo')
