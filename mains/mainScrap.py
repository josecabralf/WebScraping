import schedule, time
from datetime import date

from config import scrap_results_LV, scrap_results_ML, scrap_results_ZP
from config import path_df_LV, path_df_ML, path_df_ZP

from src.Scrapers.ThreadedScraper import ThreadedScraper
from src.Scrapers.PaginaWeb.FactoryPaginaWeb import *

from src.Filters.StrategyFilter import *

from src.Frames.InmueblesFrameBuilder import InmueblesFrameBuilder

from src.Analisis.AnalisisHandler import AnalisisHandler


def scrap(path_results, factory: FactoryPaginaWeb):
    t = ThreadedScraper(path_results, factory)
    t.execute()


def armar_frame(path_results: str, path_df: str, filter: StrategyFilter):
    b = InmueblesFrameBuilder(path_results, path_df)
    b.crear_frame()
    filter.gral_filter(b.get_frame())
    b.guardar_frame(path_df, activos=True)


def scrapLV():
    scrap(scrap_results_LV, FactoryPaginaWebLV())
    armar_frame(scrap_results_LV, path_df_LV, FilterLV())


def scrapML():
    scrap(scrap_results_ML, FactoryPaginaWebML())
    armar_frame(scrap_results_ML, path_df_ML, FilterML())


def scrapZP():
    scrap(scrap_results_ZP, FactoryPaginaWebZP())
    armar_frame(scrap_results_ZP, path_df_ZP, FilterZP())


def analisis(): AnalisisHandler().execute()


def task():
  try:
    if date.today().day == 1 or date.today().day == 15:
      scrapLV()
      scrapML()
      scrapZP()
      analisis()
    else:
      scrapML()
  except RuntimeError as e: ...
    

def main():
  schedule.every().day.at('18:00').do(task)
  while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == "__main__":
  main()