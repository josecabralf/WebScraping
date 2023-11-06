from src.Scrapers.Listado import Listado
from src.Scrapers.SoupStrategy import SoupStrategy
from src.Scrapers.Publicacion.PublicacionLV import PublicacionLV
from datetime import datetime

class ListadoLV(Listado):
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today(), publicaciones: list = [], fecha_c : datetime = None):
        self._fecha_corte = fecha_c
        super().__init__(url, archivo, strategy_soup, hoy, publicaciones)
        
    def get_publicaciones(self) -> list:
        pagina_casas = self.soup.find_all('a', class_="text-decoration-none")
        publicaciones = set()
        try:
            for link in pagina_casas: publicaciones.add(link["href"])
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', err)
        return list(publicaciones)
    
    def crear_publicacion(self, url: str) -> PublicacionLV:
        return PublicacionLV(url, self.strategy_soup, self._hoy, self._fecha_corte)
    