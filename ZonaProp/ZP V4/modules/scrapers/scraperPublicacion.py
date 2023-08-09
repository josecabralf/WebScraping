from modules.soup.soup import getSoup
from modules.scrapers.scraperCaracteristicas import *
from modules.exceptions.excepciones import agregarRevisionArchivo
from unidecode import unidecode
from datetime import timedelta


def crearObjetoJSON(datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, coord, vendedor, activo, URL):
    """Crea un diccionario con la estructura que tendrá un objeto JSON para guardar en un archivo

    Args:
        datos_interes (dict): diccionario de valores de interes
        tipo_prop (string): indica tipo de propiedad. Ej: Casa, departamento...
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        barrio (string): barrio del inmueble
        ciudad (string): ciudad del inmueble
        coord ([float, float]): coordenadas del inmueble ([latitud, longitud])
        vendedor (string): tipo de Vendedor (Inmobiliaria, Dueño directo, etc)
        activo (bool): indica si la publicacion esta activa o no
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    objetoJSON = {
        "id": id,
        "tipoPropiedad": tipo_prop,
        "precioUSD": precio,
        "fechaUltimaActualizacion": fecha,
        "vendedor": vendedor,
        "terrenoTotal": datos_interes['m² Total'],
        "terrenoEdificado": datos_interes['m² Cubierta'],
        "cantDormitorios": datos_interes['Dormitorios'],
        "cantBanos": datos_interes['Baños'],
        "cantCochera": datos_interes['Cocheras'],
        "barrio": barrio,
        "ciudad": ciudad,
        "coordX": coord[0],
        "coordY": coord[1],
        "activo": activo,
        "URL": URL
    }
    return objetoJSON


def crearLineaCSV(datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, coord, vendedor, activo, URL):
    """Crea un string con la estructura que tendrá una linea CSV para guardar en un archivo

    Args:
        datos_interes (dict): diccionario de valores de interes
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        coord (list): coordenadas de la ubicacion del inmueble
        vendedor (string): tipo de vendedor
        activo (bool): True si la publicacion está activa, False si no lo está
        URL (string): url de la publicacion

    Returns:
        str: string con estructura de linea CSV
    """
    return f"{id};{tipo_prop};{precio};{fecha};{vendedor};{datos_interes['m² Total']};{datos_interes['m² Cubierta']};{datos_interes['Dormitorios']};{datos_interes['Baños']};{datos_interes['Cocheras']};{barrio};{ciudad};{coord[0]};{coord[1]};{activo};{URL}\n"


def getPrecio(soup):
    """Obtiene el precio de una publicacion utilizando BeautifulSoup

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion

    Returns:
        Case 1 int: precio en dolares
        Case 2 bool False: si no se encuentra un precio o el mismo no está en dolares
    """
    try:
        precio = soup.find('div', class_='price-items').text.split()
        if precio[0] == 'USD':
            precio = int(precio[1].replace('.', ''))
            return precio
        else:
            return False
    except:
        return False


def getFecha(soup, hoy):
    """Obtiene la fecha de publicación/última actualización de una publicación de ZP

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion
        hoy (date): fecha del día de la fecha para calcular la fecha de publicación/última actualización

    Returns:
        date string, bool: fecha de publicación/última actualización (dd-mm-yy), activo (True/False)
    """
    try:
        delta = soup.find('div', id='user-views').find('p').text.split()
        if delta[-1] == 'hoy':
            delta = 0
        elif delta[-1] == 'ayer':
            delta = 1
        elif delta[-1] in ['día', 'días']:
            delta = int(delta[-2])
        elif delta[-1] in ['mes', 'meses']:
            delta = 31*int(delta[-2])
        elif delta[-1] in ['año', 'años']:
            delta = 365*int(delta[-2])

        activo = True
        if delta > 45:
            activo = False

        fecha = hoy - timedelta(days=delta)
        fecha = fecha.strftime("%d-%m-%Y")
        return fecha, activo
    except:
        return None, None


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


def getTipoVendedor(soup):
    vendedor = soup.find('div', class_='feature-info')
    if vendedor:
        return 'PARTICULAR'
    return 'INMOBILIARIA'


def scrapPublicacionZP(URL, hoy):
    """Scrapea una publicacion individual de ZonaProp para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

    Args:
        URL (string): url de la publicacion
        hoy (date): fecha del día de hoy para calcular fecha de publicacion/actualizacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    soup = getSoup(URL)

    # precio
    precio = getPrecio(soup)
    if not precio:
        return False

    # id
    id = URL.split('-')[-1].split('.')[0]

    # Fecha de Publicacion/Actualizacion
    fecha, activo = getFecha(soup, hoy)
    if not fecha:
        agregarRevisionArchivo(URL, id)

    # caracteristicas de interes
    datos_interes = getCaracteristicas(soup)

    # ubicacion
    ubicacion = soup.find_all('a', class_="bread-item-redirect")
    try:
        tipo_prop = ubicacion[1].text.strip().upper()
        ciudad = unidecode(ubicacion[4].text.strip().upper())
        barrio = unidecode(ubicacion[5].text.strip().upper())
        del ubicacion
    except:
        return False

    coord = getUbicGeo(soup)

    vendedor = getTipoVendedor(soup)

    objetoJSON = crearObjetoJSON(
        datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, coord, vendedor, activo, URL)

    return objetoJSON
