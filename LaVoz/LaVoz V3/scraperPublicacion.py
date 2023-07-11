from bs4 import BeautifulSoup
import requests
from scraperCaracteristicas import getDatosCaracteristicas


def crearObjetoJSON(datos_interes, precio, fecha, id, URL):
    """Crea un diccionario con la estructura que tendrá un objeto JSON para guardar en un archivo

    Args:
        datos_interes ([dynamic]): lista de valores de interes
        precio (int): precio en dolares de una propiedad
        fecha (date): fecha de publicacion/actualizacion
        id (int): numero identificador de la publicacion
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    objetoJSON = {
        "id": id,
        "tipoPropiedad": datos_interes[0],
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


def scrapLaVozPublicacion(URL):
    """Scrapea una publicacion individual de los Clasificados de La Voz para encontrar los datos que nos interesan del inmbueble y almacenarlos en un diccionario de datos.

    Args:
        URL (string): url de la publicacion

    Returns:
        dict: diccionario con estructura de objeto JSON
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    precio = getPrecio('div', 'h2 mt0 main bolder', soup)
    if not precio:
        return False

    # id
    id = URL.split('/')[5]

    # Fecha de Publicacion/Actualizacion
    fecha = soup.find('div', class_='h5 center').text.split(':')[
        1].strip().replace('.', '-')

    # caracteristicas de interes
    caracteristicas = soup.find_all('div', class_='flex-auto nowrap col-4')
    caracteristicas = [car.text.strip().split() for car in caracteristicas]
    datos_interes = getDatosCaracteristicas(caracteristicas)

    objetoJSON = crearObjetoJSON(datos_interes, precio, fecha, id, URL)

    return objetoJSON
