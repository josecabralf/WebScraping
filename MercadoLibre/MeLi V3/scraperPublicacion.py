from soup import getSoup
from scraperCaracteristicas import getCaracteristicas
from datetime import timedelta
from unidecode import unidecode


def crearObjetoJSON(datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, URL):
    """Crea un diccionario con la estructura que tendrá un objeto JSON para guardar en un archivo

    Args:
        datos_interes (dict): diccionario de valores de interes
        tipo_prop (string): indica tipo de propiedad. Ej: Casa, departamento...
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        barrio (string): barrio del inmueble
        ciudad (string): ciudad del inmueble
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    objetoJSON = {
        "id": id,
        "tipoPropiedad": tipo_prop,
        "precioUSD": precio,
        "fechaUltimaActualizacion": fecha,
        "terrenoTotal": datos_interes['Superficie total'],
        "terrenoEdificado": datos_interes['Superficie cubierta'],
        "cantDormitorios": datos_interes['Dormitorios'],
        "cantBanos": datos_interes['Baños'],
        "cantCochera": datos_interes['Cocheras'],
        "barrio": barrio,
        "ciudad": ciudad,
        "URL": URL
    }
    return objetoJSON


def getPrecio(soup):
    """Obtiene el precio de una publicacion utilizando BeautifulSoup

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion

    Returns:
        Case 1 int: precio en dolares
        Case 2 bool False: si no se encuentra un precio o el mismo no está en dolares
    """
    try:
        precio = soup.find('span', class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').find(
            'span', class_='andes-visually-hidden').text.split()
        if precio[1] == 'dólares':
            precio = int(precio[0])
            return precio
        else:
            return False
    except:
        return False


def getFecha(soup, hoy):
    """Obtiene la fecha de publicación/última actualización de una publicación de MeLi

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion
        hoy (date): fecha del día de la fecha para calcular la fecha de publicación/última actualización

    Returns:
        date: fecha de publicación/última actualización (dd-mm-yy)
    """
    try:
        dias_desde_actualiz = soup.find(
            'p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle').text.split()
    except:
        # A veces el renderizado es distinto: tiene otra clase la etiqueta p
        dias_desde_actualiz = soup.find(
            'p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title').text.split()

    if dias_desde_actualiz[3] in ["día", "días"]:
        delta = int(dias_desde_actualiz[2])
    elif dias_desde_actualiz[3] in ["mes", "meses"]:
        delta = int(dias_desde_actualiz[2]) * 31
    elif dias_desde_actualiz[3] in ["año", "años"]:
        delta = int(dias_desde_actualiz[2]) * 365

    fecha = (hoy - timedelta(days=delta)).strftime("%d-%m-%Y")
    return fecha


def getUbicacion(soup, ubic):
    """Obtiene la ubicacion en donde está la propiedad

    Args:
        soup (BeautifulSoup): contiene el HTML de la página de la publicacion
        ubic ([string]): contiene una ubicacion menos aproximada obtenida mediante la url del listado

    Returns:
        barrio (string): barrio de propiedad
        ciudad (string): ciudad de propiedad
    """
    ubicacion = soup.find_all('a', class_='andes-breadcrumb__link')

    try:
        ciudad = unidecode(ubicacion[5].text.upper())
    except:
        ciudad = ubic[0]

    try:
        barrio = unidecode(ubicacion[6].text.upper())
    except:
        barrio = ubic[1]

    return barrio, ciudad


def scrapPublicacionML(URL, hoy, ubic):
    """Scrapea una publicacion individual de Mercado Libre para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

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
    id = URL.split('-')[1]

    # Fecha de Publicacion/Actualizacion
    fecha = getFecha(soup, hoy)

    # caracteristicas de interes
    tipo_prop = (URL.split('.')[0].split('//')[1]).upper()

    datos_interes = getCaracteristicas(URL, tipo_prop)
    if not datos_interes:
        return False

    # ubicacion
    barrio, ciudad = getUbicacion(soup, ubic)

    objetoJSON = crearObjetoJSON(
        datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, URL.split('#')[0])

    return objetoJSON
