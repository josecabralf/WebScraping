from ScrapConfig import logs
from datetime import datetime
from abc import ABC


class Logger:
  _instance = None
  _logs = logs 
  @classmethod
  def get_instance(self):
      if self._instance is None:
          self._instance = self()
      return self._instance
  def crear_log_error(self, clase, razon, err = ''):
    fecha = datetime.now()
    with open(self._logs, 'a', encoding='utf-8') as archivo:
      archivo.write(f'{clase.__name__}-{fecha}\n')
      archivo.write(f'ERROR: {razon}\n')
      archivo.write(f'{err}\n')
      archivo.write('----------------------------------------\n')
      

class Loggeable(ABC):
    def crear_log_error(self, mensaje: str, err=''):
        Logger.get_instance().crear_log_error(self.__class__, mensaje, err)