import time
import threading
from scraperListadoMeLi import scrapListadoPublicaciones


def scrapHilo(link, archivo):
    """Ejecuta 1 hilo de scrap

    Args:
        link (string): url de listado
        archivo (string): ubicacion relativa del archivo
    """
    try:
        scrapListadoPublicaciones(link, archivo)
    except:
        time.sleep(10)
        scrapListadoPublicaciones(link, archivo)


def scrapMultiHilo(URLs, archivos):
    """Genera los hilos a ejecutar para realizar el scrap de forma más veloz

    Args:
        URLs ([string]): links de listados a scrapear
        archivos ([string]): ubicaciones relativas de los archivos correspondientes
    """
    threads = [None] * len(URLs)

    for i in range(len(threads)):
        threads[i] = threading.Thread(
            target=scrapHilo, args=(URLs[i], archivos[i]))

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()
