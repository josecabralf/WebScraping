from src.Scrapers.SoupStrategy import SoupStrategy
from datetime import datetime
from bs4 import BeautifulSoup
from src.Scrapers.Listado import Listado
from abc import abstractmethod
from src.Scrapers.Archivos.Logger import LoggeableScraper

class PaginaWeb(LoggeableScraper):
    def __init__(self, url: str, strategy_soup: SoupStrategy):
        self._url = url
        self._strategy_soup = strategy_soup
        self._hoy = datetime.today()
        self.set_soup()
        self._cantidad_paginas = self.get_cantidad_paginas()

    def execute_soup_strategy(self) -> BeautifulSoup: 
        return self._strategy_soup.execute(self._url)

    @abstractmethod
    def get_cantidad_paginas(self) -> int: ...
    
    @abstractmethod
    def crear_listado(self, i: int, archivo: str, publicaciones: list) -> Listado: ...

    @abstractmethod
    def crear_link_listado(self) -> str: ...
    
    def escribir_listado(self, i, archivo, publicaciones = []):
        listado = self.crear_listado(i, archivo, publicaciones)
        listado.escribir_archivo_csv()
    
    @property
    def soup(self) -> str: return self._soup
    def set_soup(self): self._soup = self.execute_soup_strategy()

    @property
    def url(self) -> str: return self._url
    
    @property
    def cantidad_paginas(self) -> int: return self._cantidad_paginas