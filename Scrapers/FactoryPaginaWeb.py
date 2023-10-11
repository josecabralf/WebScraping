from abc import ABC, abstractmethod
from Scrapers.PaginaWeb.PaginaWeb import PaginaWeb
from Scrapers.PaginaWeb.PaginaWebLV import PaginaWebLV
from Scrapers.PaginaWeb.PaginaWebML import PaginaWebML
from Scrapers.PaginaWeb.PaginaWebZP import PaginaWebZP
from Scrapers.SoupStrategy import SoupStrategyRequests, SoupStrategySelenium, SoupStrategy
from datetime import datetime
from ScrapConfig import utils_fecha_LV, URL_LV, URL_ML, URL_ZP

class FactoryPaginaWeb(ABC):
  _instance = None
  _strategy_soup : SoupStrategy = ...
  _url : str = ...
  def get_instance(self):
    if self._instance is None:
        self._instance = self()
    return self._instance
  @abstractmethod
  def crear_pagina_web(self, url) -> PaginaWeb: ...
  
  
class FactoryPaginaWebLV(FactoryPaginaWeb):
  _strategy_soup = SoupStrategyRequests.get_instance()
  _archivo_fecha_corte = utils_fecha_LV
  _url = URL_LV
  def crear_pagina_web(self) -> PaginaWebLV: 
    return PaginaWebLV(self._url, self._strategy_soup, self.fecha_corte())
  def fecha_corte(self):
    try:
        with open(self._archivo_fecha_corte, 'r') as f: fecha = f.readline()
        return datetime.strptime(fecha, "%d-%m-%Y")
    except: return None
  
  
class FactoryPaginaWebML(FactoryPaginaWeb):
  _strategy_soup = SoupStrategyRequests.get_instance()
  _url = URL_ML
  def crear_pagina_web(self) -> PaginaWebML: 
    return PaginaWebML(self._url, self._strategy_soup)
  
  
class FactoryPaginaWebZP(FactoryPaginaWeb):
  _strategy_soup = SoupStrategySelenium.get_instance()
  _url = URL_ZP
  def crear_pagina_web(self) -> PaginaWebZP: 
    return PaginaWebZP(self._url, self._strategy_soup)