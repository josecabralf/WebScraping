from src.Scrapers.Listado import Listado
from src.Scrapers.SoupStrategy import SoupStrategy
from src.Scrapers.Publicacion.PublicacionZP import PublicacionZP
from datetime import datetime
from config import URL_Base_ZP

class ListadoZP(Listado):
    _url_base = URL_Base_ZP
    
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today(),publicaciones: list = []):
        super().__init__(url, archivo, strategy_soup, hoy, publicaciones)
        
    def get_publicaciones(self) -> list:
        contenedor_casas = self.soup.find_all('div', class_='sc-i1odl-0 crUUno')
        publicaciones = []
        try: publicaciones = [self.formar_link_inmueble(inmueble["data-to-posting"]) for inmueble in contenedor_casas]
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', err)
        return publicaciones

    def formar_link_inmueble(self, inmueble: str) -> str: return self._url_base + inmueble
    
    def crear_publicacion(self, url: str) -> PublicacionZP:
        return PublicacionZP(url, self.strategy_soup, self.hoy)
    