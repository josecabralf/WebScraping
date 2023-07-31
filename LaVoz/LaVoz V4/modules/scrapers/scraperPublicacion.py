from modules.soup.soup import getSoup
from modules.scrapers.scraperCaracteristicas import getDatosCaracteristicas
import datetime
from unidecode import unidecode


def crearObjetoJSON(datos_interes, precio, fecha, id, coord, vendedor, activo, URL):
    """Crea un diccionario con la estructura que tendrá un objeto JSON para guardar en un archivo

    Args:
        datos_interes (dict): diccionario de valores de interes
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    objetoJSON = {
        "id": id,
        "tipoPropiedad": datos_interes['Tipo vivienda'],
        "precioUSD": precio,
        "fechaUltimaActualizacion": fecha,
        "tipoVendedor": vendedor,
        "terrenoTotal": datos_interes['Superficie total'],
        "terrenoEdificado": datos_interes['Superficie cubierta'],
        "cantDormitorios": datos_interes['Dormitorios'],
        "cantBanos": datos_interes['Baños'],
        "cantCochera": datos_interes['Cocheras'],
        "barrio": datos_interes['Barrio'],
        "ciudad": datos_interes['Ciudad'],
        "coordX": coord[0],
        "coordY": coord[1],
        "activo": activo,
        "URL": URL
    }
    return objetoJSON


def getPrecio(etiqueta, clase, soup):
    """Obtiene el precio de una publicacion utilizando BeautifulSoup

    Args:
        etiqueta (string): tipo de etiqueta html donde se encuentra el precio
        clase (string): clase de la etiqueta html buscada
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion

    Returns:
        Case 1 int: precio en dolares
        Case 2 bool False: si no se encuentra un precio o el mismo no está en dolares
    """
    try:
        precio = soup.find(etiqueta, class_=clase).text.strip().split()
        if precio[0] == 'U$S':
            precio = int(precio[1].replace('.', ''))
            return precio
        else:
            return False
    except:
        return False


def getDatosVendedor(soup):
    """Obtiene los datos del vendedor de una publicacion utilizando BeautifulSoup

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion

    Returns:
        dict: diccionario con los datos del vendedor
    """
    datos = soup.find('div', class_='clearfix px1 py1')
    try:
        tipoVendedor = datos.find('div', class_='h5 gray').text.strip()
    except:
        tipoVendedor = 'Particular'

    return tipoVendedor


def getFecha(soup, fechaCorte):
    """Obtiene la fecha de publicacion de una publicacion utilizando BeautifulSoup y determina si la publicacion está activa o no

    Args:
        soup (BeautifulSoup): contenidos de la página
        fechaCorte (string date): fecha del último scrap

    Returns:
        date string, bool: fecha de publicacion, True si la publicacion está activa, False si no lo está
    """
    fecha = soup.find('div', class_='h5 center').text.split(':')[
        1].strip().replace('.', '-')
    activo = True

    hoy = datetime.datetime.today()
    delta = hoy - datetime.datetime.strptime(fecha, "%d-%m-%Y")
    if delta.days > 45:
        activo = False

    if fechaCorte != None:
        if datetime.datetime.strptime(fecha, "%d-%m-%Y") < fechaCorte:
            return False

    return fecha, activo


def getUbicGeo(soup):
    """Obtiene la ubicacion geográfica desde un mapa en una publicacion de LaVoz, si es que hay un mapa

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con contenidos de la pagina

    Returns:
        [float] : coordenadas del inmueble [x, y]
    """
    try:
        img = soup.find('amp-iframe', id='map-iframe')['src']
        loc = img.split('marker=')[1]
        return [float(n) for n in loc.split('%2C')]
    except:
        return [None, None]


def scrapPublicacionLV(URL, fechaCorte):
    """Scrapea una publicacion individual de los Clasificados de La Voz para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

    Args:
        URL (string): url de la publicacion
        fechaCorte (date): fecha del día de la última lectura

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    soup = getSoup(URL)

    # Fecha de Publicacion/Actualizacion
    fecha, activo = getFecha(soup, fechaCorte)

    precio = getPrecio('div', 'h2 mt0 main bolder', soup)
    if not precio:
        return False

    # id
    id = URL.split('/')[5]

    coord = getUbicGeo(soup)

    vendedor = getDatosVendedor(soup)

    # caracteristicas de interes
    caracteristicas = soup.find_all('div', class_='flex-auto nowrap col-4')
    caracteristicas = [car.text.strip().split() for car in caracteristicas]
    datos_interes = getDatosCaracteristicas(caracteristicas, URL)

    objetoJSON = crearObjetoJSON(
        datos_interes, precio, fecha, id, coord, vendedor, activo, URL)

    return objetoJSON
