import requests
import bs4


def getTelefonoLV(soup):
    try:
        telefono = soup.find(
            'a', id='tel')['href'].replace('tel:', '')
        telefono = telefono.split('/')[0].strip()
    except:
        telefono = ''

    return telefono


url = 'https://clasificados.lavoz.com.ar/avisos/casas/5093663/oportunidad-locales-excelente-zona-comercial-en-parque-liceo-i'
res = requests.get(url)
s = bs4.BeautifulSoup(res.text, 'lxml')

nom = getTelefonoLV(s)
print(nom)
