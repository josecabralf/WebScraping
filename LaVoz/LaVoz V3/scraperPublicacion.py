from bs4 import BeautifulSoup
import requests
from scraperCaracteristicas import getDatosCaracteristicas

def crearObjetoJSON(datos_interes, precio, fecha, id, URL):
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
        "URL" : URL
    }
    return objetoJSON

def getPrecio(etiqueta, clase, soup):
    # Precio
    try:
        precio = soup.find(etiqueta, class_= clase).text.strip().split()
        if precio[0] == 'U$S':
            precio = int(precio[1].replace('.',''))
            return precio
        else:
            return False # Si no es en dolares, no nos interesa el dato (es muy variable a futuro)
    except: 
        return False # Si no hay precio, no nos interesa el dato

def scrapLaVozPublicacion(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    precio = getPrecio('div', 'h2 mt0 main bolder', soup)
    if not precio: return False
    
    # id
    id = URL.split('/')[5]

    # Fecha de Publicacion/Actualizacion
    fecha = soup.find('div', class_='h5 center').text.split(':')[1].strip().replace('.','-')

    # caracteristicas de interes
    caracteristicas = soup.find_all('div', class_= 'flex-auto nowrap col-4')
    caracteristicas = [car.text.strip().split() for car in caracteristicas]
    datos_interes = getDatosCaracteristicas(caracteristicas)

    objetoJSON = crearObjetoJSON(datos_interes, precio, fecha, id, URL)

    return objetoJSON