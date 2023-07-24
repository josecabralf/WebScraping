from bs4 import BeautifulSoup
import requests
from scraperCaracteristicas import getDatosCaracteristicas
import datetime


def crearObjetoJSON(datos_interes, precio, fecha, id, URL):
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
        "terrenoTotal": datos_interes['Superficie total'],
        "terrenoEdificado": datos_interes['Superficie cubierta'],
        "cantDormitorios": datos_interes['Dormitorios'],
        "cantBanos": datos_interes['Baños'],
        "cantCochera": datos_interes['Cocheras'],
        "barrio": datos_interes['Barrio'],
        "ciudad": datos_interes['Ciudad'],
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


def scrapPublicacionLV(URL, fechaCorte):
    """Scrapea una publicacion individual de los Clasificados de La Voz para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

    Args:
        URL (string): url de la publicacion
        fechaCorte (date): fecha del día de la última lectura

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Fecha de Publicacion/Actualizacion
    fecha = soup.find('div', class_='h5 center').text.split(':')[
        1].strip().replace('.', '-')

    if datetime.datetime.strptime(fecha, "%d-%m-%Y") < fechaCorte:
        return False

    precio = getPrecio('div', 'h2 mt0 main bolder', soup)
    if not precio:
        return False

    # id
    id = URL.split('/')[5]

    # caracteristicas de interes
    caracteristicas = soup.find_all('div', class_='flex-auto nowrap col-4')
    caracteristicas = [car.text.strip().split() for car in caracteristicas]
    datos_interes = getDatosCaracteristicas(caracteristicas, URL)

    objetoJSON = crearObjetoJSON(datos_interes, precio, fecha, id, URL)

    return objetoJSON
