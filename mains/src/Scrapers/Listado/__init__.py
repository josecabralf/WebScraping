from bs4 import BeautifulSoup
from abc import abstractmethod
from src.Scrapers.SoupStrategy import SoupStrategy
from src.Scrapers.Archivos.Logger import LoggeableScraper
from src.Scrapers.Publicacion import Publicacion
from datetime import datetime
from src.Scrapers.Listado.ListadoFileWriter import ListadoFileWriter


class Listado(LoggeableScraper):
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime, publicaciones: list):
        self._url = url
        self._file_writer = ListadoFileWriter(archivo)
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
    
    def escribir_archivo_csv(self) -> None: self._file_writer.escribir_archivo_csv(self)
    
    def publicaciones(self) -> list: return self._publicaciones
    
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