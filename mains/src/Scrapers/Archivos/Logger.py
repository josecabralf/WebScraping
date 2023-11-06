from config import logs_scrap, logs_operaciones
from datetime import datetime
from abc import ABC
from src.Singleton import Singleton

class Logger(Singleton):
  _scrap = logs_scrap
  _operations = logs_operaciones
  
  def error_scrap(self, _class, razon, err = ''):
    with open(self._scrap, 'a', encoding='utf-8') as archivo:
      archivo.write(f'{_class.__name__}-{datetime.now()}\n')
      archivo.write(f'ERROR: {razon}\n')
      archivo.write(f'{err}\n')
      archivo.write('----------------------------------------\n')
  
  def operacion(self, _class, state, pagina_class):
    with open(self._operations, 'a', encoding='utf-8') as archivo:
      archivo.write(f'{_class.__name__}-{datetime.now()}\n')
      archivo.write(f'{state}: {pagina_class.__name__}\n')
      archivo.write('----------------------------------------\n')
      

class LoggeableScraper(ABC):
    def crear_log_error(self, mensaje: str, err: str=''): 
      Logger().error_scrap(self.__class__, mensaje, err)


class LoggeableOperator(ABC):
    def crear_log_operacion(self, state: str, pagina_class: str): 
      Logger().operacion(self.__class__, state, pagina_class)
  