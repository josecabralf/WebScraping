from modules.soup.soup import getSoup


def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Clasificados de La Voz

    Args:
        url_base (string): url base de Clasificados de La Voz que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    return url_base + f'&page={i}'


def getCantPaginas(URL):
    soup = getSoup(URL)
    return int((soup.find_all('a', class_="page-link h4"))[-1].text)