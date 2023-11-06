import pandas as pd
from config import lista_barrios
from fuzzywuzzy import process, fuzz

class FuzzyCorrector:
  _choices_file: str = lista_barrios
  def __init__(self) -> None:
     self._choices: list = self.open_choices()
     
  def open_choices(self) -> list:
    barrios = pd.read_csv(self._choices_file)
    return barrios['barrio'].tolist()
  
  def execute(self, df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, 'barrio'] = df.loc[:, 'barrio'].apply(lambda name: self.fuzz_ratio(name))
    return df
  
  def fuzz_ratio(self, name):
      if not name: return ''
      posible = process.extractOne(name, self._choices, scorer= fuzz.ratio, score_cutoff = 90)
      if posible: return posible[0]
      return self.fuzz_token_sort(name)

  def fuzz_token_sort(self, name):
      posible = process.extractOne(name, self._choices, scorer= fuzz.token_sort_ratio, score_cutoff = 90)
      if posible: return posible[0]
      return self.fuzz_partial(name)

  def fuzz_partial(self, name):
      if len(name) > 3:
          posible = process.extractOne(name, self._choices, scorer= fuzz.partial_ratio, score_cutoff = 95)
          if posible: return posible[0]
      return name