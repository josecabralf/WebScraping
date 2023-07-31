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
