from Scrapers.Listado.Listado import Listado
from Scrapers.SoupStrategy import SoupStrategy
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategyZP
from Scrapers.Publicacion.PublicacionZP import PublicacionZP
from datetime import datetime
from ScrapConfig import URL_Base_ZP

class ListadoZP(Listado):
    _url_base = URL_Base_ZP
    
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today(),publicaciones: list = []):
        super().__init__(url, archivo, strategy_soup, hoy, publicaciones)
        
    def get_publicaciones(self) -> list:
        contenedor_casas = self.soup.find_all('div', class_='sc-i1odl-0 crUUno')
        publicaciones = []
        try:
            for i in range(len(contenedor_casas)):
                link = contenedor_casas[i]["data-to-posting"]
                if link: publicaciones.append(self._url_base + link)
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', err)
        if not publicaciones:
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', 'No habían publicaciones')
        return publicaciones

    def crear_publicacion(self, url: str) -> PublicacionZP:
        return PublicacionZP(url, self.strategy_soup, CaracteristicasStrategyZP.get_instance(), self.hoy)
    