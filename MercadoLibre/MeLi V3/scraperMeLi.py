from bs4 import BeautifulSoup
import requests
from math import ceil
import time
import threading
from scraperListadoMeLi import scrapListadoPublicaciones
from MeLiConfig import archivos_Meli


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


def formarArchivo(nro, i, ruta, URL):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        nro (int): id de la URL scrapeada
        i (int): indica el numero de pagina actual
        ruta (string): ruta relativa a la carpeta donde se almacenará el archivo
        url (string): url de la pagina a scrapear

    Returns:
        string: nombre y ruta del archivo
    """
    nom_base = URL.split('/')
    ar = '-'.join([f'{nro}', nom_base[6], nom_base[7], f'{i+1}.json'])
    return ruta + ar


def getCantPublicaciones(URL):
    """Obtiene la cantidad de resultados de busqueda (publicaciones) de una URL filtrada de MercadoLibre

    Args:
        URL (string): URL de busqueda filtrada

    Returns:
        int: cantidad de resultados de busqueda
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
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
    return ceil(getCantPublicaciones(URL) / 48)


def scrapPaginaMeLi(URL, nro, paginas):
    """Permite scrapear de forma veloz multiples paginas de resultados de MercadoLibre mediante el uso de threads

    Args:
        URL (string): url de la pagina listado de publicaciones
        nro (int): id de la url para la creacion del nombre del archivo en que se almacenaran los resultados
        paginas (int): cantidad de paginas de listado de publicaciones a scrapear.
    """
    for i in range(0, paginas-2, 3):
        link1, link2, link3 = formarLink(i, URL), formarLink(
            i+1, URL), formarLink(i+2, URL)
        archivo1, archivo2, archivo3 = formarArchivo(
            nro, i, archivos_Meli, URL), formarArchivo(nro, i+1, archivos_Meli, URL), formarArchivo(nro, i+2, archivos_Meli, URL)

        thread1 = threading.Thread(
            target=scrapListadoPublicaciones, args=(link1, archivo1))
        thread2 = threading.Thread(
            target=scrapListadoPublicaciones, args=(link2, archivo2))
        thread3 = threading.Thread(
            target=scrapListadoPublicaciones, args=(link3, archivo3))

        try:
            thread1.start()
        except:
            time.sleep(20)
            thread1.start()

        try:
            thread2.start()
        except:
            time.sleep(20)
            thread2.start()

        try:
            thread3.start()
        except:
            time.sleep(20)
            thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

    if paginas % 3 == 1:
        link1 = formarLink(paginas-1, URL)
        archivo1 = formarArchivo(nro, paginas-1, archivos_Meli, URL)
        scrapListadoPublicaciones(link1, archivo1)

    if paginas % 3 == 2:
        link1, link2 = formarLink(paginas-2, URL), formarLink(paginas-1, URL)
        archivo1, archivo2 = formarArchivo(
            nro, paginas-2, archivos_Meli, URL), formarArchivo(nro, paginas-1, archivos_Meli, URL)

        scrapListadoPublicaciones(link1, archivo1)
        scrapListadoPublicaciones(link2, archivo2)

    return


def scrapLinkMeLi(URL, nro):
    paginas = getCantPaginas(URL)
    scrapPaginaMeLi(URL, nro, paginas)
