from bs4 import BeautifulSoup
from abc import abstractmethod
from Scrapers.SoupStrategy import SoupStrategy
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategy
from Scrapers.Logger import Loggeable
from Scrapers.Revision import Revision
from datetime import datetime


class Publicacion(Loggeable):
    def __init__(self, url : str, strategy_soup: SoupStrategy, strategy_caract: CaracteristicasStrategy, hoy: datetime):
        self._url = url
        self._strategy_soup = strategy_soup
        self._strategy_caract = strategy_caract
        self.set_soup()
        self._validity = self.set_datos_publicacion(hoy)
        
    def set_datos_publicacion(self, hoy) -> bool:
        self.set_fecha_activo(hoy)
        if not self.activo: return False
        self.set_precio(self.find_precio())
        if not self._precio: return False
        self.set_id(self.find_id())
        self.set_vendedor(self.find_vendedor())
        self.set_coord(self.find_coord())
        self.set_caracteristicas(self.find_caracteristicas())
        if not self.caracteristicas: return False
        return True
    
    def __str__(self) -> str:
        return f"{self._id};{self._caracteristicas['tipo']};{self._precio};{self._fecha};{self._vendedor};{self._caracteristicas['TT']};{self._caracteristicas['TE']};{self._caracteristicas['Dorms']};{self._caracteristicas['Banos']};{self._caracteristicas['Cocheras']};{self._caracteristicas['Barrio']};{self._caracteristicas['Ciudad']};{self._coord[0]};{self._coord[1]};{self._activo};{self._url}\n"

    def agregar_revision(self): Revision.get_instance().agregar_revision(self._url)

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
    def set_id(self, new): self._id = new
    @abstractmethod
    def find_id(self): ...
    
    @property
    def precio(self): return self._precio
    def set_precio(self, new): self._precio = new
    @abstractmethod
    def find_precio(self): ...
    
    @property
    def fecha(self): return self._fecha
    def set_fecha(self, new): self._fecha = new
    @property
    def activo(self): return self._activo
    def set_activo(self, new): self._activo = new
    def set_fecha_activo(self, hoy):
        f,a = self.find_fecha_activo(hoy)
        self.set_fecha(f)
        self.set_activo(a)
    @abstractmethod
    def find_fecha_activo(hoy): ...
    
    @property
    def vendedor(self): return self._vendedor
    def set_vendedor(self, new): self._vendedor = new
    @abstractmethod
    def find_vendedor(self): ...
    
    @property
    def coord(self): return self._coord
    def set_coord(self, new): self._coord = new
    @abstractmethod
    def find_coord(self): ...
    
    @property
    def caracteristicas(self): return self._caracteristicas
    def set_caracteristicas(self, new): self._caracteristicas = new
    def find_caracteristicas(self) -> dict: return self._strategy_caract.execute(self)