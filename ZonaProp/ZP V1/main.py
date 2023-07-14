from config import URL_ZonaProp, archivos_ZonaProp
from soup import getSoup
from scraperZonaProp import scrapZonaProp
from math import trunc


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
    for i in range(1, paginas+1):
        scrapZonaProp(formarLink(i, URL_ZonaProp), formarArchivo(i, archivos_ZonaProp))

if __name__ == "__main__":
    main()