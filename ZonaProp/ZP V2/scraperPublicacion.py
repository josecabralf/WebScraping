from soup import getSoup
from scraperCaracteristicas import *
from excepciones import agregarRevisionArchivo, getFecha
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
        "terrenoTotal": datos_interes['m² Total'],
        "terrenoEdificado": datos_interes['m² Cubierta'],
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
        precio = soup.find('div', class_='price-items').text.split()
        if precio[0] == 'USD':
            precio = int(precio[1].replace('.', ''))
            return precio
        else:
            return False
    except:
        return False


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
    fecha = getFecha(soup, hoy)
    if not fecha:
        fecha = ''
        agregarRevisionArchivo(URL, id)

    # caracteristicas de interes
    datos_interes = getCaracteristicas(soup)

    # ubicacion
    ubicacion = soup.find_all('a', class_="bread-item-redirect")
    tipo_prop = ubicacion[1].text.strip().upper()
    ciudad = unidecode(ubicacion[4].text.strip().upper())
    barrio = unidecode(ubicacion[5].text.strip().upper())
    del ubicacion

    objetoJSON = crearObjetoJSON(
        datos_interes, tipo_prop, precio, fecha, id, barrio, ciudad, URL)

    return objetoJSON
