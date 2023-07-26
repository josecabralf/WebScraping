from ZPConfig import revisionesFecha, fechasRevisadas
from datetime import date, timedelta
from soup import getSoup


def agregarRevisionArchivo(URL, id):
    """Agrega una url al archivo de revisiones de fecha para posteriormente poder correr un proceso para recuperar el dato de la publicacion

    Args:
        URL (string): url de la publicacion
        id (int): id de la publicacion
    """
    file = open(revisionesFecha, 'a')
    file.write(f'{id} {URL}\n')
    file.close()


def getFecha(soup, hoy):
    """Obtiene la fecha de publicación/última actualización de una publicación de ZP

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion
        hoy (date): fecha del día de la fecha para calcular la fecha de publicación/última actualización

    Returns:
        Case 1 date: fecha de publicación/última actualización (dd-mm-yy)
        Case 2 bool: False para indicar que no se pudo encontrar
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

        fecha = hoy - timedelta(days=delta)
        fecha = fecha.strftime("%d-%m-%Y")
        return fecha
    except:
        return False


def revisionArchivos():
    hoy = date.today()
    revisiones = open(revisionesFecha, 'r')
    with open(fechasRevisadas, 'a') as fechas:
        for line in revisiones.readlines():
            id = line.split()[0]
            link = line.split()[1].replace('\n', '')
            while True:
                try:
                    soup = getSoup(link)
                    fecha = getFecha(soup, hoy)
                    if fecha:
                        fechas.write(f"{id} {fecha} \n")
                        break
                except:
                    continue
