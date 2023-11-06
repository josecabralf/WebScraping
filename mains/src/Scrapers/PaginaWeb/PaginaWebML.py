from src.Scrapers.PaginaWeb import PaginaWeb
from src.Scrapers.Listado.ListadoML import ListadoML
from math import ceil


class PaginaWebML(PaginaWeb):
    def __init__(self, url, strategy_soup) -> None:
        super().__init__(url, strategy_soup)

    def get_cantidad_paginas(self) -> int:
      try: paginas = int(self.soup.find('li', class_='andes-pagination__page-count').text.split()[-1])
      except: paginas = ceil(self.get_cant_publicaciones() / 48)
      return paginas
    
    def get_cant_publicaciones(self):
        n = 0
        try: n = int(self.soup.find('span', class_='ui-search-search-result__quantity-results').text.split()[0].replace('.', ''))
        except AttributeError as err: self.crear_log_error('No se pudo obtener la cantidad de paginas. Revisar etiqueta getCantPaginas() y get_cant_publicaciones()', err)
        return n
    
    def crear_listado(self, i, archivo, publicaciones) -> ListadoML:
        return ListadoML(self.crear_link_listado(i), archivo, self._strategy_soup, self._hoy, publicaciones)

    def crear_link_listado(self, i) -> str:
      if (i-1) == 0: return self.url
      link = self.url.split('_')
      link.insert(1, f"Desde_{(i-1)*48+1}")
      link = '_'.join(link)
      return link