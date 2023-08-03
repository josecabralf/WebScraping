from modules.archivos.archivos import escribirContacto
from modules.soup.soup import *
from modules.scrapers.scraperLV import *


def crearLineaCSV(datos, nombre, telefono, email):
    return f"{datos[0]}; {nombre}; {telefono}; {email}; {datos[1]}; {datos[2]}"


def scrapContactoSegunLink(datos):
    if datos[1].contains('https://clasificados.lavoz.com.ar'):
        return scrapContactoLV(datos)
    elif datos[1].contains('https://inmuebles.mercadolibre.com.ar'):
        return scrapContactoML(datos)
    return scrapContactoZP(datos)


def scrapContactoLV(datos):
    soup = getStaticSoup(datos[1])
    nombre = getNombreLV(soup)
    telefono = getTelefonoLV(soup)
    email = getEmailLV(soup)
    crearLineaCSV(datos, nombre, telefono, email)


def scrapContactoML(datos):
    soup = getStaticSoup(datos[1])
    nombre = ''
    telefono = ''
    email = ''
    crearLineaCSV(datos, nombre, telefono, email)


def scrapContactoZP(datos):
    soup = getDynamicSoup(datos[1])
    nombre = ''
    telefono = ''
    email = ''
    crearLineaCSV(datos, nombre, telefono, email)


def scrapContacto(datos):
    contacto = scrapContactoSegunLink(datos)
    if contacto:
        escribirContacto(contacto)
