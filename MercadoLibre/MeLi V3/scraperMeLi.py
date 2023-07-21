from bs4 import BeautifulSoup
import requests
from math import ceil
from MeLiConfig import archivos_Meli
from hilos import *
from archivos import formarArchivo


def formarLink(i, URL):
    """Forma links de listados de publicaciones según el criterio de Mercado Libre

    Args:
        i (int): indica el numero de pagina actual
        URL: url base a editar

    Returns:
        string: url modificada para acceder a pagina i
    """
    if i == 0:
        return URL
    link = URL.split('_')
    link.insert(1, f"Desde_{i*48+1}")
    link = '_'.join(link)
    return link


def getCantPublicaciones(soup):
    """Obtiene la cantidad de resultados de busqueda (publicaciones) de una pagina filtrada de MercadoLibre

    Args:
        soup (BeautifulSoup): pagina de busqueda filtrada

    Returns:
        int: cantidad de resultados de busqueda
    """
    cant_publicaciones = int(soup.find(
        'span', class_='ui-search-search-result__quantity-results shops-custom-secondary-font').text.split()[0].replace('.', ''))

    return cant_publicaciones


def getCantPaginas(URL):
    """Obtiene la cantidad de paginas resultantes de una busqueda filtrada de MercadoLibre

    Args:
        URL (string): url de la busqueda filtrada

    Returns:
        int: cantidad de paginas
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        paginas = int(
            soup.find('li', class_='andes-pagination__page-count').text.split()[-1])
    except:
        paginas = ceil(getCantPublicaciones(soup) / 48)
    return paginas


def scrapPaginaMeLi(URL, nro):
    """Permite scrapear de forma veloz multiples paginas de resultados de MercadoLibre mediante el uso de threads

    Args:
        URL (string): url de la pagina listado de publicaciones
        nro (int): id de la url para la creacion del nombre del archivo en que se almacenaran los resultados
    """
    paginas = getCantPaginas(URL)

    for i in range(0, paginas-2, 3):
        links = [formarLink(n, URL) for n in range(i, i+3)]
        archivos = [formarArchivo(nro, n, archivos_Meli, URL)
                    for n in range(i, i+3)]

        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        link1 = formarLink(paginas-1, URL)
        archivo1 = formarArchivo(nro, paginas-1, archivos_Meli, URL)
        scrapHilo(link1, archivo1)

    if paginas % 3 == 2:
        links = [formarLink(n, URL) for n in range(paginas-2, paginas)]
        archivos = [formarArchivo(nro, n, archivos_Meli, URL)
                    for n in range(paginas-2, paginas)]

        scrapMultiHilo(links, archivos)
