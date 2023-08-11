from bs4 import BeautifulSoup
import requests


def getSoup(URL):
    """Genera un objeto BeautifulSoup a partir de una URL

    Args:
        URL (sring): url del sitio web

    Returns:
        BeautifulSoup: objeto BeautifulSoup del sitio web
    """
    res = requests.get(URL)
    return BeautifulSoup(res.content, 'html.parser')
