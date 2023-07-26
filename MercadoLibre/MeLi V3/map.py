def getUbicGeo(soup):
    mapa = soup.find('img', class_='ui-pdp-image')["src"]
    loc = mapa.split('&')[4]
    loc = loc.split('=')[1]
    loc = [float(n) for n in loc.split('%2C')]
    return loc
