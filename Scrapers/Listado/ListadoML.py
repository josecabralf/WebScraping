from Scrapers.Listado.Listado import Listado
from Scrapers.SoupStrategy import SoupStrategy
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategyML
from Scrapers.Publicacion.PublicacionML import PublicacionML
from datetime import datetime

class ListadoML(Listado):
    def __init__(self, url : str, archivo : str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today(), publicaciones: list = []):
        super().__init__(url, archivo, strategy_soup, hoy, publicaciones)
        self._ubic = self.get_ubic_provisoria()
        
    def get_publicaciones(self) -> list:
        try:
            divs = self.soup.find_all('div', class_='ui-search-item__group__element ui-search-item__title-grid')
            publicaciones = [div.find('a')['href'] for div in divs]
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', err)
            return []
        if not publicaciones: 
            self.crear_log_error('No se pudieron obtener links de publicaciones. Revisar etiqueta de get_publicaciones()', 'No habían publicaciones')
        return publicaciones
    
    def crear_publicacion(self, url: str) -> PublicacionML:
        return PublicacionML(url, self.strategy_soup, CaracteristicasStrategyML.get_instance(), self.hoy, self._ubic)
    
    def get_ubic_provisoria(self):
      try:
        ciudad = self.url.split('/')[7].replace('-', ' ').upper()
        barrio = self.url.split('/')[8].replace('-', ' ').upper()
        if 'INMUEBLES' in barrio:
            barrio = ''
      except:
          ciudad = ''
          barrio = ''
      return [ciudad, barrio]