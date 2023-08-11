from ZPConfig import archivos_ZonaProp
from modules.soup.soup import getSoup
from modules.threads.hilos import scrapMultiHilo
from modules.format.archivos import formarArchivo
from modules.format.links import formarLink
from modules.exceptions.revisiones import revisionArchivos
from math import ceil


def getCantPublicaciones(soup):
    """Obtiene la cantidad de resultados de busqueda (publicaciones) de una pagina filtrada de MercadoLibre

    Args:
        soup (BeautifulSoup): pagina de busqueda filtrada

    Returns:
        int: cantidad de resultados de busqueda
    """
    cant_publicaciones = int(soup.find(
        'h1', class_='sc-1oqs0ed-0 dbbZNk').text.split()[0].replace('.', ''))

    return cant_publicaciones


def getCantPaginas(URL):
    """Obtiene la cantidad de paginas resultantes de una busqueda filtrada de MercadoLibre

    Args:
        URL (string): url de la busqueda filtrada

    Returns:
        int: cantidad de paginas
    """
    soup = getSoup(URL)
    paginas = ceil(getCantPublicaciones(soup) / 20)
    return paginas


def scrapPaginaZonaProp(URL, nro):
    paginas = getCantPaginas(URL)
    print(f'Cantidad de paginas: {paginas}')
    for i in range(1, paginas-1, 3):
        print(f'Progreso: {i+2}/{paginas}')
        links = [formarLink(n, URL) for n in range(i, i+3)]
        archivos = [formarArchivo(n, archivos_ZonaProp, nro)
                    for n in range(i, i+3)]
        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        scrapMultiHilo([formarLink(paginas, URL)],
                       [formarArchivo(paginas, archivos_ZonaProp, nro)])

    if paginas % 3 == 2:
        links = [formarLink(n, URL) for n in range(paginas-1, paginas+1)]
        archivos = [formarArchivo(n, archivos_ZonaProp, nro)
                    for n in range(nro, nro+2)]

        scrapMultiHilo(links, archivos)

    revisionArchivos()
