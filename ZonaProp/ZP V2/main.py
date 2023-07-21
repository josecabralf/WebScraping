from ZPConfig import archivos_ZonaProp, URL_UltimaSemana as url
from soup import getSoup
from scraperListadoZP import scrapListadoPublicaciones
from math import trunc
import time
import threading
import os


def formarLink(i, URL):
    """Forma links de listados de publicaciones según el criterio de ZonaProp

    Args:
        i (int): indica el numero de pagina actual
        URL: url base a editar

    Returns:
        string: url modificada para acceder a pagina i
    """
    if i == 1:
        return URL
    link = URL.split('.')
    link[-2] = link[-2] + f"-pagina-{i}"
    link = '.'.join(link)
    return link


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"pagina{i}.json"


def asignarValNro():
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(archivos_ZonaProp)
    if dir == []:
        return 1
    dir = [int(n.split('.')[0].split('a')[-1])
           for n in dir]
    n = max(dir)
    return n+1


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


def main():
    soup = getSoup(url)
    publicaciones = int(soup.find('h1').text.split()[0].replace('.', ''))
    paginas = int(trunc(publicaciones / 20))
    del soup
    del publicaciones
    nro = asignarValNro()
    for i in range(1, paginas-1, 3):
        links = [formarLink(n, url) for n in range(i, i+3)]
        archivos = [formarArchivo(n, archivos_ZonaProp)
                    for n in range(nro, nro+3)]
        nro += 3
        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        scrapListadoPublicaciones(formarLink(paginas, url),
                                  formarArchivo(paginas, archivos_ZonaProp))

    if paginas % 3 == 2:
        links = [formarLink(n, url) for n in range(paginas-1, paginas+1)]
        archivos = [formarArchivo(n, archivos_ZonaProp)
                    for n in range(nro, nro+2)]

        scrapMultiHilo(links, archivos)


if __name__ == "__main__":
    main()
