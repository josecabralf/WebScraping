from src.Scrapers.PaginaWeb import PaginaWeb
from src.Scrapers.Listado.ListadoLV import ListadoLV


class PaginaWebLV(PaginaWeb):
    def __init__(self, url, strategy_soup, fecha_c = None) -> None:
        self._fecha_corte = fecha_c
        super().__init__(url, strategy_soup)

    def get_cantidad_paginas(self) -> int:
        n = 0
        try: n = int((self.soup.find_all('a', class_="page-link h4"))[-1].text)
        except AttributeError as err: self.crear_log_error('No se pudo obtener la cantidad de paginas. Revisar etiqueta getCantPaginas()', err)
        return n
    
    def crear_listado(self, i, archivo, publicaciones):
        return ListadoLV(self.crear_link_listado(i), archivo, self._strategy_soup, self._hoy, publicaciones, self._fecha_corte)

    def crear_link_listado(self, i) -> str: return self.url + f'&page={i}'