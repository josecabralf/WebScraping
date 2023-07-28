from soup import getSoup


def getImgUbic(tag):
    return tag.name == 'img' and str(tag.get('src')).startswith('https://maps.googleapis.com/maps/')


def getUbicGeo(soup, URL):
    i = 1
    while True:
        try:
            img = soup.find(getImgUbic)['src']
            loc = img.split('&')[4].split('=')[1]
            if loc:
                return [float(n) for n in loc.split('%2C')]
        except:
            i += 1
            if i == 10:
                return [None, None]
            getSoup(URL)
