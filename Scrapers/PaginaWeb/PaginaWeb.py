from Scrapers.SoupStrategy import SoupStrategy
from datetime import datetime
from bs4 import BeautifulSoup
from Scrapers.Listado.Listado import Listado
from abc import abstractmethod
from Scrapers.Logger import Loggeable

class PaginaWeb(Loggeable):
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
    def crear_listado(self, i, archivo) -> Listado: ...
    
    @abstractmethod
    def crear_listado_desde_lista(self, lista, archivo) -> Listado: ...

    @abstractmethod
    def crear_link_listado(self) -> str: ...
    
    def escribir_listado(self, i, archivo):
        listado = self.crear_listado(i, archivo)
        listado.escribir_archivo_csv()
        
    def escribir_listado_desde_lista(self, publicaciones, archivo):
        listado = self.crear_listado_desde_lista(publicaciones, archivo)
        listado.escribir_archivo_csv()
    
    @property
    def soup(self) -> str: return self._soup
    def set_soup(self): self._soup = self.execute_soup_strategy()

    @property
    def url(self) -> str: return self._url

    @property
    def archiver(self) -> str: return self._archiver
    
    @property
    def cantidad_paginas(self) -> int: return self._cantidad_paginas