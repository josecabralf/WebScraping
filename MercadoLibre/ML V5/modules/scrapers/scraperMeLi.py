from modules.soup.soup import getSoup
from math import ceil
from MeLiConfig import archivos_Meli
from modules.threads.hilos import scrapMultiHilo
from modules.format.archivos import formarArchivo
from modules.format.links import formarLink


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
    soup = getSoup(URL)
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
        archivos = [formarArchivo(n, archivos_Meli, nro)
                    for n in range(i, i+3)]

        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        scrapMultiHilo([formarLink(paginas-1, URL)],
                       [formarArchivo(paginas-1, archivos_Meli, nro)])

    if paginas % 3 == 2:
        links = [formarLink(n, URL) for n in range(paginas-2, paginas)]
        archivos = [formarArchivo(n, archivos_Meli, nro)
                    for n in range(paginas-2, paginas)]

        scrapMultiHilo(links, archivos)
