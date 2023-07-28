def getUbicGeo(soup):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de ZonaProp

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    try:
        mapa = soup.find('img', id="static-map")["src"]
        loc = mapa.split('?')[1].split('&')[0].split('=')[1]
        return [float(n) for n in loc.split(',')]
    except:
        return [None, None]
