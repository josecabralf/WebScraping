from src.Scrapers.Publicacion import Publicacion
from unidecode import unidecode
from src.Scrapers.SoupStrategy import SoupStrategy
from datetime import timedelta, datetime

class PublicacionZP(Publicacion):
  def __init__(self, url: str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today()):
    super().__init__(url, strategy_soup, hoy)
  
  def find_id(self) -> str: return self._url.split('-')[-1].split('.')[0]
    
  def find_precio(self) -> int:
    try:
        precio = self.soup.find('div', class_='price-value').find('span').find('span').text.split()
        if precio[0] == 'USD':
            precio = int(precio[1].replace('.', ''))
            return precio
        else: return 0
    except AttributeError as err:
        self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
        return 0
  
  def find_fecha(self, hoy) -> str: 
    try:
        delta = self.soup.find('div', id='user-views').find('p').text.split()
        if not delta: self.agregar_revision()
        if delta[-1] == 'hoy': delta = 0
        elif delta[-1] == 'ayer': delta = 1
        elif delta[-1] in ['día', 'días']: delta = int(delta[-2])
        elif delta[-1] in ['mes']: delta = 31*int(delta[-2])
        elif delta[-1] in ['meses', 'año', 'años',]: return ''

        fecha = hoy - timedelta(days=delta)
        fecha = fecha.strftime("%Y-%m-%d")
        return fecha
    except Exception as err:
        self.crear_log_error(f'No se pudo obtener fecha de publicacion. Revisar get_fecha().', err)
        self.agregar_revision()
        return ''
  
  def find_vendedor(self) -> str:
    vendedor = self.soup.find('section', id='reactPublisherData')
    try: 
        tipo = vendedor.find('h4').text.upper()
        if tipo.split()[-1] != 'DIRECTO': 
            try : 
              nom = vendedor.find('h3').text.upper().strip()
              return nom
            except Exception as e: 
              self.crear_log_error('No se pudo obtener nombre de inmobiliaria. Revisar find_vendedor().', e)
              return 'INMOBILIARIA'
        return 'PARTICULAR'
    except Exception as err: 
      self.crear_log_error('No se pudo obtener tipo de vendedor de publicacion. Revisar find_vendedor().', err)
      return ''

  def find_coord(self) -> list:
    try:
        mapa = self.soup.find('img', id="static-map")["src"]
        loc = mapa.split('?')[1].split('&')[0].split('=')[1]
        return [float(n) for n in loc.split(',')]
    except:
        self.crear_log_error('No se pudo obtener coords de publicacion. Revisar get_coord()')
        return [None, None]
      
  class CommandCaracteristicas(Publicacion.CommandCaracteristicas):
    def execute(self,publicacion: Publicacion) -> dict:
        try:
            caracteristicas = [car.text.strip() for car in publicacion.soup.find_all('li', class_="icon-feature")]
            caracteristicas = self.get_datos_caracteristicas(caracteristicas)
            tipo, ciudad, barrio = self.get_tipo_y_ubicacion(publicacion)
        except TypeError as err:
            publicacion.crear_log_error('No se pudo obtener las caracteristicas de la publicacion. Revisar CommandCaracteristicas', err)
            return False
        
        return {
            "tipo" : tipo,
            "TT" : caracteristicas[0],
            "TE" : caracteristicas[1],
            "Dorms" : caracteristicas[2],
            "Banos" : caracteristicas[3],
            "Cocheras" : caracteristicas[4],
            "Barrio" : barrio,
            "Ciudad" : ciudad
        }
    
    def get_tipo_y_ubicacion(self, publicacion):
        ubicacion = publicacion.soup.find_all('a', class_="bread-item-redirect")
        tipo_prop = ubicacion[1].text.strip().upper()
        try:
            ciudad = unidecode(ubicacion[4].text.strip().upper())
            barrio = unidecode(ubicacion[5].text.strip().upper())
            del ubicacion
        except: return None, None, None
        return tipo_prop, ciudad, barrio
    
    def get_datos_caracteristicas(self, caracteristicas):
        deseados = {'m² tot.': -1,
                    'm² cub.': -1,
                    'dorm.': -1,
                    'Baños': -1,
                    'coch.': -1}
        for car in caracteristicas:
            car = car.split('\n')
            try:
                if car[1] in deseados: deseados[car[1]] = float(car[0])
                elif car[1][-1] != 's':
                    car[1] = car[1] + 's'
                    if car[1] in deseados: deseados[car[1]] = float(car[0])
            except: continue
        return [
            deseados['m² tot.'],
            deseados['m² cub.'],
            deseados['dorm.'],
            deseados['Baños'],
            deseados['coch.']
        ]