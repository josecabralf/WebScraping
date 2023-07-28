from soup import getSoup


def getImgUbic(tag):
    return tag.name == 'img' and str(tag.get('src')).startswith('https://maps.googleapis.com/maps/')


def getUbicGeo(soup, URL):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de MercadoLibre

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina
        URL (string): url de la pagina de publicacion

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    i = 1
    while True:
        try:
            img = soup.find(getImgUbic)['src']
            loc = img.split('&')[4].split('=')[1]
            if loc:
                return [float(n) for n in loc.split('%2C')]
        except:
            if i == 10:
                return [None, None]
            i += 1
            getSoup(URL)
