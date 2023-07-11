from bs4 import BeautifulSoup
import requests
from scraperMercadoLibre import scrapMeLi
from config import *
import threading


def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Mercado Libre

    Args:
        url_base (string): url base de Mercado Libre que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    if i == 0:
        return url_base
    link = url_base.split('_')
    link.insert(1, f"Desde_{i*48+1}")
    link = '_'.join(link)
    return link


def main():
    response = requests.get(URL_Meli)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int(
        soup.find('li', class_='andes-pagination__page-count').text.split()[-1])

    for i in range(0, paginas-2, 3):
        link1, link2, link3 = formarLink(URL_Meli, i), formarLink(
            URL_Meli, i+1), formarLink(URL_Meli, i+2)
        archivo1, archivo2, archivo3 = f'pagina{i+1}.json', f'pagina{i+2}.json', f'pagina{i+3}.json'

        hilo1 = threading.Thread(target=scrapMeLi, args=(link1, archivo1))
        hilo2 = threading.Thread(target=scrapMeLi, args=(link2, archivo2))
        hilo3 = threading.Thread(target=scrapMeLi, args=(link3, archivo3))

        hilo1.start()
        hilo2.start()
        hilo3.start()

        hilo1.join()
        hilo2.join()
        hilo3.join()

    if paginas % 3 == 1:
        scrapMeLi(URL=formarLink(URL_Meli, paginas-1))

    if paginas % 3 == 2:
        link1, link2 = formarLink(URL_Meli, paginas-2), formarLink(
            URL_Meli, paginas-1)
        archivo1, archivo2 = f'pagina{paginas-1}.json', f'pagina{paginas}.json'

        hilo1 = threading.Thread(target=scrapMeLi, args=(link1, archivo1))
        hilo2 = threading.Thread(target=scrapMeLi, args=(link2, archivo2))

        hilo1.start()
        hilo2.start()

        hilo1.join()
        hilo2.join()


if __name__ == "__main__":
    main()
