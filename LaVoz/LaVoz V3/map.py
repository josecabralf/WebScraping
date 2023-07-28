def getUbicGeo(soup):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de LaVoz, si es que hay un mapa

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    try:
        img = soup.find('amp-iframe', id='map-iframe')['src']
        loc = img.split('marker=')
        return [float(n) for n in loc.split('%2C')]
    except:
        return [None, None]
