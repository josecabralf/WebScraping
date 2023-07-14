from bs4 import BeautifulSoup
import requests
from scraperMercadoLibre import scrapMeLi
from config import *
import threading
import time


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


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"pagina{i+1}.json"


def main():
    URL = URL_Meli_DPTOS_CBA
    ar = archivos_Meli_DPTOS
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int(
        soup.find('li', class_='andes-pagination__page-count').text.split()[-1])

    for i in range(0, paginas-2, 3):
        link1, link2, link3 = formarLink(i, URL), formarLink(i+1, URL), formarLink(i+2, URL)
        archivo1, archivo2, archivo3 = formarArchivo(
            i, ar), formarArchivo(i+1, ar), formarArchivo(i+2, ar)

        thread1 = threading.Thread(target=scrapMeLi, args=(link1, archivo1))
        thread2 = threading.Thread(target=scrapMeLi, args=(link2, archivo2))
        thread3 = threading.Thread(target=scrapMeLi, args=(link3, archivo3))

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
        scrapMeLi(URL=formarLink(paginas-1, URL), archivo=formarArchivo(paginas-1, ar))

    if paginas % 3 == 2:
        link1, link2 = formarLink(paginas-2, URL), formarLink(paginas-1, URL)
        archivo1, archivo2 = formarArchivo(paginas-2, ar), formarArchivo(paginas-1, ar)

        thread1 = threading.Thread(target=scrapMeLi, args=(link1, archivo1))
        thread2 = threading.Thread(target=scrapMeLi, args=(link2, archivo2))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()


if __name__ == "__main__":
    main()
