from config import fechas
from datetime import datetime
import pandas as pd
from src.Singleton import Singleton

class Dater(Singleton):
  _archivo = fechas    
  def get_fecha(self, _class) -> datetime:
      df = pd.read_csv(self._archivo, sep=';')
      fecha = df.loc[df['Pagina'] == _class.__name__, 'Fecha'].values[0]
      return datetime.strptime(fecha, "%d-%m-%Y")
    
  def set_fecha(self, _class, fecha = datetime.now()):
      df = pd.read_csv(self._archivo, sep=';')
      df.loc[df['Pagina'] == _class.__name__, 'Fecha'] = fecha.strftime("%d-%m-%Y")
      df.to_csv(self._archivo, sep=';', index=False)