from bs4 import BeautifulSoup
import requests
from scraperClasificados import scrapLaVozClasificados
from config import *
import threading
import time


def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Clasificados de La Voz

    Args:
        url_base (string): url base de Clasificados de La Voz que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    return url_base + f'&page={i}'


def main():
    response = requests.get(URL_LaVoz)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)

    for i in range(1, paginas-1, 3):
        URL1, URL2, URL3 = formarLink(URL_LaVoz, i), formarLink(
            URL_LaVoz, i+1), formarLink(URL_LaVoz, i+2)

        archivo1, archivo2, archivo3 = archivos_LaVoz + \
            f'pagina{i}.json', archivos_LaVoz + \
            f'pagina{i+1}.json', archivos_LaVoz + f'pagina{i+2}.json'

        thread1 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL1, archivo1))
        thread2 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL2, archivo2))
        thread3 = threading.Thread(
            target=scrapLaVozClasificados, args=(URL3, archivo3))

        try:
            thread1.start()
        except:
            time.sleep(30)
            thread1 = threading.Thread(target=scrapLaVozClasificados, args=(URL1, archivo1))
            thread1.start()
        
        try:
            thread2.start()
        except:
            time.sleep(30)
            thread2 = threading.Thread(target=scrapLaVozClasificados, args=(URL2, archivo2))
            thread2.start()
            
        try:
            thread3.start()
        except:
            time.sleep(30)
            thread3 = threading.Thread(target=scrapLaVozClasificados, args=(URL3, archivo3))
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


if __name__ == "__main__":
    main()
