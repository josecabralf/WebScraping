def formarLink(url_base, i):
    """Forma links de paginas de publicaciones según el criterio de Clasificados de La Voz

    Args:
        url_base (string): url base de Clasificados de La Voz que vamos a modificar para acceder a una nueva pagina
        i (int): indica el numero de pagina actual

    Returns:
        string: url modificada para acceder a pagina i
    """
    return url_base + f'&page={i}'


URL_LaVoz = "hola"
nro = 25
URLs = [formarLink(URL_LaVoz, i) for i in range(nro-2, nro)]
print(URLs)
