from config import path_reports, path_unify
from src.Filters.Unifier import Unifier
from datetime import date
from src.Analisis.AnalisisStrategy import AnalisisStrategy, AnalisisStrategyPM2
from src.Frames.InmueblesFrameHandler import InmueblesFrameHandler

class AnalisisHandler:
  _path_reports = path_reports
  _path_unify = path_unify
  def __init__(self, analisis_strategy: AnalisisStrategy = AnalisisStrategyPM2()) -> None:
    self._strategy = analisis_strategy
    self.set_frame()
    
  def execute(self):
    self.guardar_unificada()
    self.guardar_resultados_tipo_propiedad()

  def set_frame(self):
    u = Unifier()
    u.execute()
    self._frame = u.get_frame()
    
  def get_df(self): return self._frame.get_df()
  
  def guardar_unificada(self):
    archivo = f"{self._path_unify}{date.today().strftime('%Y-%m-%d')}_df.xlsx"
    self._frame.guardar_df(archivo, excel=True)
    
  def guardar_resultados_tipo_propiedad(self):
    df = self._frame.get_df()
    for tipo in ["CASA", "DEPARTAMENTO", "TERRENO"]:
      resultados = self._strategy.execute(df.loc[df["tipoPropiedad"] == tipo])
      resultados = InmueblesFrameHandler().crear_frame(resultados)
      archivo = f"{self._path_reports}{tipo}/{date.today().strftime('%Y-%m-%d')}_{tipo}.xlsx"
      resultados.guardar_df(archivo, excel=True)
    