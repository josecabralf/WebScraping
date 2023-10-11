from bs4 import BeautifulSoup
from abc import abstractmethod
from Scrapers.SoupStrategy import SoupStrategy
from Scrapers.Logger import Loggeable
from Scrapers.Publicacion.Publicacion import Publicacion
from datetime import datetime
from ScrapConfig import cols, linea_null


class Listado(Loggeable):
    _cols = cols
    _linea_null = linea_null
    
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime, publicaciones: list):
        self._url = url
        self._archivo = archivo
        self._strategy_soup = strategy_soup
        self._hoy = hoy
        if publicaciones: self._publicaciones = publicaciones
        else:
            self.set_soup()
            self._publicaciones = self.get_publicaciones()

    def execute_soup_strategy(self) -> BeautifulSoup: 
        return self._strategy_soup.execute(self._url)

    @abstractmethod
    def get_publicaciones(self) -> list: ...
    
    def escribir_archivo_csv(self) -> None:
        with open(self._archivo, 'w', encoding='utf-8') as file:
            file.write(self._cols)
            for url in self._publicaciones:
                try: p = self.crear_publicacion(url)
                except Exception as err: 
                    self.crear_log_error(f"error al crear publicacion", err)
                    continue
                if p.is_valid():
                    file.write(str(p))
            file.write(self._linea_null)
        
    @abstractmethod
    def crear_publicacion(self, url: str) -> Publicacion: ...
    
    @property
    def url(self) -> str: return self._url
    @url.setter
    def url(self, url: str) -> None: self._url = url
    
    @property
    def archivo(self) -> str: return self._archivo
    @archivo.setter
    def archivo(self, ar: str) -> None: self._archivo = ar
    
    @property
    def strategy_soup(self) -> SoupStrategy: return self._strategy_soup
    
    @property
    def hoy(self) -> datetime: return self._hoy
    
    @property
    def soup(self) -> str: return self._soup
    def set_soup(self): self._soup = self.execute_soup_strategy()