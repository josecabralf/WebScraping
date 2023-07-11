from bs4 import BeautifulSoup
import requests
from scraperMercadoLibre import scrapMeLi
from config import *


def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Mercado Libre

    Args:
        url_base (string): url base de Mercado Libre que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    link = url_base.split('_')
    link.insert(1, f"Desde_{i*48+1}")
    link = '_'.join(link)
    return link


def main():
    response = requests.get(URL_Meli)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int(
        soup.find('li', class_='andes-pagination__page-count').text.split()[-1])

    for i in range(paginas):
        if i == 0:
            link = URL_Meli
        else:
            link = formarLink(URL_Meli, i)

        scrapMeLi(URL=link, archivo=archivos_Meli + f'pagina{i+1}.json')


if __name__ == "__main__":
    main()
