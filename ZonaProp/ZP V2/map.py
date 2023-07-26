def getUbicGeo(soup):
    mapa = soup.find('img', class_='ui-pdp-image')["src"]
    loc = mapa.split('?')[1].split('&')[0].split('=')[1]
    loc = [float(n) for n in loc.split(',')]
    return loc
