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
