from config import URL_ZonaProp, archivos_ZonaProp
from soup import getSoup
from scraperZonaProp import scrapZonaProp
from math import trunc
import time
import threading


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


def main():
    soup = getSoup(URL_ZonaProp)
    publicaciones = int(soup.find('h1').text.split()[0].replace('.', ''))
    paginas = int(trunc(publicaciones / 20))
    del soup
    del publicaciones
    
    for i in range(1, paginas-1, 3):
        link1, link2, link3 = formarLink(i, URL_ZonaProp), formarLink(i+1, URL_ZonaProp), formarLink(i+2, URL_ZonaProp)
        archivo1, archivo2, archivo3 = formarArchivo(
            i, archivos_ZonaProp), formarArchivo(i+1, archivos_ZonaProp), formarArchivo(i+2, archivos_ZonaProp)

        thread1 = threading.Thread(target=scrapZonaProp, args=(link1, archivo1))
        thread2 = threading.Thread(target=scrapZonaProp, args=(link2, archivo2))
        thread3 = threading.Thread(target=scrapZonaProp, args=(link3, archivo3))

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
        scrapZonaProp(formarLink(paginas, URL_ZonaProp), formarArchivo(paginas, archivos_ZonaProp))

    if paginas % 3 == 2:
        link1, link2 = formarLink(paginas-1, URL_ZonaProp), formarLink(paginas, URL_ZonaProp)
        archivo1, archivo2 = formarArchivo(paginas-1, archivos_ZonaProp), formarArchivo(paginas, archivos_ZonaProp)

        thread1 = threading.Thread(target=scrapZonaProp, args=(link1, archivo1))
        thread2 = threading.Thread(target=scrapZonaProp, args=(link2, archivo2))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

if __name__ == "__main__":
    main()