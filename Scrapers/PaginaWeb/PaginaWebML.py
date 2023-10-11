from Scrapers.PaginaWeb.PaginaWeb import PaginaWeb
from Scrapers.Listado.ListadoML import ListadoML
from math import ceil


class PaginaWebML(PaginaWeb):
    def __init__(self, url, strategy_soup) -> None:
        super().__init__(url, strategy_soup)

    def get_cantidad_paginas(self) -> int:
      try: paginas = int(self.soup.find('li', class_='andes-pagination__page-count').text.split()[-1])
      except: paginas = ceil(self.get_cant_publicaciones() / 48)
      return paginas
    
    def get_cant_publicaciones(self):
      try:
          cant_publicaciones = int(self.soup.find('span', class_='ui-search-search-result__quantity-results').text.split()[0].replace('.', ''))
          return cant_publicaciones
      except AttributeError as err:
          self.crear_log_error('No se pudo obtener la cantidad de paginas. Revisar etiqueta getCantPaginas() y get_cant_publicaciones()', err)
          return 0
    
    def crear_listado(self, i, archivo) -> ListadoML:
        return ListadoML(self.crear_link_listado(i), archivo, self._strategy_soup, self._hoy)

    def crear_listado_desde_lista(self, publicaciones, archivo) -> ListadoML:
        return ListadoML('', archivo, self._strategy_soup, self._hoy, publicaciones)

    def crear_link_listado(self, i) -> str:
      if (i-1) == 0: return self.url
      link = self.url.split('_')
      link.insert(1, f"Desde_{(i-1)*48+1}")
      link = '_'.join(link)
      return link