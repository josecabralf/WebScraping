from modules.scrapers.scraperListadoZP import escribirArchivo
from modules.format.archivos import asignarValNro
from ZPConfig import revisionesFecha, archivos_ZonaProp
import os


def revisionArchivos():
    if not os.path.exists(revisionesFecha):
        return
    revisiones = open(revisionesFecha, 'r')
    links_casas = [line.split()[1].replace('\n', '')
                   for line in revisiones.readlines()]
    revisiones.close()
    if links_casas == []:
        return
    n = asignarValNro(archivos_ZonaProp)
    fechas = f'{archivos_ZonaProp}{n}-fechasRevisadas.json'
    escribirArchivo(fechas, links_casas)
