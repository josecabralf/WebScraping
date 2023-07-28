from bs4 import BeautifulSoup
import requests


def getSoup(URL):
    res = requests.get(URL)
    return BeautifulSoup(res.content, 'html.parser')
