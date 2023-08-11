from modules.soup.soup import getSoup
from unidecode import unidecode
from MeLiConfig import archivos_Links, URL_Meli_CASAS, URL_Meli_DPTOS, URL_Meli_TERS


def validarCantResultados(URL):
    """Chequea si una busqueda filtrada posee más de 2016 resultados de búsqueda. Si es así, realiza un filtrado más profundo.

        Args:
        URL (string): link de la búsqueda filtrada.

        Returns:
        [string]: arreglo de urls filtradas con menos de 2016 resultados de búsqueda cada uno.
    """
    cant_publicaciones = getCantPublicaciones(URL)
    if cant_publicaciones > 2016:
        return formarListaLinks(URL)
    return [URL]


def getCantPublicaciones(URL):
    """Obtiene la cantidad de resultados de busqueda (publicaciones) de una pagina filtrada de MercadoLibre

    Args:
        URL (string): link de pagina de busqueda filtrada

    Returns:
        int: cantidad de resultados de busqueda
    """
    soup = getSoup(URL)
    cant_publicaciones = int(soup.find(
        'span', class_='ui-search-search-result__quantity-results shops-custom-secondary-font').text.split()[0].replace('.', ''))

    return cant_publicaciones


def formarListaLinks(URL):
    """Forma una lista de links filtrados a partir de una URL que contiene los posibles filtros por zona geográfica.

    Args:
        URL (string): url de filtos geográficos posibles

    Returns:
        [string]: listado de links de páginas filtradas según zona geográfica
    """
    soup = getSoup(URL)
    link_zonas = soup.find(
        'a', class_='ui-search-modal__link ui-search-modal--default ui-search-link')["href"]
    link_zonas = link_zonas.split('&')[0]
    soup = getSoup(link_zonas)

    zonas = [a["href"].split('#')[0] for a in soup.find_all(
        'a', class_='ui-search-search-modal-filter ui-search-link')]
    if zonas == []:
        return formarLinksBarrios(soup, URL)
    return zonas


def formarLinksBarrios(soup, URL):
    """Forma links para filtrar por barrio.

    Args:
        soup (BeautifulSoup): contenidos de la página de filtro posibles según barrio
        URL (string): url de la busqueda principal

    Returns:
        [string]: listado de links de páginas filtradas según barrios
    """
    nombres = [n.text.lower() for n in soup.find_all(
        'span', class_='andes-checkbox__label andes-checkbox__label-text')]
    url_base = '/'.join(URL.split('/')[0:-1])
    suffix = URL.split('/')[-1]
    links = []
    for i in range(len(nombres)):
        n = "-".join(unidecode(nombres[i]).split())
        links.append(f"{url_base}/{n}/{suffix}")
    return links


def agregarLinksArchivo(url):
    """Agrega al final de un archivo una serie de links de páginas filtradas obtenidos a partir de una URL inicial

    Args:
        url (string): url inicial
    """
    archivo = open(archivos_Links, 'a', encoding='utf-8')

    ciudades = validarCantResultados(url)
    for i in range(len(ciudades)):
        barrios = validarCantResultados(ciudades[i])
        for barrio in barrios:
            archivo.write(barrio + '\n')
    archivo.close()


def crearArchivoLinksSiNoExiste():
    """Crea un archivo de links filtrados en caso de que no exista
    """
    agregarLinksArchivo(URL_Meli_CASAS)
    print('Casas Listo')
    agregarLinksArchivo(URL_Meli_DPTOS)
    print('Departamentos Listo')
    agregarLinksArchivo(URL_Meli_TERS)
    print('Terrenos Listo')
