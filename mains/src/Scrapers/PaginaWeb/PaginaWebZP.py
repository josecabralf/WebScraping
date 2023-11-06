from src.Scrapers.PaginaWeb import PaginaWeb
from src.Scrapers.Listado.ListadoZP import ListadoZP
from math import ceil


class PaginaWebZP(PaginaWeb):
    def __init__(self, url, strategy_soup) -> None:
        super().__init__(url, strategy_soup)

    def get_cantidad_paginas(self) -> int:
      return ceil(self.get_cant_publicaciones() / 20)
    
    def get_cant_publicaciones(self) -> int:
      n = 0
      try: n = int(self.soup.find('h1', class_='sc-1oqs0ed-0 dbbZNk').text.split()[0].replace('.', ''))
      except AttributeError as err: self.crear_log_error('No se pudo obtener la cantidad de publicaciones. Revisar etiqueta get_cant_publicaciones()', err)
      return n
    
    def crear_listado(self, i, archivo, publicaciones) -> ListadoZP: 
      return ListadoZP(self.crear_link_listado(i), archivo, self._strategy_soup, self._hoy, publicaciones)

    def crear_link_listado(self, i) -> str: 
      if i == 1: return self.url
      link = self.url.split('.')
      link[-2] = link[-2] + f"-pagina-{i}"
      link = '.'.join(link)
      return link