from unidecode import unidecode


def getNombreLV(soup):
    try:
        nombre = soup.find(
            'div', class_='col col-8 pt1').find('h4').text.strip()
    except:
        nombre = ''

    return unidecode(nombre.upper())


def getTelefonoLV(soup):
    try:
        telefono = soup.find(
            'a', id='tel')['href'].replace('tel:', '').split('/')[0].strip()
    except:
        telefono = ''

    return telefono


def getEmailLV(soup):
    try:
        email = soup.find('button', id='mail').find('a')['href']
        email = email.replace('mailto:', '').split('?')[0]
    except:
        email = ''

    return email
