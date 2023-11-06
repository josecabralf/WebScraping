import pandas as pd
from src.Filters.Correctors.GeoCorrector import GeoCorrector
from src.Filters.Correctors.FuzzyCorrector import FuzzyCorrector
from src.Filters.Correctors.PatternMatcherCorrector import PatternMatcherCorrector

class Corrector:
  def __init__(self) -> None:
    self._fuzzy = FuzzyCorrector()
    self._geo = GeoCorrector()
    self._pattern = PatternMatcherCorrector()
    
  def filtrar_patrones(self, df: pd.DataFrame) -> pd.DataFrame: return self._pattern.execute(df)
  
  def filtar_coordenadas(self, df: pd.DataFrame) -> pd.DataFrame: return self._geo.execute(df)
  
  def filtrar_fuzzy(self, df: pd.DataFrame) -> pd.DataFrame: return self._fuzzy.execute(df)
  
  def busqueda_manantiales(self, dato: str) -> str: return self._pattern.patron_manantiales(dato)
  
  def busqueda_fuzz(self, dato: str) -> str: return self._fuzzy.fuzz_ratio(dato)