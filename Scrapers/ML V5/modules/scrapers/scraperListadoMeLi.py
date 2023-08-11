from modules.scrapers.scraperPublicacion import scrapPublicacionML
from modules.soup.soup import getSoup
from datetime import date
from MeLiConfig import cols


def getUbicacionProvisoria(URL):
    """Obtiene una ubicacion provisoria para los inmuebles a partir de la url del listado

    Args:
        URL (string): url del listado

    Returns:
        [string]: [ciudad, barrio] de los inmuebles
    """
    try:
        ciudad = URL.split('/')[7].replace('-', ' ').upper()
        barrio = URL.split('/')[8].replace('-', ' ').upper()
        if 'INMUEBLES' in barrio:
            barrio = ''
    except:
        ciudad = ''
        barrio = ''
    return [ciudad, barrio]


def crearListaLinks(URL):
    """Crea una lista de links de publicaciones a scrapear a partir de una URL que posee nos conduce a un listado de publicaciones.

    Args:
        URL (string): URL que nos conduce al listado de publicaciones

    Returns:
        [string]: listado de links de publicaciones individuales
    """
    soup = getSoup(URL)

    links = [link["href"] for link in soup.find_all(
        'a', class_='ui-search-item__group__element shops__items-group-details ui-search-link')]
    return links


def escribirArchivo(archivo, links_casas, ubic):
    """Esta funcion nos permite recorrer uno por uno un arreglo de links que nos conducen a publicaciones de casas individuales para poder scrapear datos sobre ellas y escribir dichos datos en un archivo csv.

    Args:
        archivo (string): define el nombre y ruta del archivo json que se quiere generar a partir de los datos scrapeados. Ej. './Casas/pagina1.csv'
        links_casas ([string]): arreglo con la lista de links de casas que se quieren scrapear
    """
    hoy = date.today()
    with open(archivo, 'w', encoding='utf-8') as archivoCSV:
        archivoCSV.write(cols)
        for link in links_casas:
            try:
                lineaCSV = scrapPublicacionML(link, hoy, ubic)
            except:
                lineaCSV = False
            if lineaCSV:
                archivoCSV.write(lineaCSV)


def scrapListadoPublicaciones(URL, archivo):
    """Esta funcion nos permite scrapear datos de una pagina web que posee un listado de publicaciones; y escribe dichos datos en un archivo

    Args:
        URL (string): URL que nos conduce al listado de publicaciones
        archivo (string): define el nombre y ruta del archivo json que se quiere generar a partir de los datos scrapeados. Ej. './Casas/pagina1.csv'
    """
    links_casas = crearListaLinks(URL)
    ubic = getUbicacionProvisoria(URL)
    escribirArchivo(archivo, links_casas, ubic)
