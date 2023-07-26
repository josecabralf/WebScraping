from scraperListadoZP import escribirArchivo
from ZPConfig import revisionesFecha, fechasRevisadas


def revisionArchivos():
    revisiones = open(revisionesFecha, 'r')
    links_casas = [line.split()[1].replace('\n', '')
                   for line in revisiones.readlines()]
    revisiones.close()
    escribirArchivo(fechasRevisadas, links_casas)


revisionArchivos()
