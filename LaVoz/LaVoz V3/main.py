from bs4 import BeautifulSoup
import requests
from scraperListadoClasificados import scrapListadoPublicaciones
from LVConfig import *
import threading
import time
import datetime
import os


def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Clasificados de La Voz

    Args:
        url_base (string): url base de Clasificados de La Voz que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    return url_base + f'&page={i}'


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"pagina{i}.json"


def escribirFechaArchivo(fecha):
    f = open(archivo_fecha, 'w')
    f.write(str(fecha.strftime("%d-%m-%Y")))
    f.close()


def recuperarFechaArchivo():
    f = open(archivo_fecha, 'r')
    fecha = f.readline()
    f.close()
    return datetime.datetime.strptime(fecha, "%d-%m-%Y")


def asignarValNro():
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(archivos_LaVoz)
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
    response = requests.get(URL_LaVoz)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)
    fecha = recuperarFechaArchivo()
    nro = asignarValNro()
    for i in range(1, paginas-1, 3):
        URLs = [formarLink(URL_LaVoz, n) for n in range(i, i+3)]
        archivos = [formarArchivo(n, archivos_LaVoz)
                    for n in range(nro, nro+3)]
        nro += 3
        scrapMultiHilo(URLs, archivos)

    if paginas % 3 == 1:
        scrapListadoPublicaciones(
            URL=formarLink(URL_LaVoz, paginas), archivo=archivos_LaVoz + f'pagina{paginas}.json')

    elif paginas % 3 == 2:
        URLs = [formarLink(URL_LaVoz, i) for i in range(paginas-1, paginas+1)]
        archivos = [formarArchivo(n, archivos_LaVoz)
                    for n in range(nro, nro+2)]

        scrapMultiHilo(URLs, archivos)

    fecha = datetime.date.today()
    escribirFechaArchivo(fecha)


if __name__ == "__main__":
    main()
