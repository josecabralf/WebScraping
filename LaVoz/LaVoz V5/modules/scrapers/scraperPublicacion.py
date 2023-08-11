from modules.soup.soup import getSoup
from modules.scrapers.scraperCaracteristicas import getDatosCaracteristicas
import datetime


def crearLineaCSV(datos_interes, precio, fecha, id, coord, vendedor, activo, URL):
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
    return f"{id};{datos_interes['Tipo vivienda']};{precio};{fecha};{vendedor};{datos_interes['Superficie total']};{datos_interes['Superficie cubierta']};{datos_interes['Dormitorios']};{datos_interes['Baños']};{datos_interes['Cocheras']};{datos_interes['Barrio']};{datos_interes['Ciudad']};{coord[0]};{coord[1]};{activo};{URL}\n"

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


def getTipoVendedor(soup):
    """Obtiene los datos del vendedor de una publicacion utilizando BeautifulSoup

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion

    Returns:
        dict: diccionario con los datos del vendedor
    """
    datos = soup.find('div', class_='clearfix px1 py1')
    try:
        tipoVendedor = datos.find('div', class_='h5 gray').text.strip().upper()
    except:
        tipoVendedor = 'PARTICULAR'

    return tipoVendedor


def getFecha(soup, fechaCorte):
    """Obtiene la fecha de publicacion de una publicacion utilizando BeautifulSoup y determina si la publicacion está activa o no

    Args:
        soup (BeautifulSoup): contenidos de la página
        fechaCorte (string date): fecha del último scrap

    Returns:
        date string, bool: fecha de publicacion, True si la publicacion está activa, False si no lo está
    """
    try:
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
    
    except:
        return None, None


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

    vendedor = getTipoVendedor(soup)

    # caracteristicas de interes
    caracteristicas = soup.find_all('div', class_='flex-auto nowrap col-4')
    caracteristicas = [car.text.strip().split() for car in caracteristicas]
    datos_interes = getDatosCaracteristicas(caracteristicas, URL)

    return crearLineaCSV(datos_interes, precio, fecha, id, coord, vendedor, activo, URL)

