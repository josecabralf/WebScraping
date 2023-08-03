from config import ar_publicaciones
from modules.scrapers.scraperContacto import scrapContacto


def main():
    publicaciones = open(ar_publicaciones, 'r')
    for line in publicaciones.readlines():
        scrapContacto(line.split(';'))
    publicaciones.close()


if __name__ == '__main__':
    main()
