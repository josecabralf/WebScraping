from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from src.Scrapers.SoupStrategy import SoupStrategy
from src.Scrapers.Archivos.Logger import LoggeableScraper
from src.Scrapers.Archivos.Revision import Revision
from datetime import datetime


class Publicacion(LoggeableScraper):
    def __init__(self, url : str, strategy_soup: SoupStrategy, hoy: datetime):
        self._url = url
        self._strategy_soup = strategy_soup
        self.set_soup()
        self._validity = self.set_datos_publicacion(hoy)
        
    def set_datos_publicacion(self, hoy) -> bool:
        self.set_fecha(self.find_fecha(hoy))
        if not self.fecha: return False
        self.set_precio(self.find_precio())
        if not self._precio: return False
        self.set_id(self.find_id())
        self.set_vendedor(self.find_vendedor())
        self.set_coord(self.find_coord())
        self.set_caracteristicas(self.find_caracteristicas())
        if not self.caracteristicas: return False
        return True
    
    def __str__(self) -> str:
        return f"{self._id};{self._caracteristicas['tipo']};{self._precio};{self._fecha};{self._vendedor};{self._caracteristicas['TT']};{self._caracteristicas['TE']};{self._caracteristicas['Dorms']};{self._caracteristicas['Banos']};{self._caracteristicas['Cocheras']};{self._caracteristicas['Barrio']};{self._caracteristicas['Ciudad']};{self._coord[0]};{self._coord[1]};{self._url}\n"

    def agregar_revision(self): Revision().agregar_revision(self._url)

    def is_valid(self): return self._validity

    @property
    def url(self) -> str: return self._url
    @url.setter
    def url(self, url: str) -> None: self._url = url
    
    @property
    def soup(self) -> BeautifulSoup: return self._soup
    def set_soup(self): self._soup = self.execute_soup_strategy()
    def execute_soup_strategy(self) -> BeautifulSoup: return self._strategy_soup.execute(self._url)
        
    @property
    def id(self): return self._id
    def set_id(self, id): self._id = id
    @abstractmethod
    def find_id(self): ...
    
    @property
    def precio(self): return self._precio
    def set_precio(self, precio): self._precio = precio
    @abstractmethod
    def find_precio(self): ...
    
    @property
    def fecha(self): return self._fecha
    def set_fecha(self, fecha): self._fecha = fecha
    @abstractmethod
    def find_fecha(hoy): ...
    
    @property
    def vendedor(self): return self._vendedor
    def set_vendedor(self, vendedor): self._vendedor = vendedor
    @abstractmethod
    def find_vendedor(self): ...
    
    @property
    def coord(self): return self._coord
    def set_coord(self, coord): self._coord = coord
    @abstractmethod
    def find_coord(self): ...
    
    @property
    def caracteristicas(self): return self._caracteristicas
    def set_caracteristicas(self, cars): self._caracteristicas = cars
    def find_caracteristicas(self) -> dict: return self.CommandCaracteristicas().execute(self)
    
    class CommandCaracteristicas(ABC):
        @abstractmethod
        def execute(self,publicacion) -> dict: ...