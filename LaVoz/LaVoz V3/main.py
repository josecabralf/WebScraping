from bs4 import BeautifulSoup
import requests
from scraperListadoClasificados import scrapLaVozClasificados
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
    dir = [int(n.split('.')[0].split('a')[-1]) for n in os.listdir(archivos_LaVoz)]
    n = max(dir)
    return n+1


def main():
    response = requests.get(URL_LaVoz)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)
    fecha = recuperarFechaArchivo()
    nro = asignarValNro()
    for i in range(1, paginas-1, 3):
        URL1, URL2, URL3 = formarLink(URL_LaVoz, i), formarLink(
            URL_LaVoz, i+1), formarLink(URL_LaVoz, i+2)

        archivo1, archivo2, archivo3 = archivos_LaVoz + \
            f'pagina{nro}.json', archivos_LaVoz + \
            f'pagina{nro+1}.json', archivos_LaVoz + f'pagina{nro+2}.json'
        nro += 3
        thread1 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL1, archivo1))
        thread2 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL2, archivo2))
        thread3 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL3, archivo3))

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
        scrapLaVozClasificados(
            URL=formarLink(URL_LaVoz, paginas), archivo=archivos_LaVoz + f'pagina{paginas}.json')

    elif paginas % 3 == 2:
        URL1, URL2 = formarLink(
            URL_LaVoz, paginas-1), formarLink(URL_LaVoz, paginas)

        archivo1, archivo2 = archivos_LaVoz + \
            f'pagina{paginas-1}.json', archivos_LaVoz + f'pagina{paginas}.json'

        thread1 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL1, archivo1))
        thread2 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL2, archivo2))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    fecha = datetime.date.today()
    escribirFechaArchivo(fecha)

if __name__ == "__main__":
    main()
