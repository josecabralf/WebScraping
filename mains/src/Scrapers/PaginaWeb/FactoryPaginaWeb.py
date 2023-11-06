from abc import abstractmethod
from src.Scrapers.PaginaWeb import PaginaWeb
from src.Scrapers.PaginaWeb.PaginaWebLV import PaginaWebLV
from src.Scrapers.PaginaWeb.PaginaWebML import PaginaWebML
from src.Scrapers.PaginaWeb.PaginaWebZP import PaginaWebZP
from src.Scrapers.SoupStrategy import Requests, Selenium
from src.Scrapers.Archivos.Dater import Dater
from src.Singleton import Singleton
from config import URL_LV, URL_ML, URL_ZP

class FactoryPaginaWeb(Singleton):
  @abstractmethod
  def crear_pagina_web(self) -> PaginaWeb: ...
  
  
class FactoryPaginaWebLV(FactoryPaginaWeb):
  _url = URL_LV
  def crear_pagina_web(self) -> PaginaWebLV: 
    return PaginaWebLV(self._url, Requests(), self.get_fecha_corte())
  
  def get_fecha_corte(self): return Dater().get_fecha(PaginaWebLV)
  
class FactoryPaginaWebML(FactoryPaginaWeb):
  _url = URL_ML
  def crear_pagina_web(self) -> PaginaWebML: 
    return PaginaWebML(self._url, Requests())
  
  
class FactoryPaginaWebZP(FactoryPaginaWeb):
  _url = URL_ZP
  def crear_pagina_web(self) -> PaginaWebZP: 
    return PaginaWebZP(self._url, Selenium())