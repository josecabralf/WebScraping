from bs4 import BeautifulSoup
import requests
from math import ceil
import time
import threading
import datetime
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
    try:
        ar = '-'.join([f'{nro}', nom_base[6], nom_base[7], f'{i+1}.json'])
    except:
        ar = '-'.join([f'{nro}',
                      datetime.date.today().strftime("%d_%m_%Y"), f'{i+1}.json'])
    return ruta + ar


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


def scrapHilo(link, archivo):
    """Ejecuta 1 hilo de scrap

    Args:
        link (string): url de listado
        archivo (string): ubicacion relativa del archivo
    """
    try:
        scrapListadoPublicaciones(link, archivo)
    except:
        time.sleep(10)
        scrapListadoPublicaciones(link, archivo)


def scrapMultiHilo(URLs, archivos):
    """Genera los hilos a ejecutar para realizar el scrap de forma más veloz

    Args:
        URLs ([string]): links de listados a scrapear
        archivos ([string]): ubicaciones relativas de los archivos correspondientes
    """
    threads = [None] * len(URLs)

    for i in range(len(threads)):
        threads[i] = threading.Thread(
            target=scrapHilo, args=(URLs[i], archivos[i]))

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()


def scrapPaginaMeLi(URL, nro, paginas):
    """Permite scrapear de forma veloz multiples paginas de resultados de MercadoLibre mediante el uso de threads

    Args:
        URL (string): url de la pagina listado de publicaciones
        nro (int): id de la url para la creacion del nombre del archivo en que se almacenaran los resultados
        paginas (int): cantidad de paginas de listado de publicaciones a scrapear.
    """
    for i in range(0, paginas-2, 3):
        links = [formarLink(n, URL) for n in range(i, i+3)]
        archivos = [formarArchivo(nro, n, archivos_Meli, URL)
                    for n in range(i, i+3)]

        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        link1 = formarLink(paginas-1, URL)
        archivo1 = formarArchivo(nro, paginas-1, archivos_Meli, URL)
        scrapListadoPublicaciones(link1, archivo1)

    if paginas % 3 == 2:
        links = [formarLink(n, URL) for n in range(paginas-2, paginas)]
        archivos = [formarArchivo(nro, n, archivos_Meli, URL)
                    for n in range(paginas-2, paginas)]

        scrapMultiHilo(links, archivos)


def scrapLinkMeLi(URL, nro):
    """Realiza el scrap de un listado de publicaciones completo de MeLi. Obtiene el conteo de paginas y luego lo scrapea.

    Args:
        URL (string): url de la pagina listado de publicaciones
        nro (int): id de la url para la creacion del nombre del archivo en que se almacenaran los resultados
    """
    paginas = getCantPaginas(URL)
    scrapPaginaMeLi(URL, nro, paginas)
