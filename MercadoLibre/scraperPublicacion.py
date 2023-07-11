from bs4 import BeautifulSoup
import requests
from scraperCaracteristicas import getDatosCaracteristicas
from datetime import timedelta, datetime


def crearObjetoJSON(datos_interes, tipo_prop, precio, fecha, id, URL):
    """Crea un diccionario con la estructura que tendrá un objeto JSON para guardar en un archivo

    Args:
        datos_interes ([dynamic]): lista de valores de interes
        tipo_prop (string): indica tipo de propiedad. Ej: Casa, departamento...
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    objetoJSON = {
        "id": id,
        "tipoPropiedad": tipo_prop,
        "precioUSD": precio,
        "fechaUltimaActualizacion": fecha,
        "terrenoTotal": datos_interes[1],
        "terrenoEdificado": datos_interes[2],
        "cantDormitorios": datos_interes[3],
        "cantBanos": datos_interes[4],
        "cantCochera": datos_interes[5],
        "ubicacion": datos_interes[6],
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


def scrapMeLiPublicacion(URL, hoy):
    """Scrapea una publicacion individual de Mercado Libre para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

    Args:
        URL (string): url de la publicacion
        hoy (date): fecha del día de hoy para calcular fecha de publicacion/actualizacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # precio
    precio = getPrecio(soup)
    if not precio:
        return False

    # id
    id = URL.split('-')[1]

    # Fecha de Publicacion/Actualizacion
    dias_desde_actualiz = int(soup.find(
        'p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle').text.split()[2])
    fecha = (hoy - timedelta(days=dias_desde_actualiz)).strftime("%d-%m-%Y")

    # caracteristicas de interes
    tipo_prop = soup.find('span', class_='ui-pdp-subtitle').text.split()[0]
    caracteristicas = soup.find()

    objetoJSON = crearObjetoJSON(
        tipo_prop, precio, fecha, id, URL.split('#')[0])

    return objetoJSON
