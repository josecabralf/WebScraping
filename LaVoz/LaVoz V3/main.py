from bs4 import BeautifulSoup
import requests
from scraperClasificados import scrapLaVozClasificados
from config import *
import threading

response = requests.get(URL_LaVoz)
soup = BeautifulSoup(response.content, 'html.parser')

paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)

for i in range(1,paginas-1, 3):
    URL1, URL2, URL3 = URL_LaVoz + f'&page={i}', URL_LaVoz + f'&page={i+1}', URL_LaVoz + f'&page={i+2}'
    archivo1, archivo2, archivo3 = archivos_LaVoz + f'pagina{i}.json', archivos_LaVoz + f'pagina{i+1}.json', archivos_LaVoz + f'pagina{i+2}.json'

    thread1 = threading.Thread(target=scrapLaVozClasificados, args=(URL1, archivo1))
    thread2 = threading.Thread(target=scrapLaVozClasificados, args=(URL2, archivo2))
    thread3 = threading.Thread(target=scrapLaVozClasificados, args=(URL3, archivo3))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

if paginas%3 == 1:
    scrapLaVozClasificados(URL=URL_LaVoz + f'&page={paginas}', archivo=archivos_LaVoz + f'pagina{paginas}.json')

elif paginas%3 == 2:
    URL1, URL2 = URL_LaVoz + f'&page={paginas-1}', URL_LaVoz + f'&page={paginas}'
    archivo1, archivo2 = archivos_LaVoz + f'pagina{paginas-1}.json', archivos_LaVoz + f'pagina{paginas}.json'
    
    thread1 = threading.Thread(target=scrapLaVozClasificados, args=(URL1, archivo1))
    thread2 = threading.Thread(target=scrapLaVozClasificados, args=(URL2, archivo2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()